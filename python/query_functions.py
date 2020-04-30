from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE
from rdflib import Graph, Literal, Namespace, URIRef

prefixRecipe = "PREFIX recipe: <http://schema.org/Recipe/>"

sparql = SPARQLWrapper("http://localhost:9999/blazegraph/sparql")

##
# Function for creating queries for a set of ingredients
def createIngredientQuery(ingredientList):
    queryString = "" + prefixRecipe + " SELECT DISTINCT ?title ?instructions" 
    
    for i in range(0, len(ingredientList)):
        queryString += " ?ingredient"+str(i)

    queryString += " WHERE { {"
    
    queryString += addInstructionsToQuery()

    for i, ingredient in enumerate(ingredientList):
        queryString += addIngredientToQuery(str(i), ingredient)

    queryString += "} }"

    return queryString

##
# Create a string for filtering for an ingredient 
def addIngredientToQuery(i, ingredient):
    return "?title recipe:recipeIngredient ?ingredient" + i + " FILTER CONTAINS(?ingredient" + i + ", \"" + ingredient + "\") . "


##
# Create a query for getting instructions 
def addInstructionsToQuery():
    return "?title recipe:recipeInstructions ?instructions ." 


##
# Send the query to sparql and convert it to JSON format
def parseQuery(query):
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

##
# Collect the recipe titles from the query result
def getRecipeTitle(query):
    print()
    results = parseQuery(query)

    print(results)

    resultList = []
    for result in results["results"]["bindings"]:
        resultList.append(result["title"]["value"])
        print(result["title"]["value"])


    return resultList

##
# Get recipe titles with instructions 
def getTitleAndInstructions(query):
    print()
    results = parseQuery(query)

    print(results)

    titleList = []
    instructionList = []
    for result in results["results"]["bindings"]:
        titleList.append(result["title"]["value"])
        print(result["title"]["value"])
        instructionList.append(result["instructions"]["value"])
        print(result["instructions"]["value"])

    return titleList, instructionList