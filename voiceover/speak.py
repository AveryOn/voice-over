import torch
import sys
import sounddevice as sd
from time import time
import numpy as np

SAMPLE_RATE=16000

model, _ = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_tts',
    language='ru',
    speaker='baya_v2'
)

def speak(text):
    sd.default.device = 8

    start = time()
    raw_audio = model.apply_tts(texts=[text], sample_rate=SAMPLE_RATE)

    audio_np = np.array(raw_audio, dtype=np.float32).flatten()

    stereo_audio = np.column_stack((audio_np, audio_np))

    print(f"⏱️ Генерация заняла {round(time() - start, 2)} сек")
    sd.play(stereo_audio, SAMPLE_RATE)
    sd.wait()

if __name__ == "__main__":
    speak(sys.argv[1])
