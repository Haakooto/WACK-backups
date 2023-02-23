from src import embed, dislodge
import os
import sys

def main(inp):
    name, ext = inp.split(".")
    if ext == "py":
        embed.main(inp)
        os.rename("output.avi", f"{name}.avi")
    elif ext == "avi":
        dislodge.main(inp)
        os.rename("output.py", f"{name}.py")

if __name__ == "__main__":
    main(sys.argv[1])
    