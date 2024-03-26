from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
from pathlib import Path
import urllib.request
import zipfile
import json
import os
import sys

def main():
    if not CheckFolders():
        return
    
    FRAME_RATE = 16000

    model = Model("model")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    try:
        aud = InputFile()

        rec.AcceptWaveform(aud.raw_data)
        result = rec.Result()
        text = json.loads(result)["text"]

        with open('data.txt', 'w') as f:
            json.dump(text, f, ensure_ascii=False, indent=4)
    except:
        print("Error")
        return

def InputFile() -> str:
    file = input("Введите путь к файлу: ")
    extension = Path(file).suffix
    return Preprocessing(extension, file)

def Preprocessing(ex, file) -> any:
    FRAME_RATE = 16000
    CHANNELS=1
    if ex == ".mp3":
        audio = AudioSegment.from_mp3(file)
        audio = audio.set_channels(CHANNELS)
        audio = audio.set_frame_rate(FRAME_RATE)
        return audio
    elif ex == ".wav":
        audio = AudioSegment.from_wav(file)
        audio = audio.set_channels(CHANNELS)
        audio = audio.set_frame_rate(FRAME_RATE)
        return audio
    return

def CheckFolders() -> bool:
    if not os.path.exists("model"):
        print("Not exist Model")
        result = input("Do you want to download the model? (y/n): ")
        if (result == "y" or result == "Y"):
            return DownLoadFile()
        return False
    return True

def DownLoadFile():
    try:
        file_url = 'https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip'
        file_name = 'vosk-model-ru-0.22.zip'
        urllib.request.urlretrieve(file_url, file_name, reporthook)
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall()
        os.rename('vosk-model-ru-0.22', 'model')
        return True
    except:
        return False
    
def reporthook(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    print(f'Downloading: {percent}%', end='\r', flush=True)

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit