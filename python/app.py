from flask import Flask, render_template, request
from query_functions import getRecipeTitle, createIngredientQuery, getTitleAndInstructions, findRecipes

app = Flask(__name__, template_folder='template')

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


if __name__ == '__main__':
    app.run(debug=True)