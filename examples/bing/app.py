from flask import Flask, render_template, request, jsonify
import folium
from geopy.distance import geodesic
import networkx as nx

app = Flask(__name__)

# Define cities and airports with their coordinates
locations = {
    "Chennai": (13.0827, 80.2707),
    "MAA": (12.9941, 80.1709),  # Chennai Airport
    "Delhi": (28.6139, 77.2090),
    "DEL": (28.5562, 77.1000),  # Delhi Airport
    "Bangalore": (12.9716, 77.5946),
    "BLR": (13.1986, 77.7066),  # Bangalore Airport
    "Mumbai": (19.0760, 72.8777),
    "BOM": (19.0896, 72.8656),  # Mumbai Airport
    "Hyderabad": (17.3850, 78.4867),
    "HYD": (17.2403, 78.4294),  # Hyderabad Airport
    "Kolkata": (22.5726, 88.3639),
    "CCU": (22.6540, 88.4467),  # Kolkata Airport
    "Nagpur": (21.1458, 79.0882),
    "NAG": (21.0922, 79.0472),  # Nagpur Airport
    "Ahmedabad": (23.0225, 72.5714),
    "AMD": (23.0722, 72.6347),  # Ahmedabad Airport
    "Jaipur": (26.9124, 75.7873),
    "JAI": (26.8288, 75.8056),  # Jaipur Airport
    "Bhopal": (23.2599, 77.4126),
    "BHO": (23.2878, 77.3371),  # Bhopal Airport
    "Varanasi": (25.3176, 82.9739),
    "VNS": (25.4520, 82.8613),  # Varanasi Airport
    "Pune": (18.5204, 73.8567),
    "PNQ": (18.5803, 73.9197),  # Pune Airport
}

# Define the connections (edges) between locations including airport routes
connections = [
    ("Chennai", "Bangalore"),
    ("Bangalore", "Hyderabad"),
    ("Hyderabad", "Nagpur"),
    ("Nagpur", "Delhi"),
    ("Mumbai", "Pune"),
    ("Pune", "Hyderabad"),
    ("Kolkata", "Varanasi"),
    ("Varanasi", "Delhi"),
    ("Mumbai", "Bhopal"),
    ("Bhopal", "Delhi"),
    ("Chennai", "Mumbai"),
    ("Hyderabad", "Bhopal"),
    ("Ahmedabad", "Jaipur"),
    ("Jaipur", "Delhi"),
    ("Chennai", "MAA"),
    ("Delhi", "DEL"),
    ("Bangalore", "BLR"),
    ("Mumbai", "BOM"),
    ("Hyderabad", "HYD"),
    ("Kolkata", "CCU"),
    ("Nagpur", "NAG"),
    ("Ahmedabad", "AMD"),
    ("Jaipur", "JAI"),
    ("Bhopal", "BHO"),
    ("Varanasi", "VNS"),
    ("Pune", "PNQ"),
    ("MAA", "DEL"),
    ("MAA", "BLR"),
    ("BLR", "HYD"),
    ("HYD", "NAG"),
    ("NAG", "DEL"),
    ("BOM", "PNQ"),
    ("PNQ", "HYD"),
    ("CCU", "VNS"),
    ("VNS", "DEL"),
    ("BOM", "BHO"),
    ("BHO", "DEL"),
    ("AMD", "JAI"),
    ("JAI", "DEL"),
]

# Create a graph and add edges with distances as weights
graph = nx.Graph()
for loc1, loc2 in connections:
    distance = geodesic(locations[loc1], locations[loc2]).kilometers
    graph.add_edge(loc1, loc2, weight=distance)

# Create the folium map
def create_map(path=[]):
    folium_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    for loc, coords in locations.items():
        folium.Marker(coords, popup=loc, icon=folium.Icon(color="blue")).add_to(folium_map)
    for loc1, loc2 in connections:
        folium.PolyLine([locations[loc1], locations[loc2]], color="gray", weight=2, opacity=0.5).add_to(folium_map)
    if path:
        path_coords = [locations[city] for city in path]
        folium.PolyLine(path_coords, color="green", weight=5, opacity=0.7).add_to(folium_map)
        for coord, city in zip(path_coords, path):
            folium.Marker(coord, popup=city, icon=folium.Icon(color="red")).add_to(folium_map)
    return folium_map

@app.route('/')
def index():
    folium_map = create_map()
    folium_map.save('map.html')
    return render_template('map.html')

@app.route('/find_route', methods=['POST'])
def find_route():
    data = request.get_json()
    start = data['start']
    end = data['end']
    try:
        shortest_path = nx.dijkstra_path(graph, start, end, weight='weight')
        distance = nx.dijkstra_path_length(graph, start, end, weight='weight')
        return jsonify({'path': shortest_path, 'distance': f"{distance:.2f} km"})
    except nx.NetworkXNoPath:
        return jsonify({'error': 'No path found between selected locations.'})

if __name__ == '__main__':
    app.run(debug=True)
