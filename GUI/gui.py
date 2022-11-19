# =============================================================================
# Custom Imports
# =============================================================================
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, scrolledtext, \
    ttk
import tkinter as tk

## dittAudio recommender
import dittAudio

## Spotify Libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# =============================================================================

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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
    print('Logging in...')
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="9232804c01d545f785fcd7272b13b149",
                                               client_secret="2cd2359e600f408c9ebc277c1de304eb",
                                               redirect_uri="http://localhost:1234/callback",
                                               scope=" ".join(scp)),
                     requests_timeout=10, retries=10)
    writeStatus("[Info] Spotify API Latched to User: "+sp.me()['uri'])
    print('success!')
    return sp

def most_popular_tracks_from_artist(artistNames,n=10):
    """Get n most popular track uris from a list of artist IDs"""
    output = []
    if n > 10 or n <= 0:
        n = 10
    for artist in artistNames:
        query = sp.artist_top_tracks(artist)
        idx = 0
        while idx < n:
            output.append(query['tracks'][idx]['uri'])
            idx+=1
    return output

def write_to_step_2(audio_features):
    """Writes af_summary dictionary to step 2"""
    af_summary = audio_features[0] #dictionary of features
    af_summary.pop('time_signature')
    af_summary.pop('duration_ms')
    af_summary.pop('analysis_url')
    af_summary.pop('track_href')
    af_summary.pop('uri')
    af_summary.pop('id')
    af_summary.pop('type')
    
    for idx in range(1,len(audio_features)):
        track = audio_features[idx]
        af_summary['danceability']     += track['danceability']
        af_summary['energy']           += track['energy']
        af_summary['key']              += track['key']
        af_summary['loudness']         += track['loudness']
        af_summary['mode']             += track['mode']
        af_summary['speechiness']      += track['speechiness']
        af_summary['instrumentalness'] += track['instrumentalness']
        af_summary['liveness']         += track['liveness']
        af_summary['valence']          += track['valence']
        af_summary['tempo']            += track['tempo']
    af_summary['danceability']      = round(af_summary['danceability']/len(audio_features),5)
    af_summary['energy']            = round(af_summary['energy']/len(audio_features),5)
    af_summary['key']               = round(af_summary['key']/len(audio_features),0)
    af_summary['loudness']          = round(af_summary['loudness']/len(audio_features),5)
    af_summary['mode']              = round(af_summary['mode']/len(audio_features),0)
    af_summary['speechiness']       = round(af_summary['speechiness']/len(audio_features),5)
    af_summary['instrumentalness']  = round(af_summary['instrumentalness']/len(audio_features),5)
    af_summary['liveness']          = round(af_summary['liveness']/len(audio_features),5)
    af_summary['valence']           = round(af_summary['valence']/len(audio_features),5)
    af_summary['tempo']             = round(af_summary['tempo']/len(audio_features),5)
    
    # populate into boxesstatus_window.delete(1.0,tk.END)
    try:
        # clear out any existing data
        entry_1.delete(0,tk.END)
        entry_2.delete(0,tk.END)
        entry_3.delete(0,tk.END)
        entry_7.delete(0,tk.END)
        entry_14.delete(0,tk.END)
        entry_15.delete(0,tk.END)
        entry_16.delete(0,tk.END)
        entry_17.delete(0,tk.END)
    except:
        print('[Warn] no data present')
        None
    entry_1.insert(tk.INSERT,str(af_summary['liveness']))
    entry_2.insert(tk.INSERT,str(af_summary['valence']))    
    entry_3.insert(tk.INSERT,str(af_summary['tempo']))
    entry_7.insert(tk.INSERT,str(af_summary['danceability']))
    entry_14.insert(tk.INSERT,str(af_summary['loudness']))
    entry_15.insert(tk.INSERT,str(af_summary['speechiness']))
    entry_16.insert(tk.INSERT,str(af_summary['acousticness']))
    entry_17.insert(tk.INSERT,str(af_summary['energy']))
    

