from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, FOAF, RDFS, OWL, XSD
from rdflib.collection import Collection

import pandas as pd

g = Graph()

ex = Namespace("http://example.org/")

#Food Ontology from BBC, an extension of other schemas
fo = Namespace("https://bbc.co.uk/ontologies/fo/")  

g.bind("ex", ex)
g.bind("fo", fo)

#Add ingredient-, quantity-, and unitstring to list 
ingredientList = []
quantityList = []
unitList = []

#Create lists that contains the name of the columns in the dataset, used for iterating
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

#Make URI valid by replacing space with underscore
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

# Loop through the CSV data, and then make RDF triples
for index, row in csv_data.iterrows():
    subject = row["Title"]
    
    #Recipe is a type of fo:Recipe
    g.add((URIRef(ex + subject), RDF.type, fo.Recipe))

    #A recipe has an instruction
    g.add((URIRef(ex + subject), fo.instruction, Literal(row["Directions"], datatype=XSD.string)))

    for i in range(0, 19):
        #list_ingredients.append(URIRef(ex + ingredient))

        if (row[ingredientList[i]] != "unknown"):
            ingredient = row[ingredientList[i]]

            #Ingredient is a type of fo:Food
            g.add((URIRef(ex + ingredient), RDF.type, fo.Food))
            
            #Blank node to create an ingredient (an ingredient is a combination of a food, quantity and unit)
            bnode_ingredient = BNode()

            #Recipe has an ingredient
            g.add((URIRef(ex + subject), fo.ingredients, bnode_ingredient))

            #Add food to ingredient (blank node)
            g.add((bnode_ingredient, fo.food, URIRef(ex + ingredient)))

            if (row[quantityList[i]] != "unknown"):
                #Add quantity to ingredient (blank node)
                g.add((bnode_ingredient, fo.quantity, Literal(row[quantityList[i]], datatype=XSD.positiveInteger)))

                if (row[unitList[i]] != "unknown"):
                    #Add unit to ingredient (blank node)
                    g.add((bnode_ingredient, fo.imperial_quantity, Literal(row[unitList[i]])))
            
        #Give the blank node a class    
        g.add((bnode_ingredient, RDF.type, fo.Ingredient))
    

#Remove nodes marked unknown 
g.remove((None, None, URIRef("http://example.org/unknown")))

# Writing the graph to a file on your system. Possible formats = turtle, n3, xml, nt.
g.serialize(destination="recipe_triples.txt", format="turtle")

print(g.serialize(format="turtle").decode())