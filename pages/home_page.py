import streamlit as st
import App_Utils as au

def home_page():
    au.on_page_load()
    st.title("Home")

    # --- Introduction Section ---
    st.markdown(
        """
        Welcome to **Squad LayerVoting Config Manager**!  

        This tool is designed for server owners running **Squad** who want to manage their **LayerVoting.cfg** files more efficiently.  
        It allows you to **visualize your configuration**, make **exclusions for Factions, Units, or Faction–Unit combinations**, and **export your settings** back to the game.
        """
    )

    st.divider()

    # --- How the Tool Works ---
    st.header("How the Tool Works")
    st.markdown(
        """
        - **Required Server Setting:** This tool is only useful for servers that have `MapRotationMode=LayerList_Vote` set in their `Server.cfg` file.  
        - **Exclusions Logic:** By default, all options are available for voting. A **checked box** indicates that a Faction–Unit combination is **excluded** from voting.  
        - **Reference Documentation:** For more details on the LayerVoting system, refer to the official Squad documentation [here](https://docs.google.com/document/d/1rtbh9gA00eTqiPPcU_O228JKhA-rWeiwTQDlKCeDPo0).  
        - **Data Formats:**  
          - **LFUT Tables:** The main data frame (`LFUT.csv`) representing all layers, factions, and units.  
          - **FU Tables:** Simplified views used for per-team exclusion settings (two-dimensional tables showing Faction–Unit combinations).
        """
    )

    st.divider()

    # --- Getting Started ---
    st.header("Getting Started")
    st.markdown(
        """
        You can start either by **starting fresh** or **importing existing settings**.

        **Starting Fresh:**  
        - You start of with all layers included and no exclusions settings applied.  
        - It is recommended to follow the website layout to configure settings in order: [Global Settings](global_page) → [Gamemode Settings](gamemode_page) → [Map Settings](map_page) → [Layer Settings](layer_page).  
        - **Settings Overwrite:** Changing exclusions on a broader scope (e.g., Global) can be overwritten by narrower scopes (e.g., Map or Layer) and vice versa.  

        **Importing Existing Settings:**  
        - If you already have a `LayerVoting.cfg` file with existing exclusions, you can import it at the bottom of this page.  
        - Your existing settings will be coppied so you can make small adjustments on the [Layer Settings](layer_page) page.  
        - Be careful using other pages; changes on broader scopes will overwrite existing settings.
        """
    )

    st.divider()

    # --- Exporting / Downloading ---
    st.header("Exporting or Copying Settings")
    st.markdown(
        """
        - On the **[Download Config](download_page)** page, your current configuration is displayed.  
        - You can export your settings to **`.cfg`** or **`.txt`** formats, or **copy the raw text** for manual pasting into your server configuration.  
        - This allows full flexibility for updating your server without losing any existing LayerVoting settings and the ability to easily share it with others.
        """
    )

    st.divider()

    # --- Data Sources ---
    st.header("Where the Data Comes From")
    st.markdown(
        """
        - The main data frame `LFUT.csv` used by this tool is **generated from a JSON file** provided by [Contributor Name / GitHub Link](#).  
        - This JSON contains all the layer, faction, and unit data.  
        """
    )

    st.divider()

    # --- Open Source / GitHub ---
    st.header("Open Source / GitHub")
    st.markdown(
        """
        - This project is **open source**!  
        - You can view the source code, contribute, or report issues on my GitHub page: [My GitHub Repository](#)  
        - Contributions and feedback are always welcome!
        """
    )

    st.divider()

    # --- Navigation ---
    au.build_bottom_nav(home_page, middle_bool=False)

    