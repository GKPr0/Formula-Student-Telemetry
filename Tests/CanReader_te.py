"""
This script will run all defined unit test in chosen directories.
"""

import subprocess

# List of directory with test files
directories = ("Communication",
             "Config",
             "DataProcessing",
             "GUI")

if __name__ == "__main__":

    for dir in directories:
        # Loop over all directory and run test files within
        cmd = 'python -m unittest discover -s' + dir + ' -p "*_test.py"'
        print("\n Runing test in /" + dir)
        subprocess.call(cmd)
    print("linux-test")
