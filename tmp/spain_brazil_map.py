import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Create figure
fig = plt.figure(figsize=(12, 6))
m = Basemap(projection='cyl', resolution='l')

# Draw features
m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='lightblue')
m.fillcontinents(color='lightgreen', lake_color='lightblue')
m.drawparallels(range(-90, 91, 30), labels=[1,0,0,0])
m.drawmeridians(range(-180, 181, 60), labels=[0,0,0,1])

# Coordinates: Madrid and Brasília
lon_spain, lat_spain = -3.7038, 40.4168
lon_brazil, lat_brazil = -47.9292, -15.7801

# Plot points
m.plot(lon_spain, lat_spain, 'ro', markersize=8)
plt.text(lon_spain + 3, lat_spain, 'SPAIN', fontsize=12, weight='bold', color='darkred')

m.plot(lon_brazil, lat_brazil, 'bo', markersize=8)
plt.text(lon_brazil + 3, lat_brazil, 'BRAZIL', fontsize=12, weight='bold', color='darkblue')

# Draw flight path (great circle)
m.drawgreatcircle(lon_spain, lat_spain, lon_brazil, lat_brazil, linewidth=2, color='black', linestyle='--')

# Add airplane emoji (rough midpoint)
mid_lon = (lon_spain + lon_brazil) / 2
mid_lat = (lat_spain + lat_brazil) / 2 + 5
plt.text(mid_lon, mid_lat, '✈️', fontsize=20, ha='center')

# Title
plt.title("Educational Map: Flight from Spain to Brazil", fontsize=14, weight='bold')

# Save image
map_path = "/mnt/data/spain_brazil_map_fallback.png"
plt.savefig(map_path, bbox_inches='tight')
plt.show()

map_path