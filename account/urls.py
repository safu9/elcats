from django.urls import path

from . import views


app_name = 'account'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('user/', views.UserView.as_view(), name='user'),
    path('user/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('user/<str:slug>/', views.UserDetailView.as_view(), name='user_detail'),
]
