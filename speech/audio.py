# 音声作成

import io
import wave
import sounddevice as sd
import numpy as np

from core.data.exception.voice_exception import VoicePlaybackError

def play(wav_data: bytes):
    try:
        wav_file = wave.open(io.BytesIO(wav_data), "rb")
        sample_rate = wav_file.getframerate()
        wav_array = np.frombuffer(wav_data, dtype=np.int16)
        sd.play(wav_array, sample_rate, blocking=False)
    except:
        raise VoicePlaybackError()

def wait():
    try:
        sd.wait()
    except:
        raise VoicePlaybackError()
    