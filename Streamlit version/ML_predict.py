import streamlit as st
import pandas as pd
import category_encoders as ce
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

TARGET = "property_value"
DROP = ['property_type', 'date', 'code_departement', 'Perimeter_geometry', 'year',
        'Surface_area_geometry', 'number_of_lots', 'District',
        'District_number', 'postal_code', 'municipality_code', 'longitude', 'Geogrpahic_sectors']
Ordinal = {
    'Construction_Period': {'Avant 1946':1, "1946-1970":2, "1971-1990":3, "Apres 1990":4},
    "zoning_risk_classification": {'light blue': 2, 'Light blue hatched':3, 'Dark Blue Zone':4, "Red zone":6},
    'Rental_Type': {'furinshed':2, 'unfurinshed':1}
}

TARGET_ENC_COLS = ['municipality_name', 'District_name', 'street_name', 'Cadastral_section_code']
OHE_COL = 'transaction_type'

st.title('Paris real estate price predictor')

def clean(df):
    df = df.drop(columns=[c for c in DROP if c in df.columns])
    for c, m in Ordinal.items():
        if c in df.columns:
            df[c] = df[c].map(m)
    return df

def encode(x, y=None, enc=None):
    enc = enc or {}
    x = x.copy()    
    for c in TARGET_ENC_COLS:
        if c in x.columns:
            if c not in enc: enc[c] = ce.TargetEncoder(smoothing=10).fit(x[[c]], y)
            x[c] = enc[c].transform(x[[c]])
    if OHE_COL in x.columns:
        if 'ohe' not in enc: enc['ohe'] = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore').fit(x[[OHE_COL]])
        ohe = pd.DataFrame(enc['ohe'].transform(x[[OHE_COL]]), index=x.index, columns=enc['ohe'].get_feature_names_out([OHE_COL]))
        x =pd.concat([x.drop(columns=[OHE_COL]), ohe], axis=1)
    x = x.select_dtypes(include='number').fillna(0)
    x =x.reindex(columns=enc['cols'], fill_value=0) if 'cols' in enc else x
    enc.setdefault('cols', x.columns.tolist())
    return x, enc

file = st.file_uploader('Upload training dataset (csv/excel)', type = ['csv', 'xlsx'])
if not file:
    st.stop()
df = clean(pd.read_csv(file) if file.name.endswith('csv') else pd.read_excel(file))

if st.button("train model", type='primary'):
    with st.spinner('Training model ...'):
        train, test = train_test_split(df, test_size=0.25, random_state=42)
        q1, q3 = train[TARGET].quantile(0.2), train[TARGET].quantile(0.8)
        iqr = q3 - q1
        train = train[(train[TARGET] >= q1 - 1.5 * iqr) & (train[TARGET] <= q3 + iqr)]

        x_train, enc = encode(train.drop(columns=[TARGET]), train[TARGET])
        x_test, _ = encode(test.drop(columns=[TARGET]), enc=enc)
        y_train, y_test = train[TARGET], test[TARGET]

        grids = {
            "RandomForest": (RandomForestRegressor(random_state=42), {'n_estimators': [25, 50], "min_samples_split" : [2, 5]}),
            "LinearRegression": (LinearRegression(), {'fit_intercept': [True, False], 'positive': [False, True]}),
            "DecisionTree": (DecisionTreeRegressor(random_state=42), {'max_depth': [3, 5, None], 'min_samples_split': [2, 5], 'min_samples_leaf': [1, 2, 5]}), 
            } 
        if HAS_XGB:
            grids['XGBoost'] = (XGBRegressor(random_state=42, verbosity=0), {'n_estimators': [25, 50], 'subsample': [0.5, 0.75, 1.0]})

        best_rmse, best = float('inf'), None
        for name, (model, params) in grids.items():
            g = GridSearchCV(model, params, cv=3, scoring='neg_mean_squared_error', n_jobs=-1).fit(x_train, y_train)
            rmse = mean_squared_error(y_test, g.best_estimator_.predict(x_test)) ** 0.5
            st.write(f"{name}: RMSE = {rmse:,.0f}")
            if rmse < best_rmse:
                best_rmse, best = rmse, g.best_estimator_
                st.session_state['best_name'] = name
        st.success(f'best model: {st.session_state["best_name"]} (RMSE {best_rmse:,.0f})')
        st.session_state.update(model=best, encoders=enc, train_cols=train.drop(columns=[TARGET]))

if 'model' in st.session_state:
    st.divider()
    mode = st.radio('Predict for:', ['Single property', 'Datasets'])

    if mode == 'Single property':
        feats = st.session_state['train_cols']

        with st.form('single'):
            entry = {}
            for c in feats.columns:
                entry[c] = st.selectbox(c, sorted(feats[c].dropna().unique())) if feats[c].dtype == 'object' \
                    else st.number_input(c, value=float(feats[c].median()))
            go = st.form_submit_button('predict')
        if go:
            x, _ = encode(pd.DataFrame([entry]), enc=st.session_state['encoders'])
            st.success(f"Predicted {TARGET}: {st.session_state['model'].predict(x)[0]:,.0f}")

    else:
        new_file = st.file_uploader('Upload dataset to predict', type=['csv', 'xlsx'], key='batch')
        if new_file:
            new_df = clean(pd.read_csv(new_file) if new_file.name.endswith('csv') else pd.read_excel(new_file))
            x_new, _ = encode(new_df.drop(columns=[TARGET], errors='ignore'), enc=st.session_state['encoders'])
            new_df[f'predicted_{TARGET}'] = st.session_state['model'].predict(x_new)
            st.dataframe(new_df, use_container_width=True)
            st.download_button('Download predictions', new_df.to_csv(index=False), file_name='predictions.csv')