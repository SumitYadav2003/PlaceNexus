from django.urls import path
from .views import prepare_view

urlpatterns = [

    path(
        'ai-preparation/',
        prepare_view,
        name='ai_preparation'
    ),

]