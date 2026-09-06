import streamlit as st
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
import plotly.express as px

st.title('match each point to nearest neighbor')
file_a = st.file_uploader('file a (match FROM)', type='csv')
file_b = st.file_uploader('file b (match TO)', type='csv')

if file_a and file_b:
    df_a, df_b = pd.read_csv(file_a), pd.read_csv(file_b)
    c1, c2 = st.columns(2)
    lat_a = c1.selectbox("Lat (A)", df_a.columns)
    lon_a = c1.selectbox("Lon (A)", df_a.columns)
    lat_b = c2.selectbox("Lat (B)", df_b.columns)
    lon_b = c2.selectbox("Lon (B)", df_b.columns)

    if st.button('find neares matches'):
        a = df_a.dropna(subset=[lat_a, lon_a]).copy()
        b = df_b.dropna(subset=[lat_b, lon_b]).copy()
        tree = cKDTree(b[[lon_b, lat_b]].values)
        dist, idx = tree.query(a[[lon_a, lat_a]]. values, k=1)
        a['match_distance'], a['matched_row_b'] = dist, idx
        st.success(f"Matched {len(a):,} points.")
        st.dataframe(a.head(20))
        st.plotly_chart(px.histogram(a, x='match_distance', nbins=40, title='match distance'), use_container_width=True)

        combined = pd.concat([
            a[[lat_a, lon_a]].rename(columns={lat_a:'latitude', lon_a: 'longitude'}).assign(layer='File A'),
            b[[lat_b, lon_b]].rename(columns={lat_b:'latitude', lon_b: 'longitude'}).assign(layer='File B')
              ])

        fig = px.scatter_mapbox(combined, lat='latitude', lon='longitude', color='layer', zoom=10, height=500)
        fig.update_layout(mapbox_style='open-street-map', margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

        st.download_button('Download mathced csv', a.to_csv(index=False).encode(), 'matched_results.csv')