import random, os, json
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv('Data/features_30_sec.csv')
df = df.drop(columns=['length','label'])
data = df.copy()
data.set_index('filename', drop=True, inplace=True)
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index)
df_normalized.head()
model = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(df_normalized)

def make_prediction(tracks):
    with open('tracks.json', 'r') as file:
        all_tracks = json.load(file)
    all_tracks = [i['text'] for i in all_tracks]
    #return all_tracks[0:7]
    
    result = []
    for track in tracks:
        distances, indices = model.kneighbors([list(dict(df_normalized.loc[track]).values())])
        result.append(df_normalized.iloc[indices[0][1]].name)
        print(f'Prediction for {track} - {result[-1]} - distance {distances[0][1]}')
    return result    
