# INFO216-Project

Dataset from https://github.com/cweber/cookbook/blob/master/recipes.csv  
Schema from http://schema.org

The dataset is modified to fit better to our program.

To run the program (local): 
1. Install blazegraph and start it with 

```java -server -Xmx4g -jar blazegraph.jar```


2. Install necessary package to python 

```pip install flask```


3. Execute csv_to_rdf.py to get the data in turtle-format, will return a file named recipe_triples.txt)

```python csv_to_rdf.py```


4. Put the file into blazegraph in the UPDATE tab


5. Run app.py and click on the address for the server (or copy the address to a webbrowser)

```python app.py```