def write_to_recommendations(rec_query_resp):
    """Writes a list of recommendations to step 3"""
    global rec_tracks
    rec_tracks = []
    resp = []
    
    # populate into boxesstatus_window.delete(1.0,tk.END)
    try:
        # clear out any existing data
        entry_13.delete(0,tk.END)
        entry_8.delete(0,tk.END)
        entry_9.delete(0,tk.END)
        entry_10.delete(0,tk.END)
        entry_11.delete(0,tk.END)
        entry_12.delete(0,tk.END)
    except:
        None
    # get track names and artist
    try:
        kyes = rec_query_resp['tracks']
        for track in rec_query_resp['tracks']:
            trackName = track['name']
            trackArtist = track['artists'][0]['name']
            data = trackName + ' - ' + trackArtist
            resp.append(data)
            rec_tracks.append(track['uri'])
    except:
        for uri in rec_query_resp.keys():
            txt = rec_query_resp[uri].split('-')
            trackName = txt[0]
            trackArtist = txt[1]
            data = trackName + ' - ' + trackArtist
            resp.append(data)
            rec_tracks.append(uri)
    entry_13.insert(tk.INSERT,str(resp[0]))
    entry_8.insert(tk.INSERT,str(resp[1]))    
    entry_9.insert(tk.INSERT,str(resp[2]))
    entry_10.insert(tk.INSERT,str(resp[3]))
    entry_11.insert(tk.INSERT,str(resp[4]))
    entry_12.insert(tk.INSERT,str(resp[5]))

def get_artist_uris(artist_query):
    """Takes a query response of artists and returns a list of artist uris"""
    artistURIs = []
    try:
        for artist in artist_query['artists']['items']:
            artistURIs.append(artist['uri'])
    except:
        print("Using Alt Structure for query response Artist")
        for artist in artist_query['items']:
            artistURIs.append(artist['uri'])
    return artistURIs

def use_my_followed_artists_function(retrn=False):
    """ Uses followed artists' top 10 songs, generates averages for audio features,
    and inputs them into step 2 for the user"""
    global seed_choice
    seed_choice = 'my_followed_artists'
    
    # Get followed artists, store URIs in a list
    followed_artists = sp.current_user_followed_artists()
    artistURIs = get_artist_uris(followed_artists)

    all_tracks = most_popular_tracks_from_artist(artistURIs)
    
    if retrn:
        return artistURIs
    
    # get all the audio features
    features = sp.audio_features(all_tracks)
    
    write_to_step_2(features)
    

def use_my_top_artists_function(retrn=False):
    """Gets audio features of top 10 artists, prints them into step 2"""
    global seed_choice
    seed_choice = 'my_top_artists'
    
    top_artists = sp.current_user_top_artists(limit=10, offset=0, time_range='medium_term')
    artistURIs = get_artist_uris(top_artists)
    
    all_tracks = most_popular_tracks_from_artist(artistURIs)
    
    if retrn:
        return artistURIs
    
    features = sp.audio_features(all_tracks)
    
    write_to_step_2(features)
    
def use_my_top_tracks_function(retrn=False):
    """Gets audio features of top 50 tracks, prints them into step 2"""
    global seed_choice
    seed_choice = 'my_top_tracks'
    
    all_tracks = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
    # get track URIs
    uris = []
    for track in all_tracks['items']:
        uris.append(track['uri'])
    
    if retrn:
        return uris
    
    features = sp.audio_features(uris)
    write_to_step_2(features)
    
    
def load_next_six():
    """Loads the next six recommendations based on which method was chosen"""
    global rec_method
    global sp_rec_offset
    
    if rec_method == '':
        writeStatus("Need to select reccomendation method in step 2!!")
        return
    
    sp_rec_offset += 6
    
    if rec_method == 'spotify':
        spotify_recommend(sp_rec_offset)
    elif rec_method == 'dittaudio':
        dittaudio_recommend(sp_rec_offset)
    
