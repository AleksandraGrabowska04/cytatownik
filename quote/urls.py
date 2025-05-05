from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-quotes/', views.my_quotes, name='my_quotes'),
    path('quote_generator/', views.quote_generator, name='quote_generator'),
    path('dodaj/', views.add_quote, name='add_quote'),
    path('edytuj/<int:quote_id>/', views.edit_quote, name='edit_quote'),
    path('usun/<int:quote_id>/', views.delete_quote, name='delete_quote'),
    path('vote/', views.toggle_vote, name='vote'),

    path('dodaj_komentarz/<int:quote_id>', views.add_comment, name='add_comment'),
    path('usun_komentarz/<int:comment_id>', views.delete_comment, name='delete_comment'),

    path('rejestracja/', views.register_view, name='register'),
    path('logowanie/', views.login_view, name='login'),
    path('wyloguj/', views.logout_view, name='logout'),
]
