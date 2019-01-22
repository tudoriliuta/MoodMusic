# MoodMusic
background music for videos based on the emotions of the people in it

## Resources:
[Documentation for Azure Face API](https://docs.microsoft.com/en-us/azure/cognitive-services/Face/QuickStarts/Python)
```python
import spotipy (pip3 install spotipy)
scc = SpotifyClientCredentials(client_id = 'ID', client_secret = 'KEY')
scc
<spotipy.oauth2.SpotifyClientCredentials object at 0x101a85e48>
sp = spotipy.Spotify(client_credentials_manager = scc)
results = sp.artist_top_tracks('spotify:artist:36QJpDe2go2KgaRleHCDTp')
```

updating line chart for displaying the emotions over time
https://github.com/tdiethe/flask-live-charts.git

https://open.spotify.com/track/3FtYbEfBqAlGO46NUDQSAt
