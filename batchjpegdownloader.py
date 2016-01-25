#!python
#
# @file This is the main project file, it can be called directly from the 
# terminal or with the method batch_jpeg_download.
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
# Downloads a list of JPEG files from any URLs into a specified output directory.
#
# Input:
#        * A text file that contains a newline-separated list of URLs to JPEG files.
#        * An output path, where the JPEG files are stored. The directory must exist at the time of calling.
#        
# Output:
#        * A list of JPEG files stored in the output directory.

class URLListFileIterator:
    def __init__(self, list_file, valid_extensions):
        self.list_file = list_file
        self.valid_extensions = valid_extensions
    
        # Use the validators package to check if the url is correct:
        try:
            from validators import url

            # Check if every line in the file is a valid URL
            for url in open(self.list_file):          
                assert validators.url(url)

        except ImportError:
            print "Warning: failed to load the validators package."
            print "To check URLs for correctness install the module via" 
            print "pip install validators"
            print ""

    def __iter__(self):
        # Process every line of the file as a URL
        for url in self.list_file:
            # Remove white spaces from the URL
            url_no_whitespaces = url.strip()
    
            # Get the file extension by splitting the URL at the last '.' and taking the right substring
            extension = url_no_whitespaces.rsplit('.', 1)[-1]

            # Check if the URL has the correct extension.
            # If not, print a warning and skip it.

            if extension in self.valid_extensions:
                # Yield the URL
                yield url_no_whitespaces
            elif len(extension) > 0:
                #Print a warning for any (non-whitespace) line in the file that is not recognized as a URL
                print "Warning: Ignoring file " + url_no_whitespaces + ", as it does not appear to be of type " + repr(self.valid_extensions) + "."

# @author Oliver Meister (o.meister@gmx.net)
#ght
# @section DESCRIPTION
#
# 

class BatchDownloader:
    def __init__(self, download_directory, default_overwrite = False, default_create_directory = False, prompt_if_error = True):
        self.download_directory = download_directory
        self.default_overwrite = default_overwrite
        self.default_create_directory = default_create_directory
        self.prompt_if_error = prompt_if_error

        self.create_download_directory()

    def create_download_directory(self):
        import os

        if not os.path.exists(self.download_directory):
            if self.prompt_if_error:
                print "Warning: Directory '" + self.download_directory + "' does not exist."

                # 'yes' and 'no' are valid answers
                valid_answers = ("yes", "no")

                # Read case-insensitive user input from the command line (TODO: is there a more elegant way to do this?)
                prompt_overwrite = raw_input("Create " + repr(valid_answers) + " ? ").lower()

                # If the user input is not valid, repeat the question until it is.
                while prompt_overwrite not in valid_answers:
                    prompt_overwrite = raw_input("Please enter one of " + repr(valid_answers) + " : ").lower()
                
                # Create directory on user request.
                create_dir = prompt_overwrite in ("yes")
            else:
                # If prompt is disabled, use the default setting
                create_dir = self.default_create_directory
            
            # If a directory should be created, do it.
            # Otherwise, throw an exception as we cannot continue from here.
            
            if (create_dir):
                os.mkdir(self.download_directory)
            else:
                print "Error: Cannot create directory '" + self.download_directory + "'. Aborting.."
                quit()

    def download_file(self, url, filename):
        import os

        # If the file already exists, prompt for overwriting or skipping

        if os.path.isfile(filename):
            if self.prompt_if_error:
                print "Warning: File '" + filename + "' already exists: "   

                # 'yes', 'no', 'all', and 'none' are valid answers
                valid_answers = ("yes", "no", "all", "none")

                # Read case-insensitive user input from the command line
                prompt_overwrite = raw_input("Overwrite " + repr(valid_answers) + "? ").lower()

                # If the user input is not valid, repeat the question until it is.
                while prompt_overwrite not in valid_answers:
                    prompt_overwrite = raw_input("Please enter one of " + repr(valid_answers) + " : ").lower()
                
                #Set flags according to user input
                self.overwrite = prompt_overwrite in ("yes", "all")
                self.prompt_if_error = prompt_overwrite in ("yes", "no")
            
            # If prompt is disabled, use the default setting

            # Skip the file if overwriting is not allowed.

            if not self.overwrite:
                print "Skipping already existing file '" + filename +"'."
                return

        # Try loading the urllib module for downloading

        try:
            import urllib
        except ImportError:
            print "Error: Failed to load the urllib library."            
            print "You may have to install the module using the command" 
            print "pip install urllib"
            quit()
            
        # Download the file to the target directory.

        print "Downloading " + url + " to " + filename + "...",
        urllib.urlretrieve(url, filename)
        print "done."

    def download(self, urls):
        # We need the OS module for file I/O       
        import os
        
        create_dir = self.default_create_directory
        prompt_if_error = self.prompt_if_error

        # Create the download directory if it does not exist yet
        self.create_download_directory()

        # Before downloading, set overwrite settings back to default
        overwrite_files = self.default_overwrite
        prompt_if_error = self.prompt_if_error

        # Check if the urls list is an iterable and fail otherwise.

        try:
            iterator = iter(urls)
        except TypeError:
           print "Error: ", urls, " object must be iterable."

        # Iterate through the list of URLS and download them to the download directory
        for url in urls:
            # Get the filename without its path by splitting the URL at the last '/' and taking the right substring
            filename_without_path = url.rsplit('/', 1)[-1]

            # Combine the filename with the download directory to get the local filename
            filename = os.path.join(self.download_directory, filename_without_path)
            
            # Download the file from the URL and save it as filename
            self.download_file(url, filename)

        print "Done."

