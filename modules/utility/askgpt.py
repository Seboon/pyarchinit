
from qgis.PyQt.QtWidgets import *
import socket
import sys, subprocess
try:
    import openai
    if openai.__version__ != "0.27.8":
        raise ImportError
        print("openai is already installed")
except ImportError:
    print("openai is not installed, installing...")
    if sys.platform.startswith("win"):
        subprocess.call(["pip", "install", "openai==0.27.8"],shell = False)
    elif sys.platform.startswith("darwin"):
        subprocess.call([ "/Applications/QGIS.app/Contents/MacOS/bin/python3", "-m", "pip","install", "openai==0.27.8"],shell = False )
    elif sys.platform.startswith("linux"):
        subprocess.call(["pip", "install", "openai==0.27.8"],shell = False)
    else:
        raise Exception(f"Unsupported platform: {sys.platform}")
    print("openai installed successfully")

try:
    import openpyxl

except ImportError:
    print("openpyxl is not installed, installing...")
    if sys.platform.startswith("win"):
        subprocess.call(["pip", "install", "openpyxl"],shell = False)
    elif sys.platform.startswith("darwin"):
        subprocess.call([ "/Applications/QGIS.app/Contents/MacOS/bin/python3", "-m", "pip","install", "openpyxl"],shell = False )
    elif sys.platform.startswith("linux"):
        subprocess.call(["pip", "install", "openpyxl"],shell = False)
    else:
        raise Exception(f"Unsupported platform: {sys.platform}")
    print("openpyxl installed successfully")


import time
import os
class MyApp(QWidget):

    def __init__(self,parent):
        super().__init__(parent)

    def ask_gpt(self,prompt,apikey,model):
        openai.api_key = apikey
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model = model,
                    messages = [
                        {"role": "system", "content": prompt}]
                )
                return response['choices'][0]['message']['content']
            except openai.error.APIError as e:
                if e.status == 429:
                    time.sleep(5)
                else:
                    raise e

    def is_connected(self):
        try:
            # Try to connect to one of the DNS servers
            socket.create_connection(("1.1.1.1", 53))
            return True
        except OSError:
            pass
        return False

