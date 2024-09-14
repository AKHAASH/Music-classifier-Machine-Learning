import librosa
import numpy as np
import joblib

# Load the trained model
model = joblib.load('I:/Music-classifier/data/music_mood_model.pkl')

# Function to extract features from a new audio file
def extract_features(file_path):
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
        
        # Combine all features into a single feature vector
        feature_vector = np.concatenate([
            mfccs,
            chroma,
            spectral_contrast,
            zero_crossing_rate,
            rms,
            spectral_rolloff
        ])
        
        return feature_vector
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None

# Function to predict the mood of a new song
def predict_mood(file_path):
    # Extract features from the new song
    features = extract_features(file_path)
    
    if features is not None:
        # Reshape the features to match the model's expected input format
        features = features.reshape(1, -1)
        
        # Predict the mood using the model
        prediction = model.predict(features)
        
        # Print the predicted mood
        return prediction[0]
    else:
        return "Could not predict mood due to feature extraction error."

# Provide the path to your new song here
new_song_path = 'I:/Music-classifier/static/uploads/Aaluma-Doluma.mp3'
mood=predict_mood(new_song_path)
print(mood)