# @author Oliver Meister (o.meister@gmx.net)
#
# @section DESCRIPTION
#
# This is a wrapper class to the argparse class, allowing a generalization to any other config class.

class ArgumentParser:
    def __init__(self):
        self.arguments = self.parse()

    def parse(self):
        # The main script uses the arparse module to parse program aguments. 
        # Try importing the module and throw an exception in case it fails to do so.

        try:
            import argparse
        except ImportError:
            print "Error: Failed to load the argparse library."
            print " If you use python 2 below version 2.7 or python 3 below version 3.2, "
            print " you may have to install the module using the command" 
            print "   pip install argparse"
            print ""
            print "Original error message:"
            raise

        # Create a parser object.
        parser = argparse.ArgumentParser(description='Downloads JPEG files given by a list of URLs into a specified output directory..')
        
        # Add a mandatory output directory argument to ensure the user knows where the data is stored.
        parser.add_argument('--output_path', type=str, required = True, help='An output path, where the JPEG files are stored.')
        
        # Add a mandatory positional argument for the JPEG list file.
        parser.add_argument('jpeg_list_file', metavar='jpeg_list_file', type=file, help='A text file that contains a newline-separated' \
'list of URLs to JPEG files.')

        # Parse the program arguments. argparse will check if all arguments have been correctly provided.
        arguments = parser.parse_args()

        return arguments
        
    @property
    def jpeg_list_file(self):
        return self.arguments.jpeg_list_file
        
    @property
    def output_path(self):
        return self.arguments.output_path

# @author Oliver Meister (o.meister@gmx.net)
#
# @section DESCRIPTION
#
# The main() method is invoked when the script is called directly from command line. 
# It parses the program arguments for the list file and passes it to the URL iterator 
# that returns an iterable. The URL iterator is passed to a batch downloader class that 
# starts downloading the files into the output path.

def main():
    print "BatchJpegDownloader, copyright 2016 by Oliver Meister"
    print ""

    #Create a config object that reads the list filename and output path from program arguments
    config = ArgumentParser()
    
    # Create an iterator over the list file and specify that we are interested in the JPEG format only
    url_iterator = URLListFileIterator(config.jpeg_list_file, ("jpg", "jpeg"))

    # Create a downloader
    downloader = BatchDownloader(config.output_path)

    # Download all the files given by the iterator
    downloader.download(url_iterator)

# If this is the main document, call the main function to read in program arguments.
if __name__ == "__main__":
    main()
