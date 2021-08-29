import unittest
import pandas as _pd
import numpy as _np
import os as _os
from glob import glob as _glob
import types as _types

########################################################################################################################
##########################################             all_around                #######################################
########################################################################################################################


from utils._code.all_around import *
class Test_all_around(unittest.TestCase):

    def test_assert_path(self):
        with self.assertRaises(TypeError): pandas_standardize_df("not a dataframe")
        norm_df = pandas_standardize_df(_pd.DataFrame(_np.array([1, 2, 3, 4])))

        norm_df = pandas_standardize_df(_pd.DataFrame(_np.array([1, 2, 3, 4])))
        self.assertEqual(str(norm_df), """          0\n0 -1.161895\n1 -0.387298\n2  0.387298\n3  1.161895""")


    def test_get_grid_coordinates(self):
        with self.assertRaises(TypeError): get_grid_coordinates(3, "2")
        with self.assertRaises(TypeError): get_grid_coordinates(None, 2)
        self.assertEqual(get_grid_coordinates(3,2), [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)])


    def test_sturges_rule(self):
        with self.assertRaises(TypeError): sturges_rule(123)
        with self.assertRaises(TypeError): sturges_rule(None)
        self.assertEqual(sturges_rule([1,2,3,4]), (1.004420127756955, 3))


    def test_unfair_coin_flip(self):
        with self.assertRaises(TypeError): unfair_coin_flip(123)
        with self.assertRaises(ValueError): unfair_coin_flip(0.0)
        with self.assertRaises(ValueError): unfair_coin_flip(1.0)


    def check_int_sign(self):
        with self.assertRaises(TypeError): int_sign(1.0)
        self.assertEqual(int_sign(-11230), -1)
        self.assertEqual(int_sign(11230), 1)


    def test_init_2d_list(self):
        with self.assertRaises(TypeError): init_2d_list(1, 2.0)
        with self.assertRaises(TypeError): init_2d_list(2.0, 1)

        self.assertEqual(
            init_2d_list(4, 3),
            [[None, None, None], [None, None, None], [None, None, None], [None, None, None]]
        )


    def test_ndarray_to_bins(self):
        with self.assertRaises(TypeError): ndarray_to_bins("not array", 2)
        with self.assertRaises(ValueError): ndarray_to_bins(_np.array([1, 2, 3, 4]), 0)

        array, bins, thresh = ndarray_to_bins(_np.array([1, 2, 3, 4]), 2)
        self.assertEqual( list(array), [1, 1, 2, 3] )
        self.assertEqual( bins, 2)
        self.assertEqual( list(thresh), [1. , 2.5, 4. ])


########################################################################################################################
##########################################             Colors                ###########################################
########################################################################################################################


