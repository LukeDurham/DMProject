from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path(r'', views.home, name='home'),
    #path('about', views.about, name='about-view'),
    path(r'signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path(r'signin/', views.signin, name='signin'),
    path(r'signout/', views.signout, name='signout'),
    path('admin/', admin.site.urls),
    path(r'add_car/', views.add_car, name='add-car'),
    path('removecar/', views.removecar, name='removecar'),
    path(r'showdb/', views.showdb, name='showdb'),
    path('about/', views.about, name='about'),
    path(r'searchCars/', views.search_Cars, name='searchCars'),
    path(r'update_cars/<CarID>', views.update_cars, name='update-cars'),
    path(r'showusers/', views.showusers, name='showusers'),

]