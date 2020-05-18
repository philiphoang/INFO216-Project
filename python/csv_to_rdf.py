from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, FOAF, RDFS, OWL
from rdflib.collection import Collection

import pandas as pd

g = Graph()
ex = Namespace("http://example.org/")

Recipe = Namespace("http://schema.org/Recipe/")


#Food Ontology from BBC, an extension of other schemas
fo = Namespace("https://bbc.co.uk/ontologies/fo/")  

g.bind("ex", ex)
g.bind("recipe", Recipe)
g.bind("fo", fo)


#Add ingredient-, quantity-, and unitstring to list 
ingredientList = []
quantityList = []
unitList = []

for i in range(1, 20):
    ingredientList.append("Ingredient" + str(i))   
    quantityList.append("Quantity" + str(i))
    unitList.append("Unit" + str(i))


#Read data
csv_data = pd.read_csv("recipes.csv")

#Replace quotations
csv_data = csv_data.replace(to_replace='"', value="", regex=True) 

#Replace commas
csv_data = csv_data.replace(to_replace=",", value="", regex=True) 

#Replace space with underscore
#sv_data = csv_data.replace(to_replace=" ", value="_", regex=True) 

#Replace underscore with space for column Directions
#csv_data["Directions"] = csv_data["Directions"].replace(to_replace="_", value=" ", regex=True) 

csv_data["Title"] = csv_data["Title"].replace(to_replace=" ", value="_", regex=True)

for ingredient in ingredientList:
    csv_data[ingredient] = csv_data[ingredient].replace(to_replace=" ", value="_", regex=True)

#Fill empty cells with unknown
csv_data = csv_data.fillna("unknown")


#1. Title
#2. Directions
#3. Quantity01
#4. Unit01
#5. Ingredient01
#6. Quantity02
#7. Unit02
#8. Ingredient02
# ...
#20. Category


#TODO 
#Place the values into approptriate RDF literals (replace ex)

# RECIPE SETUP:
# Give title an appropriate namespace (Recipe or such)
# Give each ingredient in the recipe its own node (Ingredient has a literal)
# Place quantity and unit in the ingredient node (Give them each literals)

#Example (Usage pf schema.org/Recipe):
# name:Zucchi Patties
#     recipeIngredient: 1 garlic clove
#     recipeIngredient: 1 tablespoon parmesan cheese
#     recipeInstructions: description of recipe

#Example: 
#g.add((ex.Zucchi_Patties, RDF.type, Thing.name))
#g.add((ex.Zucchi_Patties, Recipe.recipeIngredient, Literal("1 garlic clove")))

#Adding ingredient, quantity and unit to one same node 
def oneNode(subject, row):
    for i in range(19):
        if (row[ingredientList[i]] != "unknown"):
            if (row[quantityList[i]] != "unknown"):
                    if (row[unitList[i]] != "unknown"):
                        g.add((URIRef(ex + subject), URIRef(Recipe.recipeIngredient), 
                            Literal(row[quantityList[i]] + " " + row[unitList[i]] + " " + row[ingredientList[i]])))
                    else:
                        g.add((URIRef(ex + subject), URIRef(Recipe.recipeIngredient), 
                            Literal(row[quantityList[i]] + " " + row[ingredientList[i]])))

#Adding ingredient to one node, and unit and quantity to another node
def twoNodes(subject, row):
    for i in range(0, 19): 
        if (row[ingredientList[i]] != "unknown"):
            g.add((URIRef(ex + subject), URIRef(Recipe.recipeIngredient), Literal(row[ingredientList[i]])))
            
            if (row[quantityList[i]] != "unknown"):
                if (row[unitList[i]] != "unknown"):
                    g.add((URIRef(ex + subject), URIRef(ex + "quantity"), Literal(row[quantityList[i]] + " " + row[unitList[i]])))
                else:
                    g.add((URIRef(ex + subject), URIRef(ex + "quantity"), Literal(row[quantityList[i]])))

