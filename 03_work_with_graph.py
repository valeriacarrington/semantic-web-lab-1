# -*- coding: utf-8 -*-
"""
Step 3: Working with the RDF graph via RDFLib
 - read the Turtle file (after manual editing)
 - print triples to the console
 - retrieve all triples related to one specific entity
"""

from rdflib import Graph, Namespace

EX = Namespace("http://example.org/movies/")

g = Graph()
g.parse("movies.ttl", format="turtle")

print(f"Graph loaded from movies.ttl. Total triples: {len(g)}")
print("(includes the mo:imdbRating triple added by hand in the text editor)\n")

# --- Print the first 15 triples of the graph -------------------------------
print("=" * 70)
print("First 15 triples of the graph:")
print("=" * 70)
for i, (s, p, o) in enumerate(g):
    if i >= 15:
        break
    print(f"{s}\n    {p}\n    {o}\n")

# --- Check the manually added triple ---------------------------------------
print("=" * 70)
print("Checking the manually added triple (mo:imdbRating):")
print("=" * 70)
for s, p, o in g:
    if "imdbRating" in str(p):
        print(f"{s} -> {p} -> {o}")

# --- All triples related to one specific entity -----------------------------
print("\n" + "=" * 70)
print("All triples related to entity ex:scream (as subject and as object):")
print("=" * 70)

entity = EX.scream
print("--- As subject (ex:scream predicate object) ---")
for p, o in g.predicate_objects(subject=entity):
    print(f"  {p}  ->  {o}")

print("\n--- As object (subject predicate ex:scream) ---")
for s, p in g.subject_predicates(object=entity):
    print(f"  {s}  ->  {p}")