def hipster_toggle():
    """Toggles a max popularity setting for spotify recs"""
    global hipster
    if hipster:
        hipster = False
        writeStatus("Hipster Mode Disabled!")  
    else:
        hipster = True
        writeStatus("Hipster Mode Enabled!")    
    
def spotify_recommend(offset=0):
    """Uses spotify recommendation algo to recommend songs"""
    global sp_rec_offset
    global seed_choice
    global rec_method
    global hipster
    
    rec_method = 'spotify'
    
    if offset==0:
        sp_rec_offset=0
    
    if hipster:
        mp = 10
    else:
        mp = 100
    
    if seed_choice == '':
        writeStatus("Need to select seed method!")
        return
    elif seed_choice == 'my_followed_artists':
        recs = sp.recommendations(limit=6,seed_artists=use_my_followed_artists_function(True)[0:4],offset=offset+sp_rec_offset,max_popularity=mp)
    elif seed_choice == 'my_top_tracks':
        recs = sp.recommendations(limit=6,seed_tracks=use_my_top_tracks_function(True)[0:4],offset=offset+sp_rec_offset,max_popularity=mp)
    elif seed_choice == 'my_top_artists':
        recs = sp.recommendations(limit=6,seed_artists=use_my_top_artists_function(True)[0:4],offset=offset+sp_rec_offset,max_popularity=mp)
    write_to_recommendations(recs)

def dittaudio_recommend(offset=0):
    """Uses dittAudio recommendation algo to recommend songs"""
    global sp_rec_offset
    global seed_choice
    global rec_method
    
    rec_method = 'dittaudio'
    
    if offset==0:
        sp_rec_offset=0
    
    input_data = {}
    input_data = get_existing_factors()
    if input_data == {}:
        writeStatus("[Error] Must fill in step 2!!!")
        return
    recs = dittAudio.recommend_songs(input_data,offset+6)
    
    write_to_recommendations(recs)


def play_song(rec_num):
    """ Plays the recommended song on users device """
    global chosen_device
    global rec_tracks
    
    if chosen_device == '':
        devices = sp.devices()['devices']
        for device in devices:
            if device['type'] == 'Computer':
                chosen_device = device['id']
        if chosen_device == '':
            writeStatus("[Error] No devices found that can play selection")
    try:
        sp.start_playback(chosen_device,uris=[rec_tracks[rec_num]])
    except:
        error_msg = "[Error] Could not play track on device: " + str(chosen_device)
        writeStatus(error_msg)
        
def get_existing_factors():
    """Gets all the parameters from step 2 and stores them into a dictionary"""
    af_summary = {}
    
    af_summary['danceability']      = float(entry_7.get())
    af_summary['energy']            = float(entry_17.get())
    af_summary['loudness']          = float(entry_14.get())
    af_summary['speechiness']       = float(entry_15.get())
    af_summary['acousticness']      = float(entry_16.get())
    # af_summary['instrumentalness']  = entry_1.get()
    af_summary['liveness']          = float(entry_1.get())
    af_summary['valence']           = float(entry_2.get())
    af_summary['tempo']             = float(entry_3.get())
    
    return af_summary

def add_to_playlist(rec_num):
    """Gets the Text in the playlist entry, adds song to playlist. If playlist does not exist, it will make it"""
    global rec_tracks
    global user_playlists
    global rec_method
    
    if rec_method == '':
        writeStatus("Must get recommended songs first!")
        return
    
    if user_playlists == []:
        user_playlists = sp.user_playlists(sp.me()['id'],limit=50)['items']
    
    chosen_playlist = entry_4.get()
    
    if chosen_playlist == "":
        writeStatus("[Error] Enter a playlist name!")
        return
    
    selected_plist = ''
    for plist in user_playlists:
        if plist['name'] == chosen_playlist:
            selected_plist = plist['id']
    
    if selected_plist == '':
        # playlist didnt exist, lets make it
        new_playlist = sp.user_playlist_create(sp.me()['id'], chosen_playlist,public=False,collaborative=False)
        selected_plist = new_playlist['id']
        user_playlists.append(new_playlist)
    
    # add the songs
    sp.user_playlist_add_tracks(sp.me()['id'], selected_plist, [rec_tracks[rec_num]]) 
       
