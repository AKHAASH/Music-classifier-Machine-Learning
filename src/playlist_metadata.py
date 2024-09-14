import os
from mutagen.id3 import ID3
import pandas as pd
from predict_mood import predict_mood

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

# Directory containing the audio files
base_dir = 'I:/Music-classifier/static/uploads/'

# Initialize lists to store file names and their corresponding artists
file_names = []
moods=[]
artists = []

# Iterate over each audio file in the base directory
for file_name in os.listdir(base_dir):
    if file_name.endswith('.mp3'):  # Adjust if using other formats
        file_path = os.path.join(base_dir, file_name)
        file_names.append(file_name)

        # Extract artist's name
        artist = extract_artist(file_path)
        artists.append(artist)

        # Extract mood
        mood = predict_mood(file_path)
        moods.append(mood)

# Create DataFrame and save to CSV (without the mood column)
df = pd.DataFrame({
    'filename': file_names,
    'mood':moods,
    'artist': artists
})
csv_file = os.path.join('I:/Music-classifier/static/', 'labels_with_playlist_artists.csv')
df.to_csv(csv_file, index=False)

print(f"CSV file created at: {csv_file}")
