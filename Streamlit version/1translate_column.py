import streamlit as st
import pandas as pd

st.title('feature translate')
uploaded_file = st.file_uploader('Upload a CSV', type='csv')
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write('Original data:')
    st.dataframe(df.head())

    # pick column to translte
    column_translated = st.selectbox('column to translate', df.columns)
    st.write(f"Unique values in {column_translated}`:")
    st.write(df[column_translated].unique())

    # trasnaction types translate
    translate_map = {
        'Vente': 'Sale', "Vente en l'état future d'achèvement": 'Sale in future after completion',
        'Echange': 'Exchange/Swap', 'Adjudication':'Auction',
        'Expropriation':'Compulsory purchase', 'Vente terrain à bâtir': 'sale of building land'
    }

    if st.button('Translae'):
        # astype(str) if column is category type
        df[column_translated] = df[column_translated].astype(str).replace(translate_map)
        st.write('translated data:')
        st.dataframe(df.head())

        st.download_button(
            'Download transalted CSV',
            df.to_csv(index=False).encode('utf-8'),
            file_name='translate.csv', mime='text/csv'
        )