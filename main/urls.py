from .urls_api import urlpatterns as api_urls
from django.urls import path, include
from main import views

app_name = "main"

urlpatterns = [
    path('',                                                    views.base,                  name='base'),
    path('checklogin/',                                         views.checklogin,            name='checklogin'),
    path('logout/',                                             views.logout_one,            name='logout'),
    path('home/',                                               views.home,                  name='home'),
    path('login/',                                              views.login_view,            name='login'),
    path('profile/',                                            views.profile,               name='profile'),

    # Plants
    path('plants/',                                             views.plants,                name='plants'),
    path('plants/<str:plant_id>/',                              views.show_plant_details,    name='show_plant_details'),
    path('add_plant/',                                          views.add_plant,             name='add_plant'),

    # Hybridization
    path('hybridizations/',                                     views.hybridizations,        name='hybridizations'),
    path('hybrids/',                                            views.hybrids,               name='hybrids'),
    path('perform_hybridization/',                              views.perform_hybridization, name='perform_hybridization'),
    path('hybridization_results/',                              views.hybridization_results, name='hybridization_results1'),
    path('hybridization_results/<str:parent1_id>/<str:parent2_id>/', views.hybridization_results, name='hybridization_results'),

    # Moralis Web3 auth — FIXED: plant_hybridization stub replaced with login_view
    path('moralis_auth/',                                       views.login_view,            name='moralis_auth'),
    path('request_message/',                                    views.request_message,       name='request_message'),
    path('verify_message/',                                     views.verify_message,        name='verify_message'),

    # Contact
    path('contact-us/',                                         views.contact_us,            name='contact_us'),

    # REST API
    path('api/',                                                include(api_urls)),
]