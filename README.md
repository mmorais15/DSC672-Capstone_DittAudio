# DSC672-Capstone_DittAudio

Thanks for checking out our project. This was done to provide starter code for those looking to integrate a recommender system for spotify. The overall GUI is applicable to far more than just music recommendation. The idea is to compare two separate recommender systems against eachother. One that is programmed by yourself, and an existing model. This could be linked to any API, but originated as a spotify API project.

The gui.py file holds all the code to build the GUI. Please look at the dittAudio.py file as well, to see how our recommender system was implemented as a class so that the GUI could read it in and perform recommendations using the built in methods we designed. Some next step ideas are listed below, as well as in our report document.

There should be enough here to get you going using our platform. Any questions please comment on the repo or contact us directly.

Let's Keep dittAudio alive!

1.	A radar chart for step 2 instead of text based entry
2.	More customizable seed options
a.	Playlist based
b.	List of artists / tracks / playlists
c.	Genre – utilizing a drop down and existing data set for genres
3.	A like / dislike button on step 3, that will influence future recommendations
a.	Also link this to the like feature on Spotify
4.	Clean the GUI.py code – separate out GUI functions from the GUI builder code
5.	Continue considering common data formats for sharing information across recommendation algorithms – be forward thinking.
6.	Utilize json / xml packages in python to clean up field selection. Currently using it as a dictionary which gets messy and requires a lot of inefficient loops
7.	Extend beyond audio and spotify – Netflix, YouTube, Steam, Discord … allow more than one API connection, allow users to select what usage they want. Tie different account information to each recommendation algorithm. Think big!
