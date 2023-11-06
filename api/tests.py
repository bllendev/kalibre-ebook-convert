# test_convert.py
import unittest
import os
from api.convert import convert_with_pandoc

class TestConvertWithPandoc(unittest.TestCase):

    def setUp(self):
        # Create a dummy input file for testing
        with open('test.md', 'w') as f:
            f.write("# Test\nThis is a test file.")

    def tearDown(self):
        # Cleanup test files after running tests
        if os.path.exists('test.md'):
            os.remove('test.md')
        if os.path.exists('test.docx'):
            os.remove('test.docx')

    def test_conversion_success(self):
        output_path, message = convert_with_pandoc('test.md', 'docx')
        self.assertIsNotNone(output_path)
        self.assertTrue(os.path.exists(output_path))
        self.assertIn("File converted successfully", message)

    # More tests can be added, like checking invalid input, unsupported formats, etc.

if __name__ == '__main__':
    unittest.main()
