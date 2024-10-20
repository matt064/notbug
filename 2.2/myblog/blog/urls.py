from django.urls import path
from django.contrib.auth.views import LoginView

from .views import main_site, post_create, post_update, logout_page, sing_up_page

app_name = 'blog'

urlpatterns = [
    path('', main_site, name='main_site'),
    path('create/', post_create, name='post_create'),
    path('update/<int:pk>/', post_update, name='post_update'),
    
    path('registration/', sing_up_page, name='registration'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', logout_page, name='logout'),
]
