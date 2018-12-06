from django.urls import include, path

from . import views


app_name = 'wiki'
urlpatterns = [
    path('<slug:project>/wiki/', include([
        path('', views.IndexView.as_view(), name='index'),
        path('create/', views.CreateView.as_view(), name='create'),
        path('<slug:slug>/', views.DetailView.as_view(), name='detail'),
        path('<slug:slug>/update/', views.UpdateView.as_view(), name='update'),
        path('<slug:slug>/delete/', views.DeleteView.as_view(), name='delete'),
    ])),
]
