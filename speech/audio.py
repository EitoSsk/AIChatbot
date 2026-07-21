# 音声作成

import io
import wave
import sounddevice as sd
import numpy as np

def play(wav_data: bytes):
    wav_file = wave.open(io.BytesIO(wav_data), "rb")
    sample_rate = wav_file.getframerate()
    wav_array = np.frombuffer(wav_data, dtype=np.int16)
    sd.play(wav_array, sample_rate, blocking=False)

def wait():
    sd.wait()