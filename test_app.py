import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px
from  utils import *

def add_histogram(dataframe, x_axis):
    fig = px.histogram(dataframe, x=x_axis, 
                       title=f'{x_axis} Distribution',
                       width = 800,
                       height = 600)
    fig.update_layout(xaxis_title=x_axis.capitalize(), yaxis_title='# of Houses')
    return fig

def main():
    st.title('Pakistan Residential Electricity Consumption Dataset  \n An In Depth Anlysis')
    # Table of contents
    st.sidebar.title('Table of Contents')
    st.sidebar.markdown("""
                        - [Meta Data Preview](#meta-data-preview)
                        - [Distribution of Houses wrt Various Variables](#distribution-of-houses-wrt-various-variables)
                        - [Precon House Data](#precon-house-data)
                        """)
    
    
    #check if data alread exists otherwise download and extract
    check_and_download_data()

    # Read data from a default path (change the path accordingly)
    metadata_path = "data/Metadata.csv"  # Update this with your file path
    df = pd.read_csv(metadata_path)
    df.rename(columns={'Website Name': 'House_Name'}, inplace=True)
    
    precon_path = 'data/PRECON'
    precon_house_data = os.listdir(precon_path)
    precon_house_names = [get_filename_without_extension(x) for x in precon_house_data]

    st.header('Meta Data Preview')
    st.write(df.head())
    
    # Select columns for scatter plot of meta data
    st.write('Relation between different variables of the meta data')
    columns = df.columns.tolist()
    x_axis = st.selectbox("Select X-axis variable for Scatter Plot:", columns, index=0)
    y_axis = st.selectbox("Select Y-axis variable for Scatter Plot:", columns, index=1)
    fig = add_scatter_plot(df, x_axis, y_axis)
    st.plotly_chart(fig)

    # Plot histograms of metadata variables
    st.header('Distribution of Houses wrt Various Variables')
    x_axis = st.selectbox("Select X-axis variable for Histogram:", columns, index=0)

    # fig = add_histograms_generic(df, columns[1:], (14,2))
    fig = add_histogram(df, x_axis)
    st.plotly_chart(fig)


    
    ############################## Precon House Analysis #########################
    
    st.header('Precon House Data')
    house_name = st.selectbox('Select a house to plot:', precon_house_names, index=0)
    sampling_frequency = st.selectbox('Select a Time Granularity for plotting \
                                      (high granularity might slow the app):',
                                    ['10M', '1H', '3H', '6H', '9H', '12H'],
                                    index = 5)
                                                                     
    sampled_precon_house, precon_house = get_house_data(root_dir=precon_path,
                                          house_name=house_name,
                                          sampling_frequency=sampling_frequency)

    # Select a variable using a selectbox
    selected_variable = st.selectbox('Select a variable to plot against time:', sampled_precon_house.columns[1:])

    # Create an interactive plot with Plotly based on the selected variable
    fig = px.line(sampled_precon_house,
                   x='Date_Time',
                   y=selected_variable,
                   title=f'{selected_variable} over Time',
                   width=800,
                   height=600)
    fig.update_xaxes(rangeslider_visible=True, tickmode='auto', nticks=100)  # Enable the range slider for x-axis

    # Show the Plotly figure using Streamlit's Plotly support
    st.plotly_chart(fig)

    st.write(f'### Mothly and Yearly consumption of  {house_name}')
    figs = get_month_wise_stats(precon_house)
    for fig_ in figs:
        st.plotly_chart(fig_)

    ############################################################################################




if __name__ == "__main__":
    main()
