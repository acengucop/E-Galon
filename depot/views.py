# depot/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from math import radians, cos, sin, asin, sqrt

from .models import Depot
from .serializers import DepotSerializer
from .routing import get_shortest_route, GRAPH
import osmnx as ox


def haversine(lat1, lon1, lat2, lon2):
    """Hitung jarak (km) antara dua koordinat."""
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


@api_view(['GET'])
def list_depots(request):
    """Ambil semua depot."""
    depots = Depot.objects.all()
    serializer = DepotSerializer(depots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def nearest_depot(request):
    """Ambil depot terdekat (berdasarkan jarak lurus)."""
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return Response({'error': 'Parameter lat dan lon diperlukan.'}, status=400)

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return Response({'error': 'lat/lon harus berupa angka'}, status=400)

    nearest = None
    min_dist = float('inf')

    for depot in Depot.objects.all():
        if depot.latitude is None or depot.longitude is None:
            continue
        dist = haversine(lat, lon, depot.latitude, depot.longitude)
        if dist < min_dist:
            min_dist = dist
            nearest = depot

    if nearest:
        serializer = DepotSerializer(nearest)
        return Response(serializer.data)

    return Response({'error': 'Depot tidak ditemukan'}, status=404)


@api_view(['GET'])
def nearest_depot_route(request):
    """Cari depot terdekat berdasarkan waktu tempuh (via Dijkstra)."""
    try:
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid lat/lon'}, status=400)

    nearest = None
    min_time = float('inf')

    for depot in Depot.objects.all():
        if depot.latitude is not None and depot.longitude is not None:
            route = get_shortest_route(lat, lon, depot.latitude, depot.longitude)
            if route:
                try:
                    total_time = sum(ox.utils_graph.get_route_edge_attributes(GRAPH, route, 'travel_time'))
                    if total_time < min_time:
                        min_time = total_time
                        nearest = depot
                except Exception:
                    continue

    if nearest:
        serializer = DepotSerializer(nearest)
        return Response({
            'depot': serializer.data,
            'estimated_time_min': round(min_time / 60, 1)
        })

    return Response({'error': 'Tidak ada rute ke depot manapun'}, status=404)
