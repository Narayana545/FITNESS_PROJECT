from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('set_goal/', views.set_goal, name='set_goal'),
    path('achieve_goal/<int:goal_id>/', views.achieve_goal, name='achieve_goal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
