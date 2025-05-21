from recipe.models import Recipe, Category
from django.shortcuts import render
from django.db.models import Count

def main(request):
    recipes = Recipe.objects.all()[:5]
    return render(request, 'main.html', {'recipes': recipes})

def category_list(request):
    categories = Category.objects.annotate(recipe_count=Count('categories')) # для кожного об'єкта додаємо нове поле
    return render(request, 'category_list.html', {'categories': categories})
