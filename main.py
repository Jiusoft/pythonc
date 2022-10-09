import os, sys
from zipfile import ZipFile as zipopen
args = sys.argv[1:]

def license():
    print("""MIT License

Copyright (c) 2022 Jiusoft

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""")

def main():
    if os.path.exists(args[0]):
        zipfile = args[0].split("/")[-1].split('.')[0]
        if os.path.exists(zipfile):
            os.remove(zipfile)
        with open(zipfile, 'a') as f:
            f.write(f"#!/bin/sh\ncommand -v python3 >/dev/null 2>&1 || echo 'Python 3 required to run this executable.' && python3 {args[0].split('/')[-1]} \"$@\"\nexit 0\n")
        with zipopen(zipfile, 'a') as f:
            f.write(args[0])
        os.system(f"shc -r -f {zipfile}")
        os.remove(zipfile)
        os.remove(f"{zipfile}.x.c")
        os.rename(f"{zipfile}.x", zipfile)
    else:
        print("ERROR: File not found. ")


def help():
    print("""PythonC v0.1.1
Usage: pythonc script-to-compile.py

Arguments:
-h or -H or --help: Print Help
-l or -L or --license: View License Agreement""")


if len(args)==0 or args[0]=="-h" or args[0]=="-H" or args[0]=="--help":
    help()
elif args[0]=="-l" or args[0]=="-L" or args[0]=="--license":
    license()
elif len(args)>1:
    print("ERROR: Expected ONE argument. ")
else:
    main()
