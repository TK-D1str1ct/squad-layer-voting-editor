import time
import pandas as pd
import streamlit as st
import FUT_Utils as futu
import Export_Config_Settings as ecs
import Import_Config_Settings as ics

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

def on_page_load():
    #st.session_state.page_saved = True
    if st.session_state.back_state and time.time() - st.session_state.back_state_time > st.session_state.back_state_TIMEOUT:
        st.session_state.back_state = False


def build_bottom_nav(prev_page: st.Page = None, next_page: st.Page = None, middle_bool: bool = True, df : pd.DataFrame = None, table_1_df : pd.DataFrame = None, table_2_df : pd.DataFrame = None, filter = None):
    
    bottom_nav_containter = st.container()
    left, middle, right = bottom_nav_containter.columns(3)

    with left:
        if prev_page is not None and st.button('Previous page'):
            st.session_state.next_state = False
            st.session_state.back_state = True
            st.session_state.back_state_time = time.time()
        if st.session_state.back_state:
            if not st.session_state.page_saved: 
                st.warning("You may have unsaved changes!")
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
                        if table_1_df is not None and table_2_df is not None:
                            df = futu.table_to_LFUT(df, table_1_df, table_2_df, filter)
                        st.session_state.df.loc[df.index, df.columns] = df
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
                    st.warning("You may have unsaved changes!")
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

def state_maping(df:pd.DataFrame, state_map:dict):

    df = df.replace(state_map)
    df = df.infer_objects(copy=False)

    return df

def reverse_state_maping(df:pd.DataFrame, reverse_state_map:dict):

    df = df.replace(reverse_state_map)
    df = df.infer_objects(copy=False)

    return df

def select_box_FU(df:pd.DataFrame, state_map:dict):

    df = state_maping(df, state_map)

    select_options = list(state_map.values())

    column_config = {0: st.column_config.Column(disabled=True)}
    column_config.update({col: st.column_config.SelectboxColumn(options=select_options) for col in df.columns})

    return column_config


### --- Building Website --- ###

def home_page():
    st.title('Home')

    uploaded_settings = st.file_uploader("Import LayerVoting.cfg file")
    if uploaded_settings is not None:
        st.session_state.df = ics.upload_cfg_to_df(uploaded_settings)
    
    build_bottom_nav(next_page=st.Page(global_page), middle_bool=False)

