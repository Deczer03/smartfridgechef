from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('recipe/<int:recipe_id>/', views.view_recipe, name='view_recipe'),
]