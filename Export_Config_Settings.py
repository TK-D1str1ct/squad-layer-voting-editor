# %%
# --- Importing packages --- #

import pandas as pd

# %%
# --- Importing LFUT.csv --- #

LFUT_df = pd.read_csv('LFUT.csv', index_col=0)

#%%
# --- Defining standard header text --- #

HEADER = '''// LAYER_VOTING: These must be Layer_Ids. Those are different from display names! I.e. 'Belaya_AAS_v1' is correct, 'Belaya AAS v1' is not.
// NOTE: this file is used for servers running in MapRotationMode=LayerVote. This setting can be found in your Server.cfg file (make sure to use a fresh one as your basis).
// NOTE: in-line comments will not work in this config until further notice. Comment lines should be in separate lines, if used.
// NOTE: voting gives option to exclude selected faction from voting pool, I.e. 'AlBasrah_AAS_v1|CAF|RGF'. This will exclude CAF from Team 1 choices and RGF from Team2 choices.
// NOTE: Factions should be available on selected layer, also playing with factions from the same alliance is restricted. If possible voting pool will be empty it will use all possible options on selected layer.
'''

# %%
# --- Finding team SPLIT location --- #
teams = pd.Series(LFUT_df.columns[1:]).str.split("_").str[-1].astype(int)
change_mask = (teams.shift() != teams) & (teams == 2)
SPLIT = change_mask[change_mask].index[0]+1

# %%
# --- Creating Funcitons --- #

def config_translate(row:pd.Series, eel:bool):

    # Get layer name
    layer = row.name

    # Check if layer is excluded
    layer_exclude = row['Exclude']
    if layer_exclude and eel:
        return
    
    # Split the series in 2 (one for each team)
    team1_row = row[1:SPLIT]
    team2_row = row[SPLIT:]

    # Retrieve the config strings based on the settings per team
    team1_settings = team_settings(team1_row)
    team2_settings = team_settings(team2_row)

    # Create full config output for current layer
    if team1_settings is not None and team2_settings is None: # layer|exclusions_team1|
        output_string = f"{layer}|{team1_settings}|"
    elif team1_settings is None and team2_settings is not None: # layer||exclusions_team2
        output_string = f"{layer}||{team2_settings}"
    elif team1_settings is not None and team1_settings == team2_settings: # layer|exclsionons_both
        output_string = f"{layer}|{team1_settings}"
    elif team1_settings is not None and team2_settings is not None: # layer|exclusions_team1|exclusions_team2
        output_string = f"{layer}|{team1_settings}|{team2_settings}"
    else:
        output_string = f"{layer}" # layer

    # Comment out the layer if it is excluded
    if layer_exclude:
        output_string = f"// {output_string}"
    
    return output_string

def team_settings(row:pd.Series):
    
    team_settings = ""
    row.dropna(inplace=True)

    # Get updated settings series and lists of factions and units that are fully excluded
    row, factions, units = settings_check(row)

    # Append all the fully excluded factions
    for faction in factions:
        team_settings += faction+" "

    # Append all the fully excluded units
    for unit in units:
        team_settings += "+"+unit+" "

    # Append all the remaining excluded FU combinations
    if row is not None:
        for fut, status in row.items():
            if status:
                fu = fut[:-2].replace("_","+")+" "
                team_settings += fu

    # Format the correct return
    if team_settings == "": # In case nothing is excluded return None
        team_settings = None
    else: # Else remove the final " " to ensure no trailing spaces remain
        team_settings = team_settings[:-1]

    return team_settings

def settings_check(row:pd.Series):

    # Get layer name
    layer = row.name

    # Turn series into df with additional columns that display the faction and unit seperately from the FUT
    layer_df = row.reset_index()
    layer_df[["Faction", "Unit"]] = layer_df["index"].str.rsplit("_", n=2, expand=True).iloc[:, :2]
    layer_df.set_index("index", inplace=True)

    # Create list of all the Factions and Units that are available on current layer and team
    factions = layer_df["Faction"].unique().tolist()
    units = layer_df["Unit"].unique().tolist()

    # Keep only instances where a FUT is not excluded in new df
    layer_false_df = layer_df[layer_df[layer] == False]

    # Create new list of all Factions and Units that are NOT fully excluded
    factions_keep = layer_false_df["Faction"].unique().tolist()
    units_keep = layer_false_df["Unit"].unique().tolist()

    # Update list to only contain factions and units that are fully excluded
    factions = [item for item in factions if item not in factions_keep]
    units = [item for item in units if item not in units_keep]

    # Update df to only display the settings of FUT combinations that are not fully excluded
    layer_df = layer_df[~layer_df["Faction"].isin(factions) & ~layer_df["Unit"].isin(units)]

    return layer_df[layer], factions, units

def format_with_whitelines(config_series: pd.Series):
    lines = []
    prev_map = None

    for idx, val in config_series.dropna().items():
        current_map = idx.split("_")[0]
        if prev_map is not None and current_map != prev_map:
            # Insert a blank line between different maps
            lines.append("")
        lines.append(str(val))
        prev_map = current_map

    return "\n".join(lines)

# %%
# --- Export as string --- #

def download_as_cfg(LFUT_df:pd.DataFrame, eel:bool = False, icet:bool = True, iwl:bool = True):
    config_series = LFUT_df.apply(config_translate, axis=1, args=(eel,)) # Apply config translater to all layers in df
    config_series = config_series.dropna() # Remove empty rows as a consequence of not exporting excluded layers

    if iwl:
        output = format_with_whitelines(config_series)
    else:
        output = "\n".join(config_series.astype(str))

    output = f"// This LayerVoting.cfg was generated using https://squad-voting-config.streamlit.app/\n\n{output}"

    if icet:
        output = f"{HEADER}\n{output}"

    return output
