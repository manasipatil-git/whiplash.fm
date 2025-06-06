from dotenv import load_dotenv
import os
load_dotenv()

import re
from collections import Counter
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

# --- Mood detection logic ---
emotion_keywords = {
    "Happy": ["happy", "vibing", "lit", "great", "amazing", "yay", "slaying", "good"],
    "Sad": ["sad", "down", "depressed", "crying", "blue", "meh", "idk", "lost"],
    "Angry": ["angry", "mad", "annoyed", "irritated", "furious", "pissed", "raging"],
    "Excited": ["excited", "hyped", "pumped", "buzzing", "over the moon", "omg"],
    "Love": ["love", "crushing", "smitten", "obsessed", "infatuated"],
    "Frustrated": ["frustrated", "done", "over it", "fed up", "tired"],
    "Fear": ["scared", "nervous", "anxious", "worried", "panicking", "stressed"]
}
keyword_to_emotion = {word: mood for mood, words in emotion_keywords.items() for word in words}
negations = {"not", "no", "never", "n't", "none"}

def contains_negation(words, index, window=3):
    return any(words[i] in negations for i in range(max(0, index - window), index))

def detect_mood(text):
    lowered = text.casefold()
    cleaned = re.sub(r"[^\w\s]", "", lowered)
    words = cleaned.split()
    upper_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)

    detected = []

    for phrase in keyword_to_emotion:
        if " " in phrase and phrase in cleaned:
            detected.append(keyword_to_emotion[phrase])

    for i, word in enumerate(words):
        if word in keyword_to_emotion:
            if contains_negation(words, i):
                continue
            mood = keyword_to_emotion[word]
            if upper_ratio > 0.5 and mood in {"Angry", "Excited"}:
                mood += " (INTENSE)"
            detected.append(mood)

    if not detected:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.4:
            detected.append("Happy")
        elif polarity < -0.2:
            detected.append("Sad")
        else:
            detected.append("Neutral")

    mood_counts = Counter(detected)
    sorted_moods = [f"{mood} ({count})" if count > 1 else mood for mood, count in mood_counts.most_common()]

    return sorted_moods

# --- Spotify setup ---
import os
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = 'http://127.0.0.1:8501/callback'

scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-read"

@st.cache_resource
def get_spotify_client():
from spotipy.oauth2 import SpotifyClientCredentials

@st.cache_resource
def get_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    return spotipy.Spotify(auth_manager=client_credentials_manager)


@st.cache_data
def search_playlists(_sp, mood):
    results = _sp.search(q=mood, type='playlist', limit=10)
    return results

# --- Light/Dark mode toggle ---
mode = st.radio("Choose Theme", ["Light", "Dark"], horizontal=True)
if mode == "Dark":
    st.markdown("""
        <style>
        body, .main, .block-container {
            background-color: #121212 !important;
            color: #e0e0e0 !important;
        }
        .css-1cpxqw2, .css-1d391kg, .css-ffhzg2 {
            background-color: #121212 !important;
            color: #e0e0e0 !important;
        }
        a {
            color: #bb86fc !important;
            text-decoration: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .main, .block-container {
            background-color: white !important;
            color: black !important;
        }
        .css-1cpxqw2, .css-1d391kg, .css-ffhzg2 {
            background-color: white !important;
            color: black !important;
        }
        a {
            color: #1a0dab !important;
            text-decoration: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- UI ---
st.markdown("<h1 style='font-family:Whiplash, sans-serif;'>whiplash.fm</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size:32px;'>Hey you! How are you feeling?</h3>", unsafe_allow_html=True)

user_input = st.text_input("")

if user_input:
    detected_moods = detect_mood(user_input)
    top_mood = detected_moods[0] if detected_moods else "Neutral"

    # 💥 Mood bubble
    st.markdown(f"""
        <div style='
            margin-top: 20px;
            background: linear-gradient(135deg, #ff8a00, #e52e71);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 24px;
            font-weight: 600;
            color: white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        '>
            You're feeling: {top_mood}
        </div>
    """, unsafe_allow_html=True)

    # 🎵 Playlist section
    sp = get_spotify_client()
    playlists = search_playlists(sp, top_mood)
    playlist_items = playlists.get('playlists', {}).get('items', []) or []

    st.markdown(f"<h4 style='margin-top: 30px;'>Here are some playlists based on your mood: <span style='color:#e52e71'>{top_mood}</span></h4>", unsafe_allow_html=True)

    for playlist in playlist_items:
        if not isinstance(playlist, dict):
            continue
        name = playlist.get('name')
        external_urls = playlist.get('external_urls')
        if not (name and isinstance(external_urls, dict)):
            continue
        url = external_urls.get('spotify')
        if not url:
            continue
        st.markdown(f"""
            <div style='margin-left:40px; margin-bottom:10px; font-weight:500; font-size:18px;'>
                <a href="{url}" target="_blank">{name}</a>
            </div>
        """, unsafe_allow_html=True)
