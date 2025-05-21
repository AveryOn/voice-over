import torch
import sys
import sounddevice as sd
from time import time
import numpy as np
import subprocess
import re

SAMPLE_RATE=16000

torch.set_default_device("cpu")
model, _ = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_tts',
    language='ru',
    speaker='baya_v2'
)

def pad_if_too_short(text, pad='...'):
    return f'{pad} {text} {pad}' if len(text.strip()) <= 2 else text

def ensure_end_punctuation(s):
    return s if s[-1] in '.!?…' else s + '.'

def clean_text(text):
    return re.sub(r'[^\w\s.,!?А-Яа-яЁёA-Za-z0-9-]', '', text)

def get_power_profile():
    try:
        result = subprocess.run(['powerprofilesctl', 'get'], stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception:
        return None

def speak(text: str):
    if not text or not text.strip():
        print("❌ Пустой текст, пропускаем.")
        return

    print(f"[DEBUG] Озвучиваем: '{text}'")
    sd.default.device = 8
    PAUSE = np.zeros((int(SAMPLE_RATE * 0.2), 2), dtype=np.float32)
    audio_chunks = []

    try:
        text = clean_text(text)
        text = ensure_end_punctuation(text)
        text = pad_if_too_short(text)

        # chunk = model.apply_tts([text], sample_rate=SAMPLE_RATE)
        chunk = model.apply_tts([text], sample_rate=SAMPLE_RATE)[0] 
        # stereo = np.column_stack((chunk, chunk)).astype(np.float32)
        if len(chunk.shape) == 1:
            stereo = np.column_stack((chunk, chunk)).astype(np.float32)
        else:
            stereo = chunk.astype(np.float32)
        audio_chunks.append(stereo)
        audio_chunks.append(PAUSE)
    except Exception as e:
        print(f"[FALLBACK] Ошибка озвучки через Silero: {e}")
        try:
            subprocess.run(["spd-say", text])
        except Exception as fallback_error:
            print(f"[FALLBACK FAILED] {fallback_error}")
        return

    if not audio_chunks:
        print("[EMPTY AUDIO] Нет данных для воспроизведения.")
        return

    final_audio = np.concatenate(audio_chunks)
    start = time()

    print(f"⏱️ Генерация заняла {round(time() - start, 2)} сек")

    for attempt in range(3):
        try:
            sd.play(final_audio, SAMPLE_RATE)
            sd.wait()
            break
        except Exception as e:
            print(f"[AudioError] Попытка {attempt+1}: {e}")
            subprocess.run(['systemctl', '--user', 'restart', 'pipewire', 'pipewire-pulse'])
            time.sleep(2)

if __name__ == "__main__":
    speak(sys.argv[1])
