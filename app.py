# Import libraries
import streamlit as st

# Import .py files for frontend
from pages.home_page import home_page
from pages.import_page import import_page
from pages.global_page import global_page
from pages.gamemode_page import gamemode_page
from pages.map_page import map_page
from pages.layer_page import layer_page
from pages.download_page import download_page

### --- Building Website --- ###

# ordered list of page functions
PAGE_ORDER = [
    home_page,
    import_page,
    global_page,
    gamemode_page,
    map_page,
    layer_page,
    download_page,
]

# make lookup accessible everywhere
st.session_state.PAGE_ORDER = PAGE_ORDER

# build sidebar nav
pg = st.navigation(
    [st.Page(fn, title=fn.__name__.replace("_page","").capitalize()) for fn in PAGE_ORDER],
    position="sidebar"
)

# pg = st.navigation(
#     [
#         st.Page(home_page, title='Home'),
#         st.Page(import_page, title='Import Settings'),
#         st.Page(global_page, title='Global Settings'),
#         st.Page(gamemode_page, title='Gamemode Settings'),
#         st.Page(map_page, title='Map Settings'),
#         st.Page(layer_page, title='Layer Settings'),
#         st.Page(download_page, title='Download Config')
#     ], position='sidebar')
    
st.set_page_config(layout='wide')
pg.run()