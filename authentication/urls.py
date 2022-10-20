from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    #path('about', views.about, name='about-view'),
    path(r'signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path(r'signin/', views.signin, name='signin'),
    path(r'signout/', views.signout, name='signout'),
    path('admin/', admin.site.urls),
]