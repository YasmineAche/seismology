import pandas as pd
import pygmt
import datetime
import geopandas as gpd
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


def create_accelerograph_map():
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
        #     Td='jTL+o1.1c+w0.8c+lO,E,S,N+o-0.1c/3c', #north arrow             ################# This or
    )
    ######### Title #############
    fig.basemap(frame=["+tRéseau National Algérien d'Accélérographes"])

    #fig.directional_rose('jTL+o1c+w0.5c+f2+l"W,E,S,N"')  # North arrow (rose)        ################# This

    ########### Adding Wilayas ###############
    # Path to the shape file
    map_file = "Shapefiles_69_wilayas_cleaned/wilayas.shp"

    # Read the shp file
    wilaya_df = gpd.read_file(filename=map_file)

    # Plot the Wilayas
    fig.plot(data=wilaya_df, pen="IVORY3")

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

    ########### Plot text annotations #############
    fig.text(text="Algérie", x=3, y=33, font="12p,Bookman-Demi,black")
    fig.text(text="Maroc", x=-2.1, y=34, angle=90, font="7p,Bookman-Demi,black")
    fig.text(text="Tunisie", x=8.6, y=34.3, angle=-90, font="7p,Bookman-Demi,black")
    fig.text(
        text="Mer méditerranée",
        x=2.3,
        y=37.4,
        angle=10,
        font="8p,ZapfChancery-MediumItalic,black",
    )

    ########## PLOT STATIONS #####################
    nombre_etna2 = len(data_frame_stations_a)  # Calculate number of stations
    fig.plot(
        x=data_frame_stations_a.LONG,
        y=data_frame_stations_a.LAT,
        style="i0.15c",
        fill="red",
        pen="gray",
        label=f"{nombre_etna2} ETNA-2",
    )

    nombre_etna = len(data_frame_stations_b)  # Calculate number of stations
    fig.plot(
        x=data_frame_stations_b.LONG,
        y=data_frame_stations_b.LAT,
        style="i0.15c",
        fill="green",
        pen="gray",
        label=f"{nombre_etna} ETNA",
    )

    ########### legend and Scale bar #############
    # adjust font size only for legend and scale bar
    with pygmt.config(FONT_ANNOT_PRIMARY="6p"):
        fig.legend(position="g-2.59/32.025+w1.8/1.3", box="+gwhite+p1p+i", S=1.3)

    # scale bar
    # f: fancy scale (without +f a simple one line scale)
    # +u:add distance unit +l:add scale title (+ab to locate it b bottom, r right...)
    with pygmt.config(FONT_ANNOT_PRIMARY="4p"):
        fig.basemap(map_scale="jBR+o9.2c/0.3c+w50k+f+u")  # scale bar

    ########### Version ################
    date = datetime.datetime.now()
    fig.text(
        text=f"v.{date.strftime('%d')}/{date.strftime('%m')}/{date.strftime('%Y')}",
        x=8.15,
        y=37.9,
        angle=0,
        font="3p,Bookman-Demi,black",
    )

    ########### logo #############
    fig.image(
        imagefile="CGS_logo.png",
        position="jTR+o0.1c/0.2c+w1c",
        box=False,
    )

    ########### Inset #############
    # Create an inset
    with fig.inset(position="g-1.32/32.025+w0.5c+o0.1c", clearance=0, box="+p1p,gold"):
        # Create a figure in the inset using coast.
        fig.coast(
            region="g",
            projection="G10/20/?",
            land="gray",
            water="white",
            dcw="DZ+gred3",
        )

    fig.show()

    fig.savefig("Réseau National d'accélérographe.png", dpi=600)

if __name__ == "__main__":
    create_accelerograph_map()
