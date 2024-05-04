from django.urls import path
from chat import views


from django.contrib.auth import views as auth_views

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


    path('password-reset/',auth_views.PasswordResetView.as_view(template_name="chat/password_reset.html"),name='password_reset'),
    path('password-reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="chat/password_reset_done.html"), name='password_reset_done'),

    path('password-reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="chat/password_reset_confirm.html"), name='password_reset_confirm'),

    path('password-reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='chat/password_reset_complete.html'), name='password_reset_complete'),
]