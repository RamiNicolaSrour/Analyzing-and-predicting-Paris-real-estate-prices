import streamlit as st
import pandas as pd
import plotly.express as px
st.title('Avg value by category')

uploaded_file = st.file_uploader('Upload a CSV', type='csv')
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    cat_cols = df.select_dtypes(exclude='number').columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    if not cat_cols or not num_cols:
        st.warning("Need at least one text column and one number column.")
    else:
        c1,c2 = st.columns(2)
        group_col = c1.selectbox('Group by', cat_cols)
        value_col = c2.selectbox('Value column', num_cols)
        agg = st.radio('Statistic', ['mean', 'median', 'count'], horizontal=True)

        result = df.groupby(group_col)[value_col].agg(agg).sort_values()
        fig = px.bar(x=result.values, y=result.index, orientation='h', 
                     labels={'x':f"{agg} of {value_col}", 'y':group_col})
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(result.rename(f"{agg}_{value_col}"))