from query_functions import createIngredientQuery, getRecipeTitle, getTitleAndInstructions

prefixRecipe = "PREFIX recipe: <http://schema.org/Recipe/>"

#In Blazegraph:
# prefix recipe: <http://schema.org/Recipe/> 
    
#     SELECT DISTINCT * WHERE {
#         ?x recipe:recipeIngredient ?ingredient
#         FILTER regex(?ingredient, "garlic", "i").
# }


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

# Create query for getting titles 
ingrediensquery = createIngredientQuery(["beef", "tomato", "onion"])
getRecipeTitle(ingrediensquery)


# Create query for getting titles and recipe instructions 
titleAndInstructionsQuery = createIngredientQuery(["butter", "garlic"])
result = getTitleAndInstructions(titleAndInstructionsQuery)

print(result[1])