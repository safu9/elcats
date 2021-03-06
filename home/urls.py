from django.urls import path

from . import views


app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<slug:slug>/settings/', views.ProjectSettingsView.as_view(), name='project_settings'),
    path('<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]
