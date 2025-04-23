from django.db import models

class Recipe(models.Model):
    image = models.ImageField(upload_to='uploads/')
    ingredients = models.TextField(blank=True)
    recipe = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recipe {self.id}"