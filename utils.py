import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px
import numpy as np
import os
import requests
import zipfile

import os
import requests
import zipfile
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import plotly.graph_objs as go
from plotly.subplots import make_subplots

def add_histograms_generic(df, variables, grid_size):
    # Calculating number of subplots needed
    num_plots = len(variables)

    # Creating subplots for histograms
    figs = []
    for var in variables:
        fig = go.Histogram(x = df[var])
        figs.append(fig)

    # Creating a subplot grid
    rows, cols = grid_size
    fig_subplots = make_subplots(rows=rows, cols=cols, subplot_titles=variables)

    row = 1
    col = 1
    for i, fig in enumerate(figs):
        # fig_subplots.add_trace(fig['data'][0], row=row, col=col)
        fig_subplots.add_trace(fig, row=row, col=col)
        if col < cols:
            col += 1
        else:
            col = 1
            row += 1

    # Update layout for better presentation
    fig_subplots.update_layout(height=300 * rows, width=400 * cols, title_text='Histograms of Variables')

    return fig_subplots



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
    return sampled_precon_house, precon_house


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


def get_month_wise_stats(precon_house):
    df_variables = precon_house.columns[2:] if len(precon_house.columns) > 2 else precon_house.columns[1:]
    # print (f'df_variables: {df_variables}')
    figs = []
    energies = []
    for variable in df_variables:
        # print (f'variable: {str(variable)}')
        power_curve = precon_house[str(variable)]
        power_curve =  power_curve.to_numpy()
        total_energy = np.trapz(power_curve)/60
        # print (total_energy)
        energies.append(total_energy)


    
    fig = px.pie(values=energies, names=df_variables, title='Energy Consumption by Appliances through out the year (kWh)')
    figs.append(fig)

    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    months_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
    }

    

    for desired_month in months:
        filtered_df = precon_house[precon_house['Date_Time'].dt.month == desired_month]
    
        # print (df_variables)
        energies = []
        for variable in df_variables:
            # print (f'variable: {str(variable)}')
            power_curve = filtered_df[str(variable)]
            power_curve =  power_curve.to_numpy()
            total_energy = (np.trapz(power_curve))/60 #the resulting energy will be ub kW-minutes. to get energy in kWh, we divide by 60
            # print (total_energy)
            energies.append(total_energy)

        fig = px.pie(values=energies, names=df_variables, title=f'Energy Consumption by Appliances through  {months_dict[desired_month]} (kWh)')
        figs.append(fig)

    return figs

