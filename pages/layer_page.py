import streamlit as st
import App_Utils as au

def layer_page():
    au.on_page_load()

    st.title("📑 Layer Exclusion Settings")
    st.write("Exclude specific Faction–Unit–Team combinations from individual layers.")

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
              
            Additionally you can use the 'Exclude' column to exclude an entire layer as a voting option.  

            Copy-Pasting between cells is possible.
            """,
            unsafe_allow_html=True
        )

    # --- Apply filters ---
    df_filtered = au.apply_filters(st.session_state.df.copy(), row_filter_input, row_filter_mode, axis="rows") #TODO something does not work properly here. Most likely as a result of teh apply_filters function
    df_filtered = au.apply_filters(df_filtered, col_filter_input, col_filter_mode, axis="cols")
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

    au.build_bottom_nav(layer_page, df=edited_df)
