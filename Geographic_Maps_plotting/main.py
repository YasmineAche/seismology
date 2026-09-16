import pandas as pd
import pygmt
import datetime
import geopandas as gpd
from pygmt.params import Position
from shapely.geometry import Polygon

"""
    Generate a detailed map of North Algeria with various elements and annotations.

    This script uses the PyGMT library to create a map that includes coastlines, borders, 
    country names, sea names, station locations, a legend, and more. It also adds information
    about Wilayas and stations in Algeria. The map is then saved as an image file.

    Usage:
    - Run the script to generate the map.
    - The generated map is saved as 'Réseau National daccélérographes.png' in the current directory.

    Prerequisites:
    - Ensure that the required Python libraries, including Pandas, PyGMT, Geopandas, and Shapely, are installed.
    - Prepare two Excel files ('ETNA2.xlsx' and 'ETNA.xlsx') with station data. 
      These files should be located in the directory '/Users/user/Desktop/programs_of_the_graphical_interface/'.

    Elements and Annotations:
    - The map includes the following elements:
        - Coastlines with specified attributes.
        - National borders.
        - Highlighted map of Algeria.
        - Rivers, lakes, and frames.
        - A title for the map.
        - A north arrow (rose) indicating directions.
        - Wilayas (administrative divisions) displayed with their names.
        - Additional text annotations for Algeria, Morocco, Tunisia, and the Mediterranean Sea.
        - Plotting of stations with symbols and colors.
        - A legend indicating map scale, station keys, and a map of Algeria within the world map.
        - A scale bar for reference.
        - The script also adds a version number and a logo.

    Map Region:
    - The map region is defined by specifying 'xmin', 'xmax', 'ymin', and 'ymax' coordinates.
    - You can adjust these values to focus on a specific geographic area.

    Example:
    To generate the map, run the script. The resulting map image will be saved in the current directory.

    Author: [Yasmine ACHEMINE]
    Date: [June 5, 2023]
"""

# Reading Excel files + creation of a data frames
data_frame_stations_a = pd.DataFrame(data=pd.read_excel("stations_type_A.xlsx"))
data_frame_stations_b = pd.DataFrame(data=pd.read_excel("stations_type_B.xlsx"))
print("Reading excel files and creation of a data frames complete")


