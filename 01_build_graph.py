# -*- coding: utf-8 -*-
"""
Lab work #1
Topic: Semantic Web technologies: RDF and SPARQL
Domain: MOVIES (horror / gothic selection)

Step 1: Building an RDF graph with Python + RDFLib
"""

from rdflib import Graph, Namespace, RDF, RDFS, Literal, XSD
from rdflib.namespace import FOAF, DC

# ---------------------------------------------------------------------------
# 1. Namespaces
# ---------------------------------------------------------------------------
EX = Namespace("http://example.org/movies/")            # own resources
MO = Namespace("http://example.org/movies/ontology#")    # own ontology (classes/props)
SCHEMA = Namespace("http://schema.org/")                  # existing vocabulary #1

g = Graph()
g.bind("ex", EX)
g.bind("mo", MO)
g.bind("foaf", FOAF)
g.bind("dc", DC)
g.bind("schema", SCHEMA)

# ---------------------------------------------------------------------------
# 2. Entity types (classes) - 5 total:
#    mo:Movie, mo:Person (Director, Actor), mo:Genre, mo:Country, mo:Studio
# ---------------------------------------------------------------------------

# --- Directors ------------------------------------------------------------
directors = {
    "burton": "Tim Burton",
    "del_toro": "Guillermo del Toro",
    "craven": "Wes Craven",
    "wong": "James Wong",
    "ellis": "David R. Ellis",
    "selick": "Henry Selick",
    "collet_serra": "Jaume Collet-Serra",
    "nispel": "Marcus Nispel",
    "schmidt": "Rob Schmidt",
    "myrick": "Daniel Myrick",
    "muschietti": "Andy Muschietti",
}
for uid, name in directors.items():
    uri = EX[uid]
    g.add((uri, RDF.type, MO.Person))
    g.add((uri, RDF.type, MO.Director))
    g.add((uri, FOAF.name, Literal(name)))

# --- Actors -----------------------------------------------------------
actors = {
    "depp": "Johnny Depp",
    "ricci": "Christina Ricci",
    "green": "Eva Green",
    "bonham_carter": "Helena Bonham Carter",
    "hastie": "Jonathan Hyde",
    "campbell": "Neve Campbell",
    "cox": "Courteney Cox",
    "arquette": "David Arquette",
    "barrymore": "Drew Barrymore",
    "sadler": "William Sadler",
    "hewitt": "Jennifer Love Hewitt",
    "cook": "Ali Larter",
    "goth": "Mia Goth",
    "biel": "Jessica Biel",
    "mcgowan": "Rose McGowan",
    "skarsgard": "Bill Skarsgard",
    "lillard": "Skeet Ulrich",
}
for uid, name in actors.items():
    uri = EX[uid]
    g.add((uri, RDF.type, MO.Person))
    g.add((uri, RDF.type, MO.Actor))
    g.add((uri, FOAF.name, Literal(name)))

# --- Genres --------------------------------------------------------------
genres = ["Horror", "Gothic", "Slasher", "Fantasy", "Thriller", "Comedy"]
for g_id in genres:
    uri = EX["genre_" + g_id]
    g.add((uri, RDF.type, MO.Genre))
    g.add((uri, RDFS.label, Literal(g_id)))

# --- Countries -----------------------------------------------------------
countries = ["USA", "UK", "Mexico", "Germany"]
for c_id in countries:
    uri = EX["country_" + c_id]
    g.add((uri, RDF.type, MO.Country))
    g.add((uri, RDFS.label, Literal(c_id)))

# --- Studios --------------------------------------------------------------
studios = {
    "paramount": "Paramount Pictures",
    "dimension": "Dimension Films",
    "warner": "Warner Bros.",
    "disney": "Walt Disney Pictures",
    "newline": "New Line Cinema",
    "legendary": "Legendary Pictures",
}
for uid, name in studios.items():
    uri = EX[uid]
    g.add((uri, RDF.type, MO.Studio))
    g.add((uri, RDFS.label, Literal(name)))