from utils._code.colors import *
class Test_colors(unittest.TestCase):

    def test_is_legal_hex(self):
        self.assertEqual(is_legal_hex("Something"), False)
        self.assertEqual(is_legal_hex([1,2,3]), False)
        self.assertEqual(is_legal_hex("#c51cbe"), True)


    def test_is_legal_rgb(self):
        self.assertEqual(is_legal_rgb([1, 1, 1, 1]), False)
        self.assertEqual(is_legal_rgb("#c51cbe"), False)
        self.assertEqual(is_legal_rgb((1, 2, 3)), True)
        self.assertEqual(is_legal_rgb([0, 0, 256]), False)
        self.assertEqual(is_legal_rgb([1, 2, 3]), True)
        self.assertEqual(is_legal_rgb([1, 2, 3.0]), False)


    def test_get_color_type(self):
        self.assertEqual(get_color_type("#c51cbe"), "hex")
        self.assertEqual(get_color_type("#c51cbe_asd"), None)
        self.assertEqual(get_color_type([0,0,255]), "rgb")
        self.assertEqual(get_color_type([0,0,255,0]), None)


    def test_assert_type_str(self):
        with self.assertRaises(ValueError): _assert_type_str("something")
        with self.assertRaises(ValueError): _assert_type_str("lalal")
        with self.assertRaises(TypeError): _assert_type_str(None)
        for color_type in legal_types:
            _assert_type_str(color_type)


    def test_assert_color(self):
        with self.assertRaises(TypeError): assert_color("something")
        with self.assertRaises(TypeError): assert_color("lalal")
        with self.assertRaises(TypeError): assert_color([0, 23, 10.])
        with self.assertRaises(TypeError): assert_color("#c51cbe_")
        for color in ["#c51cbe", (1, 5, 100), [0, 23, 10]]:
            assert_color(color)


    def test_assert_color_scheme(self):
        with self.assertRaises(ValueError): _assert_color_scheme("not_seaborn")
        with self.assertRaises(TypeError): _assert_color_scheme(123)
        for scheme in scheme_name_to_colors.keys():
            _assert_color_scheme(scheme)


    def test_assert_color_word(self):
        with self.assertRaises(TypeError): _assert_color_word( (0,0,0), "seaborn")
        with self.assertRaises(TypeError): _assert_color_word( "blue", None)
        with self.assertRaises(ValueError): _assert_color_word("not_a_color", "not_seaborn")

        for scheme, scheme_colors in scheme_name_to_colors.items():
            for color in scheme_colors:
                _assert_color_word(color, scheme)


    def test_convert_color(self):
        with self.assertRaises(TypeError): convert_color("#ffffff", None)
        with self.assertRaises(TypeError): convert_color("#ffffff_", "rgb")
        with self.assertRaises(TypeError): convert_color("asd", "rgb")
        with self.assertRaises(TypeError): convert_color([1,2,3,4], "rgb")
        with self.assertRaises(TypeError): convert_color(_np.array([1, 2, 3]), "hex")
        with self.assertRaises(TypeError): convert_color([1,2,3.0], "hex")
        with self.assertRaises(TypeError): convert_color([1,2,3,5], "hex")

        convert_color([1,2,3], "hex")
        convert_color((1,2,3), "hex")
        convert_color((1,2,3), "rgb")
        convert_color("#Ffffff", "hex")
        convert_color("#ffffff", "rgb")


    def test_random_color(self):
        with self.assertRaises(TypeError): random_color(None)
        with self.assertRaises(TypeError): random_color("rgb", amount=1.0)
        with self.assertRaises(TypeError): random_color("rgb", min_rgb=1.0)
        with self.assertRaises(TypeError): random_color("rgb", max_rgb=1.0)
        with self.assertRaises(ValueError): random_color("not_at_color_type_str")
        with self.assertRaises(ValueError): random_color(min_rgb=600)
        with self.assertRaises(ValueError): random_color(max_rgb=0)
        with self.assertRaises(ValueError): random_color(min_rgb=100, max_rgb=50)
        with self.assertRaises(ValueError): random_color(amount=0)

        self.assertEqual( len(random_color("rgb", amount=3)), 3)
        self.assertEqual( len(random_color("hex", amount=3)), 3)
        self.assertEqual( len(random_color("hex", 3, 120, 140)), 3)


    def test_hex_to_rgb(self):
        with self.assertRaises(ValueError): hex_to_rgb("#fffff_")
        with self.assertRaises(TypeError): hex_to_rgb([1,2,3])
        self.assertEqual(hex_to_rgb("#ffffff"), (255,255,255))


    def test_rgb_to_hex(self):
        with self.assertRaises(TypeError): rgb_to_hex("[1,2,3]")
        with self.assertRaises(ValueError): rgb_to_hex([1,2,300])
        self.assertEqual(rgb_to_hex((255, 255, 255)), "#ffffff")


    def test_color_from_name(self):

        with self.assertRaises(TypeError): color_from_name( (0, 0, 0))
        with self.assertRaises(TypeError): color_from_name("blue", None)
        with self.assertRaises(ValueError): color_from_name("blue", "not_a_valid_type", "seaborn")
        with self.assertRaises(ValueError): color_from_name("blue", "rgb", "not_seaborn")

        for scheme, scheme_colors in scheme_name_to_colors.items():
            for color in scheme_colors:
                for color_type in legal_types:
                    color_from_name(color, color_type, scheme)


    def test_display_colors(self):
        with self.assertRaises(TypeError): display_colors("asd")
        with self.assertRaises(TypeError): display_colors(["asd"])
        with self.assertRaises(TypeError): display_colors(["#fffff_"])
        with self.assertRaises(TypeError): display_colors([(1,2,3,4)])

        display_colors( list(scheme_name_to_colors["seaborn"].values()) )

    def test_get_colors_from_scheme(self):

        with self.assertRaises(TypeError): get_colors_from_scheme("seaborn", None)
        with self.assertRaises(ValueError): get_colors_from_scheme("seaborn", "no_valid_type")

        self.assertEqual( get_colors_from_scheme("seaborn"), list(scheme_name_to_colors["seaborn"].values()))
        self.assertEqual( get_colors_from_scheme("seaborn", "hex"), [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#e1ffff'
        ])


