import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Function to find the nearest neighbors
def find_nearest_neighbors(df, input_row, k=3, distance_metric='euclidean'):
    if 'Dye Type' in df.columns:
        df = df.drop(columns=['Dye Type'])
    df_encoded = pd.get_dummies(df)
    features = df_encoded.iloc[:, 1:]
    input_row_encoded = pd.get_dummies(pd.DataFrame([input_row], columns=df.columns[1:]))
    input_row_encoded = input_row_encoded.reindex(columns=features.columns, fill_value=0).values
    knn = NearestNeighbors(n_neighbors=k, metric=distance_metric)
    knn.fit(features)
    distances, neighbors_indices = knn.kneighbors(input_row_encoded)
    nearest_neighbors = df.iloc[neighbors_indices[0], :]
    return nearest_neighbors

# Sample additional data (change the path accordingly)
additional_data_df = pd.read_csv('../Indexedonly100types.csv')

# Streamlit UI
st.title('Nearest Yarn')

# File uploader for CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Initialize session state
if 'nearest_neighbors' not in st.session_state:
    st.session_state.nearest_neighbors = None
if 'input_row' not in st.session_state:
    st.session_state.input_row = None

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Input form for the user
    input_row = {}
    input_row['Cellulose of yarn (%)'] = st.number_input('Cellulose of yarn (%)', value=78.2)
    input_row['Lignin of yarn (%)'] = st.number_input('Lignin of yarn (%)', value=8.53)
    input_row['pH Level of yarn'] = st.number_input('pH Level of yarn', value=5.36)
    input_row['Fineness of yarn (tex)'] = st.number_input('Fineness of yarn (tex)', value=2.90)
    input_row['Fiber Tenacity of yarn (gm/tex)'] = st.number_input('Fiber Tenacity of yarn (gm/tex)', value=46.99)
    input_row['Elongation of yarn (%)'] = st.number_input('Elongation of yarn (%)', value=2.90)
    input_row['Moisture Regain of yarn (%)'] = st.number_input('Moisture Regain of yarn (%)', value=11.63)
    input_row['Tensile Strength of yarn (MPa)'] = st.number_input('Tensile Strength of yarn (MPa)', value=1500)

    # Allow the user to select the number of neighbors and distance metric
    k = st.number_input('Number of neighbors (k)', value=3)
    distance_metric = st.selectbox('Distance metric', ['euclidean', 'manhattan'])

    if st.button('Find Nearest Neighbors'):
        nearest_neighbors = find_nearest_neighbors(df, input_row, k=k, distance_metric=distance_metric)
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

        # Adding feature to show additional data on click
        selected_index = st.selectbox('Select a neighbor row to view additional data', output_df.index[1:], key='selectbox')
        if selected_index is not None:
            selected_sample_id = output_df.at[selected_index, 'Sample ID']
            additional_info = additional_data_df[additional_data_df['newItemcode'] == selected_sample_id]
            st.write('Additional Data for Selected Neighbor:')
            st.write(additional_info)
else:
    st.warning('Please upload a CSV file to proceed.')