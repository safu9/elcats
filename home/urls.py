from django.urls import path

from . import views


app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('project/', views.ProjectListView.as_view(), name='project_list'),
    path('project/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('project/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<slug:slug>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('project/<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]
