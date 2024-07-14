import os
import sys
from pydub import AudioSegment
from pydub.utils import which
import numpy as np
from scipy.fftpack import fft

# Set the paths to ffmpeg and ffprobe
AudioSegment.ffmpeg = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

def get_audio_fingerprint(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_channels(1)  # Convert to mono
        audio = audio.set_frame_rate(44100)  # Standardize sample rate
        samples = np.array(audio.get_array_of_samples())
        return np.abs(fft(samples))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        raise

def compare_audio_files(file1, file2):
    print(f"Comparing {file1} with {file2}")
    try:
        fingerprint1 = get_audio_fingerprint(file1)
        fingerprint2 = get_audio_fingerprint(file2)
        return np.linalg.norm(fingerprint1 - fingerprint2) / len(fingerprint1)
    except Exception as e:
        print(f"Error comparing files '{file1}' and '{file2}': {e}")
        return float('inf')

def find_duplicates(directory, threshold=1.0):  # Adjust threshold here
    files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith('.mp3'):
                files.append(os.path.join(dirpath, filename))

    print(f"Directory path: {directory}")
    print(f"Found {len(files)} MP3 files:")
    for f in files:
        print(f" - {f}")
    
    duplicates = []
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            similarity_score = compare_audio_files(files[i], files[j])
            if similarity_score < threshold:  # Adjust threshold as needed
                duplicates.append((files[i], files[j], similarity_score))
    return duplicates

if __name__ == "__main__":
    directory = input("Please enter the directory path containing your MP3 files: ").strip()
    if not os.path.isdir(directory):
        print("The provided path is not a valid directory.")
        sys.exit(1)
    else:
        duplicates = find_duplicates(directory)
        if duplicates:
            for file1, file2, score in duplicates:
                print(f"Duplicate found: {file1} and {file2} with similarity score {score}")
        else:
            print("No duplicates found.")
