from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.index_view, name='resumebuild'),
    path('job_recommendations/', views.job_recommendations, name='job_recommendations'),
]
