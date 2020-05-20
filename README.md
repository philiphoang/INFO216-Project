# INFO216-Project

Recipe Dataset: https://github.com/cweber/cookbook/blob/master/recipes.csv  
BBC Food Ontology: https://www.bbc.co.uk/ontologies/fo
Download Blazegraph here: https://github.com/blazegraph/database/releases/tag/BLAZEGRAPH_2_1_6_RC

The dataset is modified to fit better to our program.

To run the program (local): 
1. Install Blazegraph and start it with 

```java -server -Xmx4g -jar blazegraph.jar```


2. Install necessary package to python for running the application

```pip install flask```


3. Execute csv_to_rdf.py to get the data in turtle-format, will return a file named recipe_triples.txt

```python csv_to_rdf.py```


4. Put recipe_triples.txt into Blazegraph in the UPDATE tab through localhost (default is localhost:9999)


5. Run app.py and click on the address for the server (or copy the address to a webbrowser)

```python app.py```
