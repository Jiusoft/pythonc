import os, sys
args = sys.argv[1:]

def main():
    if os.path.exists(args[0]):
        code = []
        with open(args[0]) as f:
            for line in f:
                code.append(line.strip("\n"))
            filename = args[0].split("/")[-1].split(".")[0]

        with open(f"{filename}.tmpbash", 'w') as f:
            f.write("#!/bin/bash\n\npython3 -c \"\nimport os\n__file__ = f\\\"{os.getcwd()}/"+args[0].split("/")[-1]+"\\\"\n\n")
            for line in code:
                line = line.replace("\\", "\\\\").replace("\"", "\\\"")
                f.write(f"{line}\n")
            f.write("\n\" $@")

        os.system(f"shc -f {filename}.tmpbash")
        #os.remove(f"{filename}.tmpbash")
        os.remove(f"{filename}.tmpbash.x.c")
        os.rename(f"{filename}.tmpbash.x", f"{filename}.binary")
    else:
        print("ERROR: File not found. ")


def help():
    print("""Usage: pythonc script-to-compile.py

Arguments:
-h or --help: Print Help""")

if len(args)==0 or len(args)>1 or args[0]=="-h" or args[0]=="--help":
    help()
else:
    main()