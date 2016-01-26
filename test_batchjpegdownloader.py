#!/usr/bin/python
#
# @file This file contains a set of unit tests for batchjpegdownloader.
#
# @author Oliver Meister (o.meister@gmx.net)
#
# @section LICENSE
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Oliver Meister

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# @section DESCRIPTION
#
# Executes unit tests for the ListFileURLGenerator class, the 
#
# Input:
#        * none.
#        
# Output:
#        * none.

import unittest
from batchjpegdownloader import ListFileURLGenerator, BatchDownloader

class TestListFileURLGenerator(unittest.TestCase):
    def test_invalid_file(self):
        # Test an invalid list file
        url_iterator = ListFileURLGenerator(None, ())
        assert len([_ for _ in url_iterator]) == 0, repr([_ for _ in url_iterator])

    def test_empty_extensions(self):
        # Test an empty set of extensions
        url_iterator = ListFileURLGenerator(open("unit_tests/test_valid.list"), ())
        assert len([_ for _ in url_iterator]) == 0, repr([_ for _ in url_iterator])

    def test_wrong_extensions(self):
        # Test an empty set of extensions
        url_iterator = ListFileURLGenerator(open("unit_tests/test_valid.list"), ("wrong"))
        assert len([_ for _ in url_iterator]) == 0, repr([_ for _ in url_iterator])

    def test_valid(self):
        # Test an empty set of extensions
        url_iterator = ListFileURLGenerator(open("unit_tests/test_valid.list"), ("jpg"))
        assert len([_ for _ in url_iterator]) == 3, repr([_ for _ in url_iterator])

    def test_incorrect_link(self):
        # Test an incorrect link in the list file
        url_iterator = ListFileURLGenerator(open("unit_tests/test_incorrect_link.list"), ("jpg"))
        assert len([_ for _ in url_iterator]) == 2, repr([_ for _ in url_iterator])

    def test_invalid_link(self):
        # Test an invalid link in the list file
        url_iterator = ListFileURLGenerator(open("unit_tests/test_invalid_link.list"), ("jpg"))
        assert len([_ for _ in url_iterator]) == 2, repr([_ for _ in url_iterator])

    def test_invalid_extension(self):
        # Test an invalid extension in the list file
        url_iterator = ListFileURLGenerator(open("unit_tests/test_invalid_extension.list"), ("jpg"))
        assert len([_ for _ in url_iterator]) == 2, repr([_ for _ in url_iterator])

# If this is the main document, call the unit test main function to automatically run all unit tests
if __name__ == "__main__":
    unittest.main()

