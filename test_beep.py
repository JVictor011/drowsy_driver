"""Test the beep alert function"""
import sys
sys.path.insert(0, 'src')

from drowsy_driver.alert.beep import beep

print("Testing beep function...")
print("You should hear a sound now:")
beep()
print("Did you hear the sound? (y/n)")
