from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, FOAF, RDFS, OWL
import pandas as pd
from rdflib.collection import Collection

g = Graph()
ex = Namespace("http://example.org/")
recipe = Namespace('https://schema.org/Recipe')
Allergy = Namespace('http://purl.bioontology.org/ontology/SNOMEDCT/90260006')
g.bind("ex", ex)
g.bind('allergy', Allergy)

# Load the CSV data as a pandas Dataframe.
csv_data = pd.read_csv("recipes2.csv")

# Here I deal with spaces (" ") in the data. I replace them with "_" so that URI's become valid.
csv_data = csv_data.replace(to_replace=" ", value="_", regex=True)

# Here I mark all missing/empty data as "unknown". This makes it easy to delete triples containing this later.
csv_data = csv_data.fillna("unknown")

# Loop through the CSV data, and then make RDF triples.
for index, row in csv_data.iterrows():
    subject = row['Title']
    #g.add((URIRef(ex + subject), RDF.type, URIRef(ex + row['Allergen1'])))
    #g.add((URIRef(ex + subject), RDF.type, URIRef(ex + row['Allergen2'])))
    #g.add((URIRef(ex + subject), RDF.type, URIRef(ex + row['Allergen3'])))
    g.add((URIRef(ex + subject), Allergy.Allergen, Literal(row["Allergen1"])))
    g.add((URIRef(ex + subject), Allergy.Allergen, Literal(row["Allergen2"])))
    g.add((URIRef(ex + subject), Allergy.Allergen, Literal(row["Allergen3"])))


allergenList = []

for i in range(21, 23):
    allergenList.append("Allergen" + str(i))

def nodeAllergen(subject, row):
    for i in range(21, 23):
        if (row[allergenList[i]] != "unknown"):
            g.add((URIRef(ex + subject), URIRef(Allergy.Allergen), Literal(row[allergenList[i]])))




# I remove triples that I marked as unknown earlier.
g.remove((None, None, URIRef("http://example.org/unknown")))

# Clean printing of the graph.
g.serialize(destination="recipe_triples2.txt", format="turtle")
print(g.serialize(format="turtle").decode())
