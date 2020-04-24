from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, Namespace, URIRef

sparql = SPARQLWrapper("http://localhost:9999/blazegraph/sparql")

#In Blazegraph:
# prefix recipe: <http://schema.org/Recipe/> 
    
#     SELECT DISTINCT * WHERE {
#         ?x recipe:recipeIngredient ?ingredient
#         FILTER regex(?ingredient, "garlic", "i").
# }


#SELECT recipes based on one ingredient (example: garlic)
sparql.setQuery("""
    PREFIX recipe: <http://schema.org/Recipe/> 
    
    SELECT DISTINCT * WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER regex(?ingredient, "garlic", "i").
    }
""")

#Can also use CONTAINS(?o, "regex")


#SELECT recipes based on either ingredients (example: chicken OR ham)
sparql.setQuery("""
    PREFIX recipe: <http://schema.org/Recipe/> 
    
    SELECT DISTINCT * WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER (
            regex(?ingredient, "chicken", "i") ||
            regex(?ingredient, "ham", "i")
        ).
    }
""")




#TODO
#Create a query, save that result. Reuse that result to the new query
#SELECT recipes based on two ingredients (example: beef AND tomato)

sparql.setQuery("""
    PREFIX recipe: <http://schema.org/Recipe/> 
    
    SELECT DISTINCT * 
    WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER CONTAINS(?ingredient, "beef") .
    }
""")

sparql.setQuery("""
    PREFIX recipe: <http://schema.org/Recipe/> 
    
    SELECT DISTINCT * 
    WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER CONTAINS(?ingredient, "round") .
    }
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["title"]["value"])


