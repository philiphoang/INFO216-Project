from flask import Flask, render_template, request, url_for, redirect
from query_functions import getRecipeTitle, createIngredientQuery, insertRecipe, getTitleAndInstructions, findRecipes, createInsertRecipeQuery

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

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


@app.route("/add_recipe", methods=["POST"])
def addvalue():
    title = request.form["title"] 

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
    
    instructions = request.form["instructions"]

    query = createInsertRecipeQuery(title, ingredientList, instructions)
    insertRecipe(query)

    recipes = findRecipes(ingredientList)

    return render_template("recipes.html", recipes = recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    return render_template("add_recipe.html")

    
@app.route("/index.html", methods=["GET", "POST"])
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)