########################################################################################################################
##########################################             Formatting                #######################################
########################################################################################################################


from utils._code.formatting import *
class Test_formatting(unittest.TestCase):

    def test_scientific_notation(self):
        with self.assertRaises(TypeError): scientific_notation("not a number", 2)
        with self.assertRaises(TypeError): scientific_notation(2, "not a number")
        with self.assertRaises(TypeError): scientific_notation(2, 2.0)

        self.assertEqual(scientific_notation(2.1234, 3), "2.123E+00")
        self.assertEqual(scientific_notation(10_000_000, 3), "1.000E+07")


    def test_string_to_dict(self):
        with self.assertRaises(TypeError): string_to_dict(123)
        self.assertEqual(string_to_dict("{'a':1, 'b':2}"), {'a': 1, 'b': 2})


    def test_string_to_list(self):
        with self.assertRaises(TypeError): string_to_list(123)
        self.assertEqual(string_to_list('[198, 86, 292, 149]'), ['198', '86', '292', '149'])
        self.assertEqual(string_to_list('[198, 86, 292, 149]', element_type=int), [198, 86, 292, 149])


########################################################################################################################
##########################################             Images                ###########################################
########################################################################################################################


#TODO add tests, all missing
from utils._code.images import *
class Test_images(unittest.TestCase):
    pass


########################################################################################################################
##########################################             imports                ##########################################
########################################################################################################################


from utils._code.imports import *
from utils._code import imports
class Test_imports(unittest.TestCase):
    def test_get_imports(self):
        with self.assertRaises(TypeError): get_imports("not a list")
        with self.assertRaises(ValueError): get_imports(["Not a valid request"])


    def test_get_module_path(self):
        with self.assertRaises(TypeError): get_imports("not a Module")
        self.assertEqual(_os.path.abspath("../_code/imports.py"), get_module_path(imports))


    def test_get_available_functions(self):
        with self.assertRaises(TypeError): get_imports("not a Module")
        self.assertEqual( sorted(get_available_functions(imports)), sorted(imports.__all__))


    def test_get_all_available_import_classes(self):
        with self.assertRaises(TypeError): get_imports("not a Module")
        self.assertEqual(get_all_available_import_classes(imports), [])


########################################################################################################################
##########################################             Input_output                #####################################
########################################################################################################################


