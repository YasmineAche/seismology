# Geographic Maps Plotting

Python project for generating a high-resolution geographic map of the Algerian accelerograph network using **PyGMT**, **Pandas**, **GeoPandas**, and **Shapely**.

The script combines station information from Excel spreadsheets with a 69-wilaya Algerian administrative boundary shapefile and produces a publication-ready PNG map containing the station network, administrative boundaries, geographic annotations, legend, scale bar, logo, and a world-map inset locating Algeria.

## Overview

The main program is `main.py`.

It currently generates a map covering northern Algeria, approximately:

- Longitude: **-2.6° to 9°**
- Latitude: **32° to 38°**

The map displays two station categories:

- **Station A** — plotted as an orange/red inverted triangle.
- **Station B** — plotted as a green inverted triangle.

The station locations are read from the two Excel files included in this directory.

## Features

The map-generation script includes:

- North Algeria geographic background
- National and administrative boundaries
- 69 Algerian wilayas
- Wilaya names
- Station locations for two station types
- Station counts in the legend
- North arrow
- Scale bar
- Country and sea labels
- Algeria highlighted in the geographic context
- Logo
- Map version/date
- World-map inset with Algeria highlighted
- High-resolution PNG output at **600 DPI**

## Project Structure

```text
Geographic_Maps_plotting/
│
├── main.py
├── stations_type_A.xlsx
├── stations_type_B.xlsx
├── logo.png
├── my map.png
├── Readme.md
│
└── Shapefiles_69_wilayas_cleaned/
    ├── wilayas.shp
    ├── wilayas.shx
    ├── wilayas.dbf
    ├── wilayas.prj
    └── wilayas.cpg
```

### `main.py`

The main Python script responsible for the complete map-generation workflow.

The workflow is:

```text
Excel station data
        │
        ▼
Pandas DataFrames
        │
        ▼
PyGMT map initialization
        │
        ├── Coastlines / water / land
        ├── National borders
        ├── Wilaya boundaries
        ├── Wilaya names
        ├── Geographic annotations
        ├── Station A
        ├── Station B
        ├── Legend
        ├── Scale bar
        ├── Version/date
        ├── Logo
        └── World-map inset
        │
        ▼
High-resolution PNG
```

### `stations_type_A.xlsx`

Contains the coordinates and basic information for Type A stations.

Expected columns:

| Column | Description |
|---|---|
| `Type` | Station type |
| `ID` | Station identifier |
| `Wilaya` | Wilaya where the station is located |
| `LAT` | Latitude in decimal degrees |
| `LONG` | Longitude in decimal degrees |

### `stations_type_B.xlsx`

Contains the same type of information for Type B stations.

Expected columns:

| Column | Description |
|---|---|
| `Type` | Station type |
| `ID` | Station identifier |
| `Wilaya` | Wilaya where the station is located |
| `LAT` | Latitude in decimal degrees |
| `LONG` | Longitude in decimal degrees |

### `Shapefiles_69_wilayas_cleaned/`

Contains the cleaned administrative shapefile used to draw the 69 Algerian wilayas.

The shapefile contains:

- `name_fr` — French wilaya name
- `name_en` — English wilaya name
- `name_ar` — Arabic wilaya name
- `Code` — Wilaya code
- `geometry` — geographic polygon

The shapefile uses **WGS 84 / EPSG:4326** geographic coordinates.

The five files (`.shp`, `.shx`, `.dbf`, `.prj`, and `.cpg`) must remain together for the shapefile to work correctly.

### `logo.png`

Logo used on the generated map.

### `my map.png`

Example/generated map output included with the project.

## Requirements

The project requires Python and the following Python packages:

- `pandas`
- `pygmt`
- `geopandas`
- `shapely`

The Python standard library modules `datetime` and `pathlib` are not required as separate installations.

### GMT

PyGMT is a Python interface to the Generic Mapping Tools (**GMT**). A GMT installation is therefore required in addition to the Python package.

For PyGMT, using a Conda environment is generally convenient because it can install the GMT dependency together with the required geospatial packages.

## Installation

### Using Conda

Create a dedicated environment:

```bash
conda create -n geographic_maps python=3.12
conda activate geographic_maps
```

Install the required packages:

```bash
conda install -c conda-forge pygmt geopandas pandas shapely
```

Check the PyGMT installation:

```bash
python -c "import pygmt; print(pygmt.__version__)"
```

### Using an existing Python environment

If GMT is already installed and configured on the system, install the Python packages with:

```bash
pip install pandas geopandas shapely pygmt
```

PyGMT may require additional GMT configuration depending on the operating system.

## Running the Project

Open a terminal in the `Geographic_Maps_plotting` directory and run:

