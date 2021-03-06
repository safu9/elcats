from django.urls import include, path

from . import apis, views


app_name = 'schedule'
urlpatterns = [
    path('api/schedule/participate/', apis.set_participant, name='participant_api'),

    path('user/<str:username>/schedule/', views.UserScheduleView.as_view(), name='user_schedule'),

    path('<slug:project>/schedule/', include([
        path('', views.IndexView.as_view(), name='index'),
        path('week/', views.WeekView.as_view(), name='week'),
        path('week/<int:year>-<int:month>-<int:day>/', views.WeekView.as_view(), name='week'),
        path('month/', views.MonthView.as_view(), name='month'),
        path('month/<int:year>-<int:month>/', views.MonthView.as_view(), name='month'),
        path('create/', views.CreateView.as_view(), name='create'),
        path('<int:pk>/', views.DetailView.as_view(), name='detail'),
        path('<int:pk>/update/', views.UpdateView.as_view(), name='update'),
        path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    ])),
]
