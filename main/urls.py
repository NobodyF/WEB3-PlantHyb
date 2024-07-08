from .urls_api import urlpatterns as api_urls
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import views

app_name = "main"

urlpatterns = [
    path('', views.base, name="base"),
    path('checklogin/', views.checklogin, name="checklogin"),
    path('logout/', views.logout_one, name="logout"),
    path('home/', views.home, name='home'),
    path('hybridizations/', views.hybridizations, name='hybridizations'),
    path('plants/', views.plants, name='plants'),
    path('add_plant/', views.add_plant, name='add_plant'),
    path('hybrids/', views.hybrids, name='hybrids'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('api/', include(api_urls)),
    path('login/', views.login_view, name='login'),
    path('plant_hybridization', views.plant_hybridization, name='moralis_auth'),
    path('request_message', views.request_message, name='request_message'),
    path('profile/', views.profile, name='profile'),
    path('verify_message', views.verify_message, name='verify_message'),
    path('plants/<str:plant_id>/', views.show_plant_details, name='show_plant_details'),
    path('perform_hybridization/', views.perform_hybridization, name='perform_hybridization'),
    path('hybridization_results', views.hybridization_results, name='hybridization_results1'),
    path('hybridization_results/<str:parent1_id>/<str:parent2_id>', views.hybridization_results, name='hybridization_results'),

    
]
