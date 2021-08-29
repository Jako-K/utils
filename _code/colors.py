"""
Description:
Helper functions for working with colors.
Intended use through the class instance `colors`.

Example:
>> colors.random_color(color_type="hex", amount=2)
['#c51cbe', '#0dc76a']
"""
# TODO: Add support for BGR
# TODO: Add @param to all

import re as _re
import random as _random
from PIL import ImageColor as _ImageColor
import numpy as _np
import matplotlib as _matplotlib
import matplotlib.pyplot as _plt
from . import type_check as _type_check


# Seaborn color scheme
seaborn_blue = (31, 119, 180)
seaborn_orange = (255, 127, 14)
seaborn_green = (44, 160, 44)
seaborn_red = (214, 39, 40)
seaborn_purple = (148, 103, 189)
seaborn_brown = (140, 86, 75)
seaborn_pink = (227, 119, 194)
seaborn_grey = (127, 127, 127)
seaborn_white = (225, 255, 255)
seaborn_colors = {"blue": seaborn_blue,
                  "orange": seaborn_orange,
                  "green": seaborn_green,
                  "red": seaborn_red,
                  "purple": seaborn_purple,
                  "brown": seaborn_brown,
                  "pink": seaborn_pink,
                  "grey": seaborn_grey,
                  "white": seaborn_white}

legal_types = ["rgb", "hex"]
scheme_name_to_colors = {"seaborn": seaborn_colors}
colors_schemes = list(scheme_name_to_colors.keys())


def is_legal_hex(color: str):
    return isinstance(color, str) and (_re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color) is not None)


def is_legal_rgb(color):
    """ Legal RGB colors are of type tuple/list and comprised of 3 integers in the range 0-255 """
    if not isinstance(color, (tuple, list)):  # Is a list or a tuple
        return False
    if len(color) != 3:  # Has len 3
        return False
    if sum([isinstance(color_channel, int) for color_channel in color]) != 3:  # All channels is of type int
        return False
    if sum([0 <= color_channel <= 255 for color_channel in color]) != 3:  # All channels is within 0-256
        return False

    return True


def get_color_type(color):
    """ Try to detect and return color type, only `legal_types` color types are supported """
    if is_legal_hex(color):
        return "hex"
    elif is_legal_rgb(color):
        return "rgb"

    return None


def _assert_type_str(color_type: str):
    """ assert color type is supported """
    _type_check.assert_type(color_type, str)
    if color_type not in legal_types:
        raise ValueError(f"Received unknown color type `{color_type}`. Legal types are: `{legal_types}`")


def assert_color(color):
    """ Detect color type and assert it's supported """
    if get_color_type(color) is None:
        raise TypeError(f"Color format cannot be interpreted. Legal color types are: `{legal_types}`")


def _assert_color_scheme(scheme: str):
    """ assert color scheme is supported """
    _type_check.assert_type(scheme, str)
    if scheme not in colors_schemes:
        raise ValueError(f"Received unknown color scheme {scheme}. Legal types: {colors_schemes}")


def _assert_color_word(color_name:str, scheme_name:str):
    """ Check if `color_name` is in `scheme_name` (scheme is assumed legal) """
    _type_check.assert_types([color_name, scheme_name], [str, str])
    _assert_color_scheme(scheme_name)
    color_scheme = scheme_name_to_colors[scheme_name]
    if color_name not in color_scheme.keys():
        raise ValueError(f"Color `{color_name}` is not present in color scheme `{scheme_name}`")


def convert_color(color, convert_to:str):
    """ convert color from one format to another e.g. from RGB --> HEX """
    _type_check.assert_type(convert_to, str)
    _assert_type_str(convert_to)
    assert_color(color)
    convert_from_type = get_color_type(color)

    if convert_from_type == convert_to:
        return color
    elif (convert_from_type == "rgb") and (convert_to == "hex"):
        return rgb_to_hex(color)
    elif (convert_from_type == "hex") and (convert_to == "rgb"):
        return hex_to_rgb(color)
    else:
        raise AssertionError("Shouldn't have gotten this far")


def random_color(color_type:str="rgb", amount:int=1, min_rgb:int=0, max_rgb:int=255):
    """
    return `amount` number of random colors in accordance with `min_rgb` and `max_rgb`
    in the color format specified by `color_type`.
    """
    _type_check.assert_types([color_type, amount, min_rgb, max_rgb], [str, int, int, int])
    _assert_type_str(color_type)

    if not (0 <= min_rgb <= 255):
        raise ValueError("Expected min_rgb in 0-255, received {min_rgb}")
    if not (0 <= max_rgb <= 255):
        raise ValueError("Expected max_rgb in 0-255, received {max_rgb}")
    if max_rgb <= min_rgb:
        raise ValueError("Received min_rgb > max_rgb")
    if amount < 1:
        raise ValueError("Received amount < 1")

    generated_colors = []
    for _ in range(amount):
        color = [_random.randint(min_rgb, max_rgb) for _ in range(3)]
        color_converted = convert_color(color, color_type)
        generated_colors.append(color_converted)

    return generated_colors[0] if (amount == 1) else generated_colors


