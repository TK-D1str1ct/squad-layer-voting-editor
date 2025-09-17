import streamlit as st
import App_Utils as au
import Import_Config_Settings as ics

def import_page():
    au.on_page_load()
    # --- Side-by-side Upload & Paste ---
    # st.subheader("Import settings:")

    # st.radio("Exclude missing layers?", ["Yes", "No"], index=0, horizontal=True, help="Whether to pre-set a layer as excluded if it is not found in your config settings.", key="missing_layers_exclude") #TODO
    # st.radio("Keep obsolete settings?", ["Yes", "No"], index=1, horizontal=True, help="Whether to keep settings that are excluded by default", key="obsolete_settings") #TODO (in future version)
    # # TODO Mod support (upload personal .json file to get mod specific LFUT)

    file_col, paste_col = st.columns(2)

    with file_col:
        # --- File Upload Section ---
        st.subheader("Import from File")
        uploaded_settings = st.file_uploader(
            "Upload your existing LayerVoting file [.cfg, .txt]", 
            type=["cfg", "txt"],
            key="file_upload"
        )
        if uploaded_settings is not None:
            try:
                st.session_state.df = ics.upload_cfg_to_df(uploaded_settings)
                st.success("Settings imported successfully from file!")
            except Exception as e:
                st.error(f"Failed to import settings: {e}")

    with paste_col:
        # --- Manual Paste Section ---
        st.subheader("Or Paste Settings Manually")
        manual_input = st.text_area(
            "Paste the contents of your LayerVoting file here",
            height=200,
            placeholder="Paste your LayerVoting.cfg contents..."
        )
        if manual_input:
            try:
                st.session_state.df = ics.upload_cfg_to_df(manual_input)
                st.success("Settings imported successfully from pasted input!")
            except Exception as e:
                st.error(f"Failed to import settings: {e}")

    # if st.button("Reset settings", help="Reset settings to default (no exclusions)", key="reset_settings"):
    #     st.session_state.df = empty_LFUT_df #TODO
    #     st.success("Settings reset")

    st.divider()

    au.build_bottom_nav(import_page, middle_bool=False)