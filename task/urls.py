from django.urls import include, path

from . import apis, views


app_name = 'task'
urlpatterns = [
    path('<slug:project>/task/', include([
        path('', views.IndexView.as_view(), name='index'),
        path('board/', views.BoardView.as_view(), name='board'),
        path('gantt/', views.GanttView.as_view(), name='gantt'),
        path('create/', views.CreateView.as_view(), name='create'),
        path('<int:pk>/', views.DetailView.as_view(), name='detail'),
        path('<int:pk>/update/', views.UpdateView.as_view(), name='update'),
        path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    ])),

    path('api/task/state/', apis.set_state, name='state_api'),
]
