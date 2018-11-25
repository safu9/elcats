from django.urls import path

from . import views


app_name = 'chat'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.ChannelView.as_view(), name='channel'),
    path('new/<int:pk>/', views.NewChannelView.as_view(), name='new_channel'),
]
