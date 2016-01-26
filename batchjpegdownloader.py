#!/usr/bin/python

"""
BatchJPEGDownloader, Copyright (c) 2016 Oliver Meister (o.meister@gmx.net)

This is the main project file of BatchJPEGDownloader, it can be called directly from the 
terminal. 

Downloads a list of JPEG files from any URLs into a specified output directory.

Input:
    A text file that contains a newline-separated list of URLs to JPEG files.
    An output path, where the JPEG files are stored. The directory must exist at the time of calling.
    
Output:
    A list of JPEG files stored in the output directory.
"""

class ArgumentParser:
    """Reads in command line arguments and stores them in object attributes.
    
    This is a wrapper class to the argparse class, allowing a generalization to any other config class.      

    Attributes:
        arguments (object): Program arguments given by the argparse class.

    """

    def __init__(self):
        """Initializes the object by calling the internal parser, reading in program arguments and storing them in the arguments attribute.
        """

        self.arguments = self.parse()

    def parse(self):        
        """Defines arguments for the command line and calls the parser to read them into the arguments attribute.
        """

        # Try importing the argparse module and throw an exception in case importing fails.

        try:
            import argparse
        except ImportError:
            print("Error: Failed to load the argparse library.")
            print(" If you use python 2 below version 2.7 or python 3 below version 3.2, ")
            print(" you may have to install the module using the command")
            print("   pip install argparse")
            print("")
            raise

        # Create a parser object.
        parser = argparse.ArgumentParser(description='Downloads a list of JPEG files into a specified output directory.')
        
        # Add a mandatory output directory argument to ensure the user knows where the data is stored.
        parser.add_argument('-o', '--out', type=str, required = True, help='Output directory, where the JPEG files will be stored.')

        # Add a mandatory positional argument for the JPEG list file.
        parser.add_argument('FILE', type=str, help='Text file that contains a URL link to a JPEG file in each line.')
       
        # Add an optional argument to ensure the user knows where the data is stored.
        parser.add_argument('-c', '--create', nargs='?', type=bool, const = True, default= False, help='If true, the output directory will be created if it does not exist.')
        
        # Add an optional argument to ensure the user knows where the data is stored.
        parser.add_argument('-f', '--force', nargs='?', type=bool, const = True, default= False, help='If true, existing files will be overwritten.')
        
        # Parse the program arguments. argparse will check if all arguments have been correctly provided.
        arguments = parser.parse_args()

        return arguments
        
    @property
    def jpeg_list_file(self):        
        """Text file that contains a URL link to a JPEG file in each line.
        """
        return self.arguments.FILE
        
    @property
    def output_directory(self):        
        """Output directory, where the JPEG files will be stored.
        """
        return self.arguments.out
        
    @property
    def force_download(self):        
        """If true, existing files will be overwritten.
        """
        return self.arguments.force
        
    @property
    def create_output_directory(self):        
        """If true, the output directory will be created if it does not exist.
        """
        return self.arguments.create

class ListFileURLGenerator:
    """Reads a list of URLs from a file and iterates over it.
    
    This class is designed as a generator that iterates over every line of a file and produces
    an URL if the line matches a given pattern.

    Attributes:
        filename (str): Input file that contains a list of URLs, seperated by new lines
        
        pattern (str): File pattern for the generator output. May contain wildcards.
    """

    def __init__(self, filename, pattern = "*"):
        """Initializes a URL generator from a list provided by a text file. The pattern argument allows to filter the URLs by their names.

        Args:
            filename (str):  Input file that contains a list of URLs, seperated by new lines
            pattern (str): Optional filter to include only some file types in the generator. May contain wildcards.

        Example:
            generator = ListFileURLGenerator("example/test_valid.list", "*.jpg")
        """

        self.filename = filename

        # Check if we can open the file and fail otherwise
        try:
            with open(self.filename, 'r') as list_file:
                self.pattern = pattern

                # Use the validators package (if available) to check if the urls are correctly formatted:
                try:
                    import validators
                    
                    # Check if every (non-whitespace) line in the file is a valid URL
                    for url in list_file:
                        # Remove whitespaces from the URL
                        url_no_whitespaces = url.strip()

                        if len(url_no_whitespaces) > 0 and not validators.url(url_no_whitespaces):
                            raise ValueError("Invalid URL: " + repr(url_no_whitespaces) + " in source file " + repr(self.filename))

                except ImportError:
                    # If importing fails, print a warning but continue execution

                    print("Warning: failed to load the validators package.")
                    print("To check URLs for correctness install the module via")
                    print("pip install validators")
                    print("")

        except IOError:
            print("Error: " + repr(filename) + " does not appear to be a valid file.")
            raise

    def __iter__(self):    
        """ Iterates over the list file in the attribute self.filename and generates an object for every 
        line with a valid URL that matches the filter defined in the attribute self.pattern."
        """

        # Load the fnmatch module to test filenames against the user-specified file pattern
        import fnmatch

        # Try opening the file
        with open(self.filename, 'r') as list_file:
            # Process every line of the file as a URL
            for url in list_file:
                # Remove whitespaces from the URL
                url_no_whitespaces = url.strip()

                # Check if the (non-whitespace) URL matches the user-specified file pattern
                # If not, print a warning and skip the file.

                if (url_no_whitespaces != ""):
                    if fnmatch.fnmatch(url_no_whitespaces, self.pattern):
                        # Yield the URL
                        yield url_no_whitespaces
                    else:
                        #Print a warning for any URL that is not recognized as the correct file type
                        print("Warning: Ignoring file " + repr(url_no_whitespaces) + \
                        ", as it does not appear to be of type " + repr(self.pattern) + ".")

