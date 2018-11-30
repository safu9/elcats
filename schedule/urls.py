from django.urls import path

from . import views


app_name = 'schedule'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('week/', views.WeekView.as_view(), name='week'),
    path('week/<int:year>-<int:month>-<int:day>/', views.WeekView.as_view(), name='week'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.UpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
]
