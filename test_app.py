import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px
from  utils import *



def main():
    st.title('Pakistan Residential Electricity Consumption Dataset  \n An In Depth Anlysis')
    # Table of contents
    st.sidebar.title('Table of Contents')
    st.sidebar.markdown("""
                        - [Meta Data Preview](#meta-data-preview)
                        - [Precon House Data](#precon-house-data)
                        """)
    
    
    #check if data alread exists otherwise download and extract
    check_and_download_data()

    # Read data from a default path (change the path accordingly)
    metadata_path = "data/Metadata.csv"  # Update this with your file path
    df = pd.read_csv(metadata_path)
    
    precon_path = 'data/PRECON'
    precon_house_data = os.listdir(precon_path)
    precon_house_names = [get_filename_without_extension(x) for x in precon_house_data]

    st.header('Meta Data Preview')
    st.write(df.head())
    
    # Select columns for scatter plot of meta data
    st.write('Relation between different variables of the meta data')
    columns = df.columns.tolist()
    x_axis = st.selectbox("Select X-axis data:", columns, index=0)
    y_axis = st.selectbox("Select Y-axis data:", columns, index=1)
    
    fig = add_scatter_plot(df, x_axis, y_axis)
    st.plotly_chart(fig)

    
    st.header('Precon House Data')
    house_name = st.selectbox('Select a house to plot:', precon_house_names, index=0)
    sampling_frequency = st.selectbox('Select a Time Granularity for plotting \
                                      (high granularity might slow the app):',
                                    ['10M', '1H', '3H', '6H', '9H', '12H'],
                                    index = 5)
                                                                     
    sampled_precon_house = get_house_data(root_dir=precon_path,
                                          house_name=house_name,
                                          sampling_frequency=sampling_frequency)

    # Select a variable using a selectbox
    selected_variable = st.selectbox('Select a variable to plot against time:', sampled_precon_house.columns[1:])

    # Create an interactive plot with Plotly based on the selected variable
    fig = px.line(sampled_precon_house,
                   x='Date_Time',
                   y=selected_variable,
                   title=f'{selected_variable} over Time',
                   width=1200,
                   height=900)
    fig.update_xaxes(rangeslider_visible=True, tickmode='auto', nticks=100)  # Enable the range slider for x-axis

    # Show the Plotly figure using Streamlit's Plotly support
    st.plotly_chart(fig)





if __name__ == "__main__":
    main()


