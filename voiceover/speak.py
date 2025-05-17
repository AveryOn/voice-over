import torch
import sys
import sounddevice as sd
from time import time
import numpy as np
import subprocess

SAMPLE_RATE=16000

torch.set_default_device("cpu")
model, _ = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_tts',
    language='ru',
    speaker='baya_v2'
)

def get_power_profile():
    try:
        result = subprocess.run(['powerprofilesctl', 'get'], stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception:
        return None

def speak(text):
    print(f"[DEBUG] Озвучиваем текст: '{text}'")
    if not text or not text.strip():
        print("❌ Текст для озвучки пустой. Пропускаем.")
        return

    # profile = get_power_profile()
    # print("[MODE]:::", profile)
    # if profile == "performance":
    #     SAMPLE_RATE=11025
    #     sd.default.device = 9
    # else:
    sd.default.device = 8

    start = time()
    raw_audio = model.apply_tts(texts=[text], sample_rate=SAMPLE_RATE)

    audio_np = np.array(raw_audio, dtype=np.float32).flatten()

    stereo_audio = np.column_stack((audio_np, audio_np))

    print(f"⏱️ Генерация заняла {round(time() - start, 2)} сек")
    # sd.play(stereo_audio, SAMPLE_RATE)
    sd.play(stereo_audio, SAMPLE_RATE)
    sd.wait()
    print(1)

if __name__ == "__main__":
    speak(sys.argv[1])