class BatchDownloader:
    """
    Downloads files from a list of URLs.

    Downloads a list of files defined in an iterable object. Users must provide a download directory and may provide flags to
    create new directories, overwrite existing files and activate an interactive mode.
    """

    def __init__(self, download_directory, default_overwrite = False, default_create_directory = False):
        """Initializes a batch downloader for a list of files. 
        You may specify a download directory and a set of flags for error handling. 
        If it does not exist yet, the download directory will be created upon request.

        Args:
            download_directory (str): Target directory for the downloaded files.
            default_overwrite (bool): If True, already existing files will be overwritten.
            default_create_directory (bool): If True, the directory will be created if it does not exist already.

        Example:
            downloader = BatchDownloader(download_directory = "downloads", default_create_directory = True)
        """

        self.download_directory = download_directory
        self.default_overwrite = default_overwrite
        self.default_create_directory = default_create_directory

        # Create the download directory if it does not exist yet
        self.create_download_directory()

    def create_download_directory(self):
        """Checks if the download directory exists. 
        If the directory does not exist and permission is given, 
        the directory will be created. Otherwise, it will raise 
        a ValueError exception.
        """

        # We need the OS module to check if the path exists.
        import os

        # For python 3 compatibility, bind input to raw_input in python 2

        try:
           get_input = raw_input
        except NameError:
           get_input = input

        # Check if the directory exists already

        if not os.path.isdir(self.download_directory):
            if (self.default_create_directory):                
                try:
                    # Create the directory.
                    os.mkdir(self.download_directory)
                except OSError:
                    # Ignore OS errors if the directory already exists. This may be caused by a race condition.
                    if not os.path.isdir(self.download_directory):
                        raise
            else:
                raise ValueError("Output directory " + repr(self.download_directory) + " does not exist.")

    def download_file(self, url, filename):
        """Downloads a single file from the given URL to the local system, renaming it 
        to the filename argument in the process. 
        If the file already exists, it will either be overwrittenor skipped.        

        Args:
            url (str): URL to the source 
            filename (str): If True, already existing files will be overwritten.
        """

        # We need the OS module for file output
        import os

        # Bind get_input to raw_input (Python 2) or input (Python 3)

        try:
           get_input = raw_input
        except NameError:
           get_input = input

        # If the file already exists, check if it may be overwritten.

        if os.path.isfile(filename):
            # Skip the file if overwriting is not allowed.

            if not self.default_overwrite:
                print("Skipping already existing file " + repr(filename) +".")
                return

        # Print a status message for each download (without newline)
        from sys import stdout
        stdout.write("Downloading " + repr(url) + " to " + repr(filename) + "...")
            
        # Load the urllib module.
        # For compatibility, try both urllib (Python 2) and urllib.request (Python 3)

        try:
            from urllib import urlretrieve
        except ImportError: 
            from urllib.request import urlretrieve
    
        # Download the file. If an IO Error occurs, forward the exception.

        try:
            urlretrieve(url, filename)
            print("done.")
        except IOError as e:
            print("failed.")
            raise

    def download(self, urls):
        """Download a set of files from the given URL to the local folder defined in the download_directory attribute.   

        Args:
            urls (iterable): an iterable list of URLs that will be downloaded to the folder specified in the download_directory attribute.
        """

        # We need the OS module for portable joining of paths     
        import os

        # Check if the urls list is an iterable and throw a Type Error otherwise.

        try:
            iterator = iter(urls)
        except TypeError:
            print("Error: " + repr(urls) + " object is not iterable.")
            raise

        # Iterate over the list of URLS and download them to the download directory
        for url in urls:
            # Get the filename without its path by splitting the URL at the last '/' and taking the right substring
            # If the rsplit method is not found, throw a Type Error as the URL does not appear to be a string.

            try:
                filename_without_path = url.rsplit('/', 1)[-1]
            except AttributeError:
                raise TypeError("Error: " + repr(url) + " object in " + repr(urls) + " is not of type string.")

            # Combine the filename with the download directory to get the local filename
            filename = os.path.join(self.download_directory, filename_without_path)
            
            # Download the file from the URL and save it as filename
            self.download_file(url, filename)

        print("Done.")

def main():
    """Main entry point of the program.

    The main() method is invoked when the script is called directly from command line. 
    It parses the program arguments for a file that contains a list of URLs and passes it to the URL generator 
    that extracts the URLs and is iterable. Next, a batch downloader class is created together with an output directory. 
    Finally, the URL generator is passed to the downloader to start downloading the files into the output path.
    """

    print("BatchJPEGDownloader, Copyright (c) 2016 Oliver Meister")
    print("")

    #Create a config object that reads the list filename and output path from program arguments
    config = ArgumentParser()

    # Create a generator over the list file and specify that we are interested in the JPEG format only
    url_iterator = ListFileURLGenerator(config.jpeg_list_file, "*.jpg")

    # Create a downloader
    downloader = BatchDownloader(download_directory = config.output_directory, \
        default_overwrite = config.force_download, default_create_directory = config.create_output_directory)

    # Download all the files given by the generator
    downloader.download(url_iterator)

# If this is the main document, call the main function to read in program arguments.
if __name__ == "__main__":
    main()

