import geopandas as gpd
from shapely.ops import voronoi_diagram
from shapely.ops import unary_union
from shapely.geometry import shape
from shapely import Polygon
import random

random.seed(0)

def generate_voronoi_plot(n_points):

    x0, y0 = 1821519.591, 5525357.547
    x1, y1 = 1822519.591, 5526357.547
    envelope = Polygon([
        [x0, y0],
        [x0, y1],
        [x1, y1],
        [x1, y0],
        [x0, y0]
    ])

    envelope = gpd.GeoDataFrame(index=[0], crs='epsg:2193', geometry=[envelope])
    
    # Sample points and create Voronoi diagram
    points = envelope.sample_points(n_points)
    points = [shape(geometry) for geometry in points]
    mp = unary_union(points)
    vor = gpd.GeoDataFrame(gpd.GeoSeries(voronoi_diagram(mp, envelope=envelope.geometry[0]))).set_geometry(0).explode()
    
    # Clip Voronoi diagram
    vor = gpd.clip(vor, envelope, keep_geom_type=True).set_crs('EPSG:2193')
    
    # Use the assign method to create a new column filled with random values
    vor = vor.assign(val=[random.randint(0, 1) for _ in range(len(vor))])
    return vor.dissolve('val')
    
# Call the function with the file path
n_points=75
for i in range(0, 10):
    shapes = generate_voronoi_plot(n_points)
    shapes.to_file(f'output-{i}.gpkg')