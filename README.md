# whiplash.fm
mood-based music app built for GenZ brains on shuffle (for the generation that feels everything, everywhere, all at once)


**What It Does:**
  - Detects your mood using smart keyword matching and sentiment analysis
  
  - Searches Spotify for mood-matching playlists using the Spotify Web API
  
  - Gives you playlists to match your vibe
  
  - It is GenZ coded! Understands 'meh', 'vibing', 'idk', and everything in between

**How To Use:**
 (Spotify Setup)
To use whiplash.fm: the mood-based music mixer for Gen Z brains, you’ll need your own Spotify Developer credentials.

Spotify requires each user to authenticate their account to access music data. Here’s how to set it up:

**Step 1**: 
    Create a Spotify Developer App
    Go to Spotify Developer Dashboard
    
    Log in with your Spotify account
    
    Click "Create an App"
    
    Name your app (e.g., whiplash.fm)

    Under Redirect URIs, add:

      http://localhost:8501/callback
      
    Or if you're deploying it (e.g., Streamlit Cloud), add:

      https://your-app-name.streamlit.app/callback

      
**Step 2**: Set Your Credentials
    Create a file named .env in the root folder of the project and paste:

      SPOTIFY_CLIENT_ID=your_client_id_here
      SPOTIFY_CLIENT_SECRET=your_client_secret_here
⚠️ Do not share your .env file publicly. This keeps your keys safe.

**Step 3**: Run the App
    Run the app using:

      streamlit run copyshare.py

On first launch, Spotify will ask you to log in and authorize access to your account.

**Note**
This app does not collect or store any user data

It simply uses your Spotify session to fetch mood-based playlists





  
