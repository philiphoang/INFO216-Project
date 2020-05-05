from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, POST 
from rdflib import Graph, Literal, Namespace, URIRef

## Prefixes
prefixRecipe = "PREFIX recipe: <http://schema.org/Recipe/>"
prefixEx = "PREFIX ex: <http://example.org/>"
prefixRdf = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"

## Connection to Blazegraph
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
    print()
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

##
# Collect the recipe titles from the query result
def getRecipeTitle(query):
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

##
# Get a dictionary containing title and instructions
def getTitleAndInstructionsInDictionary(query):
    results = parseQuery(query)

    print(results)

    d = {}
    for result in results["results"]["bindings"]:
        title = result["title"]["value"]
        instructions = result["instructions"]["value"]

        if (title not in d.keys()):
            d[title] = instructions

    return d


##
# Get all ingredients and instructions
def getAllIngredientsAndInstructions(query):
    results = parseQuery(query)

    recipeDict = {}
    for result in results["results"]["bindings"]:
        title = result["title"]["value"]
        ingredient = result["ingredient"]["value"]
        instruction = result["instruction"]["value"]

        if (title not in recipeDict):
            recipeDict[title] = []
        
        recipeDict.get(title).append(ingredient)
            
    return recipeDict

##
# Match the chosen ingredients with all recipes to get all ingredients
def findRecipes(ingredientList):
    ingredientQuery = createIngredientQuery(ingredientList) #Create query 
    titleAndInstructionDict = getTitleAndInstructionsInDictionary(ingredientQuery) #Get result of query

    allRecipeDict = getAllIngredientsAndInstructions("" + prefixRecipe +
        """SELECT DISTINCT ?title ?ingredient ?instruction WHERE
        {
            ?title recipe:recipeIngredient ?ingredient .
            ?title recipe:recipeInstructions ?instruction
        }    
    """)

    resultDict = {}

    for title in allRecipeDict.keys():
        if (title in titleAndInstructionDict):
            resultDict[title] = allRecipeDict[title]

            resultDict.get(title).insert(len(resultDict.get(title)),  titleAndInstructionDict[title])

    print(resultDict)
    return resultDict

def createInsertRecipeQuery(title, ingredientList, instructions):
    newTitle = title.replace(' ', '_')
    exTitle = "ex:" + newTitle + " "

    query = "" + prefixRecipe + " " + prefixRdf + " " + prefixEx + " INSERT DATA {"
    query += exTitle + "rdf:type recipe:name . "

    for ingredient in ingredientList:
        query += exTitle + "recipe:recipeIngredient \"" + ingredient + "\" . "
    
    query += exTitle + "recipe:recipeInstructions \"" + instructions + "\" . }"
    
    print(query)
    return query


##
# Insert recipe 
def insertRecipe(query):
    sparql.setMethod(POST)
    sparql.setQuery(query)

    results = sparql.query()
    print(results.response.read())