import streamlit as st
import App_Utils as au
import Export_Config_Settings as ecs

def download_page():
    au.on_page_load()

    st.title("We are Download")
    st.dataframe(st.session_state.df)
    "some config settings"

    if st.button("Export current settings"):
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

            st.download_button(
                label='Download as LayerVoting.txt',
                data=cache,
                on_click='ignore',
                file_name='LayerVoting.txt',
                type='primary',
                icon=":material/download:"
            )

        with col2:
            st.code(cache, language=None)

    au.build_bottom_nav(download_page, middle_bool=False)