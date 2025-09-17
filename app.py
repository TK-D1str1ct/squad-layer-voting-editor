# Import libraries
import streamlit as st
import pandas as pd

# Import .py files for frontend
import App_Utils as au
from app_pages.home_page import home_page
from app_pages.import_page import import_page
from app_pages.global_page import global_page
from app_pages.gamemode_page import gamemode_page
from app_pages.map_page import map_page
from app_pages.layer_page import layer_page
from app_pages.download_page import download_page

pd.set_option('future.no_silent_downcasting', True)

## initialization 

empty_LFUT_df = pd.read_csv('LFUT.csv', index_col=0)

if 'df' not in st.session_state:
    st.session_state.df = empty_LFUT_df

if 'page_saved' not in st.session_state:
    st.session_state.page_saved = True

if 'back_state' not in st.session_state:
    st.session_state.back_state = False
    st.session_state.back_state_time = None
    st.session_state.back_state_TIMEOUT = 10

if 'next_state' not in st.session_state:
    st.session_state.next_state = False
    st.session_state.next_state_time = None
    st.session_state.next_state_TIMEOUT = 10

Index_parts = empty_LFUT_df.index.astype(str).str.split("_")

# Collect maps (first part of the index)
Maps = sorted({parts[0] for parts in Index_parts})

# Collect gamemodes (second part of the index)
Gamemodes = sorted({parts[1] for parts in Index_parts})

State_map = {
        True: "✅",
        False: "⬜",
        "Mixed": "➖"
    }

Reverse_state_map = {v: k for k, v in State_map.items()}

### --- Building Website --- ###

pg = st.navigation(
    [
        st.Page(home_page, title='Home'),
        st.Page(import_page, title='Import Settings'),
        st.Page(global_page, title='Global Settings'),
        st.Page(gamemode_page, title='Gamemode Settings'),
        st.Page(map_page, title='Map Settings'),
        st.Page(layer_page, title='Layer Settings'),
        st.Page(download_page, title='Download Config')
    ], position='sidebar')
    
st.set_page_config(layout='wide')
pg.run()