from utils._code.input_output import *
class Test_input_output(unittest.TestCase):

    def test_assert_path(self):
        with self.assertRaises(TypeError): assert_path(123)
        with self.assertRaises(ValueError): assert_path("./something_lalalaalala.txt.png")
        assert_path("../_code/input_output.py")


    def test_assert_path_dont_exists(self):
        with self.assertRaises(TypeError): assert_path_dont_exists(123)
        with self.assertRaises(ValueError): assert_path_dont_exists("../_code/input_output.py")
        assert_path_dont_exists("./something_lalalaalala.txt.png")


    def test_path_exists(self):
        with self.assertRaises(TypeError): path_exists(123)
        self.assertEqual(path_exists("../_code/input_output.py"), True)
        self.assertEqual(path_exists("something_lalalaalala.txt.png"), False)


    def test_add_path_to_system(self):
        with self.assertRaises(TypeError): add_path_to_system(None)
        with self.assertRaises(ValueError): add_path_to_system("This_path_hopefully_dont_exists.asd")
        add_path_to_system("./")


    def test_get_current_directory(self):
        self.assertEqual(type(get_current_directory()), str)
        # Check if "input_output.py" is somewhere within the current folder
        paths = _glob(_os.path.join("../_code", "*"))
        self.assertEqual(sum([path.find("input_output.py") != -1 for path in paths]) != 0, True)


    def test_save_plt_plot(self):
        with self.assertRaises(TypeError): save_plt_plot(None)
        with self.assertRaises(TypeError): save_plt_plot("string", 123)
        with self.assertRaises(TypeError): save_plt_plot("string", None, 300.0)
        with self.assertRaises(ValueError): save_plt_plot("string.notJPG.", None, 300)

        # Test function work
        save_plt_plot("./test_plt.png")
        assert_path("./test_plt.png")
        _os.remove("./test_plt.png")


    def test_get_file_basename(self):
        with self.assertRaises(TypeError): get_file_basename(123)
        with self.assertRaises(TypeError): get_file_basename("path", None)

        self.assertEqual( get_file_basename('C:/Users/JohnDoe/Desktop/test.png', assert_path_exists=False), "test")
        self.assertEqual( get_file_basename('C:/Users/JohnDoe/Desktop/test.png', True, False), "test.png")
        self.assertEqual( get_file_basename('C:/Users/JohnDoe/Desktop/test.png.jpg', True, False), "test.png.jpg")


    def test_write_to_file(self):
        with self.assertRaises(TypeError): write_to_file(123, "string")
        with self.assertRaises(TypeError): write_to_file("string", 123)

        # Open file, write to it, check it's correct and delete it.
        with open("./test.txt", "w") as f: f.close()
        write_to_file("./test.txt", "hello_world 123")
        with open("./test.txt", "r") as F:
            self.assertEqual(F.read(), "hello_world 123")
        _os.remove("./test.txt")


    def test_read_json(self):
        with self.assertRaises(TypeError): read_json(123)
        with self.assertRaises(ValueError): read_json("test.png")

        # Open file, write to it, check it's correct and delete it.
        with open("./test.json", "w") as f: f.close()
        write_to_file("./test.json", '{"hello_world": []}')
        with open("./test.json", "r") as F:
            self.assertEqual(F.read(), '{"hello_world": []}')
        _os.remove("./test.json")

    def test_get_number_of_files(self):
        with self.assertRaises(TypeError): get_number_of_files(123)
        with self.assertRaises(ValueError): get_number_of_files("not_a_real_path.asdasd")

        # Create folder with 3 files, check number and delete all again.
        assert_path_dont_exists("./testdir")
        _os.mkdir("./testdir")
        for i in range(3):
            with open(f"./testdir/t{i}.txt", "w") as f:
                f.close()
        self.assertEqual(get_number_of_files("./testdir"), 3)
        [_os.remove(f"./testdir/t{i}.txt") for i in range(3)]
        _os.rmdir("./testdir")


    def test_read_txt_file(self):
        with self.assertRaises(TypeError): read_txt_file(123)
        with self.assertRaises(ValueError): read_txt_file("string.wrong_extension")

        # Open file, write to it, check it's correct and delete it.
        with open("./test.txt", "w") as f: f.close()
        write_to_file("./test.txt", "hello_world 123")
        self.assertEqual(read_txt_file("./test.txt"), "hello_world 123")
        _os.remove("./test.txt")


    def test_save_and_load_pickle(self):
        with self.assertRaises(TypeError): save_as_pickle(None, 123, "string")
        with self.assertRaises(ValueError): save_as_pickle("string.not_pkl", "string")

        with self.assertRaises(TypeError): load_pickle_file(12)
        with self.assertRaises(ValueError): load_pickle_file("string.not_pkl")

        save_as_pickle([1,2,3], "test.pkl", "./")
        self.assertEqual( load_pickle_file("./test.pkl"), [1,2,3])
        _os.remove("./test.pkl")


    def test_copy_folder(self):
        _os.mkdir("./testdir")
        with self.assertRaises(TypeError): copy_folder(123, "./testdir")
        with self.assertRaises(TypeError): copy_folder("./testdir", 123)
        with self.assertRaises(ValueError): copy_folder("./testdir", "./testdir")

        copy_folder("./testdir", "./testdir1")
        assert_path("./testdir1")

        _os.rmdir("./testdir")
        _os.rmdir("./testdir1")


