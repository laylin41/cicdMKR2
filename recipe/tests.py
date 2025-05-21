from django.test import TestCase
from django.urls import reverse
from recipe.models import Recipe, Category

class RecipeViewsTestCase(TestCase):

    def setUp(self):
        # Створимо кілька категорій і рецептів для тестування
        self.category1 = Category.objects.create(name="Dessert")
        self.category2 = Category.objects.create(name="Main Course")

        for i in range(7):
            Recipe.objects.create(
                title=f"Recipe {i}",
                description=f"Description {i}",
                instructions="Do something",
                ingredients="Some ingredients",
                category=self.category1 if i % 2 == 0 else self.category2
            )

    def test_main_view_returns_5_latest_recipes(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200) # перевіряємо що сторінка відкривається
        self.assertTemplateUsed(response, 'main.html') # перевіряємо що використовується правильний шаблон

        recipes = response.context['recipes']
        self.assertEqual(len(recipes), 5) # перевіряємо що повертається тільки 5 об'єктів
        self.assertTrue(all(isinstance(r, Recipe) for r in recipes)) # перевіряємо що ці об'єкти - це Рецепти

    def test_category_list_view_counts_recipes(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200) # перевіряємо що сторінка відкривається
        self.assertTemplateUsed(response, 'category_list.html') # перевіряємо що використовується правильний шаблон

        categories = response.context['categories'] 
        self.assertEqual(len(categories), 2) # перевіряємо що категорій стільки скільки ми задали в setUp

        # Перевірка що підрахунок рецептів був правильний
        for category in categories:
            if category.name == "Dessert":
                self.assertEqual(category.recipe_count, Recipe.objects.filter(category=self.category1).count())
            elif category.name == "Main Course":
                self.assertEqual(category.recipe_count, Recipe.objects.filter(category=self.category2).count())
