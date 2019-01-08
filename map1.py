import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")

lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

#Create a color for the marker according to vulcano's elevation
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif elevation < 3000:
        return 'orange'
    else:
        return 'red'


map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Mapbox Bright")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html = html % (name, name, el), width = 200, height =
            100)

    #add marker for each vulcano
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(iframe),
        fill_color=color_producer(el), color='grey', fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

#add a background for the world map and fill country according to population
fgp.add_child(folium.GeoJson(
    data=open("world.json", 'r', encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005']
        < 10000000 else 'orange' if x['properties']['POP2005'] < 20000000 else
        'red'}))


map.add_child(fgv)
map.add_child(fgp)

#Enable/Disable layers in map
map.add_child(folium.LayerControl())

map.save("Map1.html")
