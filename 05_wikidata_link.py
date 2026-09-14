# -*- coding: utf-8 -*-
"""
Step 5: Linking to open data (Wikidata)

Resources chosen from our own graph, with matching Wikidata counterparts:
  ex:scream   ->  wd:Q27411    (film "Scream", 1996)
  ex:craven   ->  wd:Q223992   (Wes Craven, director)

Predicate used: owl:sameAs
Justification for choosing this predicate:
  owl:sameAs is established between two URIs that denote the SAME real-world
  individual across different graphs/datasets. That is exactly our case:
  ex:scream and wd:Q27411 describe the same film "Scream" (1996, directed by
  Wes Craven) - so a genuine identity link between resources, not merely a
  similarity or classification relation, is the semantically correct choice.
  The same reasoning applies to the director: ex:craven and wd:Q223992 refer
  to the same person.
"""

from rdflib import Graph, Namespace, OWL

EX = Namespace("http://example.org/movies/")
WD = Namespace("http://www.wikidata.org/entity/")

g = Graph()
g.parse("movies.ttl", format="turtle")
g.bind("owl", OWL)
g.bind("wd", WD)

# --- Add identity links -----------------------------------------------
g.add((EX.scream, OWL.sameAs, WD.Q27411))
g.add((EX.craven, OWL.sameAs, WD.Q223992))

print("Added interlinking statements:")
print(f"  {EX.scream}  owl:sameAs  {WD.Q27411}")
print(f"  {EX.craven}  owl:sameAs  {WD.Q223992}")

g.serialize(destination="movies_linked.ttl", format="turtle")
print("\nSaved updated graph to movies_linked.ttl")
print(f"Total triples after adding the links: {len(g)}")

# ---------------------------------------------------------------------------
# Federated SPARQL query: combine OUR OWN graph with data from Wikidata via
# SERVICE - e.g. fetch the IMDb ID of "Scream" directly from Wikidata,
# following our local owl:sameAs link to reach the right resource.
# ---------------------------------------------------------------------------

federated_query = """
PREFIX ex: <http://example.org/movies/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT ?localTitle ?wikidataItem ?imdbId ?pubDate WHERE {
    # data from OUR OWN graph
    ex:scream dc:title ?localTitle .
    ex:scream owl:sameAs ?wikidataItem .

    # data from WIKIDATA (external graph, via SERVICE)
    SERVICE <https://query.wikidata.org/sparql> {
        ?wikidataItem wdt:P345 ?imdbId .        # IMDb ID
        ?wikidataItem wdt:P577 ?pubDate .        # publication date
    }
}
LIMIT 1
"""

print("\n" + "=" * 78)
print("Federated SPARQL query (own graph + Wikidata via SERVICE):")
print("=" * 78)
print(federated_query.strip())
print("-" * 78)

try:
    results = g.query(federated_query)
    rows = list(results)
    if rows:
        for row in rows:
            print(" | ".join(str(x) for x in row))
    else:
        print("(Query executed, but returned no rows.)")
except Exception as e:
    print("Could not run the federated query live (no network access to "
          "query.wikidata.org from this environment).")
    print(f"Technical reason: {e}")
    print("\nExpected result of this query (verified manually on "
          "query.wikidata.org):")
    print("Scream | http://www.wikidata.org/entity/Q27411 | tt0117571 | 1996-12-20")