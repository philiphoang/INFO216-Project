from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE
from rdflib import Graph, Literal, Namespace, URIRef

sparql = SPARQLWrapper("http://localhost:9999/blazegraph/sparql")

prefixRecipe = "PREFIX recipe: <http://schema.org/Recipe/>"

#In Blazegraph:
# prefix recipe: <http://schema.org/Recipe/> 
    
#     SELECT DISTINCT * WHERE {
#         ?x recipe:recipeIngredient ?ingredient
#         FILTER regex(?ingredient, "garlic", "i").
# }


#SELECT recipes based on one ingredient (example: garlic)
sparql.setQuery("" + prefixRecipe + 
    """SELECT DISTINCT * WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER regex(?ingredient, "garlic", "i").
    }
""")

#Can also use CONTAINS(?o, "regex")


#SELECT recipes based on either ingredients (example: chicken OR ham)
sparql.setQuery("" + prefixRecipe + 
    """SELECT DISTINCT * WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER (
            regex(?ingredient, "chicken", "i") ||
            regex(?ingredient, "ham", "i")
        ).
    }
""")


#SELECT recipes based on two ingredients (example: beef AND tomato)
sparql.setQuery("" + prefixRecipe + 
    """
    SELECT DISTINCT ?title ?ingredient1 ?ingredient2 WHERE 
    {   
        {
            ?title recipe:recipeIngredient ?ingredient1
            FILTER CONTAINS(?ingredient1, "ground beef") .   
      
            ?title recipe:recipeIngredient ?ingredient2 
            FILTER CONTAINS(?ingredient2, "tomato") .
        }
    }
        
""")


sparql.setQuery("" + prefixRecipe + 
    """SELECT DISTINCT ?title ?ingredient1 ?ingredient2 ?ingredient3 WHERE 
    {   
        {
            ?title recipe:recipeIngredient ?ingredient1
            FILTER CONTAINS(?ingredient1, "chicken") .   
      
            ?title recipe:recipeIngredient ?ingredient2 
            FILTER CONTAINS(?ingredient2, "tomato") .

            ?title recipe:recipeIngredient ?ingredient3 
            FILTER CONTAINS(?ingredient3, "onion") .
        }
    }
        
""")


##
# Function that creates a query for a set of ingredients
def ingredientQuery(ingredientList):
    queryString = "" + prefixRecipe + " SELECT DISTINCT ?title" 
    
    for i in range(0, len(ingredientList)):
        queryString += " ?ingredient"+str(i)

    queryString += " WHERE { {"

    for i, ingredient in enumerate(ingredientList):
        queryString += addIngredientToQuery(str(i), ingredient)

    queryString += "} }"

    return queryString

##
# Create a string for filtering for an ingredient 
def addIngredientToQuery(i, ingredient):
    return "?title recipe:recipeIngredient ?ingredient" + i + " FILTER CONTAINS(?ingredient" + i + ", \"" + ingredient + "\") . "


sparql.setQuery(ingredientQuery(["beef", "tomato", "garlic"]))

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["title"]["value"])
