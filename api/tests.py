# test_convert.py
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from api.convert import convert_with_pandoc


class TestConvertWithPandoc(TestCase):

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


class ConvertEndpointTest(TestCase):

    def setUp(self):
        # Initialize the test client
        self.client = Client()

    def test_convert_file(self):
        test_file_content = b'This is a test content.'
        test_file_name = 'test_file.txt'
        
        # Create an instance of SimpleUploadedFile with test content
        test_file = SimpleUploadedFile(
            name=test_file_name,
            content=test_file_content,
            content_type='text/plain'
        )

        # Make a POST request to the endpoint with the file
        response = self.client.post('/api/convert/?output_format=pdf', {'input_file': test_file})

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # TODO: add logging and be have it work as intended in cicd
        # # Check that the Content-Type header is 'application/pdf' (or the expected type)
        # self.assertEqual(response['Content-Type'], 'application/pdf', response)

        # # Check that the Content-Disposition header is set to attachment
        # self.assertTrue('attachment' in response['Content-Disposition'])