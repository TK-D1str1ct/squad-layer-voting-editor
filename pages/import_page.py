import streamlit as st
import App_Utils as au
import Import_Config_Settings as ics

def import_page():
    au.on_page_load()
    st.title("📥 Import Config Settings")

    st.subheader("Import settings:")
    st.markdown("Change import settings based on your preferences. Make sure to do this *before* uploading or pasting your settings")
    
    col1, col2, col3 = st.columns(3)
    exclusion_options = [
                "Exclude all layers",
                "Exclude missing layers",
                "Use imported exclusions only",
                "Include all layers"
            ]

    with col1:
        exclusion_mode = st.radio(
            "Layer Exclusion Mode:",
            exclusion_options,
            help = """\
                **Exclude all layers** → Every layer is excluded, regardless of what’s in your imported file.  
                **Exclude missing layers** → Keep imported exclusions, and also exclude any layers not found in your imported file.  
                **Use imported exclusions only** → Only apply the exclusions from your imported file.  
                **Include all layers** → All layers are included, even if excluded in your imported file.  
                """,
            index = 2,
            horizontal = False,
            key = "layers_exclude")
        
    # with col2:
    #     idl = st.radio(
    #         "Include deprecated layers?",
    #         ["Yes", "No"],
    #         help = "Whether to show deprecated layers from your import file in the export file.",
    #         index = 1,
    #         horizontal = False,
    #         key = "deprecated_layers_include",
    #         disabled = True) #TODO
    
    # with col3:
    #     kos = st.radio(
    #         "Keep obsolete settings?",
    #         ["Yes", "No"],
    #         help = "Whether to keep settings that are excluded by default",
    #         index = 1,
    #         horizontal = False,
    #         key = "obsolete_settings",
    #         disabled = True) #TODO

    st.divider()

    # Change variables based on radio settings
    if exclusion_mode == exclusion_options[0]:
        eal = True
        eml = True
        ial = False
    elif exclusion_mode == exclusion_options[1]:
        eal = False
        eml = True
        ial = False
    elif exclusion_mode == exclusion_options[2]:
        eal = False
        eml = False
        ial = False
    else:
        eal = False
        eml = False
        ial = True

    # if idl == "Yes":
    #     idl = True
    # else:
    #     idl = False

    # if kos == "Yes":
    #     kos = True
    # else:
    #     kos = False
    
    # # TODO Mod support (upload personal .json file to get mod specific LFUT)

    file_col, paste_col = st.columns(2)
    with file_col:
        with st.container(border=True, height=300):
            # --- File Upload Section ---
            st.subheader("Import Config Settings")
            uploaded_settings = st.file_uploader(
                "Upload your existing LayerVoting file [.cfg, .txt]", 
                type=["cfg", "txt"],
                key="file_upload"
            )
            if uploaded_settings is not None:
                try:
                    st.session_state.df = ics.upload_cfg_to_df(uploaded_settings, eml=eml, eal=eal, ial=ial)#, idl=idl)#, kos=kos) TODO
                    st.success("Settings imported successfully from file!")
                except Exception as e:
                    st.error(f"Failed to import settings: {e}")

    with paste_col:
        with st.container(border=True, height=300):
            # --- Manual Paste Section ---
            st.subheader("Paste Config Settings")
            manual_input = st.text_area(
                "Paste the contents of your LayerVoting.cfg file here",
                height=200,
                placeholder="Paste your LayerVoting.cfg contents..."
            )
            if manual_input:
                try:
                    st.session_state.df = ics.upload_cfg_to_df(manual_input, eml=eml, eal=eal, ial=ial)#, idl=idl)#, kos=kos) TODO
                    st.success("Settings imported successfully from pasted input!")
                except Exception as e:
                    st.error(f"Failed to import settings: {e}")

    if st.button("Reset settings", help="Reset settings to default (no exclusions)", key="reset_settings"):
        st.session_state.df = au.empty_LFUT_df
        st.success("Settings reset")

    au.build_bottom_nav(import_page, middle_bool=False)