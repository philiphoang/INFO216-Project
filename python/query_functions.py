from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, POST 
from rdflib import Graph, Literal, Namespace, URIRef

## Prefixes
prefixFo = "PREFIX fo: <https://bbc.co.uk/ontologies/fo/>"
prefixEx = "PREFIX ex: <http://example.org/>"
prefixRdf = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"

## Connection to Blazegraph
sparql = SPARQLWrapper("http://localhost:9999/blazegraph/sparql")

##
# Function for creating queries for a set of ingredients
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
# Create a string for filtering for an ingredient 
def addIngredientToQuery(i, ingredient):
    newIngredient = ingredient.replace(' ', '_')
    return "?title fo:ingredients ?ingredient" + i + " BIND (ex:" + newIngredient + " as ?i" + i + ") ?ingredient" + i + " fo:food ?i" + i + " ."
    

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
        instructionList.append(result["instruction"]["value"])
        print(result["instruction"]["value"])

    return titleList, instructionList

##
# Get a dictionary containing title and instructions
def getTitleAndInstructionsInDictionary(query):
    results = parseQuery(query)

    print(results)

    d = {}
    for result in results["results"]["bindings"]:
        title = result["title"]["value"]
        instruction = result["instruction"]["value"]

        if (title not in d.keys()):
            d[title] = instruction

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

    allRecipeDict = getAllIngredientsAndInstructions("" + prefixFo + prefixEx +
        """SELECT DISTINCT ?title ?ingredient ?instruction WHERE
        {
            ?title fo:instruction ?instruction .
          
            ?title fo:ingredients ?food .
           
            ?food fo:food ?ingredient .
        }    
    """)

    resultDict = {}

    for title in allRecipeDict.keys():
        if (title in titleAndInstructionDict):
            resultDict[title] = allRecipeDict[title]

            resultDict.get(title).insert(len(resultDict.get(title)),  titleAndInstructionDict[title])

    print(resultDict)
    return resultDict

##
# Create an insertion query based on title, ingredients and instructions 
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
    
    print(query)
    return query


##
# Insert the recipe into the graph 
def insertRecipe(query):
    sparql.setMethod(POST)
    sparql.setQuery(query)

    results = sparql.query()
    print(results.response.read())