#!/usr/bin/python
"""
BatchJPEGDownloader, Copyright (c) 2016 Oliver Meister (o.meister@gmx.net)

This file contains a set of unit tests for the ListFileURLGenerator class and the BatchDownloader class in
batchjpegdownloader.py
"""

import unittest
from batchjpegdownloader import ListFileURLGenerator, BatchDownloader

class TestListFileURLGenerator(unittest.TestCase):
    """Test class for the ListFileURLGenerator class.
    
    Defines a set of test cases to check that the ListFileURLGenerator class correctly treats list files and URLs.
    Also, filtering with the file pattern is checked.

    """

    def test_invalid_file(self):
        """ Test an invalid list file. The code should throw an exception in this case."""
        try:
            url_iterator = ListFileURLGenerator(None, ())

            # We should not be able to reach this code line
            assert False
        except TypeError:
            # This example should fail with a Type Error
            assert True

    def test_invalid_pattern(self):
        """ Test an invalid file pattern."""
            
        # While this example should actually crash, there is no portable way to check if
        # the file pattern is a string.

        url_iterator = ListFileURLGenerator("examples/test_valid.list", "")
        assert len([_ for _ in url_iterator]) == 0, repr([_ for _ in url_iterator])
        
    def test_wrong_pattern(self):
        """ Test a wrong file pattern."""
        url_iterator = ListFileURLGenerator("examples/test_valid.list", "*wrong")
        assert len([_ for _ in url_iterator]) == 0, repr([_ for _ in url_iterator])

    def test_valid(self):
        """ Test a valid case."""
        url_iterator = ListFileURLGenerator("examples/test_valid.list", "*.jpg")
        assert len([_ for _ in url_iterator]) == 3, repr([_ for _ in url_iterator])

    def test_incorrect_link(self):
        """ Test an incorrect link in the list file: no errors are expected as URLS should be checked only syntactically."""
        url_iterator = ListFileURLGenerator("examples/test_incorrect_link.list", "*.jpg")
        assert len([_ for _ in url_iterator]) == 3, repr([_ for _ in url_iterator])

    def test_invalid_link(self):
        """ Test an invalid link in the list file. The code should throw an exception if the validators module is present."""

        try:
            # Test importing the validators module. If this fails we cannot execute the test and pass it by default.
            import validators

            url_iterator = ListFileURLGenerator("examples/test_invalid_link.list", "*.jpg")

            # We should not be able to reach this code line
            assert False
        except (ImportError, ValueError):
            # This example should fail with a Value Error or an Import Error
            assert True

    def test_invalid_extension(self):
        """Test an invalid extension in the list file."""
        url_iterator = ListFileURLGenerator("examples/test_invalid_extension.list", "*.jpg")
        assert len([_ for _ in url_iterator]) == 2, repr([_ for _ in url_iterator])

class TestBatchDownloader(unittest.TestCase):    
    """Test class for the BatchDownloader class.
    
    Defines a set of test cases to check handling of invalid URL lists, invalid URLs, incorrect URLs and valid testcases.

    Attributes:
        downloader (object): A BatchDownloader object that is initialized for all test cases. Interactive user requests are disabled.

    """

    def setUp(self):
        """Create a downloader and disable interactive features as we cannot test them in an automated environment."""
        self.downloader = BatchDownloader("download", default_overwrite = True, default_create_directory = True)

    def test_empty_list(self):
        """Test an empty list. The code should throw an exception in this case."""
        try:
            self.downloader.download(None)

            # We should not be able to reach this code line
            assert False
        except TypeError:
            # This example should fail with a Type Error
            assert True

    def test_invalid_list(self):
        """Test an invalid list. The code should throw an exception in this case."""

        try:
            self.downloader.download([None])

            # We should not be able to reach this code line
            assert False
        except TypeError:
            # This example should fail with a Type Error
            assert True

    def test_invalid_link(self):        
        """Test an invalid link. The code should throw an exception if the validators module is present."""

        try:
            # Test importing the validators module. If this fails we cannot execute the test and pass it by default.
            import validators

            self.downloader.download([  "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg", \
                "https:///upload.wikimedia.org/wikipedia/en/7/72/Example-serious.jpg", \
                "https://upload.wikimedia.org/wikipedia/commons/2/29/Example_image_not_be_used_in_article_namespace.jpg"])

            # We should not be able to reach this code line
            assert False
        except (ImportError, IOError):
            # This example should fail with an IO Error or an Import Error
            assert True

    def test_incorrect_link(self):        
        """Test an incorrect link. The code should throw an exception."""
        try:
            self.downloader.download([  "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg", \
                "https://thislinkdoesnotexist.com/Example-serious.jpg", \
                "https://upload.wikimedia.org/wikipedia/commons/2/29/Example_image_not_be_used_in_article_namespace.jpg"])

            # We should not be able to reach this code line
            assert False
        except IOError:
            # This example should fail with an IO Error
            assert True

    def test_valid(self):
        """Test a valid list. This method does not check the results but assumes correctness if no exception was raised."""

        self.downloader.download([  "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg", \
            "https://upload.wikimedia.org/wikipedia/en/7/72/Example-serious.jpg", \
            "https://upload.wikimedia.org/wikipedia/commons/2/29/Example_image_not_be_used_in_article_namespace.jpg"])

        assert True

# If this is the main document, call the unit test main function to automatically run all unit tests
if __name__ == "__main__":
    unittest.main()

