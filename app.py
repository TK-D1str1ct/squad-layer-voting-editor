import time
import pandas as pd
import streamlit as st
import FUT_Utils as futu
import Export_Config_Settings as ecs
import Import_Config_Settings as ics

## initialization 

#faction_colors_df = pd.read_csv("faction_colors.csv") #TODO apply column colors based on faction (cant do it with st.dataframe?) --> can't be done with st.data_editor


if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('LFUT_Settings.csv', index_col=0) #TODO get LFUT version with tripple column headers (team | faction | unit) for display purposes
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

def on_page_load():
    #st.session_state.page_saved = True
    if st.session_state.back_state and time.time() - st.session_state.back_state_time > st.session_state.back_state_TIMEOUT:
        st.session_state.back_state = False


def build_bottom_nav(prev_page: st.Page = None, next_page: st.Page = None, middle_bool: bool = True, edited_df : pd.DataFrame = None):
    
    bottom_nav_containter = st.container()
    left, middle, right = bottom_nav_containter.columns(3)

    with left:
        if prev_page is not None and st.button('Previous page'):
            st.session_state.next_state = False
            st.session_state.back_state = True
            st.session_state.back_state_time = time.time()
        if st.session_state.back_state:
            if not st.session_state.page_saved: 
                st.warning("You have unsaved changes!")
                if st.button("Discard changes", key="back_anyways"):
                    st.session_state.back_state = False
                    st.session_state.page_saved = True
                    st.switch_page(prev_page)
            else:
                st.session_state.back_state = False
                st.switch_page(prev_page)

    if middle_bool:
        with middle:
            with st.container(horizontal_alignment='center'):
                ml, mr = st.columns(2)
                with ml:
                    with st.container(horizontal_alignment='right'):
                        if st.button('Reset changes'):
                            st.session_state.back_state = False
                            st.session_state.next_state = False
                            st.session_state.page_saved = True
                            st.rerun()
                with mr:
                    if st.button('Save Changes'):
                        st.session_state.df.loc[edited_df.index, edited_df.columns] = edited_df
                        st.session_state.page_saved = True
                        st.success("Changes saved!")
                        # st.session_state.df = df
    
    with right:
        with st.container(horizontal_alignment='right'):
            if next_page is not None and st.button('Next page'):
                st.session_state.back_state = False
                st.session_state.next_state = True
                st.session_state.next_state_time = time.time()
            if st.session_state.next_state:
                if not st.session_state.page_saved: 
                    st.warning("You have unsaved changes!")
                    if st.button("Discard changes", key="next_anyways"):
                        st.session_state.next_state = False
                        st.session_state.page_saved = True
                        st.switch_page(next_page)
                else:
                    st.session_state.next_state = False
                    st.switch_page(next_page)
    return bottom_nav_containter

def apply_filters(df, filter_input, filter_mode, axis="rows"):
    if not filter_input.strip():
        return df

    filters = [f.strip() for f in filter_input.split(",") if f.strip()]
    if not filters:
        return df

    if axis == "rows":
        target = df.index.astype(str)
    else:
        target = df.columns.astype(str)

    # Initialize mask
    if filter_mode == "OR":
        mask = pd.Series([False] * len(target))
        for f in filters:
            mask |= target.str.contains(f, case=False, na=False)
    else:  # AND
        mask = pd.Series([True] * len(target))
        for f in filters:
            mask &= target.str.contains(f, case=False, na=False)

    # Apply mask
    if axis == "rows":
        return df.loc[mask.values]  # mask.values = numpy array
    else:
        return df.loc[:, mask.values]

def home_page():
    st.title('Home')
    

def global_page():
    # 2 tables, 1 for team 1 one for team 2
    # rows are factions
    # columns are units
    # Should update all other tables accordingly

    st.title("Global Exclusion Settings")

    team1_df, team2_df = futu.LFUT_to_table(st.session_state.df) #TODO
    #col_config = {

    #}
    st.header('Team 1')
    st.dataframe(team1_df)
    #edited_team1_df = st.data_editor(team1_df, column_config=col_config)
    st.header('Team 2')
    st.dataframe(team2_df)
    #edited_team2_df = st.data_editor(team2_df, column_config=col_config)
    #st.session_state.df = futu.table_to_LFUT(st.session_state.df, team1_df, team2_df) <-- This uses the correct func name, also added extra input argument (st.session_state.df)

    build_bottom_nav(st.Page(home_page), st.Page(gamemode_page))

