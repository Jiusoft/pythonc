import os, sys
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

def main(output=None):
    if os.path.exists(args[0]):
        code = []; code.append(line.strip("\n") for line in open(args[0]))
        filename = args[0].split("/")[-1].split(".")[0]

        with open(f"{filename}.tmpbash", 'w') as f:
            f.write("#!/bin/bash\n\nfilepath=$(realpath $0)\n\npython3 -c '\nimport os, sys\n__file__ = sys.argv[0] = '\"\\\"$filepath\\\"\"'\n\n")
            for line in code:
                line = line.replace("'", "'\"'\"'")
                f.write(f"{line}\n")
            f.write("' \"$@\"")

        os.system(f"shc -f {filename}.tmpbash")
        os.remove(f"{filename}.tmpbash")
        os.remove(f"{filename}.tmpbash.x.c")
        if output is None:
            os.rename(f"{filename}.tmpbash.x", f"{filename}.binary")
        else:
            os.rename(f"{filename}.tmpbash.x", f"{output}")
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
elif args[0]=="-l" or args[0]=="-L" or args[0]=="--license" or args[0]=="--licence":
    license()
elif len(args)==2 and ('-h', '-H', '--help', '-l', '-L', '--license', '--licence') not in args:
    print("ERROR: Expected ONE argument. ")
else:
    main()
