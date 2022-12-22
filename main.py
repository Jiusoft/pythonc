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
        print("Started Compilation...")
        code = [line.strip("\n") for line in open(args[0])]
        filename = args[0].split("/")[-1].split(".")[0]

        with open(f"{filename}.tmpbash", 'w') as f:
            f.write("""#!/bin/bash

install_python() {
    echo "Python Installation Not Found, Installing Python..."
    read -sp "Please Enter Sudo Password for Permissions: " password
    if [ -x "$(command -v apt)" ]; then
        echo $password | sudo -S apt install python3 python3-pip python3-tk &> /dev/null
    elif [ -x "$(command -v dnf)" ]; then
        echo $password | sudo -S dnf install python3 python3-pip python3-tk &> /dev/null
    else
        echo "Package Manager Not Supported. Please Install Python Manually!"
    fi
}

execute_python() {
    python3 -c '__file__="'"$(pwd)/$0"'"\n""")
            for idx, line in enumerate(code):
                if all(i in line for i in ('import', 'sys')):
                    if line.startswith('    '):
                        nt = len(line) - len(line.lstrip('    '))
                    elif line.startswith('\t'):
                        nt = len(line) - len(line.lstrip('\t'))
                    else:
                        nt = 0
                    line = line.replace("'", "'\"'\"'")
                    ps = "\n"
                    for _ in range(nt):
                        ps+='\t'
                    ps += "sys.argv[0] = \"'\"$0\"'\""
                    line += ps
                    f.write(f"{line}" if idx == len(code)-1 else f"{line}\n")
                else:
                    line = line.replace("'", "'\"'\"'")
                    f.write(f"{line}" if idx == len(code)-1 else f"{line}\n")
            f.write("""' "$@"
}

[[ "$(python3 -V)" =~ "Python 3" ]] || install_python && execute_python "$@"\n""")
        os.system(f"shc -rf {filename}.tmpbash > /dev/null 2>&1")
        os.remove(f"{filename}.tmpbash")
        os.remove(f"{filename}.tmpbash.x.c")
        if output is None:
            os.rename(f"{filename}.tmpbash.x", f"{filename}.binary")
        else:
            os.rename(f"{filename}.tmpbash.x", f"{output}")
        print("Compilation Finished!")
    else:
        print("ERROR: File not found. ")


def help():
    print("""PythonC v2.0.0
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
