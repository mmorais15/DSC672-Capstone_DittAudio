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
    print('trying...')
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="9232804c01d545f785fcd7272b13b149",
                                               client_secret="2cd2359e600f408c9ebc277c1de304eb",
                                               redirect_uri="http://localhost:1234/callback",
                                               scope=" ".join(scp)),
                     requests_timeout=10, retries=10)
    writeStatus("[Info] Spotify API Latched to User: "+sp.me()['uri'])
    print('done!')
# =============================================================================


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
status_window.insert(tk.INSERT,"FirstText!")
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

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    652.5,
    314.5,
    image=entry_image_1
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

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    652.5,
    338.5,
    image=entry_image_2
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

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    652.5,
    362.5,
    image=entry_image_3
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
    477.0,
    anchor="nw",
    text="Device:",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    847.0,
    450.0,
    anchor="nw",
    text="Play this Playlist",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

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

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    1042.0,
    489.5,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_5.place(
    x=898.0,
    y=478.0,
    width=288.0,
    height=21.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=846.0,
    y=132.0,
    width=328.0,
    height=26.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=839.0,
    y=320.0,
    width=328.0,
    height=26.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=844.0,
    y=510.0,
    width=328.0,
    height=26.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=1006.0,
    y=448.0,
    width=203.0,
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

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=1156.0,
    y=287.0,
    width=21.0,
    height=24.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=1156.0,
    y=262.0,
    width=21.0,
    height=24.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=1156.0,
    y=237.0,
    width=21.0,
    height=24.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=1156.0,
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
    419.0,
    46.0,
    anchor="nw",
    text="Any *Get* buttons will return an output to the Status Box",
    fill="#F9D5FF",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    9.0,
    353.0,
    anchor="nw",
    text="Lists artist names below, separate by +",
    fill="#6C007E",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    9.0,
    503.0,
    anchor="nw",
    text="List seed playlist below",
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
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat"
)
button_9.place(
    x=53.0,
    y=192.0,
    width=301.0,
    height=59.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat"
)
button_10.place(
    x=53.0,
    y=289.0,
    width=301.0,
    height=59.0
)

button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_11 clicked"),
    relief="flat"
)
button_11.place(
    x=46.0,
    y=434.0,
    width=301.0,
    height=59.0
)

button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_12 clicked"),
    relief="flat"
)
button_12.place(
    x=59.0,
    y=590.0,
    width=282.0,
    height=59.0
)

button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_13 clicked"),
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
    command=lambda: print("button_14 clicked"),
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
    command=lambda: print("button_15 clicked"),
    relief="flat"
)
button_15.place(
    x=512.0,
    y=471.0,
    width=195.0,
    height=59.0
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    199.5,
    401.5,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_6.place(
    x=20.0,
    y=384.0,
    width=359.0,
    height=33.0
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    652.5,
    194.5,
    image=entry_image_7
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

entry_image_8 = PhotoImage(
    file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(
    1008.0,
    199.5,
    image=entry_image_8
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

entry_image_9 = PhotoImage(
    file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(
    1008.0,
    224.5,
    image=entry_image_9
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

entry_image_10 = PhotoImage(
    file=relative_to_assets("entry_10.png"))
entry_bg_10 = canvas.create_image(
    1008.0,
    249.5,
    image=entry_image_10
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

entry_image_11 = PhotoImage(
    file=relative_to_assets("entry_11.png"))
entry_bg_11 = canvas.create_image(
    1008.0,
    274.5,
    image=entry_image_11
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

entry_image_12 = PhotoImage(
    file=relative_to_assets("entry_12.png"))
entry_bg_12 = canvas.create_image(
    1008.0,
    299.5,
    image=entry_image_12
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

entry_image_13 = PhotoImage(
    file=relative_to_assets("entry_13.png"))
entry_bg_13 = canvas.create_image(
    1008.0,
    174.5,
    image=entry_image_13
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

entry_image_14 = PhotoImage(
    file=relative_to_assets("entry_14.png"))
entry_bg_14 = canvas.create_image(
    652.5,
    242.5,
    image=entry_image_14
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

entry_image_15 = PhotoImage(
    file=relative_to_assets("entry_15.png"))
entry_bg_15 = canvas.create_image(
    652.5,
    266.5,
    image=entry_image_15
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

entry_image_16 = PhotoImage(
    file=relative_to_assets("entry_16.png"))
entry_bg_16 = canvas.create_image(
    652.5,
    290.5,
    image=entry_image_16
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

entry_image_17 = PhotoImage(
    file=relative_to_assets("entry_17.png"))
entry_bg_17 = canvas.create_image(
    652.5,
    218.5,
    image=entry_image_17
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

entry_image_18 = PhotoImage(
    file=relative_to_assets("entry_18.png"))
entry_bg_18 = canvas.create_image(
    196.5,
    553.5,
    image=entry_image_18
)
entry_18 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_18.place(
    x=17.0,
    y=536.0,
    width=359.0,
    height=33.0
)

button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_16 clicked"),
    relief="flat"
)
button_16.place(
    x=1156.0,
    y=161.0,
    width=21.0,
    height=24.0
)

button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_17 clicked"),
    relief="flat"
)
button_17.place(
    x=1156.0,
    y=187.0,
    width=21.0,
    height=24.0
)
window.resizable(False, False)
window.mainloop()
