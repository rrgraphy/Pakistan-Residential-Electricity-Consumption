import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

import os
import requests
import zipfile

import os
import requests
import zipfile

def add_scatter_plot(df, x_axis, y_axis):

    # Create an interactive scatter plot with Plotly based on the selected variables
    fig = px.scatter(df, x=x_axis, y=y_axis,
                      title=f"Scatter Plot between {x_axis} and {y_axis}",
                      width=800,
                      height=600)
    
    # Update x-axis tick properties for fine-grained ticks
    # Set limits on the x-axis values (change the range as needed)
    x_min_value = df[x_axis].min()
    x_max_value = df[x_axis].max()

    fig.update_xaxes(range=[x_min_value, x_max_value], tickmode='auto', nticks=50)  # Set the range of x-axis values

    return fig

def get_filename_without_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def get_house_data(root_dir, house_name, sampling_frequency):
    # Read the CSV file into a Pandas DataFrame
    precon_house = pd.read_csv(os.path.join(root_dir, house_name+'.csv'))
    precon_house['Date_Time'] = pd.to_datetime(precon_house['Date_Time'])

    # Create a new DataFrame by resampling based on the specified interval
    sampled_precon_house = precon_house.resample(sampling_frequency, on='Date_Time').mean().reset_index()
    return sampled_precon_house


def check_and_download_data():
    metadata_url = 'http://web.lums.edu.pk/~eig/precon_files/Metadata.csv'
    precon_url = 'http://web.lums.edu.pk/~eig/precon_files/PRECON.zip'
    data_directory = './data'
    precon_directory = os.path.join(data_directory, 'PRECON')
    if not os.path.exists(precon_directory):
            os.mkdir(precon_directory)

    # Check if Metadata.csv and PRECON directory exist
    metadata_path = os.path.join(data_directory, 'Metadata.csv')
    precon_exists = os.path.exists(precon_directory)

    if not (os.path.exists(metadata_path) and precon_exists):
        print ('Metadata.csv and PRECON directory do not exist. Downloading files...')
        # Download Metadata.csv
        response_metadata = requests.get(metadata_url)
        with open(metadata_path, 'wb') as metadata_file:
            metadata_file.write(response_metadata.content)

        # Download PRECON.zip
        response_precon = requests.get(precon_url)
        precon_zip_path = os.path.join(data_directory, 'PRECON.zip')
        with open(precon_zip_path, 'wb') as precon_zip_file:
            precon_zip_file.write(response_precon.content)

        # Extract PRECON.zip
        with zipfile.ZipFile(precon_zip_path, 'r') as zip_ref:
            zip_ref.extractall(precon_directory)

        # Delete the PRECON.zip file
        os.remove(precon_zip_path)

        print("Files downloaded, PRECON directory extracted, and zip file deleted.")
    else:
        print("Metadata.csv and PRECON directory already exist.")

