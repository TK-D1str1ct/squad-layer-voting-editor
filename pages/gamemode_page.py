import streamlit as st
import App_Utils as au
import FUT_Utils as futu

def gamemode_page():
    au.on_page_load()

    st.title("🎮 Gamemode Exclusion Settings")
    st.write("Exclude Factions, Units, or specific combinations from layers with the selected Gamemode.")

    # Gamemode selector
    selected_gamemode = st.selectbox("Choose a Gamemode filter:", au.gamemodes, key="gamemode_filter")

    # Explanation in collapsible box
    au.FU_explainer(selected_gamemode)

    team1_df, team2_df = futu.LFUT_to_table(st.session_state.df, filter=st.session_state.gamemode_filter)

    st.header('Team 1')
    team_1_table = st.data_editor(au.state_maping(team1_df, au.state_map), column_config=au.select_box_FU(team1_df, au.state_map), key="team1_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    st.header('Team 2')
    team_2_table = st.data_editor(au.state_maping(team2_df, au.state_map), column_config=au.select_box_FU(team2_df, au.state_map), key="team2_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    au.build_bottom_nav(gamemode_page, df=st.session_state.df, table_1_df=au.state_maping(team_1_table, au.reverse_state_map), table_2_df=au.state_maping(team_2_table, au.reverse_state_map), filter=st.session_state.gamemode_filter)    
