# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:21:16 2022

@author: Matt Morais
"""
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA

from scipy.spatial.distance import cdist



class dittAudio:
    
    def __init__(self,sp_link):
        self.sp = sp_link
        self.data = pd.read_csv("data.csv")
        self.genre_data = pd.read_csv("data_by_genres.csv")
        self.y = self.data['popularity'] #target
        self.build_kmeans()
        
    
    def build_kmeans(self):
        """ Builds and preps the recommender """
        self.song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                  ('kmeans', KMeans(n_clusters=20, 
                                   verbose=False))
                                 ], verbose=False)

        X = self.data[['danceability','energy','loudness','speechiness','acousticness','liveness','valence','tempo']]
        self.number_cols = list(X.columns)
        self.song_cluster_pipeline.fit(X)
        self.song_cluster_labels = self.song_cluster_pipeline.predict(X)
        self.data['cluster_label'] = self.song_cluster_labels
        
        pca_pipeline = Pipeline([('scaler', StandardScaler()), ('PCA', PCA(n_components=2))])
        song_embedding = pca_pipeline.fit_transform(X)
        projection = pd.DataFrame(columns=['x', 'y'], data=song_embedding)
        projection['title'] = self.data['name']
        projection['cluster'] =self.data['cluster_label']

    def get_mean_vector(self, song_list):    
        number_cols = ['danceability','energy','loudness','speechiness','acousticness','liveness','valence','tempo']
        song_vectors = []
        song_df = pd.Series(song_list)
        song_vector = song_df[number_cols].values
        song_vectors.append(song_vector)  
        song_matrix = np.array(list(song_vectors))    
        arr = np.mean(song_matrix, axis=0)
        return arr
    
    def recommend_songs(self,song_data, n_songs=10):
        """actual recommender using Kmeans clustering and mean vector distances
        
        @param song_data Dictionary of keys that match spotify track features 
        with corresponding values. Typically this is the average of what the user
        selects for a seed
        
        @return Dictionary containing n_songs recommended songs
        """
        metadata_cols = ['name', 'artists','id']
        song_center = self.get_mean_vector(song_data)
        scaler = self.song_cluster_pipeline.steps[0][1]
        scaled_data = scaler.transform(self.data[self.number_cols])
        scaled_song_center = scaler.transform(song_center.reshape(1, -1))
        distances = cdist(scaled_song_center, scaled_data, 'cosine')
        index = list(np.argsort(distances)[:, :n_songs][0])[-6:]
        print("index: ",index)
        rec_songs = self.data.iloc[index]
        rec_songs = rec_songs[metadata_cols].to_dict(orient='records')
        outDict = {}
        for x in rec_songs:
            songid = x['id']
            key = 'spotify:track:' + songid
            val1 = x['name']
            val2 = ','.join([l.strip().strip('\'') for l in x['artists'].strip('[,]').split(',')])
            value = val1 + '-' + val2
            outDict[key] = value
            
        #pd.Series(outDict)
        return outDict
        