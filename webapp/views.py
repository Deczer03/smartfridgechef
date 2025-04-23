import requests
from django.shortcuts import render, redirect
from .models import Recipe
from django.conf import settings

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        recipe = Recipe.objects.create(image=image)

        # Analyze the image
        ingredients = analyze_image(recipe.image.path)
        if ingredients:
            recipe.ingredients = ", ".join(ingredients)
            recipe.recipe = generate_recipe_with_spoonacular(ingredients)  # Use Spoonacular
            recipe.save()

        return redirect('view_recipe', recipe_id=recipe.id)
    return render(request, 'upload.html')

def analyze_image(image_path):
    api_url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
    headers = {"Authorization": f"Bearer {settings.HUGGING_FACE_API_KEY}"}

    with open(image_path, "rb") as f:
        response = requests.post(api_url, headers=headers, data=f)

    if response.status_code == 200:
        result = response.json()
        # Extract detected objects (labels)
        ingredients = [item["label"] for item in result if "label" in item]
        return ingredients
    else:
        error_message = response.json().get("error", "Unknown error")
        print(f"API Error: {error_message}")
        return []

def view_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipe.html', {'recipe': recipe})

import requests

def generate_recipe_with_spoonacular(ingredients):
    api_key = "ad2ffd8cc3114424b95c440ba22228ce"
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ",".join(ingredients),
        "number": 1,  # Get one recipe
        "apiKey": api_key,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        if results:
            recipe_id = results[0]["id"]
            return get_recipe_details(recipe_id, api_key)
    return "No recipe found for the given ingredients."

def get_recipe_details(recipe_id, api_key):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("instructions", "No instructions available.")
    return "Failed to fetch recipe details."
#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