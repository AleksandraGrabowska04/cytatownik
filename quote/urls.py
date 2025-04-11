from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-quotes/', views.my_quotes, name='my_quotes'),
    path('dodaj/', views.add_quote, name='add_quote'),
    path('edytuj/<int:quote_id>/', views.edit_quote, name='edit_quote'),
    path('usun/<int:quote_id>/', views.delete_quote, name='delete_quote'),

    path('rejestracja/', views.register_view, name='register'),
    path('logowanie/', views.login_view, name='login'),
    path('wyloguj/', views.logout_view, name='logout'),
]
