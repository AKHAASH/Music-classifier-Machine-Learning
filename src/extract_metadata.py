import os
from mutagen.id3 import ID3

def extract_artist(file_path):
    try:
        audio = ID3(file_path)
        artist_tag = audio.get('TPE1')  # 'TPE1' is the ID3 tag for artist
        artist = artist_tag.text[0] if artist_tag else 'Unknown Artist'
        if ' -' in artist:
            artist = artist.split(' -')[0]
        return artist
    except Exception as e:
        return f"Error: {e}"

# Directory containing labeled audio files
base_dir = 'data/labeled/'

# Initialize lists to store file names, their corresponding labels, and artists
file_names = []
labels = []
artists = []

# Iterate over each mood directory
for label in os.listdir(base_dir):
    mood_dir = os.path.join(base_dir, label)
    if os.path.isdir(mood_dir):
        # Iterate over each audio file in the mood directory
        for file_name in os.listdir(mood_dir):
            if file_name.endswith('.mp3'):  # Adjust if using other formats
                file_path = os.path.join(mood_dir, file_name)
                file_names.append(file_name)
                labels.append(label)

                # Extract artist's name
                artist = extract_artist(file_path)
                artists.append(artist)

# Create DataFrame and save to CSV
import pandas as pd
df = pd.DataFrame({
    'filename': file_names,
    'mood': labels,
    'artist': artists
})
csv_file = os.path.join(base_dir, 'labels_with_artists.csv')
df.to_csv(csv_file, index=False)

print(f"CSV file created at: {csv_file}")
