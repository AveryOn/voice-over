def main():
    import sys
    from voiceover.speak import speak

    if len(sys.argv) < 2:
        print("❌ Нужно передать prompt.")
        sys.exit(1)

    text = sys.argv[1]
    speak(text)
    # import sounddevice as sd
    # print(sd.query_devices())
