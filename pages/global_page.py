import streamlit as st
import App_Utils as au
import FUT_Utils as futu

def global_page():
    au.on_page_load()

    st.title("🌍 Global Exclusion Settings")
    st.markdown(
        """
        Exclude **Factions**, **Units**, or specific combinations across **all layers**.
        """
    )
    au.FU_explainer()

    team1_df, team2_df = futu.LFUT_to_table(st.session_state.df)

    st.header('Team 1')
    team_1_table = st.data_editor(au.state_maping(team1_df, au.state_map), column_config=au.select_box_FU(team1_df, au.state_map), key="team1_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    st.header('Team 2')
    team_2_table = st.data_editor(au.state_maping(team2_df, au.state_map), column_config=au.select_box_FU(team2_df, au.state_map), key="team2_editor", on_change=lambda: st.session_state.__setitem__("page_saved", False))

    au.build_bottom_nav(global_page, df=st.session_state.df, table_1_df=au.state_maping(team_1_table, au.reverse_state_map), table_2_df=au.state_maping(team_2_table, au.reverse_state_map))
