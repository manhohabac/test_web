# test_app/urls.py

from django.urls import path
from .views import home, start_test, test_view, flip_view, next_card_view, check_answer_view
from .views import register_view, login_view, logout_view, result_page, upload_csv, export_results
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login_view, name='login'),  # Default to login view
    path('home/', home, name='home'),
    path('start_test/', start_test, name='start_test'),
    path('test/', test_view, name='test'),
    path('flip/', flip_view, name='flip'),
    path('next_card/', next_card_view, name='next_card'),
    path('check_answer/', check_answer_view, name='check_answer'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('result_page/', result_page, name='result'),
    path('upload_csv/', upload_csv, name='upload_csv'),
    path('export_results/', export_results, name='export_results'),
]
