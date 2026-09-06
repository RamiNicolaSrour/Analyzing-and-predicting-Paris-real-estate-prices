import streamlit as st
import pandas as pd
import plotly.express as px

st.title('remove outliers from a column')
uploaded_file = st.file_uploader('Upload a CSV', type='csv')

if uploaded_file:
    df= pd.read_csv(uploaded_file)
    st.write('Original data:')
    st.dataframe(df.head())
    # pick which numeric olumn to clean
    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    column_clean = st.selectbox('column to remove outliers from', numeric_columns)
    series = df[column_clean].dropna()
    col_min, col_max = float(series.min()), float(series.max())
    st.write(f"Current range: {col_min:,.0f} to {col_max:,.0f}")
    # slider pick acceptable values
    low, high = st.slider(
        "Keep values between",
        min_value=col_min, max_value=col_max,
        value=(col_min, col_max)
    )
    # show box plot
    st.write('Before:')
    fig_before = px.box(df,y=column_clean, title="column before filter outliers")
    st.plotly_chart(fig_before, use_container_width=True)
    # apply filter
    filtered_df = df[(df[column_clean] >= low) & (df[column_clean] <= high)]
    before_count = len(df)
    after_count = len(filtered_df)
    st.metric('Rows kept', f"{after_count:,}", delta=f"-{before_count - after_count:,} removed")
    # boxplt after filter
    st.write("After:")
    fig_after = px.box(filtered_df, y=column_clean, title='after filter')
    st.plotly_chart(fig_after, use_container_width=True)

    st.download_button(
        "download csv",
        filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='filtered.csv',
        mime="text/csv"
    )