def create_stations_map():
    """
    Create a map of North Algeria with various elements and annotations.

    - Creates a map of North Algeria with a title.
    - Plots stations.
    - Adds a north arrow, country names, sea names, date of creation, and a logo.
    - Adds a legend that contains a map scale, keys (symbol, types, numbers of stations),
      and a map of the world with Algeria highlighted.

    Parameters:
    None

    Returns:
    None
    """
    xmin, xmax, ymin, ymax = [-2.6, 9, 32, 38]
    region = [xmin, xmax, ymin, ymax]

    fig = pygmt.Figure()

    # Plot the coastlines and other features
    fig.coast(
        region=region,
        projection="M10c",
        shorelines="0.5,black",  # Coastlines are 0.5 mm thick
        resolution="f",  # f for full resolution of the coastline
        borders="1/0.5p,black",  # Draw national borders with a 1-point black line
        land="LIGHTYELLOW3",
        dcw="DZ+gLIGHTYELLOW1",  # Color Algeria in different color
        water="LIGHTSKYBLUE1",
        rivers=[
            "a/0.2p,LIGHTSKYBLUE1,solid"
        ],  # a:all rivers and canals, r:all permanent rivers
        lakes="skyblue",
        frame=["a2f1"],  # plot frame and title , f:frame, a:annotation, g:grid)
        Td='jTL+o1.5c+w0.5c+lO,E,S,N+o-0.1c/3c', #north arrow
    )
    ######### Title #############
    fig.basemap(frame=["+tTitle Of The Map"])
    print("Adding title complete")

    ########### Adding Wilayas ###############
    # Path to the shape file
    map_file = "Shapefiles_69_wilayas_cleaned/wilayas.shp"

    # Read and plot the wilayas
    wilaya_df = gpd.read_file(filename=map_file)
    fig.plot(data=wilaya_df, pen="IVORY3")
    print("Plotting of wilayas complete")

    ############ Adding wilaya names #################
    # Extract information about Wilayas
    wilaya_name = []
    for index, row in wilaya_df.iterrows():
        wilaya_name.append(
            {
                "name": row["name_fr"],
                "center": row["geometry"].centroid,
                "Geometry": row["geometry"],
            }
        )

    frame_region = Polygon([(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)])

    for i in range(len(wilaya_df)):
        if wilaya_name[i]["Geometry"].intersects(
            frame_region
        ) and frame_region.contains(wilaya_name[i]["center"]):
            fig.text(
                text=wilaya_name[i]["name"],
                x=wilaya_name[i]["center"].x,
                y=wilaya_name[i]["center"].y,
                font="2.5p,NewCenturySchlbk-Italic",  # ,LIGHTGOLDENROD4
                no_clip=True,
            )
    print("Adding wilaya names complete")

    ####### plot country borders ###########
    # dissolve wilayas to a single country polygon
    country_border = wilaya_df.dissolve()

    # Extract all exterior coordinates
    border_coords_list = []
    geom = country_border.geometry.iloc[0]
    if geom.geom_type == "Polygon":
        border_coords_list.append(list(geom.exterior.coords))
    elif geom.geom_type == "MultiPolygon":
        for poly in geom.geoms:
            border_coords_list.append(list(poly.exterior.coords))

    # Plot
    for border_coords in border_coords_list:
        fig.plot(x=[c[0] for c in border_coords],
                 y=[c[1] for c in border_coords],
                 pen="0.5p,black")
    print("Adding country border complete")

    ########### Plot text annotations #############
    fig.text(text="Algeria", x=3, y=33, font="12p,Bookman-Demi,black")
    fig.text(text="Morocco", x=-2.1, y=34, angle=90, font="7p,Bookman-Demi,black")
    fig.text(text="Tunisia", x=8.6, y=34.3, angle=-90, font="7p,Bookman-Demi,black")
    fig.text(
        text="Mediterranean sea",
        x=2.3,
        y=37.4,
        angle=10,
        font="8p,ZapfChancery-MediumItalic,black",
    )
    print("Adding other countries' names complete")

    ########## PLOT STATIONS #####################
    number_of_stations_a = len(data_frame_stations_a)  # Calculate number of stations
    fig.plot(
        x=data_frame_stations_a.LONG,
        y=data_frame_stations_a.LAT,
        style="i0.15c",
        fill="red",
        pen="gray",
        label=f"{number_of_stations_a} Station A",
    )

    number_of_stations_b = len(data_frame_stations_b)  # Calculate number of stations
    fig.plot(
        x=data_frame_stations_b.LONG,
        y=data_frame_stations_b.LAT,
        style="i0.15c",
        fill="green",
        pen="gray",
        label=f"{number_of_stations_b} Station B",
    )
    print("Plotting stations complete")
    ########### legend and Scale bar #############
    # adjust font size only for legend and scale bar
    with pygmt.config(FONT_ANNOT_PRIMARY="6p"):
        fig.legend(position="g-2.59/36.78+w1.8/1.3", box="+gwhite+p1p+i", scale=1.3)

    # scale bar
    # f: fancy scale (without +f a simple one line scale)
    # +u:add distance unit +l:add scale title (+ab to locate it b bottom, r right...)
    with pygmt.config(FONT_ANNOT_PRIMARY="4p", MAP_SCALE_HEIGHT="2p"):
        #fig.basemap(map_scale="jBR+o9.2c/0.3c+w50k+f+u")  # scale bar
        fig.scalebar(
            position=Position((-1.95, 37.2), cstype="mapcoords"),
            length="50k",
            unit=True,
            fancy=True,
        )
    print("Adding legend and scale bar complete")

    ########### Version ################
    date = datetime.datetime.now()
    fig.text(
        text=f"v.{date.strftime('%d')}/{date.strftime('%m')}/{date.strftime('%Y')}",
        x=8.15,
        y=37.9,
        angle=0,
        font="3p,Bookman-Demi,black",
    )
    print("Adding version complete")

    ########### logo #############
    fig.image(
        imagefile="logo.png",
        position="jTR+o0.1c/0.1c+w1c",
        box=False,
    )
    print("Adding logo complete")

    ########### Inset #############
    # Create an inset
    with fig.inset(position="g-1.32/36.78+w0.5c+o0.1c", clearance=0, box="+p1p,gold"):
        # Create a figure in the inset using coast.
        fig.coast(
            region="g",
            projection="G10/20/?",
            land="gray",
            water="white",
            dcw="DZ+gred3",
        )
    print("Adding insert complete")

    ########### Show and save map #############
    fig.savefig("my map.png", dpi=600)
    fig.show()
    print("Map created and saved successfully")

if __name__ == "__main__":
    create_stations_map()