# ---------------------------------------------------------------------------
# 3. Movies - the core entities (15 films)
# ---------------------------------------------------------------------------
movies = [
    # id, title, year, director, actors[], genres[], country, studio
    ("sleepy_hollow", "Sleepy Hollow", 1999, "burton",
     ["depp", "ricci"], ["Horror", "Gothic", "Fantasy"], "USA", "paramount"),
    ("dark_shadows", "Dark Shadows", 2012, "burton",
     ["depp", "green", "bonham_carter"], ["Horror", "Gothic", "Comedy"], "USA", "warner"),
    ("crimson_peak", "Crimson Peak", 2015, "del_toro",
     ["hastie", "goth"], ["Horror", "Gothic", "Thriller"], "USA", "legendary"),
    ("scream", "Scream", 1996, "craven",
     ["campbell", "cox", "arquette", "barrymore"], ["Horror", "Slasher"], "USA", "dimension"),
    ("scream_2", "Scream 2", 1997, "craven",
     ["campbell", "cox", "arquette", "mcgowan"], ["Horror", "Slasher"], "USA", "dimension"),
    ("final_destination", "Final Destination", 2000, "wong",
     ["sadler", "hewitt"], ["Horror", "Thriller"], "USA", "newline"),
    ("final_destination_2", "Final Destination 2", 2003, "ellis",
     ["sadler", "cook"], ["Horror", "Thriller"], "USA", "newline"),
    ("edward_scissorhands", "Edward Scissorhands", 1990, "burton",
     ["depp", "ricci"], ["Gothic", "Fantasy"], "USA", "disney"),
    ("corpse_bride", "Corpse Bride", 2005, "burton",
     ["depp", "bonham_carter"], ["Gothic", "Fantasy", "Comedy"], "UK", "warner"),
    ("nightmare_before_christmas", "The Nightmare Before Christmas", 1993, "selick",
     ["ricci"], ["Gothic", "Fantasy", "Comedy"], "USA", "disney"),
    ("house_of_wax", "House of Wax", 2005, "collet_serra",
     ["biel", "cook"], ["Horror", "Slasher", "Thriller"], "USA", "warner"),
    ("texas_chainsaw_massacre", "The Texas Chainsaw Massacre", 2003, "nispel",
     ["biel"], ["Horror", "Slasher"], "USA", "newline"),
    ("wrong_turn", "Wrong Turn", 2003, "schmidt",
     ["goth", "lillard"], ["Horror", "Slasher", "Thriller"], "USA", "legendary"),
    ("blair_witch_project", "The Blair Witch Project", 1999, "myrick",
     ["ricci"], ["Horror", "Thriller"], "USA", "dimension"),
    ("it", "It", 2017, "muschietti",
     ["skarsgard", "goth"], ["Horror", "Fantasy", "Thriller"], "USA", "warner"),
]

for uid, title, year, director, cast, genre_list, country, studio in movies:
    uri = EX[uid]
    g.add((uri, RDF.type, MO.Movie))
    g.add((uri, RDF.type, SCHEMA.Movie))            # link to schema.org
    g.add((uri, DC.title, Literal(title)))           # Dublin Core: dc:title
    g.add((uri, SCHEMA.datePublished, Literal(year, datatype=XSD.gYear)))
    g.add((uri, MO.releaseYear, Literal(year, datatype=XSD.integer)))
    g.add((uri, MO.directedBy, EX[director]))
    g.add((uri, MO.producedBy, EX[studio]))
    g.add((uri, MO.releasedIn, EX["country_" + country]))
    for a in cast:
        g.add((uri, MO.hasActor, EX[a]))
        g.add((EX[a], MO.actedIn, uri))              # inverse relation
    for gname in genre_list:
        g.add((uri, MO.hasGenre, EX["genre_" + gname]))

# ---------------------------------------------------------------------------
# 4. One more relation type: "colleagueOf" between actors who co-starred
# ---------------------------------------------------------------------------
g.add((EX.campbell, MO.colleagueOf, EX.cox))
g.add((EX.cox, MO.colleagueOf, EX.campbell))
g.add((EX.depp, MO.colleagueOf, EX.ricci))
g.add((EX.biel, MO.colleagueOf, EX.cook))

print(f"Total triples in the graph: {len(g)}")
print(f"Unique subject resources: {len(set(g.subjects()))}")

# ---------------------------------------------------------------------------
# 5. Save the graph
# ---------------------------------------------------------------------------
g.serialize(destination="movies.ttl", format="turtle")
g.serialize(destination="movies.xml", format="xml")   # RDF/XML - a second format
g.serialize(destination="movies.nt", format="nt")

print("Graph saved as Turtle (movies.ttl), RDF/XML (movies.xml), N-Triples (movies.nt)")