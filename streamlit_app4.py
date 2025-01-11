import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors

def find_nearest_neighbors(df_main, input_row, k=3, distance_metric='euclidean'):
    if 'Dye Type' in df_main.columns:
        df_main = df_main.drop(columns=['Dye Type'])
    df_encoded = pd.get_dummies(df_main)
    features = df_encoded.iloc[:, 1:]
    input_row_encoded = pd.get_dummies(pd.DataFrame([input_row], columns=df_main.columns[1:]))
    input_row_encoded = input_row_encoded.reindex(columns=features.columns, fill_value=0).values
    knn = NearestNeighbors(n_neighbors=k, metric=distance_metric)
    knn.fit(features)
    distances, neighbors_indices = knn.kneighbors(input_row_encoded)
    nearest_neighbors = df_main.iloc[neighbors_indices[0], :]
    return nearest_neighbors

def find_alternative_poy(df_poy, sample_id, k=3, distance_metric='euclidean'):
    if 'Dye Type' in df_poy.columns:
        df_poy = df_poy.drop(columns=['Dye Type'])
    df_poy_encoded = pd.get_dummies(df_poy)
    features_poy = df_poy_encoded.iloc[:, 1:]
    
    if sample_id not in df_poy['Sample ID'].values:
        raise ValueError(f"Sample ID {sample_id} not found in the dataset")
    
    input_row_encoded = features_poy[df_poy['Sample ID'] == sample_id].values
    features_without_input = features_poy[df_poy['Sample ID'] != sample_id]
    
    knn = NearestNeighbors(n_neighbors=k, metric=distance_metric)
    knn.fit(features_without_input)
    distances, neighbors_indices = knn.kneighbors(input_row_encoded)
    
    neighbors_indices = neighbors_indices[0]
    nearest_neighbors_sample_ids = df_poy.iloc[neighbors_indices, :]['Sample ID'].values
    
    nearest_neighbors_rows = df_poy[df_poy['Sample ID'].isin(nearest_neighbors_sample_ids)]
    columns_to_drop = ['Rcpdate', 'Sample ID', 'Unnamed: 0']
    nearest_neighbors_rows = nearest_neighbors_rows.drop(columns=columns_to_drop, errors='ignore')
    nearest_neighbors_rows = nearest_neighbors_rows.drop_duplicates()
    
    return nearest_neighbors_rows

df_main = pd.read_csv('./Indexedonly100types.csv')
df_additional = pd.read_csv('./Indexedonly100types.csv') 
df_poy = pd.read_csv('mappeditmname1.csv')
st.title('Fabric Composition Analyzer')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")


if 'nearest_neighbors' not in st.session_state:
    st.session_state.nearest_neighbors = None
if 'input_row' not in st.session_state:
    st.session_state.input_row = None

if uploaded_file is not None:
    
    df_uploaded = pd.read_csv(uploaded_file)
    
    input_row = {}
    input_row['Cellulose of yarn (%)'] = st.number_input('Cellulose of yarn (%)', value=78.2)
    input_row['Lignin of yarn (%)'] = st.number_input('Lignin of yarn (%)', value=8.53)
    input_row['pH Level of yarn'] = st.number_input('pH Level of yarn', value=5.36)
    input_row['Fineness of yarn (tex)'] = st.number_input('Fineness of yarn (tex)', value=2.90)
    input_row['Fiber Tenacity of yarn (gm/tex)'] = st.number_input('Fiber Tenacity of yarn (gm/tex)', value=46.99)
    input_row['Elongation of yarn (%)'] = st.number_input('Elongation of yarn (%)', value=2.90)
    input_row['Moisture Regain of yarn (%)'] = st.number_input('Moisture Regain of yarn (%)', value=11.63)
    input_row['Tensile Strength of yarn (MPa)'] = st.number_input('Tensile Strength of yarn (MPa)', value=1500)

    k = st.number_input('Number of neighbors (k)', value=3)
    distance_metric = st.selectbox('Distance metric', ['euclidean', 'manhattan'])

    if st.button('Find Nearest Neighbors'):
        nearest_neighbors = find_nearest_neighbors(df_uploaded, input_row, k=k, distance_metric=distance_metric)
        st.session_state.nearest_neighbors = nearest_neighbors
        st.session_state.input_row = input_row

    if st.session_state.nearest_neighbors is not None:
        input_row_df = pd.DataFrame([st.session_state.input_row])
        output_df = pd.concat([input_row_df, st.session_state.nearest_neighbors], axis=0)
        output_df = output_df[['Sample ID'] + [col for col in output_df.columns if col != 'Sample ID']]
        st.write('Input Row:')
        st.write(input_row_df)
        st.write('Nearest Neighbors:')
        st.write(output_df)

        
        selected_index = st.selectbox('Select a neighbor row to view additional data', output_df.index[1:], key='selectbox')
        if selected_index is not None:
            selected_sample_id = output_df.at[selected_index, 'Sample ID']
            additional_info = df_additional[df_additional['newItemcode'] == selected_sample_id]
            st.write('Additional Data for Selected Neighbor:')
            st.write(additional_info)

            
            if not additional_info.empty:
                itmname_options = additional_info['itmname'].tolist()
                selected_itmname = st.selectbox('Select itmname to find alternative POY', itmname_options)
                
                if selected_itmname:
                    
                    poy_sample_id = df_poy[df_poy['itmname'] == selected_itmname]['Sample ID'].values
                    if len(poy_sample_id) > 0:
                        alternative_poy = find_alternative_poy(df_poy, poy_sample_id[0], k=3, distance_metric='euclidean')
                        st.write('Alternative POY:')
                        st.write(alternative_poy)
                    else:
                        st.warning(f"No matching Sample ID found for itmname: {selected_itmname}")
else:
    st.warning('Please upload a CSV file to proceed.')