########################################################################################################################
##########################################             jupyter                ##########################################
########################################################################################################################


from utils._code.jupyter import *
class Test_jupyter(unittest.TestCase):
    def test_all(self):
        # I don't really know how to test these properly, since I cannot guarantee to be in a jupyter env.
        # I think the only real way is to test them in a manually in a jupyter env. every time i run tests

        # Run ./tests/test_jupyter.ipynb to test manually

        self.assertIn(in_jupyter(), [False, True])
        try:
            assert_in_jupyter()
        except RuntimeError:
            pass


########################################################################################################################
##########################################             pytorch                ##########################################
########################################################################################################################


# TODO add tests, all missing
from utils._code.pytorch import *
class Test_pytorch(unittest.TestCase):
    pass


########################################################################################################################
######################################             system_info                ##########################################
########################################################################################################################


from utils._code.system_info import *
class Test_system_info(unittest.TestCase):

    def test_get_vram_info(self):
        self.assertEqual( isinstance(windows_illegal_file_name_character, list), True)
        self.assertEqual( isinstance(get_vram_info(), dict) and len(get_vram_info()) == 4, True)


    def test_get_gpu_info(self):
        self.assertEqual(isinstance(get_gpu_info(), dict) and len(get_gpu_info()) == 5, True)


    def test_get_screen_dim(self):
        WxH = get_screen_dim(WxH=True)
        self.assertEqual(isinstance(WxH, tuple), True)
        self.assertEqual(isinstance(WxH[0], int), True)
        self.assertEqual(isinstance(WxH[1], int), True)

        HxW = get_screen_dim(WxH=False)
        self.assertEqual(isinstance(HxW, tuple), True)
        self.assertEqual(isinstance(HxW[0], int), True)
        self.assertEqual(isinstance(HxW[1], int), True)


    def test_get_os(self):
        self.assertEqual(isinstance(get_os(), str), True)


    def test_on_windows(self):
        self.assertEqual(isinstance(on_windows(), bool), True)


    def test_get_computer_info(self):
        import sys, io
        # Suppress print start
        suppress_text = io.StringIO()
        sys.stdout = suppress_text

        self.assertEqual(isinstance(get_computer_info(), type(None)), True)

        # Suppress print end
        sys.stdout = sys.__stdout__


########################################################################################################################
######################################             type_check                ###########################################
########################################################################################################################


