from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, POST 
from rdflib import Graph, Literal, Namespace, URIRef

## Prefixes
prefixFo = "PREFIX fo: <https://bbc.co.uk/ontologies/fo/>"
prefixEx = "PREFIX ex: <http://example.org/>"
prefixRdf = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"

## Connection to Blazegraph
sparql = SPARQLWrapper("http://localhost:9999/blazegraph/sparql")

# Create a string for filtering for an ingredient 
#
# Returns a query string 
def addIngredientToQuery(i, ingredient):
    newIngredient = ingredient.replace(' ', '_')
    return "?title fo:ingredients ?ingredient" + i + " BIND (ex:" + newIngredient + " as ?i" + i + ") ?ingredient" + i + " fo:food ?i" + i + " ."
    

##
# Send the query to sparql and convert the result to JSON format
#
# Returns the result of a query
def parseQuery(query):
    print()
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

##
# Collect the recipe titles from the query result
#
# Returns a list containing the recipe titles
def getRecipeTitle(query):
    results = parseQuery(query)

    resultList = []
    for result in results["results"]["bindings"]:
        resultList.append(result["title"]["value"])
        print(result["title"]["value"])

    return resultList

##
# Get recipe titles with instructions 
#
# Returns title and instructions on list
def getTitleAndInstructions(query):
    results = parseQuery(query)

    titleList = []
    instructionList = []
    for result in results["results"]["bindings"]:
        titleList.append(result["title"]["value"])
        print(result["title"]["value"])
        instructionList.append(result["instruction"]["value"])
        print(result["instruction"]["value"])

    return titleList, instructionList

##
# Get a dictionary containing title and instructions
#
# Returns the results in a dictionary 
def getTitleAndInstructionsInDictionary(query):
    results = parseQuery(query)

    d = {}
    for result in results["results"]["bindings"]:
        title = result["title"]["value"]
        instruction = result["instruction"]["value"]

        if (title not in d.keys()):
            d[title] = instruction

    return d


##
# Get all ingredients and instructions
#
# Returns a dictionary containing all information of a recipe
def getAllInformationOfARecipe(query):
    results = parseQuery(query)

    recipeDict = {}
    for result in results["results"]["bindings"]:
        title = result["title"]["value"]
        food = result["food"]["value"]
        instruction = result["instruction"]["value"]
        quantity = result["quantity"]["value"]
        unit = result["unit"]["value"]

        ingredient = []
        if (title not in recipeDict): 
            recipeDict[title] = ingredient

        recipeDict.get(title).append([food, quantity, unit, instruction])

        print(instruction)

    return recipeDict

##
# Match the chosen ingredients with all recipes to get all ingredients
# Creates two query:
# 1. one for finding the recipes that matches the ingredients
# 2. second for finding all the recipes with all their ingredients 
# Combines the result by adding all the ingredients to the recipes that has the matching ingredients 
#
# Returns a dictionary containing all information of a recipe, but returns only the recipes that has the matching ingredients of the given input
def findRecipes(ingredientList):
    ingredientQuery = createIngredientQuery(ingredientList) #Create query 
    titleAndInstructionDict = getTitleAndInstructionsInDictionary(ingredientQuery) #Get result of query

    allRecipeDict = getAllInformationOfARecipe("" + prefixFo + prefixEx +
        """SELECT DISTINCT ?title ?quantity ?unit ?food ?instruction WHERE
        {
            ?title fo:instruction ?instruction .
          
            ?title fo:ingredients ?ingredient .
           
            ?ingredient fo:food ?food .
          
          	?ingredient fo:quantity ?quantity .
          
          	?ingredient fo:imperial_quantity ?unit
        }  
    """)

    resultDict = {}

    for title in allRecipeDict.keys():
        if (title in titleAndInstructionDict):
            resultDict[title] = allRecipeDict[title]

    return resultDict

##
# Function for creating queries for a set of ingredients
# 
# Returns a query string 
def createIngredientQuery(ingredientList):
    queryString = "" + prefixEx + " " + prefixFo + " SELECT DISTINCT ?title ?instruction" 
    
    for i in range(0, len(ingredientList)):
        queryString += " ?i"+str(i)

    queryString += " WHERE {"
    
    queryString += "?title fo:instruction ?instruction ."

    for i, ingredient in enumerate(ingredientList):
        queryString += addIngredientToQuery(str(i), ingredient)

    queryString += "}"

    return queryString

##
# Create an insertion query based on title, ingredients and instructions 
# 
# Returns a query string for insertion
def createInsertRecipeQuery(title, ingredientList, instructions):
    newTitle = title.replace(' ', '_')
    exTitle = "ex:" + newTitle + " "

    query = "" + prefixFo + " " + prefixRdf + " " + prefixEx + " INSERT DATA {"
    query += exTitle + " rdf:type fo:Recipe . "

    i = 0
    for ingredient in ingredientList:
        newIngredient = ingredient[0].replace(' ', '_')

        query += "ex:" + newIngredient + " rdf:type fo:Food ."

        query += exTitle + "fo:ingredients _:i" + str(i) + " ."

        query += " _:i" + str(i) + " fo:food ex:" + newIngredient + " ."
        query += " _:i" + str(i) + " fo:quantity " + str(ingredient[1]) + " ."

        if len(ingredient) == 3:
            query += " _:i" + str(i) + " fo:imperial_quantity \"" + ingredient[2] + "\" ."

        query += " _:i" + str(i) + " rdf:type fo:Ingredient ."
        
        i = i + 1

    query += exTitle + "fo:instruction \"" + instructions + "\" . }"
    
    # print(query)
    return query


##
# Insert the recipe into the graph 
def insertRecipe(query):
    sparql.setMethod(POST)
    sparql.setQuery(query)

    results = sparql.query()
    print(results.response.read())

