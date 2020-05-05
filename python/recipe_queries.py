from query_functions import createIngredientQuery, getRecipeTitle, getTitleAndInstructions, getAllIngredientsAndInstructions, findRecipes, getTitleAndInstructionsInDictionary, insertRecipe, createInsertRecipeQuery

prefixRecipe = "PREFIX recipe: <http://schema.org/Recipe/>"

#SELECT recipes based on one ingredient (example: garlic)
getRecipeTitle("" + prefixRecipe + 
    """SELECT DISTINCT * WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER regex(?ingredient, "garlic", "i").
    }
""")

#Can also use CONTAINS(?o, "regex")

#SELECT recipes based on either ingredients (example: chicken OR ham)
getRecipeTitle("" + prefixRecipe + 
    """SELECT DISTINCT * WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER (
            regex(?ingredient, "chicken", "i") ||
            regex(?ingredient, "ham", "i")
        ).
    }
""")


#SELECT recipes based on two ingredients (example: beef AND tomato)
getRecipeTitle("" + prefixRecipe + 
    """
    SELECT DISTINCT ?title ?ingredient1 ?ingredient2 WHERE 
    {   
        {
            ?title recipe:recipeIngredient ?ingredient1
            FILTER CONTAINS(?ingredient1, "ground beef") .   
      
            ?title recipe:recipeIngredient ?ingredient2 
            FILTER CONTAINS(?ingredient2, "tomato") .
        }
    }
        
""")

#Having an ingredient that does not match fails the query
#FIX: Want to recipes that matches most of the users' ingredients
#OPTIONAL: Having this as a feature because there may exist no ingredient with all of these ingredients
getRecipeTitle("" + prefixRecipe + 
    """SELECT DISTINCT ?title ?ingredient1 ?ingredient2 ?ingredient3 WHERE 
    {   
        {
            ?title recipe:recipeIngredient ?ingredient1
            FILTER CONTAINS(?ingredient1, "chicken") .   
      
            ?title recipe:recipeIngredient ?ingredient2 
            FILTER CONTAINS(?ingredient2, "tomato") .

            ?title recipe:recipeIngredient ?ingredient3 
            FILTER CONTAINS(?ingredient3, "onion") .
        }
    }
        
""")

#SELECT recipes with instructions based on an ingredient
getTitleAndInstructions("" + prefixRecipe +
    """SELECT DISTINCT ?title ?instructions ?ingredient1 WHERE 
    {
        {
            ?title recipe:recipeInstructions ?instructions .
            
            ?title recipe:recipeIngredient ?ingredient1
            FILTER CONTAINS(?ingredient1, "butter") .

        }
    }    

""")


# Query for getting all ingredients and instructions
# getAllIngredientsAndInstructions("" + prefixRecipe +
#     """SELECT DISTINCT ?title ?ingredient ?instruction WHERE
#     {
#         ?title recipe:recipeIngredient ?ingredient .
#         ?title recipe:recipeInstructions ?instruction
#     }    
# """)



#Query for inserting a recipe 
insertRecipe("""PREFIX recipe: <http://schema.org/Recipe/>
PREFIX ex: <http://example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

INSERT DATA {
	ex:Dolmio_Lasagne rdf:type recipe:name . 
  	ex:Dolmio_Lasagne recipe:recipeIngredient "1 Dolmio Bechamel sauce".
  	ex:Dolmio_Lasagne recipe:recipeIngredient "1 Dolmio Lasagne sauce".
  	ex:Dolmio_Lasagne recipe:recipeIngredient "400 gram minced meat".
  ex:Dolmio_Lasagne recipe:recipeIngredient "100 gram grated cheese".
  ex:Dolmio_Lasagne recipe:recipeIngredient "9 lasagne pasta plates".
  ex:Dolmio_Lasagne recipe:recipeIngredient "2 tbsp butter".
  
  ex:Dolmio_Lasagne recipe:recipeInstructions "Heat butter in a pan. Brown the meat. Pour Dolmio Lasagne sauce and reduce on low heat for 10 min. Start with Dolmio Bechamel and end with it. Layer the sauce and plate. Put cheese on top. Put in oven for 30 min with 200 celsius degree.".
}""")


# USING FUNCTIONS FOR CREATING QUERIES
# Create query for getting titles 
ingrediensquery = createIngredientQuery(["beef", "tomato", "onion"])
getRecipeTitle(ingrediensquery)


# Create query for getting titles and recipe instructions 
titleAndInstructionsQuery = createIngredientQuery(["butter", "garlic"])
result = getTitleAndInstructions(titleAndInstructionsQuery)

# Find recipes with matching ingredients
findRecipes(["beef", "tomato", "onion"])

# Insert new recipe 
title = "Basic Pizza"
ingredientList = ["1 box chopped tomatoes", "1 pizza dough", "100 gram grated cheese"]
instruction = "Roll out pizza dough. Spread chopped tomatoes. Put cheese on top. Put pizza in oven for 15 min with 200 degree celsius."
createInsertRecipeQuery(title, ingredientList, instruction)

title = "Glass Milk"
ingredientList = ["1 empty glass, 3 dl milk"]
instruction = "Pour glass in milk. Drink"
query = createInsertRecipeQuery(title, ingredientList, instruction)
insertRecipe(query)

findRecipes(["glass"])
