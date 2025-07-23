from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.task),
    path('task/<int:pk>', views.task),
]
