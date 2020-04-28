from query_functions import createIngredientQuery, getRecipes

prefixRecipe = "PREFIX recipe: <http://schema.org/Recipe/>"

#In Blazegraph:
# prefix recipe: <http://schema.org/Recipe/> 
    
#     SELECT DISTINCT * WHERE {
#         ?x recipe:recipeIngredient ?ingredient
#         FILTER regex(?ingredient, "garlic", "i").
# }


#SELECT recipes based on one ingredient (example: garlic)
getRecipes("" + prefixRecipe + 
    """SELECT DISTINCT * WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER regex(?ingredient, "garlic", "i").
    }
""")

#Can also use CONTAINS(?o, "regex")


#SELECT recipes based on either ingredients (example: chicken OR ham)
getRecipes("" + prefixRecipe + 
    """SELECT DISTINCT * WHERE {
        ?title recipe:recipeIngredient ?ingredient
        FILTER (
            regex(?ingredient, "chicken", "i") ||
            regex(?ingredient, "ham", "i")
        ).
    }
""")


#SELECT recipes based on two ingredients (example: beef AND tomato)
getRecipes("" + prefixRecipe + 
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
getRecipes("" + prefixRecipe + 
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

# Call functions that create a query based on the number of ingrediens
ingrediensquery = createIngredientQuery(["beef", "tomato", "onion"])
getRecipes(ingrediensquery)