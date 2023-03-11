from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

app_name = 'root'
urlpatterns = [
    path('', index, name='index'),
    path('documents', documents, name='documents'),
    path('upload_file', upload_file, name='upload_file'),
    path('download_file', download_file, name='download_file'),
    path('invalid_call', invalid_call, name='invalid_call'),
    path('login/', LoginView.as_view(template_name='root/login.html')),
	path('logout/', LogoutView.as_view(next_page='/')),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('add_task', add_task, name='add_task'),
    path('delete_task', delete_task, name='delete_task'),
    path('high_security_page', high_security_page, name='high_security_page'),
    path('download_secrets', download_secrets, name='download_secrets'),
    path('shoppinglist/', ShoppinglistView.as_view(), name='shoppinglist'),
    path('add_item', add_item, name='add_item'),
    path('delete_item', delete_item, name='delete_item'),    
]