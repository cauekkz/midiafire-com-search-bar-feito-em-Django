from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('requests', views.requests, name='requests'),
    path('upload', views.upload, name='upload'),
    path('file/<str:fileName>/download', views.download_file, name='download'),
    path('file/<str:fileName>', views.fileName, name='fileName'),
    path('allowUser',views.allowUser, name='allowUser'),
    path('perfil/<str:username>', views.perfil, name='perfil'),
    path('search', views.search, name='search'),
    path('settings', views.settings_perfil, name='settings')
    
]