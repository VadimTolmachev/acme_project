from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    # path('', views.homepage, name='homepage'),
    path('', views.HomePage.as_view(), name='homepage'),
]