```bash
python main.py
```

Or run `main.py` directly from an IDE such as PyCharm.

The script reads:

```text
stations_type_A.xlsx
stations_type_B.xlsx
logo.png
Shapefiles_69_wilayas_cleaned/wilayas.shp
```

and creates:

```text
my map.png
```

The output is saved at **600 DPI**.

## Station Data Format

Station coordinates must be provided as decimal degrees.

For example:

```text
Type    ID      Wilaya       LAT     LONG
A       ID-1    Ain Defla     36.3    2.1
A       ID-2    Alger         36.6    3.0
```

Use a **decimal point (`.`)** for coordinates rather than a decimal comma.

For example:

```text
36.3
```

not:

```text
36,3
```

The column names used by the current script must remain:

```text
Type
ID
Wilaya
LAT
LONG
```

## Modifying the Map Region

The geographic extent is defined near the beginning of `create_stations_map()`:

```python
xmin, xmax, ymin, ymax = [-2.6, 9, 32, 38]
```

The values correspond to:

```text
xmin = minimum longitude
xmax = maximum longitude
ymin = minimum latitude
ymax = maximum latitude
```

For example:

```python
xmin, xmax, ymin, ymax = [-5, 12, 30, 38]
```

would create a wider geographic extent.

The projection is currently:

```python
projection="M10c"
```

which uses a Mercator projection with a 10 cm map width.

## Adding or Updating Stations

To update the network displayed on the map, modify the appropriate Excel file.

The script automatically calculates the number of stations in each file:

```python
number_of_stations_a = len(data_frame_stations_a)
number_of_stations_b = len(data_frame_stations_b)
```

These numbers are then used in the legend.

No changes to `main.py` are required when only station coordinates or station information are updated, provided that the Excel structure remains unchanged.

## Wilaya Boundaries

The project uses a cleaned 69-wilaya shapefile.

The boundaries are plotted with:

```python
fig.plot(data=wilaya_df, pen="IVORY3")
```

Wilaya names are extracted from the `name_fr` field and positioned using the centroid of each geometry.

The national border is subsequently generated by dissolving the individual wilaya polygons into a single geometry.

## World-Map Inset

The map contains a small geographic inset showing the world and highlighting Algeria:

```python
with fig.inset(...):
    fig.coast(
        region="g",
        projection="G10/20/?",
        land="gray",
        water="white",
        dcw="DZ+gred3",
    )
```

This provides geographic context for the main map of northern Algeria.

## Output

The main output is:

```text
my map.png
```

The image is generated at:

```python
fig.savefig("my map.png", dpi=600)
```

A 600 DPI output is appropriate when the map is intended for high-resolution documents, reports, or presentations.

## Customization

Several visual elements can be modified directly in `main.py`, including:

### Station symbols

The current station symbols are created with:

```python
style="i0.15c"
```

The fill and legend labels can be changed independently for each station type.

### Wilaya labels

Wilaya names are generated from:

```python
row["name_fr"]
```

The font size and font family can be changed in the `fig.text()` call.

### Geographic annotations

The positions and styles of labels such as:

- Algeria
- Morocco
- Tunisia
- Mediterranean Sea

are explicitly defined in `main.py` and can be adjusted according to the map extent.

### Logo

The logo is loaded from:

```python
logo.png
```

Its position and size can be modified in the `fig.image()` call.

## Notes

### Relative paths

The current script uses relative paths. Therefore, run the script from the `Geographic_Maps_plotting` directory, or make sure the working directory configured in your IDE points to this directory.

For example:

```text
Geographic_Maps_plotting/
    main.py
    logo.png
    stations_type_A.xlsx
    stations_type_B.xlsx
```

### PyGMT version

The script was developed with PyGMT and may require adjustments when used with newer versions because PyGMT periodically deprecates older GMT/PyGMT parameters.

For example, newer PyGMT versions may issue warnings for older scale-bar or legend syntax. These warnings should be reviewed when upgrading the environment.

## Possible Future Improvements

Potential improvements to the project include:

- Moving file paths into a configuration file
- Adding command-line arguments for the input files and output name
- Automatically validating station coordinates
- Validating that all required Excel columns exist before plotting
- Adding interactive station information
- Adding station IDs or wilaya names as optional labels
- Separating map configuration from data processing
- Adding automated tests for input data
- Exporting additional formats such as PDF or SVG
- Supporting different geographic regions through configuration rather than editing the source code

## Author

**Yasmine ACHEMINE**

Original project date: **June 2023**

## License

No license file is currently included in this directory. If this project is intended to be reused or distributed publicly, add an appropriate `LICENSE` file to the repository.