# =============================================================================
seed_choice = ''
sp_rec_offset = 0
rec_tracks = []
chosen_device = ''
user_playlists = []
rec_method = ''
hipster = False

window = Tk()

window.geometry("1220x675")
window.configure(bg = "#6C007E")
window.title("dittAudio")


canvas = Canvas(
    window,
    bg = "#6C007E",
    height = 675,
    width = 1220,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

# =============================================================================
# Custom Windows
# =============================================================================
## Status Window
status_window = scrolledtext.ScrolledText(window,
                                          width = 450,
                                          height=78,
                                          font = ("Inter",14))
status_window.grid(column=0,pady=10,padx=10)
status_window.insert(tk.INSERT,"Welcome to DittAudio")
status_window.place(
    x=419.0,
    y=560.0,
    width=800.0,
    height=120.0
)
# =============================================================================

canvas.place(x = 0, y = 0)
canvas.create_text(
    89.0,
    2.0,
    anchor="nw",
    text="dittAudio",
    fill="#FFFFFF",
    font=("Inter", 64 * -1)
)

canvas.create_rectangle(
    0.0,
    103.0,
    407.0,
    675.0,
    fill="#F9D5FF",
    outline="")

canvas.create_rectangle(
    419.0,
    103.0,
    800.0,
    675.0,
    fill="#F9D5FF",
    outline="")

factor_entry = PhotoImage(
    file=relative_to_assets("factor_entry.png"))
entry_bg_1 = canvas.create_image(
    652.5,
    314.5,
    image=factor_entry
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=610.0,
    y=303.0,
    width=85.0,
    height=21.0
)

entry_bg_2 = canvas.create_image(
    652.5,
    338.5,
    image=factor_entry
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_2.place(
    x=610.0,
    y=327.0,
    width=85.0,
    height=21.0
)

entry_bg_3 = canvas.create_image(
    652.5,
    362.5,
    image=factor_entry
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_3.place(
    x=610.0,
    y=351.0,
    width=85.0,
    height=21.0
)

canvas.create_rectangle(
    813.0,
    103.0,
    1220.0,
    675.0,
    fill="#F9D5FF",
    outline="")


canvas.create_text(
    828.0,
    405.0,
    anchor="nw",
    text="Name:",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    1033.0,
    417.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_4.place(
    x=889.0,
    y=406.0,
    width=288.0,
    height=21.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("next_6_recs.png"))
next_6_recommendations_button = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: load_next_six(),
    relief="flat"
)
next_6_recommendations_button.place(
    x=839.0,
    y=320.0,
    width=328.0,
    height=26.0
)

canvas.create_text(
    847.0,
    378.0,
    anchor="nw",
    text="Click the + to add to a new playlist",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

play_button = PhotoImage(
    file=relative_to_assets("play_button.png"))
add_button = PhotoImage(
    file=relative_to_assets("add_button.png"))

button_5 = Button(
    image=play_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: play_song(5),
    relief="flat"
)
button_5.place(
    x=1156.0,
    y=287.0,
    width=21.0,
    height=24.0
)

button_5a = Button(
    image=add_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_to_playlist(5),
    relief="flat"
)
button_5a.place(
    x=1180.0,
    y=287.0,
    width=21.0,
    height=24.0
)

button_6 = Button(
    image=play_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: play_song(4),
    relief="flat"
)
button_6.place(
    x=1156.0,
    y=262.0,
    width=21.0,
    height=24.0
)

button_6a = Button(
    image=add_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_to_playlist(4),
    relief="flat"
)
button_6a.place(
    x=1180.0,
    y=262.0,
    width=21.0,
    height=24.0
)

button_7 = Button(
    image=play_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: play_song(3),
    relief="flat"
)
button_7.place(
    x=1156.0,
    y=237.0,
    width=21.0,
    height=24.0
)

button_7a = Button(
    image=add_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_to_playlist(3),
    relief="flat"
)
button_7a.place(
    x=1180.0,
    y=237.0,
    width=21.0,
    height=24.0
)

button_8 = Button(
    image=play_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: play_song(2),
    relief="flat"
)
button_8.place(
    x=1156.0,
    y=212.0,
    width=21.0,
    height=24.0
)

button_8a = Button(
    image=add_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_to_playlist(2),
    relief="flat"
)
button_8a.place(
    x=1180.0,
    y=212.0,
    width=21.0,
    height=24.0
)

canvas.create_rectangle(
    0.0,
    81.0,
    407.0,
    130.0,
    fill="#FDFDFD",
    outline="")

canvas.create_rectangle(
    419.0,
    81.0,
    800.0,
    130.0,
    fill="#FDFDFD",
    outline="")

canvas.create_rectangle(
    813.0,
    80.0,
    1220.0,
    129.0,
    fill="#FDFDFD",
    outline="")

canvas.create_text(
    445.0,
    94.0,
    anchor="nw",
    text="Step 2: Provide Modifications",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    825.0,
    91.0,
    anchor="nw",
    text="Step 3: Look Through Recommendations",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    44.0,
    40.0,
    image=image_image_1
)

canvas.create_text(
    422.0,
    531.0,
    anchor="nw",
    text="Status Box",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    846.0,
    163.0,
    anchor="nw",
    text="1.",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    846.0,
    189.0,
    anchor="nw",
    text="2.",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    846.0,
    214.0,
    anchor="nw",
    text="3.",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    846.0,
    238.0,
    anchor="nw",
    text="4.",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    846.0,
    263.0,
    anchor="nw",
    text="5.",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    846.0,
    288.0,
    anchor="nw",
    text="6.",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    33.0,
    135.0,
    anchor="nw",
    text="Pick one of three options below",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    445.0,
    140.0,
    anchor="nw",
    text="Optional. Modify Factors as Desired",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    486.0,
    183.0,
    anchor="nw",
    text="Danceability",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    537.0,
    207.0,
    anchor="nw",
    text="Energy",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    511.0,
    231.0,
    anchor="nw",
    text="Loudness",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    482.0,
    255.0,
    anchor="nw",
    text="Speechiness",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    476.0,
    279.0,
    anchor="nw",
    text="Acousticness",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    520.0,
    303.0,
    anchor="nw",
    text="Liveness",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    528.0,
    327.0,
    anchor="nw",
    text="Valence",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    538.0,
    351.0,
    anchor="nw",
    text="Tempo",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    22.0,
    94.0,
    anchor="nw",
    text="Step 1: Provide Seeds",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
use_my_followed_artists_button = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: use_my_followed_artists_function(),
    relief="flat"
)
use_my_followed_artists_button.place(
    x=53.0,
    y=190.0,
    width=301.0,
    height=59.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
use_my_top_tracks_button = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: use_my_top_tracks_function(),
    relief="flat"
)
use_my_top_tracks_button.place(
    x=53.0,
    y=290.0,
    width=301.0,
    height=59.0
)

button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
use_my_top_artists_button = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: use_my_top_artists_function(),
    relief="flat"
)
use_my_top_artists_button.place(
    x=53.0,
    y=390.0,
    width=301.0,
    height=59.0
)

button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: spotify_recommend(),
    relief="flat"
)
button_13.place(
    x=616.0,
    y=393.0,
    width=167.0,
    height=59.0
)

button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: dittaudio_recommend(0),
    relief="flat"
)
button_14.place(
    x=436.0,
    y=393.0,
    width=167.0,
    height=59.0
)

button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: hipster_toggle(),
    relief="flat"
)
button_15.place(
    x=512.0,
    y=471.0,
    width=195.0,
    height=59.0
)

