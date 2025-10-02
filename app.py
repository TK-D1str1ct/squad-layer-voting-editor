# Import libraries
import streamlit as st

from App_Utils import init_session

### --- Building Website --- ###

init_session()

# Import .py files for frontend
from pages.home_page import home_page
from pages.import_page import import_page
from pages.global_page import global_page
from pages.gamemode_page import gamemode_page
from pages.map_page import map_page
from pages.layer_page import layer_page
from pages.download_page import download_page

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

PAGE_TITLES = {
    "home_page": "Home",
    "import_page": "Import Config Settings",
    "global_page": "Global Exclusions",
    "gamemode_page": "Gamemode Exclusions",
    "map_page": "Map Exclusions",
    "layer_page": "Layer Exclusions",
    "download_page": "Download Config",
}

# make lookup accessible everywhere
st.session_state.PAGE_ORDER = PAGE_ORDER

# build sidebar nav
pg = st.navigation(
    [st.Page(fn, title=PAGE_TITLES[fn.__name__]) for fn in PAGE_ORDER],
    position="sidebar",
)
    
st.set_page_config(layout='wide')
pg.run()