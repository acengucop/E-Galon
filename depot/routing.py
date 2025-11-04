# depot/routing.py

import osmnx as ox
import networkx as nx

# Unduh graf jalan untuk wilayah tertentu (misal: Pekanbaru, Indonesia)
# ⚠️ Ganti dengan lokasi yang sesuai jika perlu
GRAPH = ox.graph_from_place("Pekanbaru, Indonesia", network_type="drive")

# Tambahkan atribut waktu tempuh (dalam detik)
# travel_time = jarak (m) / kecepatan (m/s)
for u, v, k, data in GRAPH.edges(keys=True, data=True):
    length_m = data.get('length', 0)
    speed_kph = data.get('speed_kph', 40)  # default 40 km/h jika tidak tersedia
    speed_mps = speed_kph * 1000 / 3600
    data['travel_time'] = length_m / speed_mps if speed_mps > 0 else float('inf')


def get_shortest_route(orig_lat, orig_lon, dest_lat, dest_lon):
    """
    Mengembalikan rute tercepat (berdasarkan waktu tempuh) antara dua titik.
    Jika gagal, kembalikan None.
    """
    try:
        orig_node = ox.distance.nearest_nodes(GRAPH, X=orig_lon, Y=orig_lat)
        dest_node = ox.distance.nearest_nodes(GRAPH, X=dest_lon, Y=dest_lat)
        route = nx.shortest_path(GRAPH, orig_node, dest_node, weight='travel_time')
        return route
    except Exception as e:
        print(f"Routing error: {e}")
        return None
