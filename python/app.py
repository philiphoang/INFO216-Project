from flask import Flask, render_template, request
from query_functions import getRecipes

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
        return render_template('index.html')

@app.route("/", methods=["POST"])
def getvalue():
    ingredient1 = request.form["ingredient1"]
    ingredient2 = request.form["ingredient2"]

    ingredientList = []
    ingredientList.append(ingredient1)
    ingredientList.append(ingredient2)

    resultList = getRecipes(ingredientList)
    resultList = list(dict.fromkeys(resultList))

    return render_template("recipes.html", resultList=resultList)

if __name__ == '__main__':
    app.run(debug=True)