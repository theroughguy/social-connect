from django.urls import path
from chat import views


urlpatterns = [
    path('login/',views.login_page,name= 'login'),
    path('register/', views.registerpage, name='registration'),

    path('logout/', views.logout_user, name='logout'),

    path('',views.home,name = 'home'),
    path('room/<str:pk>/',views.room_view,name = 'room'),

    path('user-profile/<str:pk>/',views.user_profile,name = "user-profile"),
    path('room-create',views.room_create,name='room-create'),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
    path('update-message/<str:pk>/', views.update_message, name='update-message'),
    path('update-user/', views.update_user, name='update-user'),

]