def global_page():

    st.title("🌍 Global Exclusion Settings")
    st.markdown(
        """
        Exclude **Factions**, **Units**, or specific combinations across **all layers**.
        """
    )
    with st.expander("ℹ️ How global exclusions work"):
        st.markdown(
            f"""
            - {State_map[True]} → **Excluded**  
            This Faction–Unit combination is :blue-background[not available] as a voting option on *any* layer for this team.  

            - {State_map[False]} → **Included**  
            This Faction–Unit combination is :blue-background[available] as a voting option on *all* layers for this team.  

            - {State_map["Mixed"]} → **Mixed**  
            This Faction–Unit combination is :blue-background[excluded] on *at least one layer*, but not on all.  
            *(Selecting or saving changes with "Mixed" selected will have no effect for the specific Faction-Unit combination.)*
            """
        )

    team1_df, team2_df = futu.LFUT_to_table(st.session_state.df)

    st.header('Team 1')
    team_1_table = st.data_editor(state_maping(team1_df, State_map), column_config=select_box_FU(team1_df, State_map), key="team1_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    st.header('Team 2')
    team_2_table = st.data_editor(state_maping(team2_df, State_map), column_config=select_box_FU(team2_df, State_map), key="team2_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    build_bottom_nav(st.Page(home_page), st.Page(gamemode_page), df=st.session_state.df, table_1_df=reverse_state_maping(team_1_table, Reverse_state_map), table_2_df=reverse_state_maping(team_2_table, Reverse_state_map))

def gamemode_page():

    st.title("🎮 Gamemode Exclusion Settings")
    st.write("Exclude Factions, Units, or specific combinations from layers with the selected Gamemode.")

    # Gamemode selector
    selected_gamemode = st.selectbox("Choose a Gamemode filter:", Gamemodes, key="gamemode_filter")

    # Explanation in collapsible box
    with st.expander("ℹ️ How gamemode exclusions work"):
        st.markdown(
            f"""
            The symbols indicate the current exclusion state for **{selected_gamemode}** layers:

            - {State_map[True]} → **Excluded**  
            This Faction–Unit combination is :blue-background[not available] as a voting option on *any* **{selected_gamemode}** layer for this team.  

            - {State_map[False]} → **Included**  
            This Faction–Unit combination is :blue-background[available] as a voting option on *all* **{selected_gamemode}** layers for this team.  

            - {State_map["Mixed"]} → **Mixed**  
            This Faction–Unit combination is :blue-background[excluded] on *at least one* **{selected_gamemode}** layer, but not on all.  
            *(Selecting or saving changes with "Mixed" selected will have no effect for the specific Faction-Unit combination.)*
            """
        )

    team1_df, team2_df = futu.LFUT_to_table(st.session_state.df, filter=st.session_state.gamemode_filter)

    st.header('Team 1')
    team_1_table = st.data_editor(state_maping(team1_df, State_map), column_config=select_box_FU(team1_df, State_map), key="team1_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    st.header('Team 2')
    team_2_table = st.data_editor(state_maping(team2_df, State_map), column_config=select_box_FU(team2_df, State_map), key="team2_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    build_bottom_nav(st.Page(global_page), st.Page(map_page), df=st.session_state.df, table_1_df=reverse_state_maping(team_1_table, Reverse_state_map), table_2_df=reverse_state_maping(team_2_table, Reverse_state_map), filter=st.session_state.gamemode_filter)    

def map_page():
    
    st.title("🗺️ Map Exclusion Settings")
    st.write("Exclude Factions, Units, or specific combinations from layers with the selected Map.")

    selected_map = st.selectbox("Choose a Map filter:", Maps, key="map_filter")

    with st.expander(f"ℹ️ How map exclusions work"):
        st.markdown(
            f"""
            The symbols indicate the exclusion state for **{selected_map}** layers:

            - {State_map[True]} → **Excluded**  
            This Faction–Unit combination is :blue-background[not available] as a voting option on **all {selected_map}** layers for this team.  

            - {State_map[False]} → **Included**  
            This Faction–Unit combination is :blue-background[available] as a voting option on **all {selected_map}** layers for this team.  

            - {State_map["Mixed"]} → **Mixed**  
            This Faction–Unit combination is :blue-background[excluded] on *at least one* **{selected_map}** layer, but not on all.  
            *(Selecting or saving changes with "Mixed" selected will have no effect for the specific Faction-Unit combination.)*
            """
        )

    team1_df, team2_df = futu.LFUT_to_table(st.session_state.df, filter=st.session_state.map_filter)

    st.header('Team 1')
    team_1_table = st.data_editor(state_maping(team1_df, State_map), column_config=select_box_FU(team1_df, State_map), key="team1_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    st.header('Team 2')
    team_2_table = st.data_editor(state_maping(team2_df, State_map), column_config=select_box_FU(team2_df, State_map), key="team2_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    build_bottom_nav(st.Page(gamemode_page), st.Page(layer_page), df=st.session_state.df, table_1_df=reverse_state_maping(team_1_table, Reverse_state_map), table_2_df=reverse_state_maping(team_2_table, Reverse_state_map), filter=st.session_state.map_filter)


def layer_page():
    on_page_load()

    st.title("📑 Layer Exclusion Settings")
    st.write("Exclude specific Faction–Unit–Team combinations from individual layers.")

    st.container()
    with st.container(border=True):
        st.markdown("### 🔎 Filters")
        with st.expander("ℹ️ How filtering works"):
            st.markdown(
                """
                Use filters to narrow down the table below by **Layers** and/or **Faction-Unit** combinations.  
                You can enter **multiple search keys**, separated by commas.  

                **Examples:**
                - **Layer Filter** → `AlBasrah, BlackCoast` with **Mode = OR**  
                → Shows only layers from the maps *AlBasrah* **or** *BlackCoast*.  

                - **Faction/Unit Filter** → `BAF, 2` with **Mode = AND**  
                → Shows only columns matching *BAF* **and** *team 2*.  
                """
            )
        row_filter, column_filter = st.columns(2)

        with row_filter:
            with st.container(border=True):
                row_filter_input = st.text_input("Layer filter (comma-separated)")
                row_filter_mode = st.radio("Layer filter mode", ["OR", "AND"], horizontal=True)

        with column_filter:
            with st.container(border=True):
                col_filter_input = st.text_input("Faction/Unit filter (comma-separated)")
                col_filter_mode = st.radio("Faction/Unit filter mode", ["OR", "AND"], horizontal=True)

    with st.expander("ℹ️ How layer exclusions work"):
        st.markdown(
            """
            Each cell in the table represents a **Faction–Unit–Team** combination for a given **Layer**.  
            The checkboxes determine whether that combination is available for voting:

            <input type="checkbox" disabled checked> → **Excluded**  
              This Faction–Unit–Team combination is :blue-background[not available] as a voting option for the specific layer.  
            <input type="checkbox" disabled> → **Included**  
              This Faction–Unit–Team combination is :blue-background[available] as a voting option for the specific layer.  
            """,
            unsafe_allow_html=True
        )

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

    build_bottom_nav(st.Page(map_page), st.Page(download_page), df=edited_df)

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
    
st.set_page_config(layout='wide')
pg.run()