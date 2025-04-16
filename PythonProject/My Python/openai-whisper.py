import os
import json
import whisper
from pathlib import Path

model=whisper.load_model("tiny")
media_extensions={".mp3",".wav",".m4a",".mp4",".mkv",".mov",".avi"}

def find_media_files(path):
    path=Path(path)
    if path.is_file() and path.suffix.lower() in media_extensions:
        return [str(path)]
    elif path.is_dir():
        media_files=[]
        for root,_, files in os.walk(path):
            for file in files:
                if Path(file).suffix.lower() in media_extensions:
                    media_files.append(os.path.join(root, file))
        return media_files
    else:
        print(f"Error:{path} is not a valid media file or directory")
        return []

def transcribe_file(file_path):
    print(f"Transcribing:{file_path}")
    result=model.transcribe(str(file_path))
    return result["text"]

def save_transcription(file_path,transcription,output_dir):
    output_file=Path(output_dir)/(Path(file_path).stem+".json")
    with open(output_file,"w",encoding="utf-8") as f:
        json.dump({"file":str(file_path),"transcription":transcription},f,indent=4)
    print(f"Saved transcription to: {output_file}")

def process_media(input_path, output_dir):
    media_files=find_media_files(input_path)
    os.makedirs(output_dir, exist_ok=True)
    if not media_files:
        print("No valid media files found.")
        return
    for media_file in media_files:
        transcription= transcribe_file(media_file)
        save_transcription(media_file, transcription, output_dir)

input_path=r"E:\audio.mp3"
output_directory=r"D:\whisper"

process_media(input_path, output_directory)