def gamemode_page():
    # dropdown menu with all available game modes
    # 2 tables, 1 for team 1 one for team 2
    # rows are factions
    # columns are units
    # Should update all other tables accordingly

    st.title("Gamemode Exclusion Settings")

    team1_df, team2_df = futu.LFUT_to_table(st.session_state.df, filter="Invasion") #TODO

    st.header('Team 1')
    st.dataframe(team1_df)
    #edited_team1_df = st.data_editor(team1_df, column_config=col_config)
    st.header('Team 2')
    st.dataframe(team2_df)

    build_bottom_nav(st.Page(global_page), st.Page(map_page))
    

def map_page():
    # dropdown menu with all available maps
    # 2 tables, 1 for team 1 one for team 2
    # rows are factions
    # columns are units
    # Should update all other tables accordingly
    
    st.title("Map Exclusion Settings")

    team1_df, team2_df = futu.LFUT_to_table(st.session_state.df, filter="Fallujah") #TODO

    st.header('Team 1')
    st.dataframe(team1_df)
    #edited_team1_df = st.data_editor(team1_df, column_config=col_config)
    st.header('Team 2')
    st.dataframe(team2_df)

    build_bottom_nav(st.Page(gamemode_page), st.Page(layer_page))


def layer_page():
    on_page_load()
    st.title("we are layer")

    # --- Filter UI ---
    st.subheader("Row / Column Filters")

    row_filter_input = st.text_input("Row filter (comma-separated substrings)")
    row_filter_mode = st.radio("Row filter mode", ["OR", "AND"], horizontal=True)

    col_filter_input = st.text_input("Column filter (comma-separated substrings)")
    col_filter_mode = st.radio("Column filter mode", ["OR", "AND"], horizontal=True)

    # --- Apply filters ---
    df_filtered = apply_filters(st.session_state.df.copy(), row_filter_input, row_filter_mode, axis="rows")
    df_filtered = apply_filters(df_filtered, col_filter_input, col_filter_mode, axis="cols")
    df_filtered = df_filtered.dropna(axis=1, how="all")

    # --- Example column config ---
    config = {
        0: st.column_config.Column(disabled=True),
        "Exclude": st.column_config.Column(pinned=True),
    }

    # --- Editable table ---
    edited_df = st.data_editor(
        df_filtered,
        key="editor",
        column_config=config,
        width='stretch',
        on_change=lambda: st.session_state.__setitem__("page_saved", False)
    )

    # --- Update session state (optional) ---
    #st.session_state.df.update(edited_df)

# --- ABOVE = NEW | BELOW = OLD --- #

    # config = {
    #     0: st.column_config.Column(disabled = True),
    #     'Exclude': st.column_config.Column(pinned = True)
    # }

    # edited_df = st.data_editor(st.session_state.df, column_config=config, key = 'editor', on_change= lambda: st.session_state.__setitem__("page_saved", False))

    build_bottom_nav(st.Page(map_page), st.Page(download_page), edited_df=edited_df)

def download_page():
    st.title("We are Download")
    st.dataframe(st.session_state.df)
    "some config settings"

    if st.button("Export as cfg file"):
        cache = ecs.download_as_cfg(st.session_state.df)

        col1, col2 = st.columns([1, 2])  # left = download button, right = raw text

        with col1:
            st.download_button(
                label='Download as LayerVoting.cfg',
                data=cache,
                on_click='ignore',
                file_name='LayerVoting.cfg',
                type='primary',
                icon=":material/download:"
            )

        with col2:
            st.code(cache, language=None)
            # st.text_area(
            #     "Copy/Paste Config",
            #     value=cache,
            #     height=300,
            #     label_visibility="collapsed"  # hides the label, keeps only box
            # )

    build_bottom_nav(st.Page(layer_page), middle_bool=False)

pg = st.navigation(
    [
        st.Page(home_page, title='Home'), 
        st.Page(global_page, title='Global Settings'),
        st.Page(gamemode_page, title='Gamemode Settings'),
        st.Page(map_page, title='Map Settings'),
        st.Page(layer_page, title='Layer Settings'),
        st.Page(download_page, title='Download Config')
    ], position='sidebar')
    
pg.run()