#Adding all of them to three different nodes 
def threeNodes(subject, row):
    for i in range(0, 19): 
        if (row[ingredientList[i]] != "unknown"):
            g.add((URIRef(ex + subject), URIRef(Recipe.recipeIngredient), Literal(row[ingredientList[i]])))
            
            if (row[quantityList[i]] != "unknown"):
                g.add((URIRef(ex + subject), URIRef(ex + "quantity"), Literal(row[quantityList[i]])))
                if (row[unitList[i]] != "unknown"):
                    g.add((URIRef(ex + subject), URIRef(ex + "quantity"), Literal(row[unitList[i]])))


for index, row in csv_data.iterrows():
    subject = row["Title"]
    
    #Recipe is a type of fo:Recipe
    g.add((URIRef(ex + subject), RDF.type, fo.Recipe))

    #A recipe has an instruction
    g.add((URIRef(ex + subject), fo.instruction, Literal(row["Directions"])))

    
    bnode = BNode()
    #Add Ingredient to Recipe
    g.add((URIRef(ex + subject), fo.ingredients, bnode))

    list_ingredients = []
    Collection(g, bnode, list_ingredients)
    for i in range(0, 19):
        #list_ingredients.append(URIRef(ex + ingredient))

        ingredient = row[ingredientList[i]]

        list_ingredients.append(URIRef(ex + ingredient))  

        #Ingredient is a type of fo:Ingredient
        if (row[ingredientList[i]] != "unknown"):
            g.add((URIRef(ex + ingredient), RDF.type, fo.Food))

            if (row[quantityList[i]] != "unknown"):
                #Add quantity to Ingredient
                g.add((URIRef(ex + ingredient), fo.quantity, Literal(row[quantityList[i]])))
                
                if (row[unitList[i]] != "unknown"):
                    #Add unit to Ingredient
                    g.add((URIRef(ex + ingredient), fo.imperial_quantity, Literal(row[unitList[i]])))

    Collection(g, bnode, list_ingredients)
    

    




#Remove nodes marked unknown 
g.remove((None, None, URIRef("http://example.org/unknown")))

# Writing the graph to a file on your system. Possible formats = turtle, n3, xml, nt.
g.serialize(destination="recipe_triples.txt", format="turtle")

print(g.serialize(format="turtle").decode())


## Example (Ideal)
# ex:Cake a fo:Recipe
#   fo:Ingredient (
#       ex:Egg
#           fo:quantity "2"
#       ex:Milk
#           fo:quantity "3"
#           fo:unit "dl"
#       ex:Sugar
#           fo:quantity "100"
#           fo:unit "gram"
#       ex:Flour
#           fo:quantity "500"
#           fo:unit "gram"    
#   )
#   recipe:recipeInstructions "Mix all ingredients togheter"

## Adding an ingredient and its quantity and unit 
#g.add(ex:ingredient, RDF.type, fo:Ingredient)
#g.add(ex:ingredient, fo:quantity, Literal(...))
#g.add(ex:ingredient, fo:imperial_quantity, Literal(..)) (same as unit)

## Something to think about 
#1. Somehow add Blank Node to Ingredient, make it contain unit and metric 
#2. Label??? -> label("ingredient quantity unit"), show this string 
#3. Use owl:sameAs for the same unit (example: Tablespoon, Tbsp)
#4. fo:Food is a singular item 
#5. fo:Ingredient is a combination of quantity and a food

## PROBLEM:
# 1. Make quantity and unit appear under the ingredients for each recipe
#    At the momemt, all the quantities and units appear under the same ingredient



##
# Making the data more semantic

# Giving the subjet RDF type of Recipe.name 
# g.add((URIRef(ex + subject), URIRef(ex + RDF.type), Recipe.name))

# # 
# node_ingredients = BNode()
# g.add((URIRef(ex + subject), Recipe.recipeIngredients, node_ingredients))

# list_ingredients = [URIRef(ex + ingredient)]

# list_ingredients.append()
# Collection(g, )