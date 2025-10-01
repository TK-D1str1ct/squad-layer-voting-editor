import streamlit as st
import App_Utils as au
import Export_Config_Settings as ecs

def download_page():
    au.on_page_load()

    st.title("📤 We are Download", help="Blame Leon for this title")
    st.dataframe(st.session_state.df)

    st.subheader("Export settings:")

    # Outer container wrapping everything below
    with st.container(border=True):
        # Export settings
        st.markdown("Change export settings based on your preferences. Make sure to do this *before* clicking the export button")
        col1, col2, col3 = st.columns(3)
        with col1:
            eel = st.radio(
                "Export excluded layers?",
                ["Yes", "No"],
                help = "Whether to export excluded layers as commented out lines or leave them out entirely",
                index = 0,
                horizontal = False,
                key = "export_excluded",
                disabled = False
            )
        
        with col2:
            icet = st.radio(
                "Include config explainer text?",
                ["Yes", "No"],
                help = "Whether to include the default explainer text at the top of a new LayerVoting.cfg file",
                index = 1,
                horizontal = False,
                key = "include_explain",
                disabled = False
            )
        
        with col3:
            iwl = st.radio(
                "Include white line between maps?",
                ["Yes", "No"],
                help = "Whether to include a white line in between layers from different maps",
                index = 0,
                horizontal = False,
                key = "include_whiteline",
                disabled = False
            )

        # Change variables based on radio settings
        if eel == "Yes":
            eel = False
        else:
            eel = True

        if icet == "Yes":
            icet = True
        else:
            icet = False

        if iwl == "Yes":
            iwl = True
        else:
            iwl = False

        # Export button (centered)
        export_clicked = st.columns([3, 1, 3])[1].button(
            "Export current settings", type="primary"
        )
        if export_clicked:
            cache = ecs.download_as_cfg(st.session_state.df, eel, icet, iwl)
            
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