# 音声作成

import io
import wave
import simpleaudio

def play(data: bytes):
    wav_file = wave.open(io.BytesIO(data), "rb")

    channels = wav_file.getnchannels()
    sample_width = wav_file.getsampwidth()
    sample_rate = wav_file.getframerate()
    pcm_data = wav_file.readframes(wav_file.getnframes())
    play_obj = simpleaudio.play_buffer(
        pcm_data,
        channels,
        sample_width,
        sample_rate,
    )
    play_obj.wait_done()