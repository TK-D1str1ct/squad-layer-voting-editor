# %%
# --- Importing packages --- #

import time
import pandas as pd
import streamlit as st

import FUT_Utils as futu

# %%
# --- Initialization --- #

# Empty LFUT df
empty_LFUT_df = pd.read_csv('LFUT.csv', index_col=0)

def init_session():
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

# %%
# --- Define variables --- #

# Dropdown menu options
maps = sorted({parts[0] for parts in empty_LFUT_df.index.astype(str).str.split("_")})
gamemodes = sorted({parts[1] for parts in empty_LFUT_df.index.astype(str).str.split("_")})

# FU table icons
state_map = {
        True: "✅",
        False: "⬜",
        "Mixed": "➖"
    }
reverse_state_map = {v: k for k, v in state_map.items()}

# %%
# --- Define page building functions --- #

# Does something (i think? EDIT: Leon told me it does)
def on_page_load():
    if st.session_state.back_state and time.time() - st.session_state.back_state_time > st.session_state.back_state_TIMEOUT:
        st.session_state.back_state = False

# TODO clean up function and place explainers
def build_bottom_nav(current_page_fn, middle_bool: bool = True,
                     df: pd.DataFrame = None,
                     table_1_df: pd.DataFrame = None,
                     table_2_df: pd.DataFrame = None,
                     filter: str = None):
    """
    Build a bottom navigation bar with Previous, Next, Reset, and Save buttons.
    Automatically determines previous/next pages from st.session_state.PAGE_ORDER.
    """
    bottom_nav_container = st.container()
    left, middle, right = bottom_nav_container.columns([1, 2, 1])

    # get page order from session state
    pages = st.session_state.PAGE_ORDER
    idx = pages.index(current_page_fn)
    prev_page = pages[idx - 1] if idx > 0 else None
    next_page = pages[idx + 1] if idx < len(pages) - 1 else None

    prev_page_name = prev_page.__name__ if prev_page else None
    next_page_name = next_page.__name__ if next_page else None

    prev_page_name = "pages/" + prev_page.__name__ + ".py" if prev_page else None
    next_page_name = "pages/" + next_page.__name__ + ".py" if next_page else None    

    # LEFT: Previous page
    with left:
        if prev_page and st.button("⬅️ Previous"):
            st.session_state.next_state = False
            st.session_state.back_state = True
            st.session_state.back_state_time = time.time()

        if st.session_state.get("back_state", False):
            if not st.session_state.get("page_saved", True):
                st.warning("You have unsaved changes!")
                if st.button("Discard changes", key="back_anyways"):
                    st.session_state.back_state = False
                    st.session_state.page_saved = True
                    st.switch_page(st.Page(prev_page_name))
            else:
                st.session_state.back_state = False
                st.switch_page(st.Page(prev_page_name))

    # MIDDLE: Reset / Save
    if middle_bool:
        with middle:
            with st.container(horizontal_alignment='center'):
                ml, mr = st.columns(2)
                with ml:
                    with st.container(horizontal_alignment='right'):
                        if st.button("🔄 Reset changes", help="Not functional"): #TODO
                            st.session_state.back_state = False
                            st.session_state.next_state = False
                            st.session_state.page_saved = True
                            st.rerun()
                with mr:
                    if st.button("💾 Save Changes"):
                        # Apply FU table updates if provided
                        if table_1_df is not None and table_2_df is not None:
                            df = futu.table_to_LFUT(df, table_1_df, table_2_df, filter)
                        if df is not None:
                            st.session_state.df.loc[df.index, df.columns] = df
                        st.session_state.page_saved = True
                        st.success("Changes saved!")

    # RIGHT: Next page
    with right:
        with st.container(horizontal_alignment='right'):
            if next_page and st.button("Next ➡️"):
                st.session_state.back_state = False
                st.session_state.next_state = True
                st.session_state.next_state_time = time.time()

            if st.session_state.get("next_state", False):
                if not st.session_state.get("page_saved", True):
                    st.warning("You have unsaved changes!")
                    if st.button("Discard changes", key="next_anyways"):
                        st.session_state.next_state = False
                        st.session_state.page_saved = True
                        st.switch_page(st.Page(next_page_name))
                else:
                    st.session_state.next_state = False
                    st.switch_page(st.Page(next_page_name))

    return bottom_nav_container

# Very comlicated function that needs to be cleaned up at some point #TODO
# def build_bottom_nav(prev_page = None, next_page = None, middle_bool:bool = True, df:pd.DataFrame = None, table_1_df:pd.DataFrame = None, table_2_df:pd.DataFrame = None, filter:str = None):
    
