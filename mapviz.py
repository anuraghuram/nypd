# -----------------------
# Filename: mapviz.py
# Author: Anu R
# Created: May 2020
# Python version: 3.7
# -----------------------

import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
import cleaning

# -------------------
# Data prep
# -------------------

# Import cleaned nypd df
df = pd.read_csv('NYPD_Complaint_Data_Historic_Clean.csv')

# Select random sample (clean df = ~600k obs) to reduce runtime
df = df.sample(n=10000)

# Import borough boundary data
geo_data = 'Borough Boundaries.geojson'

# Format NYPD data borough names so they are consistent with the geojson. This is necessary for creating the choropleths
nypd_boro_names = ['BROOKLYN', 'BRONX', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']
geojson_boro_names = ['Brooklyn', 'Bronx', 'Manhattan', 'Queens', 'Staten Island']

# Reassign with bucketed offense categories
for i in range(0, len(nypd_boro_names)):
    df['BORO_NM'] = df['BORO_NM'].apply(lambda x: geojson_boro_names[i] if x in nypd_boro_names[i] else x)

# Create relevant cross-tabs to produce timeseries choropleth
#   1. borough x offense type
boro_ofns_type = pd.crosstab(df['BORO_NM'], df['OFNS_DESC']).reset_index()
boro_ofns_type.sort_index(axis=1)
boro_ofns_type['TOTAL'] = boro_ofns_type.iloc[:, 1:7].sum(axis=1)
boro_ofns_type.iloc[:, 1:7] = boro_ofns_type.iloc[:, 1:7].apply(lambda x: x/boro_ofns_type['TOTAL']*100).astype(float).round(1)
boro_ofns_type = boro_ofns_type.drop('TOTAL', axis=1)

#   2. borough x crime location
boro_ofns_loc = pd.crosstab(df['BORO_NM'], df['PREM_TYP_DESC']).reset_index()
boro_ofns_loc.sort_index(axis=1)
boro_ofns_loc['TOTAL'] = boro_ofns_loc.iloc[:, 1:7].sum(axis=1)
boro_ofns_loc.iloc[:, 1:7] = boro_ofns_loc.iloc[:, 1:7].apply(lambda x: x/boro_ofns_loc['TOTAL']*100).astype(float).round(1)
boro_ofns_loc = boro_ofns_loc.drop('TOTAL', axis=1)

# --------------------------
# Creating the snapshot map
# --------------------------

# Set coordinates for NYC metro area
nyc_coordinates = [40.7128, -74.0060]

# Create the base map
crime_map = folium.Map(location=nyc_coordinates,
                       tiles='CartoDB positron',
                       name="Base map",
                       zoom_start=12)

# Create choropleth of borough x offense type
for crime in cleaning.ofns_cats:
    folium.Choropleth(geo_data=geo_data,
                      data=boro_ofns_type,
                      columns=['BORO_NM', crime],
                      key_on='feature.properties.boro_name',
                      fill_color='YlOrRd',
                      fill_opacity=0.4,
                      line_opacity=0.3,
                      legend_name=crime + ' CRIMES (%)',
                      name='CRIME TYPE: ' + crime,
                      highlight=True,
                      show=False).add_to(crime_map)

# Create choropleth of borough x crime location
for crime_loc in cleaning.loc_cats:
    folium.Choropleth(geo_data=geo_data,
                      data=boro_ofns_loc,
                      columns=['BORO_NM', crime_loc],
                      key_on='feature.properties.boro_name',
                      fill_color='YlOrRd',
                      fill_opacity=0.4,
                      line_opacity=0.3,
                      legend_name=crime_loc + '' + ' CRIMES (%)',
                      name='CRIME LOCATION: ' + crime_loc,
                      highlight=True,
                      show=False).add_to(crime_map)

# Add clusters to show density of each crime type by borough
# To do that, format cols containing latitude and longitude coordinates from the nypd clean data
df.iloc[:, [27, 28]].replace(' ', np.nan, inplace=True)
df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
df['Latitude'] = df['Latitude'].astype(float).round(7)
df['Longitude'] = df['Longitude'].astype(float).round(7)

# Then iterate over each crime type
for crime in cleaning.ofns_cats:
    crime_df = df[df['OFNS_DESC'] == crime]
    lat_lon = crime_df[['Latitude', 'Longitude']]
    locations = lat_lon.values.tolist()

    # Then use these location points to create the clusters
    mc = MarkerCluster().add_to(crime_map)

    for point in range(0, len(locations)):
        folium.Marker(locations[point],
                      popup=crime,
                      show=False).add_to(mc)

# Add layer toggles for both the cross tabs and cluster options
folium.LayerControl().add_to(crime_map)

# Write out to HTML
output_file = "crime_map.html"
crime_map.save(output_file)
