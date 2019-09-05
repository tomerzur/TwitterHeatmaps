import gmaps
import gmaps.datasets
from ipywidgets.embed import embed_minimal_html
import config


class HeatmapCreator:
    def build_map(self, locations):
        gmaps.configure(api_key=config.google_api_key)
        f = gmaps.figure()
        heatmap_layer = gmaps.heatmap_layer(locations)
        f.add_layer(heatmap_layer)
        embed_minimal_html('export.html', views=[f])