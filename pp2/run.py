import os
import subprocess
import serial
from start import start

ser = None

if start():
    subprocess.run(["python", "main.py"])
