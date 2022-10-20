import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="9232804c01d545f785fcd7272b13b149",
                                               client_secret="",
                                               redirect_uri="http://localhost:1234/callback",
                                               scope="user-top-read user-library-read user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private playlist-read-collaborative playlist-read-private"))

def query2tdf(results,writeHeader=False):
    '''Converts a query into a tab delimited file(tdf)'''
    with open('outfile.txt','a',encoding='utf-8') as oof:
        if writeHeader:
            oof.write('track\t')
            oof.write('trackID\t')
            oof.write('album\t')
            oof.write('artist\t')
            oof.write('genres\t')
            features = ['danceability','energy','key','loudness','mode', \
                        'speechiness','acousticness','instrumentals', \
                        'liveness','valence','tempo','type','id','uri','trackhref', \
                        'analysisuri','duration_ms','time_signature']
            for feature in features:
                oof.write(feature + '\t')
            oof.write('\n')
            
        items = results['tracks']['items']
        for item in items:
            track_name = item['name']
            track_id = item['id']
            artist = item['album']['artists'][0]['name']
            artist_id = item['album']['artists'][0]['id']
            album = item['album']['name']
            # get list of genres for artist
            genres = sp.artist(artist_id)['genres']
            # write to file
            oof.write(track_name + '\t')
            oof.write(track_id + '\t')
            oof.write(album + '\t')
            oof.write(artist + '\t')
            oof.write(','.join(genres) + '\t')
            # get audio features
            features = sp.audio_features(track_id)[0]
            for feature in features:
                oof.write(str(features[feature]) + '\t')
            oof.write('\n')

def limitedSearch(query,lim,offs):
    '''Performs a limited search for data specific to our project'''
    results = sp.search(q=query, limit=lim,offset=offs)
    
    track_Keepers = ['items']
    track_items_Keepers=['name','id','album']
    track_items_album_Keepers = ['artists','name','id']
    
    for k in results['tracks'].keys():
        if k not in track_Keepers:
            results['tracks'][k] = ''
        else:
            for songIdx in range(0,len(results['tracks']['items'])):
                
                for ke in results['tracks']['items'][songIdx].keys():
                    if ke not in track_items_Keepers:
                        results['tracks']['items'][songIdx][ke] = ''
                    else:
                        if ke == 'album':
                            for key in results['tracks']['items'][songIdx]['album']:
                                if key not in track_items_album_Keepers:
                                    results['tracks']['items'][songIdx]['album'][key] = ''
    return results

#list of genres
genres = sp.recommendation_genre_seeds()['genres']

numPages = 19 # max number of pages allowed per query
output = ''
for year in range(2012,2022,1):
    print('Year: '+str(year))
    for genre in genres:
        print('  Genre: '+genre)

        for pageIdx in range(0,numPages):
            result = limitedSearch('genre:'+genre+',year:'+str(year),50,pageIdx*50)
            if output == '':
                output = result
            else:
                for track in result['tracks']['items']:
                    output['tracks']['items'].append(track)
        query2tdf(output)
        
    