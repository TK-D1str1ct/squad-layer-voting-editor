# Squad Layer Voting Editor

A project intended to simplify creation and editing of Squad voting pool configurations for server admins.

## Terminology

This project uses a compact acronym system to describe how voting data is stored and edited. These acronyms appear in code, comments, CSV data, and the UI.

- `LFUT` = `Layer/Faction/Unit/Team`
- `FUT` = `Faction/Unit/Team`
- `FU` = `Faction/Unit`

### How to read the data model

- An `FU` pair describes a faction and unit without a team attached yet, for example `BAF_Mech`.
- A `FUT` triplet describes one selectable team-side option on a layer, for example `BAF_Mech_1`.
- `LFUT` is the full voting matrix used by the app:
  - rows are `L` values, meaning layer IDs such as `Belaya_AAS_v1`
  - columns are `FUT` values such as `BAF_Mech_1`
  - cell values are booleans indicating whether that `FUT` option is excluded on that `L`
- The special `Exclude` column in `LFUT.csv` stores whole-layer exclusion state independently from the per-`FUT` columns.

## Local setup

Dependencies and project metadata handled by [uv](https://github.com/astral-sh/uv)

Run the following commands to install deps and run the server for local development

```sh
# Install dependencies
uv sync

# Run server locally
uv run streamlit run app.py
```

A Taskfile.yml with common local tasks is also included.  See <https://taskfile.dev/> for documentation on installation/usage.
