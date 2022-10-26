# =============================================================================
# Custom Imports
# =============================================================================
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, scrolledtext, \
    ttk
import tkinter as tk

## Spotify Libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# =============================================================================


# =============================================================================
# Custom Functions
# =============================================================================
def writeStatus(string):
    """Writes a string to the status screen"""
    print(string)
    status_window.insert(tk.INSERT,"\n" + string)

def clearStatus():
    """Clears out the status box"""
    status_window.delete(1.0,tk.END)

def sp_connect():
    """Creates connection to spotify api"""
    scp = ["user-top-read",
      "user-library-read",
      "user-read-currently-playing",
      "user-read-private",
      "user-follow-read",
      "user-read-playback-state",
      "user-modify-playback-state",
      "playlist-modify-public",
      "playlist-modify-private",
      "playlist-read-collaborative",
      "playlist-read-private",
      "user-read-recently-played",
      "streaming",
      "user-follow-modify"]
    print('trying...')
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="9232804c01d545f785fcd7272b13b149",
                                               client_secret="2cd2359e600f408c9ebc277c1de304eb",
                                               redirect_uri="http://localhost:1234/callback",
                                               scope=" ".join(scp)),
                     requests_timeout=10, retries=10)
    writeStatus("[Info] Spotify API Latched to User: "+sp.me()['uri'])
    print('done!')
# =============================================================================


# =============================================================================
# Custom Windows
# =============================================================================
## Status Window
status_window = scrolledtext.ScrolledText(window,
                                          width = 450,
                                          height=78,
                                          font = ("Inter",14))
status_window.grid(column=0,pady=10,padx=10)
status_window.insert(tk.INSERT,"FirstText!")
status_window.place(
    x=419.0,
    y=531.0,
    width=700.0,
    height=120.0
)
# =============================================================================