from utils._code.type_check import *
class Unit_type_check(unittest.TestCase):

    def test_assert_type(self):
        with self.assertRaises(TypeError):
            assert_type(to_check=0, expected_type=str)
        with self.assertRaises(ValueError):
            assert_type(to_check="string", expected_type=str, allow_none=22)
        assert_type(to_check=12, expected_type=int)
        assert_type(to_check=None, expected_type=type(None))
        assert_type(to_check=None, expected_type=str, allow_none=True)


    def test_assert_types(self):
        with self.assertRaises(TypeError):
            assert_types(to_check=[22, "string", None], expected_types=[int, str, int])
        with self.assertRaises(TypeError):
            assert_types(to_check=[22, "string", None], expected_types=[int, str, int])
        with self.assertRaises(TypeError):
            assert_types(to_check=["string", None], expected_types=[int, str])
        with self.assertRaises(ValueError):
            assert_types(to_check=[22, None], expected_types=[int, str, int], allow_nones=[0, 1, 0])
        with self.assertRaises(ValueError):
            assert_types(to_check=[22, None, 23], expected_types=[int, str, int], allow_nones=[0, 1])
        with self.assertRaises(TypeError):
            assert_types(to_check=[22, None], expected_types=[int, None], allow_nones=[0, 1])

        assert_types(to_check=[22, "string", None], expected_types=[int, str, int], allow_nones=[0, 0, 1])
        assert_types(
            to_check=[22, 0.2, None, unittest],
            expected_types=[int, float, str, _types.ModuleType],
            allow_nones=[0, 0, 1, 0]
        )


    def test_assert_list_slow(self):
        with self.assertRaises(ValueError):
            assert_list_slow(to_check=[1, 2, 3], expected_type=int, expected_length=4)
        with self.assertRaises(TypeError):
            assert_list_slow(to_check=[1, 2, 3], expected_type=str)
        with self.assertRaises(TypeError):
            assert_list_slow(to_check=[None, "hello", 3], expected_type=str)
        with self.assertRaises(ValueError):
            assert_list_slow(to_check=[3, 4], expected_type=int, expected_length=-1)
        with self.assertRaises(TypeError):
            assert_list_slow(to_check=[1, "2", 3], expected_type=int)
        with self.assertRaises(TypeError):
            assert_list_slow(to_check=[1, None, 3], expected_type=int, allow_none=False)

        assert_list_slow(to_check=[1, None, 3], expected_type=int, allow_none=True)
        assert_list_slow(to_check=[1, 2, 3], expected_type=int)
        assert_list_slow(to_check=[None, None, None], expected_type=type(None))


    def test_assert_int(self):
        with self.assertRaises(RuntimeError): assert_in("a", 2)
        with self.assertRaises(ValueError): assert_in("a", ["b", "c"])
        assert_in("b", ["b", "c"])
        assert_in(1, ["b", 1, None])


    def test_assert_comparison_number(self):
        with self.assertRaises(TypeError): assert_comparison_number("3", 0, ">=", "number_of_cats")
        with self.assertRaises(TypeError): assert_comparison_number(3, 0, ">=", None)
        with self.assertRaises(TypeError): assert_comparison_number(3.0, 0, ">=", "number_of_cats")

        with self.assertRaises(ValueError): assert_comparison_number(3.0, 0.0, ">==", "number_of_cats")
        with self.assertRaises(ValueError): assert_comparison_number(3, 0, "==", "number_of_cats")
        with self.assertRaises(ValueError): assert_comparison_number(3, 0, "=", "number_of_cats")
        with self.assertRaises(ValueError): assert_comparison_number(3, 0, "<", "number_of_cats")
        with self.assertRaises(ValueError): assert_comparison_number(3., 0., "<=", "number_of_cats")
        with self.assertRaises(ValueError): assert_comparison_number(0., 3., ">", "number_of_cats")
        with self.assertRaises(ValueError): assert_comparison_number(0., 3., ">=", "number_of_cats")

        assert_comparison_number(3, 0, ">=", "number_of_cats")
        assert_comparison_number(3.0, 0.0, ">=", "number_of_cats")
        assert_comparison_number(3, 0, ">", "number_of_cats")
        assert_comparison_number(3.0, 3.0, "<=", "number_of_cats")
        assert_comparison_number(0.0, 3.0, "<", "number_of_cats")
        assert_comparison_number(0, 0, "==", "number_of_cats")
        assert_comparison_number(0, 0, "=", "number_of_cats")



if __name__ == "__main__":
    unittest.main(verbosity=2)