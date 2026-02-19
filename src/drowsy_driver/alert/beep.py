from __future__ import annotations
import sys

def beep():
    """Play an alert sound"""
    if sys.platform.startswith("win"):
        import winsound
        # Toca um som de sistema mais alto
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        # Também toca beeps audíveis: frequência 1000Hz por 500ms, 3 vezes
        try:
            for _ in range(3):
                winsound.Beep(1000, 200)  # 1000Hz, 200ms
        except RuntimeError:
            # Se não conseguir tocar beep, tenta som do sistema
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    else:
        # Unix/Linux/Mac
        print("\a" * 3, end="", flush=True)
