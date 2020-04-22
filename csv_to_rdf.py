from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, FOAF, RDFS, OWL
import pandas as pd

g = Graph()
ex = Namespace("http://example.org/")
Recipe = Namespace("http://schema.org/Recipe/")

g.bind("ex", ex)
g.bind("recipe", Recipe)

#Read data
csv_data = pd.read_csv("recipes.csv")

#Replace quotations
csv_data = csv_data.replace(to_replace='"', value="", regex=True) 

#Replace commas
csv_data = csv_data.replace(to_replace=",", value="", regex=True) 

#Replace space with underscore
csv_data["Title"] = csv_data["Title"].replace(to_replace=" ", value="_", regex=True) 

#Replace underscore with space for column Directions
#csv_data["Directions"] = csv_data["Directions"].replace(to_replace="_", value=" ", regex=True) 

#Fill empty cells with unknown
csv_data = csv_data.fillna("unknown")

#Add ingredient-, quantity-, and unitstring to list 
ingredientList = []
quantityList = []
unitList = []

for i in range(1, 20):
    ingredientList.append("Ingredient" + str(i))   
    quantityList.append("Quantity" + str(i))
    unitList.append("Unit" + str(i))

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

    #g.add((URIRef(ex + subject), URIRef(ex + "title"), Literal(subject)))

    #g.add((URIRef(ex + subject), URIRef(ex + "directions"), Literal(row["Directions"])))

    g.add((URIRef(ex + subject), RDF.type, Recipe.name))

    g.add((URIRef(ex + subject), Recipe.recipeInstructions, Literal(row["Directions"])))

    oneNode(subject, row)


g.remove((None, None, URIRef("http://example.org/unknown")))


print(g.serialize(format="turtle").decode())



