import streamlit as st
import App_Utils as au
import FUT_Utils as futu

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

            Copy-Pasting between cells is possible.
            """
        )

    team1_df, team2_df = futu.LFUT_to_table(st.session_state.df, filter=st.session_state.map_filter)

    st.header('Team 1')
    team_1_table = st.data_editor(state_maping(team1_df, State_map), column_config=select_box_FU(team1_df, State_map), key="team1_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    st.header('Team 2')
    team_2_table = st.data_editor(state_maping(team2_df, State_map), column_config=select_box_FU(team2_df, State_map), key="team2_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    build_bottom_nav(st.Page(gamemode_page), st.Page(layer_page), df=st.session_state.df, table_1_df=reverse_state_maping(team_1_table, Reverse_state_map), table_2_df=reverse_state_maping(team_2_table, Reverse_state_map), filter=st.session_state.map_filter)