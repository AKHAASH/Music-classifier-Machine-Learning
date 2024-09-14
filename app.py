from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import urllib.parse
import subprocess


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Run the metadata extraction script
def run_metadata_script():
    script_path = 'I:/Music-classifier/src/playlist_metadata.py'  # Adjust this path
    subprocess.run(['venv/Scripts/python', script_path], check=True)

# Load artist names from the CSV, ensuring unique and individual artist names
def get_artists():
    df = pd.read_csv('./static/labels_with_playlist_artists.csv')
    unique_artists = sorted(set(artist.strip() for artists in df['artist'] for artist in artists.split(',')))
    return unique_artists

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    artists = get_artists()  # Get the list of unique artists
    return render_template('index.html', files=files, artists=artists)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Run the script after saving the file
        run_metadata_script()
        refresh_song_data()

        return redirect(url_for('index'))

@app.route('/remove/<filename>', methods=['POST'])
def remove_file(filename):
    decoded_filename = urllib.parse.unquote(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], decoded_filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        
        # Run the script after removing the file
        run_metadata_script()
        refresh_song_data()

    return redirect(url_for('index'))

song_data = pd.read_csv('I:/Music-classifier/static/labels_with_playlist_artists.csv')

def refresh_song_data():
    global song_data
    song_data = pd.read_csv('I:/Music-classifier/static/labels_with_playlist_artists.csv')

@app.route('/apply_filters', methods=['POST'])
def apply_filters():
    # Get selected moods and singers from the form
    selected_moods = request.form.getlist('emotion')
    selected_singers = request.form.getlist('singer')
    
    # Filter the DataFrame based on the selected options
    filtered_data = song_data.copy()
    
    # Apply both filters if selections are made
    if selected_moods and selected_singers:
        filtered_data = filtered_data[
            (filtered_data['mood'].isin(selected_moods)) &
            (filtered_data['artist'].apply(lambda artists: any(singer in artists for singer in selected_singers)))
        ]
    elif selected_moods:  # If only moods are selected
        filtered_data = filtered_data[filtered_data['mood'].isin(selected_moods)]
    elif selected_singers:  # If only singers are selected
        filtered_data = filtered_data[filtered_data['artist'].apply(lambda artists: any(singer in artists for singer in selected_singers))]


    
    # Extract only the filenames of the filtered songs
    filtered_files = filtered_data['filename'].tolist()
    
    # Reuse the index view but with filtered files
    artists = get_artists()  # Get the list of unique artists again for the filters
    return render_template('index.html', files=filtered_files, artists=artists)

if __name__ == '__main__':
    app.run(debug=True)
