import sys

def beep():
    if sys.platform.startswith("win"):
        import winsound
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
    else:
        print("\a", end="", flush=True)
