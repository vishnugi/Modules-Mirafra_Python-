from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_person, name='add_person'),
    path('list/', views.person_list, name='person_list'),
]