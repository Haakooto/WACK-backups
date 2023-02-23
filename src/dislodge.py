from subprocess import Popen, PIPE
from scipy.io import wavfile
import os
import sys


def recover_audio(path, here):
    cmd = f"{here}/isg_4real dislodge -i {path} -o re_audiod.wav"
    p = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
    p.communicate()
    os.remove(path)


def transcribe(here):
    base_files = {str(i): wavfile.read(f"{here}/audio_bits/{i}.wav")[1] for i in range(10)}
    base_files["stop"] = wavfile.read(f"{here}/audio_bits/stop.wav")[1]
    lens = {k: len(v) for k, v in base_files.items()}

    infile = wavfile.read("re_audiod.wav")[1]
    os.remove("re_audiod.wav")
    head = 0
    msg = ""

    while head < len(infile):
        for num in base_files.keys():
            if (infile[head: head + lens[num]] == base_files[num]).all():
                if num == "stop":
                    msg += " "
                else:
                    msg += num
                head += lens[num]
                break
    return msg


def decode(source):
    return "".join([chr(int(i)) for i in source.split(" ")])


def main(name, here="src"):
    recover_audio(name, here)
    ascii = transcribe(here)
    content = decode(ascii)
    exec(content)
    with open("output.py", "w") as f:
        f.write(content)


if __name__ == "__main__":
    main(sys.argv[1], ".")

