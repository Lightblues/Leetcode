from typing import List
import collections
import math
import bisect

class SolutionD68:
    def mostWordsFound(self, sentences: List[str]) -> int:
        words = [len(s.split(' ')) for s in sentences]
        return max(words)

    """ 2115. 从给定原材料中找到所有可以做出的菜 """
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        result = []
        def rec():
            changed = False
            for recipe, ingredient in zip(recipes, ingredients):
                if all(i in supplies for i in ingredient):
                    result.append(recipe)
                    supplies.append(recipe)
                    changed = True
                    recipes.remove(recipe)
                    ingredients.remove(ingredient)
            return changed
        while rec():
            continue
        return result

sol = SolutionD68()
result = [
    sol.findAllRecipes(["bread","sandwich"], [["yeast","flour"],["bread","meat"]], ["yeast","flour","meat"])
]
for r in result:
    print(r)