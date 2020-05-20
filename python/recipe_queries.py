from query_functions import createIngredientQuery, getRecipeTitle, getTitleAndInstructions, getAllInformationOfARecipe, findRecipes, getTitleAndInstructionsInDictionary, insertRecipe, createInsertRecipeQuery

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

## USING FUNCTIONS TO CREATE QUERIES

#Create query for getting titles for a set of ingredients 
ingrediensquery = createIngredientQuery(["cheese", "salt"])
getTitleAndInstructions(ingrediensquery)

#Create query for getting titles and recipe instructions 
titleAndInstructionsQuery = createIngredientQuery(["butter", "garlic"])
result = getTitleAndInstructions(titleAndInstructionsQuery)

#Find recipes with matching ingredients
findRecipes(["salt", "butter", "flour"])
