from TwitterDataRetriever import TwitterDataRetriever
from HeatmapCreator import HeatmapCreator
import sys

if __name__ == '__main__':
    t = TwitterDataRetriever()
    print("hello")
    if len(sys.argv) <= 1:
        locations = t.get_tweet_locations()
    else:
        locations = t.get_tweet_locations(query=sys.argv[1])
    h = HeatmapCreator()
    h.build_map(locations)
    print("heatmap created for the keyword " + sys.argv[1] + ". View the heatmap by opening the export.html file in"
                                                             " your browser.")