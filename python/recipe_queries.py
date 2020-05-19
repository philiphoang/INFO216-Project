from query_functions import createIngredientQuery, getRecipeTitle, getTitleAndInstructions, getAllIngredientsAndInstructions, findRecipes, getTitleAndInstructionsInDictionary, insertRecipe, createInsertRecipeQuery

#Prefixes 
prefixFo = "PREFIX fo: <https://bbc.co.uk/ontologies/fo/>"
prefixEx = "PREFIX ex: <http://example.org/>"

#SELECT recipe titles based on one ingredient (example: salt)
getRecipeTitle("" + prefixFo + prefixEx +
    """SELECT DISTINCT ?title WHERE {
             
        ?title fo:ingredients ?ingredient1 . 
        
        BIND (ex:salt as ?i1)
        ?ingredient1 fo:food ?i1 .  
                
    }
""")



# #SELECT recipe titles based on three ingredients (example: beef AND tomato)
getRecipeTitle("" + prefixFo + " " + prefixEx + 
    """SELECT DISTINCT ?title ?i1 ?i2 ?i3 WHERE 
    {   
        
        ?title fo:ingredients ?ingredient1 . 
        BIND (ex:salt as ?i1) 
	    ?ingredient1 fo:food ?i1 .    	
      
        ?title fo:ingredients ?ingredient2 . 
        BIND (ex:butter as ?i2)
	    ?ingredient2 fo:food ?i2.  

        ?title fo:ingredients ?ingredient3 . 
        BIND (ex:flour as ?i3)
        ?ingredient3 fo:food ?i3.  
      
    }      
    
""")


## USING FUNCTIONS FOR CREATING QUERIES

#Create query for getting titles for a set of ingredients 
ingrediensquery = createIngredientQuery(["cheese", "salt"])
getTitleAndInstructions(ingrediensquery)

#Create query for getting titles and recipe instructions 
titleAndInstructionsQuery = createIngredientQuery(["butter", "garlic"])
result = getTitleAndInstructions(titleAndInstructionsQuery)

#Find recipes with matching ingredients
findRecipes(["salt", "butter", "flour"])

#Insert new recipes 
title = "Basic_Pizza"
ingredientList = [["Pizza dough", 1], ["Tomato sauce", 1, "glass"], ["grated cheese", 100, "gram"]]
instruction = "Roll out pizza dough. Spread chopped tomatoes. Put cheese on top. Put pizza in oven for 15 min with 200 degree celsius."
query = createInsertRecipeQuery(title, ingredientList, instruction)
insertRecipe(query)

#Search for the new recipe containing glass
findRecipes(["Pizza_Dough"])
