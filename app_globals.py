import sys, os

for dirpath, dirnames, filenames in os.walk(os.path.abspath('.')):
    sys.path.append(dirpath)