#     bottom_nav_containter = st.container()
#     left, middle, right = bottom_nav_containter.columns(3)

#     with left:
#         if prev_page is not None and st.button('Previous page'):
#             st.session_state.next_state = False
#             st.session_state.back_state = True
#             st.session_state.back_state_time = time.time()
#         if st.session_state.back_state:
#             if not st.session_state.page_saved: 
#                 st.warning("You may have unsaved changes!")
#                 if st.button("Discard changes", key="back_anyways"):
#                     st.session_state.back_state = False
#                     st.session_state.page_saved = True
#                     st.switch_page(prev_page)
#             else:
#                 st.session_state.back_state = False
#                 st.switch_page(prev_page)

#     if middle_bool:
#         with middle:
#             with st.container(horizontal_alignment='center'):
#                 ml, mr = st.columns(2)
#                 with ml:
#                     with st.container(horizontal_alignment='right'):
#                         if st.button('Reset changes'):
#                             st.session_state.back_state = False
#                             st.session_state.next_state = False
#                             st.session_state.page_saved = True
#                             st.rerun()
#                 with mr:
#                     if st.button('Save Changes'):
#                         if table_1_df is not None and table_2_df is not None:
#                             df = futu.table_to_LFUT(df, table_1_df, table_2_df, filter)
#                         st.session_state.df.loc[df.index, df.columns] = df
#                         st.session_state.page_saved = True
#                         st.success("Changes saved!")
#                         # st.session_state.df = df
    
#     with right:
#         with st.container(horizontal_alignment='right'):
#             if next_page is not None and st.button('Next page'):
#                 st.session_state.back_state = False
#                 st.session_state.next_state = True
#                 st.session_state.next_state_time = time.time()
#             if st.session_state.next_state:
#                 if not st.session_state.page_saved: 
#                     st.warning("You may have unsaved changes!")
#                     if st.button("Discard changes", key="next_anyways"):
#                         st.session_state.next_state = False
#                         st.session_state.page_saved = True
#                         st.switch_page(next_page)
#                 else:
#                     st.session_state.next_state = False
#                     st.switch_page(next_page)
#     return bottom_nav_containter

# %%
# --- Define LFUT table building functions --- #

# Layer filter function
def apply_filters(df:pd.DataFrame, filter_input:str, filter_mode:str, axis:str = "rows"):

    # Check if there is a filter to apply
    if not filter_input.strip():
        return df

    # Create list for comma seperated filter inputs
    filters = [f.strip() for f in filter_input.split(",") if f.strip()]

    if not filters:
        return df

    # Create target index list based on the rows or columns
    if axis == "rows":
        target = df.index.astype(str)
    else:
        target = df.columns.astype(str)

    # Initialize mask based on where the filter matches with the target
    if filter_mode == "OR":
        mask = pd.Series([False] * len(target))
        for f in filters:
            mask |= target.str.contains(f, case=False, na=False)
    else:
        mask = pd.Series([True] * len(target))
        for f in filters:
            mask &= target.str.contains(f, case=False, na=False)

    # Apply mask to return only the rows or clumns where the filter matched
    if axis == "rows":
        return df.loc[mask.values]
    else:
        return df.loc[:, mask.values]

# %%
# --- Define FU table building functions --- #

# Explainer for FU tables
def FU_explainer(filter:str = ""):

    if filter != "":
        filter = " "+filter
    
    with st.expander("ℹ️ How global exclusions work"):
        st.markdown(
            f"""
            The symbols indicate the current exclusion state for **all{filter}** layers:

            - {state_map[True]} → **Excluded**  
            This Faction–Unit combination is :blue-background[not available] as a voting option on **all{filter}** layers for the specified team.  

            - {state_map[False]} → **Included**  
            This Faction–Unit combination is :blue-background[available] as a voting option on **all{filter}** layers for the specified team.  

            - {state_map["Mixed"]} → **Mixed**  
            This Faction–Unit combination is :blue-background[excluded] on **at least one{filter}** layer for the specified team, but not on all.  
            *(Selecting or saving changes with "Mixed" selected will have no effect for the specific Faction-Unit combination.)*  

            Copy-Pasting between cells is possible.
            """
        )

# Replaces df cell values according to state_map dictionary
def state_maping(df:pd.DataFrame, state_map:dict):

    df = df.replace(state_map)
    df = df.infer_objects(copy=False)

    return df

# Creates column config settings for FU tables
def select_box_FU(df:pd.DataFrame, state_map:dict):

    df = state_maping(df, state_map)

    select_options = list(state_map.values())

    column_config = {0: st.column_config.Column(disabled=True)}
    column_config.update({col: st.column_config.SelectboxColumn(options=select_options) for col in df.columns})

    return column_config