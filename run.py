"""Run the drowsy driver detection application"""
import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from drowsy_driver import run

if __name__ == "__main__":
    run()
