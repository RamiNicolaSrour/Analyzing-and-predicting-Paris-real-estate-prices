import streamlit as st
import pandas as pd

st.title('merge two tables')
file_left = st.file_uploader('Left table', type='csv')
file_right = st.file_uploader('Right table', type='csv')

if file_left and file_right:
    df_left, df_right = pd.read_csv(file_left), pd.read_csv(file_right)
    c1, c2 = st.columns(2)
    key_left = c1.selectbox('Join column (left)', df_left.columns)
    key_right = c1.selectbox('Join column (right)', df_right.columns)    
    how = st.radio('Join type', ['left', 'inner', 'outer', 'right'], horizontal=True)

    if st.button('Merge tables'):
        merged = df_left.merge(df_right, left_on=key_left, right_on=key_right, how=how)

        if len(merged) > len(df_left):
            st.warning(f"Rows grew {len(df_left):,} -> {len(merged):,} - `{key_right}` likely has duplicate values.")
        else:
            st.success(f"Merge ok: {len(df_left):,} -> {len(merged):,} rows.")

        st.dataframe(merged.head(20))
        st.download_button('Download merged CSV', merged.to_csv(index=False).encode(), 'merged.csv')