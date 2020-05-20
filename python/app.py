from flask import Flask, render_template, request, url_for, redirect
from query_functions import getRecipeTitle, createIngredientQuery, insertRecipe, getTitleAndInstructions, findRecipes, createInsertRecipeQuery

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

##
# Function that listen to page index.html 
# The page takes the user input, creates a SELECT query, and shows the result
@app.route("/", methods=["POST"])
def getvalue():
    ingredientList = []
    if ("ingredient1" in request.form):
        ingredientList.append(request.form["ingredient1"])

    if ("ingredient2" in request.form):
        ingredientList.append(request.form["ingredient2"])
    
    if ("ingredient3" in request.form):
        ingredientList.append(request.form["ingredient3"])
    
    if ("ingredient4" in request.form):
        ingredientList.append(request.form["ingredient4"])
    
    if ("ingredient5" in request.form):
        ingredientList.append(request.form["ingredient5"])
    
    recipes = findRecipes(ingredientList)


    return render_template("recipes.html", recipes = recipes)

##
# Function that listen to page recipes.html 
# It takes the user input, creates an INSERT query, and shows the result on a new page
@app.route("/add_recipe", methods=["POST"])
def addvalue():
    title = request.form["title"] 

    ingredientList = []
    foodList = []
    addFieldIfNotEmpty("1", ingredientList, foodList)
    addFieldIfNotEmpty("2", ingredientList, foodList)
    addFieldIfNotEmpty("3", ingredientList, foodList)
    addFieldIfNotEmpty("4", ingredientList, foodList)
    addFieldIfNotEmpty("5", ingredientList, foodList)

    instructions = request.form["instructions"]

    query = createInsertRecipeQuery(title, ingredientList, instructions)
    insertRecipe(query)

    recipes = findRecipes(foodList)

    return render_template("recipes.html", recipes = recipes)

##
# Check if the fields are not empty
# If not empty, read the user input 
def addFieldIfNotEmpty(fieldnr, ingredientList, foodList):
    if ("food"+str(fieldnr) in request.form):
        ingredient1 = []
        ingredient1.append(request.form["food"+str(fieldnr)])
        foodList.append(request.form["food"+str(fieldnr)])
        
        if ("quantity"+str(fieldnr) in request.form):
            ingredient1.append(request.form["quantity"+str(fieldnr)])

            if ("unit"+str(fieldnr) in request.form):
                ingredient1.append(request.form["unit"+str(fieldnr)])

        ingredientList.append(ingredient1)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    return render_template("add_recipe.html")

    
@app.route("/index.html", methods=["GET", "POST"])
def home():
    return render_template("index.html")
    

if __name__ == '__main__':
    app.run(debug=True)