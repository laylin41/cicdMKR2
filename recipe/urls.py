from django.urls import path
from . import views

urlpatterns=[
path('', views.main, name='main'),
path('category/', views.category_list, name='category_list')
]
