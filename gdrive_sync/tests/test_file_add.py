import unittest
import sys
import os

try:
    sys.path.append("../")
    import file_add
except ImportError:
    from .. import file_add

dir_path = os.path.dirname(os.path.realpath(__file__))
home = os.path.expanduser("~")


class FileAddTest(unittest.TestCase):
    """
    tests for file_add module
    """

    def test_get_f_name_dir(self):
        """
        tests the get_f_name module for directory
        :return:
        """

        result = file_add.get_f_name(dir_path)
        self.assertEqual(result, "tests")

    def test_get_f_name_file(self):
        """
        tests the get_f_name module for file
        :return:
        """

        mock_file = os.path.join(home, "shivam.txt")
        with open(mock_file, "w+") as file:
            file.write("This is a testing file!")

        result = file_add.get_f_name(mock_file)
        self.assertEqual(result, "shivam.txt")

    def test_get_f_name_error(self):
        """
        tests the get_f_name module for wrong input
        :return:
        """

        self.assertRaises(TypeError, file_add.get_f_name, "123")
        self.assertRaises(TypeError, file_add.get_f_name, "1j32hkf")
        self.assertRaises(TypeError, file_add.get_f_name, "~/thealphashivam")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
