import streamlit as st
import App_Utils as au
import Export_Config_Settings as ecs

def download_page():
    au.on_page_load()

    st.title("We are Download", help="Blame Leon for this title")
    st.dataframe(st.session_state.df)

    # Outer container wrapping everything below
    with st.container(border=True):
        # Export button (centered)
        export_clicked = st.columns([3, 1, 3])[1].button(
            "Export current settings", type="primary"
        )
        if export_clicked:
            cache = ecs.download_as_cfg(st.session_state.df)
            
            # First inner container -> two download buttons
            with st.container(border=True):
                st.markdown(
                    """
                    Download your current config settings as either a .cfg or .txt file:
                    """
                )
                col1, col2, col3 = st.columns([0.18, 0.18, 0.64])
                with col1:
                    st.download_button(
                        label='Download as LayerVoting.cfg',
                        data=cache,
                        file_name='LayerVoting.cfg',
                        type='primary',
                        icon=":material/download:",
                        key="dl_cfg"
                    )
                with col2:
                    st.download_button(
                        label='Download as LayerVoting.txt',
                        data=cache,
                        file_name='LayerVoting.txt',
                        type='primary',
                        icon=":material/download:",
                        key="dl_txt"
                    )

            # Second inner container -> code block
            with st.container(border=True):
                st.markdown(
                    """
                    Manually copy your config settings (copy all button in top right of text block):
                    """
                )
                st.code(cache, language=None, height=200)

    au.build_bottom_nav(download_page, middle_bool=False)