entry_bg_7 = canvas.create_image(
    652.5,
    194.5,
    image=factor_entry
)
entry_7 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_7.place(
    x=610.0,
    y=183.0,
    width=85.0,
    height=21.0
)

recommendation_entry = PhotoImage(
    file=relative_to_assets("recommendation_entry.png"))
entry_bg_8 = canvas.create_image(
    1008.0,
    199.5,
    image=recommendation_entry
)
entry_8 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_8.place(
    x=864.0,
    y=188.0,
    width=288.0,
    height=21.0
)

entry_bg_9 = canvas.create_image(
    1008.0,
    224.5,
    image=recommendation_entry
)
entry_9 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_9.place(
    x=864.0,
    y=213.0,
    width=288.0,
    height=21.0
)

entry_bg_10 = canvas.create_image(
    1008.0,
    249.5,
    image=recommendation_entry
)
entry_10 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_10.place(
    x=864.0,
    y=238.0,
    width=288.0,
    height=21.0
)

entry_bg_11 = canvas.create_image(
    1008.0,
    274.5,
    image=recommendation_entry
)
entry_11 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_11.place(
    x=864.0,
    y=263.0,
    width=288.0,
    height=21.0
)

entry_bg_12 = canvas.create_image(
    1008.0,
    299.5,
    image=recommendation_entry
)
entry_12 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_12.place(
    x=864.0,
    y=288.0,
    width=288.0,
    height=21.0
)

