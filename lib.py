import os
def buildDirectories(path,directories):
    p = os.getcwd()
    os.chdir(path)
    for directory in directories:
        if directory not in os.listdir():
            os.mkdir(directory)
        buildDirectories(directory,directories[directory])
    os.chdir(p)