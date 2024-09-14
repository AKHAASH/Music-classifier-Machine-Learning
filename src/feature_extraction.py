import os
import librosa
import pandas as pd
import numpy as np

# Directory containing labeled audio files
base_dir = './data/labeled/'  # Adjust this path based on your actual directory structure

# Initialize lists to store features and labels
features = []
labels = []

# Iterate over each mood directory
for label in os.listdir(base_dir):
    mood_dir = os.path.join(base_dir, label)
    if os.path.isdir(mood_dir):
        # Iterate over each audio file in the mood directory
        for file_name in os.listdir(mood_dir):
            if file_name.endswith('.wav') or file_name.endswith('.mp3'):
                file_path = os.path.join(mood_dir, file_name)
                try:
                    # Load the audio file
                    y, sr = librosa.load(file_path, sr=None)
                    
                    # Extract features
                    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).T, axis=0)
                    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0)
                    spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0)
                    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=y).T, axis=0)
                    rms = np.mean(librosa.feature.rms(y=y).T, axis=0)
                    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr).T, axis=0)
                    
                    # Combine all features
                    feature_vector = np.concatenate([
                        mfccs,
                        chroma,
                        spectral_contrast,
                        zero_crossing_rate,
                        rms,
                        spectral_rolloff
                    ])
                    
                    # Append features and label
                    features.append(feature_vector)
                    labels.append(label)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Create a DataFrame from the features and labels
columns = [
    'mfcc_' + str(i) for i in range(13)
] + [
    'chroma_' + str(i) for i in range(12)
] + [
    'spectral_contrast_' + str(i) for i in range(7)
] + [
    'zero_crossing_rate'
] + [
    'rms'
] + [
    'spectral_rolloff'
]

df = pd.DataFrame(features, columns=columns)
df['mood'] = labels

# Save the DataFrame to a CSV file
features_csv_file = './data/features.csv'
df.to_csv(features_csv_file, index=False)

print(f"Features CSV file created at: {features_csv_file}")
