# -*- coding: utf-8 -*-
"""
Step 2: Visualization of the built RDF graph
"""

from rdflib import Graph, RDF
import networkx as nx
import matplotlib.pyplot as plt

g = Graph()
g.parse("movies.ttl", format="turtle")


def short(uri):
    """Shortens a URI to its last path segment (drops the namespace)."""
    s = str(uri)
    if "#" in s:
        return s.split("#")[-1]
    return s.rstrip("/").split("/")[-1]


G = nx.DiGraph()
type_map = {}

for s, p, o in g:
    if p == RDF.type:
        t = short(o)
        if t in ("Movie", "Person", "Director", "Actor", "Genre", "Country", "Studio"):
            type_map.setdefault(short(s), t)
        continue
    if str(o).startswith("http"):
        G.add_edge(short(s), short(o), label=short(p))

color_by_type = {
    "Movie": "#4C72B0",
    "Director": "#DD8452",
    "Actor": "#55A868",
    "Person": "#55A868",
    "Genre": "#C44E52",
    "Country": "#8172B2",
    "Studio": "#937860",
}

node_colors = [color_by_type.get(type_map.get(n, "Movie"), "#CCCCCC") for n in G.nodes()]

plt.figure(figsize=(22, 18))
pos = nx.spring_layout(G, k=0.6, seed=42, iterations=50)

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=900, alpha=0.9)
nx.draw_networkx_labels(G, pos, font_size=7)
nx.draw_networkx_edges(G, pos, alpha=0.3, arrows=True, arrowsize=8, width=0.7)

edge_labels = nx.get_edge_attributes(G, "label")
sparse_labels = {k: v for i, (k, v) in enumerate(edge_labels.items()) if i % 5 == 0}
nx.draw_networkx_edge_labels(G, pos, edge_labels=sparse_labels, font_size=5)

legend_items = [plt.Line2D([0], [0], marker='o', color='w', label=t,
                            markerfacecolor=c, markersize=10)
                 for t, c in color_by_type.items() if t != "Person"]
plt.legend(handles=legend_items, loc="upper left", fontsize=10)

plt.title("RDF graph of the movie domain (horror / gothic)", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.savefig("movies_graph.png", dpi=150)
print("Visualization saved to movies_graph.png")
print(f"Nodes: {G.number_of_nodes()}, edges: {G.number_of_edges()}")