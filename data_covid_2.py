####################################### Aquisição de dados
#import basics
import streamlit as st 
import requests
import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as pyplot
matplotlib.style.use('fivethirtyeight')
import numpy as np
from functools import reduce
#expericing library
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')
from holoviews.plotting.links import RangeToolLink
import plotly.graph_objects as go
import datetime
#data sources
import datetime as dt
import base64
import io
#feito para traduzir o nome dos gráficos 
from deep_translator import GoogleTranslator



#gerando funcoes para os dados 
@st.cache
def get_covid_data():
    url='https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    df= pd.read_csv(url, sep=',')
    return df

def get_table_download_linko(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    towrite = io.BytesIO()
    downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download excel file</a>'
    return linko

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    towrite = io.BytesIO()
    downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True,decimal= ",")
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download excel file</a>' # decode b'abc' => abc

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False,decimal= ",")

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def df_filtered(
    df: pd.DataFrame,  # Source dataframe
    #f_date_range: [int, int],  # Current value of an ST date slider
    f_manager: list = [],  # Current value of an ST multi-select
    f_program: list = [],  # Current value of another ST multi-select
) -> pd.DataFrame:
    dff = df.copy()
    #df.loc[f_date_range[0] : f_date_range[1]].reset_index(drop=True)
    if len(f_manager) > 0:
        dff = dff.loc[(dff["location"].isin([f_manager]))].reset_index(drop=True)
    if len(f_program) > 0:
         columns= dff[f_program]
         print(columns)
        #dff = dff.loc[(dff.columns.isin(f_program))].reset_index(drop=True)
        #dff = dff[columns]
    return columns


# pegando os dados
df = get_covid_data()

with st.expander("See explanation"):
    loc_list = df['location'].drop_duplicates()
    loc_select = st.multiselect('select country',loc_list)
    var_list = df.columns.to_list()
    var_select = st.multiselect('select var',var_list)
    data =df[df['location'].isin(loc_select)]
    #data.location = data['location'].apply(translator.translate, src='ing', dest='port').apply(getattr, args=('text',))
    data = data[['location', 'date', var_select[0]]]
    data = data.pivot_table(index='date',columns='location', values=var_select[0]).reset_index()


st.write(data)
   

#gerando os botoes de dados 
if st.button('Download Dataframe as CSVV'):
    tmp_download_link = download_link(data, 'YOUR_DF.csv', 'Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

if st.button('Download Dataframe as Excell'):
    link= get_table_download_linko(data)
    st.markdown(link, unsafe_allow_html=True)