entry_bg_13 = canvas.create_image(
    1008.0,
    174.5,
    image=recommendation_entry
)
entry_13 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_13.place(
    x=864.0,
    y=163.0,
    width=288.0,
    height=21.0
)

entry_bg_14 = canvas.create_image(
    652.5,
    242.5,
    image=factor_entry
)
entry_14 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_14.place(
    x=610.0,
    y=231.0,
    width=85.0,
    height=21.0
)

entry_bg_15 = canvas.create_image(
    652.5,
    266.5,
    image=factor_entry
)
entry_15 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_15.place(
    x=610.0,
    y=255.0,
    width=85.0,
    height=21.0
)

entry_bg_16 = canvas.create_image(
    652.5,
    290.5,
    image=factor_entry
)
entry_16 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_16.place(
    x=610.0,
    y=279.0,
    width=85.0,
    height=21.0
)

entry_bg_17 = canvas.create_image(
    652.5,
    218.5,
    image=factor_entry
)
entry_17 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_17.place(
    x=610.0,
    y=207.0,
    width=85.0,
    height=21.0
)

button_16 = Button(
    image=play_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: play_song(0),
    relief="flat"
)
button_16.place(
    x=1156.0,
    y=161.0,
    width=21.0,
    height=24.0
)
button_16a = Button(
    image=add_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_to_playlist(0),
    relief="flat"
)
button_16a.place(
    x=1180.0,
    y=161.0,
    width=21.0,
    height=24.0
)

button_17 = Button(
    image=play_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: play_song(1),
    relief="flat"
)
button_17.place(
    x=1156.0,
    y=187.0,
    width=21.0,
    height=24.0
)
button_17a = Button(
    image=add_button,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_to_playlist(1),
    relief="flat"
)
button_17a.place(
    x=1180.0,
    y=187.0,
    width=21.0,
    height=24.0
)

# connect to spotify after gui is built
sp = sp_connect()
dittAudio = dittAudio.dittAudio(sp)
window.resizable(False, False)

# start the main loop
window.mainloop()
