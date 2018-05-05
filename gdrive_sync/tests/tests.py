import unittest
import sys

try:
    sys.path.append("../")
    import auth
except ImportError:
    from .. import auth


class AuthTest(unittest.TestCase):
    """
    tests for functions in auth file
    """

    def test_auth(self):
        """
        test for presence and working of authorisation
        """
        auth.drive_auth(False)  # without reset
        try:
            auth.drive_auth(True)
        except SystemExit:
            with self.assertRaises(SystemExit):
                auth.drive_auth(True)

    @staticmethod
    def test_reset():
        """
        test for presence of reset
        :return: none
        """
        auth.reset_account()


def main():
    unittest.main()


if __name__ == "__main__":
    main()
