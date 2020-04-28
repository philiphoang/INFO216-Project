from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE
from rdflib import Graph, Literal, Namespace, URIRef

prefixRecipe = "PREFIX recipe: <http://schema.org/Recipe/>"

sparql = SPARQLWrapper("http://localhost:9999/blazegraph/sparql")

##
# Function for creating queries for a set of ingredients
def createIngredientQuery(ingredientList):
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

##
# Send the query to sparql and convert it to JSON format
def parseQuery(query):
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

##
# Collect the recipe from the result of query
def getRecipes(query):
    results = parseQuery(query)

    resultList = []
    for result in results["results"]["bindings"]:
        resultList.append(result["title"]["value"])
        print(result["title"]["value"])


    return resultList

