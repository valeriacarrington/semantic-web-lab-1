# -*- coding: utf-8 -*-
"""
Step 4: SPARQL queries against our own graph.

Questions the queries answer (as required by the assignment):
 Q1. Which movies did Tim Burton direct? (FILTER on the director's name)
 Q2. Which movies were released after 2000, sorted by year? (FILTER + ORDER BY)
 Q3. Which actors starred in Horror-genre movies? (traversal across several
     linked entity types: Actor -> hasActor <- Movie -> hasGenre -> Genre)
 Q4. How many movies did each director make? (COUNT aggregate + GROUP BY)
 Q5. Which actors starred in movies produced by a given studio, released in a
     given country, directed by Tim Burton? (traversal through at least 3
     graph relations: Director -> Movie -> Studio, Movie -> Country,
     Movie -> Actor)
"""

from rdflib import Graph

g = Graph()
g.parse("movies.ttl", format="turtle")

PREFIXES = """
PREFIX ex: <http://example.org/movies/>
PREFIX mo: <http://example.org/movies/ontology#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""


def run(title, query):
    print("=" * 78)
    print(title)
    print("=" * 78)
    print(query.strip())
    print("-" * 78)
    results = g.query(PREFIXES + query)
    for row in results:
        print(" | ".join(str(x) for x in row))
    print(f"\n[Result rows: {len(results)}]\n")


# --- Q1: FILTER ------------------------------------------------------------
q1 = """
SELECT ?title WHERE {
    ?movie mo:directedBy ?director .
    ?director foaf:name ?dname .
    ?movie dc:title ?title .
    FILTER (?dname = "Tim Burton")
}
ORDER BY ?title
"""
run("Q1. Movies directed by Tim Burton (FILTER)", q1)

# --- Q2: FILTER + sorting ----------------------------------------------
q2 = """
SELECT ?title ?year WHERE {
    ?movie dc:title ?title .
    ?movie mo:releaseYear ?year .
    FILTER (?year > 2000)
}
ORDER BY DESC(?year)
"""
run("Q2. Movies released after 2000, newest first (FILTER + ORDER BY)", q2)

# --- Q3: traversal Actor<->Movie->Genre ------------------------------------
q3 = """
SELECT DISTINCT ?actorName WHERE {
    ?movie mo:hasGenre ?genre .
    ?genre rdfs:label "Horror" .
    ?movie mo:hasActor ?actor .
    ?actor foaf:name ?actorName .
}
ORDER BY ?actorName
"""
run("Q3. Actors who starred in Horror-genre movies (multi-entity traversal)", q3)

# --- Q4: COUNT aggregate ----------------------------------------------------
q4 = """
SELECT ?dname (COUNT(?movie) AS ?movieCount) WHERE {
    ?movie mo:directedBy ?director .
    ?director foaf:name ?dname .
}
GROUP BY ?dname
ORDER BY DESC(?movieCount)
"""
run("Q4. Number of movies per director (COUNT aggregate)", q4)

# --- Q5: at least 3 relation hops --------------------------------------
q5 = """
SELECT DISTINCT ?movieTitle ?actorName ?studioLabel ?countryLabel WHERE {
    ?director foaf:name "Tim Burton" .
    ?movie mo:directedBy ?director .          # hop 1: director -> movie
    ?movie mo:producedBy ?studio .            # hop 2: movie -> studio
    ?studio rdfs:label ?studioLabel .
    ?movie mo:releasedIn ?country .           # hop 3: movie -> country
    ?country rdfs:label ?countryLabel .
    ?movie mo:hasActor ?actor .               # hop 4: movie -> actor
    ?actor foaf:name ?actorName .
    ?movie dc:title ?movieTitle .
}
ORDER BY ?movieTitle
"""
run("Q5. Burton's movies: studio, country, actors (4-hop graph traversal)", q5)