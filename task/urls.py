from django.urls import include, path

from . import apis, views


app_name = 'task'
urlpatterns = [
    path('api/task/state/', apis.set_state, name='state_api'),

    path('user/<str:username>/task/', views.UserTaskView.as_view(), name='user_task'),

    path('<slug:project>/task/', include([
        path('', views.IndexView.as_view(), name='index'),
        path('board/', views.BoardView.as_view(), name='board'),
        path('gantt/', views.GanttView.as_view(), name='gantt'),
        path('create/', views.CreateView.as_view(), name='create'),
        path('<int:number>/', views.DetailView.as_view(), name='detail'),
        path('<int:number>/update/', views.UpdateView.as_view(), name='update'),
        path('<int:number>/delete/', views.DeleteView.as_view(), name='delete'),
    ])),
]
