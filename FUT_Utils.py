# %%
# --- Importing packages --- #

import pandas as pd

# %%
# --- Helper Functions --- #

def get_FU_list(LFUT_df:pd.DataFrame, team_int:int, filter=None):

    if filter is not None:
        LFUT_filter_df = LFUT_df[LFUT_df.index.str.contains(filter)]
        LFUT_filter_df = LFUT_filter_df.dropna(axis=1, how="all")
        FUT_list = LFUT_filter_df.columns.to_list()[1:]
    else:
        FUT_list = LFUT_df.columns.to_list()[1:]
    
    FU_list = [x for x in FUT_list if x.endswith(f"_{team_int}")]

    return FU_list

def create_empty_FU_df(LFUT_df:pd.DataFrame, team_int:int, filter=None):

    FUT_list = get_FU_list(LFUT_df, team_int, filter)

    factions = list(dict.fromkeys(fut.split("_")[0] for fut in FUT_list))
    units = sorted({fut.split("_")[1] for fut in FUT_list})

    FU_df = pd.DataFrame(index=factions, columns=units)

    for fut in FUT_list:
        faction, unit, _ = fut.split("_")
        FU_df.loc[faction, unit] = False

    return FU_df

def match_exclusions(LFUT_df:pd.DataFrame, team_int:int, filter=None):

    FUT_list = get_FU_list(LFUT_df, team_int, filter)
    FU_df = create_empty_FU_df(LFUT_df, team_int, filter)

    if filter is not None:
        LFUT_filter_df = LFUT_df[LFUT_df.index.str.contains(filter)]
        LFUT_filter_df = LFUT_filter_df.dropna(axis=1, how="all")
        LFUT_filter_df = LFUT_filter_df[FUT_list]
    else:
        LFUT_filter_df = LFUT_df[FUT_list]

    for col in LFUT_filter_df.columns:
        faction, unit, team = col.split("_")
        series = LFUT_filter_df[col].dropna()
        unique_vals = series.unique()

        if len(unique_vals) == 1:
            # Only one unique value
            if unique_vals[0] is True:
                FU_df.loc[faction, unit] = True
            elif unique_vals[0] is False:
                FU_df.loc[faction, unit] = False
        else:
            # Mixed True/False
            FU_df.loc[faction, unit] = "Mixed" #TODO give permanent name

    return FU_df

def implemet_exclusions(LFUT_df:pd.DataFrame, table_df:pd.DataFrame, team_int:int, filter=None):

    FUT_action_s = table_df.stack()
    FUT_action_s.index = [f"{faction}_{unit}_{team_int}" for faction, unit in FUT_action_s.index]

    LFUT_df = apply_FUT_to_df(LFUT_df, FUT_action_s, filter)

    return LFUT_df

def apply_FUT_to_df(LFUT_df:pd.DataFrame, FUT_action_s:pd.Series, filter=None):

    for fut, action in FUT_action_s.items():
        if action in [True, False]:
            if fut in LFUT_df.columns:
                if filter is None:
                    mask = LFUT_df[fut].notna()
                else:
                    mask = LFUT_df[fut].notna() & LFUT_df.index.str.contains(filter)
                LFUT_df.loc[mask, fut] = action

    return LFUT_df

# %%
# --- Table functions (LFUT -> Table) --- #

def LFUT_to_table(active_LFUT_df:pd.DataFrame, filter=None):

    table_team1 = match_exclusions(active_LFUT_df, 1, filter)
    table_team2 = match_exclusions(active_LFUT_df, 2, filter)

    table_team1 = (
        table_team1.replace({None: " "}).infer_objects(copy=False)
    )
    table_team2 = (
        table_team2.replace({None: " "}).infer_objects(copy=False)
    )

    return table_team1, table_team2

# --- Table functions (Table -> LFUT) --- #

def table_to_LFUT(active_LFUT_df:pd.DataFrame, table_team1:pd.DataFrame, table_team2:pd.DataFrame, filter=None):

    active_LFUT_df = implemet_exclusions(active_LFUT_df, table_team1, 1, filter)
    active_LFUT_df = implemet_exclusions(active_LFUT_df, table_team2, 2, filter)

    return active_LFUT_df