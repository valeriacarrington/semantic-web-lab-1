# -*- coding: utf-8 -*-
"""
Step 6: Erroneous vs. corrected example (for the lab report, point 6)

This file demonstrates a real, reproducible mistake made while writing a
SPARQL query, why it fails silently (returns 0 rows instead of an error),
how it was diagnosed, and the corrected version.

MISTAKE: SPARQL string literals are case-sensitive. The graph stores genre
labels with a capital first letter (e.g. "Horror", "Gothic" - see
01_build_graph.py, the `genres` list). A FILTER comparing against the
lowercase string "horror" does not match anything, because RDF literal
comparison is exact and case-sensitive - there is no automatic case folding.
The query is syntactically valid, so RDFLib does not raise an error; it
simply returns an empty result set, which is a common source of confusion
for beginners (a "silent" bug rather than a crash).
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

# ---------------------------------------------------------------------------
# BROKEN QUERY: looking for actors in "horror" movies (lowercase)
# ---------------------------------------------------------------------------
broken_query = """
SELECT ?actorName WHERE {
    ?movie mo:hasGenre ?genre .
    ?genre rdfs:label "horror" .
    ?movie mo:hasActor ?actor .
    ?actor foaf:name ?actorName .
}
"""

print("=" * 78)
print("BROKEN QUERY (genre label written in lowercase: \"horror\")")
print("=" * 78)
print(broken_query.strip())
print("-" * 78)
results = g.query(PREFIXES + broken_query)
rows = list(results)
print(f"Result rows: {len(rows)}")
if not rows:
    print(">>> No error was raised, but the query returned ZERO rows.")
    print(">>> This is the bug: it looks like 'no actors match', but the")
    print(">>> real cause is a literal case mismatch, not missing data.\n")

# ---------------------------------------------------------------------------
# DIAGNOSIS: check what the actual stored label value looks like
# ---------------------------------------------------------------------------
print("=" * 78)
print("DIAGNOSIS: inspect the real rdfs:label values stored for genres")
print("=" * 78)
diagnosis_query = """
SELECT ?genre ?label WHERE {
    ?genre a mo:Genre .
    ?genre rdfs:label ?label .
}
ORDER BY ?label
"""
for row in g.query(PREFIXES + diagnosis_query):
    print(f"  {row.genre}  ->  label = \"{row.label}\"")
print("\n>>> The stored value is \"Horror\" (capital H), not \"horror\".")
print(">>> That confirms the query's FILTER value was simply typed wrong.\n")

# ---------------------------------------------------------------------------
# FIXED QUERY: same query, correct capitalisation
# ---------------------------------------------------------------------------
fixed_query = """
SELECT DISTINCT ?actorName WHERE {
    ?movie mo:hasGenre ?genre .
    ?genre rdfs:label "Horror" .
    ?movie mo:hasActor ?actor .
    ?actor foaf:name ?actorName .
}
ORDER BY ?actorName
"""

print("=" * 78)
print("FIXED QUERY (genre label corrected to \"Horror\")")
print("=" * 78)
print(fixed_query.strip())
print("-" * 78)
fixed_results = g.query(PREFIXES + fixed_query)
fixed_rows = list(fixed_results)
for row in fixed_rows:
    print(f"  {row.actorName}")
print(f"\nResult rows: {len(fixed_rows)}")
print(">>> The corrected query now returns the expected actors.")

robust_query = """
SELECT DISTINCT ?actorName WHERE {
    ?movie mo:hasGenre ?genre .
    ?genre rdfs:label ?label .
    FILTER (LCASE(STR(?label)) = "horror")
    ?movie mo:hasActor ?actor .
    ?actor foaf:name ?actorName .
}
ORDER BY ?actorName
"""

print("\n" + "=" * 78)
print("ROBUST VERSION: case-insensitive FILTER using LCASE(), so future typos")
print("in capitalisation no longer silently break the query")
print("=" * 78)
print(robust_query.strip())
print("-" * 78)
robust_rows = list(g.query(PREFIXES + robust_query))
print(f"Result rows: {len(robust_rows)} (matches the fixed query above)")