def hex_to_rgb(hex_color: str):
    _type_check.assert_type(hex_color, str)
    if not is_legal_hex(hex_color):
        raise ValueError(f"`{hex_color=}` is not recognized as a HEX color")
    return _ImageColor.getcolor(hex_color, "RGB")


def rgb_to_hex(rgb_color):
    _type_check.assert_type(rgb_color, (tuple, list))
    if not is_legal_rgb(rgb_color):
        raise ValueError(f"`{rgb_color=}` is not recognized as a RGB color")
    return "#" + '%02x%02x%02x' % tuple(rgb_color)


def color_from_name(color_name:str, color_type:str="rgb", color_scheme:str="seaborn"):
    """
    Return color of name `color_name` from `color_scheme` in the format defined by `color_type`.
    Note: `color_name` should only contain the acutal color e.g. "blue" without prefix e.g. "seaborn_blue"
    """
    _type_check.assert_types([color_name, color_type, color_scheme], [str, str, str])
    _assert_type_str(color_type)
    _assert_color_scheme(color_scheme)
    _assert_color_word(color_name, color_scheme)

    color_scheme = scheme_name_to_colors[color_scheme]
    color = color_scheme[color_name]
    color_converted = convert_color(color, color_type)

    return color_converted


def display_colors(colors: list):
    """ Display all colors in `colors` in a matplotlib plot with corresponding hex, rgb etc. values"""
    # Checks
    _type_check.assert_type(colors, list)
    if len(colors) < 1:
        raise ValueError(f"Expected at least 1 color, received `{len(colors)}` number of colors")
    for color in colors:
        assert_color(color)

    fig, ax = _plt.subplots(figsize=(15, len(colors)))
    _plt.xlim([0, 100])
    _plt.ylim([0, 100])
    square_height = 100 / len(colors)

    for i, color in enumerate(colors):
        assert_color(color)

        # matplotlib's Rectangle expect RGB channels in 0-1
        color_rgb = convert_color(color, "rgb")
        color_rgb_01 = [c / 255 for c in color_rgb]

        # Draw colored rectangles
        y_start = 100 - (i + 1) * square_height
        rect = _matplotlib.patches.Rectangle((0, y_start), 100, square_height, color=color_rgb_01)
        ax.add_patch(rect)

        # Write colors in all legal formats
        for j, color_type in enumerate(legal_types):
            color_text = convert_color(color, color_type)
            if color_type == "rgb":
                color_text = [" " * (3 - len(str(c))) + str(c) for c in color]
            text = f"{color_type}: {color_text}".replace("'", "")

            # White text if light color, black text if dark color + text plot
            brightness = _np.mean(color_rgb)
            text_color = "black" if brightness > 50 else "white"
            _plt.text(5 + j * 20, y_start + square_height // 2, text, color=text_color, size=15)

    _plt.axis("off")
    _plt.show()

    return fig, ax


def get_colors_from_scheme(color_scheme:str, color_type:str="rgb"):
    """ Return the color values from `color_scheme` in the format specified by `color_type`"""
    _type_check.assert_types([color_scheme, color_type], [str, str])
    _assert_type_str(color_type)
    _assert_color_scheme(color_scheme)

    # Grab all the color values and change their format to match that of `color_type`
    colors = scheme_name_to_colors[color_scheme].values()
    return [convert_color(color, color_type) for color in colors]


__all__ = [
    # Constants
    "seaborn_blue",
    "seaborn_orange",
    "seaborn_green",
    "seaborn_red",
    "seaborn_purple",
    "seaborn_brown",
    "seaborn_pink",
    "seaborn_grey",
    "seaborn_white",
    "seaborn_colors",
    "legal_types",
    "scheme_name_to_colors",
    "colors_schemes",

    # Functions
    "is_legal_hex",
    "is_legal_rgb",
    "get_color_type",
    "_assert_type_str",
    "assert_color",
    "_assert_color_scheme",
    "_assert_color_word",
    "convert_color",
    "random_color",
    "hex_to_rgb",
    "rgb_to_hex",
    "color_from_name",
    "display_colors",
    "get_colors_from_scheme"
]