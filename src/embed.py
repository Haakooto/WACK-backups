from gtts import gTTS
from pydub import AudioSegment
from subprocess import Popen, PIPE
import os
import sys


to_letters = {'0': 'zero',
              '1': 'one',
              '2': 'two',
              '3': 'three',
              '4': 'four',
              '5': 'five',
              '6': 'six',
              '7': 'seven',
              '8': 'eight',
              '9': 'nine',
              'stop': 'stop'}

def make_audio_units():
    # * Function for making a soundbyte for each number
    # * Using gTTS to make .mp3, then pydub to convert to .wav
    # * Need only be called once
    for num, let in to_letters.items():
        tts = gTTS(let, lang="en", tld="us", slow=False)
        tts.save(f"audio_bits/{num}.mp3")
        mp3 = AudioSegment.from_mp3(f"audio_bits/{num}.mp3")
        mp3.export(f"audio_bits/{num}.wav", format="wav")
        os.remove(f"audio_bits/{num}.mp3")


def say(source: str):
    # * Makes an ascii-'encoded' audio file from the given source
    # * For each character in source, convert to ascii-number,
    # * split up digits, and set everything together, with characters separated by a 'stop'
    # * Outputs an audio-file with each digits said out loud.
    ascii = [" ".join([n for n in str(ord(i))]) for i in source]
    merged = " stop ".join(ascii).split(" ")
    try:
        sound_files = [AudioSegment.from_wav(
            f"audio_bits/{num}.wav") for num in merged]
    except FileNotFoundError:
        make_audio_units()
        say(source)
    else:
        combined_sound = sum(sound_files)
        combined_sound.export(f"output.wav", format="wav")


def to_video():
    # * Converts .wav to .avi using Infinate-Storage-Glitch
    cmd = "./isg_4real embed -i output.wav -p paranoid --mode colored --block-size 4 --threads 8 --fps 10 --resolution 360"
    p = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
    p.communicate()
    os.remove("output.wav")


def main(path):
    source = open(path, "r").read()
    say(source)
    os.remove(path)
    to_video()


if __name__ == "__main__":
    main(sys.argv[1])

