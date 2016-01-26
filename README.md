BatchJPEGDownloader
===================

BatchJPEGDownloader - A tool for batch downloading a list of JPEG files from any URLs into a specified output directory.

Website: [BatchJPEGDownloader](https://github.com/omeister/BatchJpegDownloader)

## Contents

1. Prerequisites
2. Installation
4. Execution

## Prerequisites

The following prerequisites are necessary in order to install and run sam(oa)²:
* [git](http://git-scm.com/)
* python 2.7 or higher OR python 3.3 or higher

## Installation

### Local Systems

Create a directory (named bjd here) and execute the following steps:

    cd <bjd>
    git clone https://github.com/omeister/BatchJpegDownloader .

This will download the source files for into <bjd>.
Additionally, you may have to install the argparse module in order to read in program arguments. The validators module checks URLs for correctness and is optional. Both can be installed in a single command line:

    pip install argparse validators 

## Execution

Check if everything is correctly installed by running the test script from the main directory:
    
    cd <bjd>
    python test_batchjpegdownloader.py

If all test cases pass, you can run the code now using

    python batchjpegdownloader.py

Refer to the online help with the parameters '-h' or '--help' for runtime arguments.

##Build Status

[![Build Status](https://travis-ci.org/omeister/BatchJpegDownloader.svg)](https://travis-ci.org/omeister/BatchJpegDownloader)
