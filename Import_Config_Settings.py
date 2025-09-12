# %%
# --- Importing packages --- #

import pandas as pd

# %%
# --- Creating Funcitons --- #

def config_to_dict(settings_list:list):

    # Create empty dict
    config_dict = {}

    # For loop over all layers in config file
    for layer in settings_list:
        excluded_layer = layer.startswith("//") # Check if the layer is excluded
        if excluded_layer:
            layer = layer.lstrip("//").strip() # If it is excluded strip away the "// " TODO make sure it works without space or maybe not

        parts = layer.split("|") # Split the config line into the different exclusion parts based on the "|"
        layer_name = parts[0].strip() # Get layer name as the first part of the split
        team1, team2 = [], []   # Create empty lists for the exclusions for team 1 and 2

        if len(parts) == 1: # If only layer name is given --> pass
            pass
        elif len(parts) == 2: # If there is only 1 '|' separator: layer|exclsionons_both
            excl = parts[1].split()
            if parts[1] == "": # Redundancy check in case there is no exclusions provided
                pass
            else:
                team1, team2 = excl, excl
        elif len(parts) == 3: # If there is 2 '|' separators
            if parts[1] and not parts[2]: # If the separators have an exclusions in between but not after the last separator: layer|exclusion_team1|
                team1 = parts[1].split()
            elif not parts[1] and parts[2]: # If the separators dont have an exclusions in between but do after the last separator: layer||exclusion_team2
                team2 = parts[2].split()
            else: # If the separators have an exclusion in between and after the last separator: layer|exclusions_team1|exclusions_team2
                team1 = parts[1].split()
                team2 = parts[2].split()

        # Add the exclusions to the dictionary
        config_dict[layer_name] = {
            "Exclude": excluded_layer,
            "team1": team1,
            "team2": team2
        }

    return config_dict

def apply_config_settings(row:pd.Series, config_dict:dict, missing_layers:list):

    # Get layer name
    layer = row.name
    layer_settings = row.copy()

    # Find the layer in the config_dict
    layer_config_settings = config_dict.get(layer)

    if layer_config_settings is None: # Check if the layer exists in the .cfg file
        missing_layers.append(layer) # If the layer does not exist it will be added to a warning list and no exclusions at all will be implemented
    else:
        layer_settings['Exclude'] = layer_config_settings['Exclude']
        layer_settings = get_config_settings(layer_settings, layer_config_settings['team1'], 1)
        layer_settings = get_config_settings(layer_settings, layer_config_settings['team2'], 2)

    return layer_settings
    
def get_config_settings(layer_settings:pd.Series, team_config_settings:list, team:int):

    for exclusions in team_config_settings:
        exclusions = exclusions.strip()
        if not exclusions:
            continue

        if exclusions.startswith("+"):
            unit = exclusions
            mask = layer_settings.index.str.contains(f"_{unit}_") & layer_settings.index.str.contains(f"_{team}") & layer_settings.notna()
            layer_settings[mask] = True

        elif "+" in exclusions:
            faction, unit = exclusions.split("+", 1)
            mask = layer_settings.index.str.startswith(f"{faction}_{unit}") & layer_settings.index.str.contains(f"_{team}") & layer_settings.notna()
            layer_settings[mask] = True

        else:
            faction = exclusions
            mask = layer_settings.index.str.startswith(f"{faction}_") & layer_settings.index.str.contains(f"_{team}") & layer_settings.notna()
            layer_settings[mask] = True

    return layer_settings

# %%
# --- Import cfg file --- #

def upload_as_csv(cfg_file):

    missing_layers = []
    LFUT_empty_df = pd.read_csv('LFUT.csv', index_col=0)

    with open(cfg_file) as f:
        settings_list = [line.strip() for line in f if line.strip()]
    
    LFUT_import_df = LFUT_empty_df.apply(apply_config_settings, axis=1, args=(config_to_dict(settings_list),missing_layers,))

    return LFUT_import_df