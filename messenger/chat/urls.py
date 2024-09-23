from django.urls import path
from .views import UserRegistrationView, registration_page, group_chats, chat_page, send_chat_message, create_chat , delete_chat, profile_page, user_list, inbox, send_direct_message

urlpatterns = [
    path('', registration_page, name='registration'),  # Главная страница
    path('api/register/', UserRegistrationView.as_view(), name='api-register'),  # API регистрации
    path('group_chats/', group_chats, name='group_chats'),  # Путь для group_chats
    path('chat/<str:chat_name>/', chat_page, name='chat_page'),
    path('api/send_chat_message/', send_chat_message, name='send_chat_message'),  # API для отправки сообщений в чат
    path('api/send_direct_message/', send_direct_message, name='send_direct_message'),  # API для отправки прямых
    path('api/create_chat/', create_chat, name='create_chat'),  # API для создания группового чата
    path('api/delete_chat/<int:chat_id>/', delete_chat, name='delete_chat'),
    path('profile/', profile_page, name='profile'),
    path('users/', user_list, name='user_list'),
    path('inbox/', inbox, name='inbox'),
]

