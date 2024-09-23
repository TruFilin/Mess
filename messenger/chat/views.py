from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from .models import ChatMessage, GroupChat
from django.http import JsonResponse
from .models import UserProfile, DirectMessage
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def registration_page(request):
    return render(request, 'register.html')


def group_chats(request):
    return render(request, 'group_chats.html')  # Создай этот шаблон


@login_required
def chat_page(request, chat_name):
       messages = ChatMessage.objects.filter(chat_name=chat_name).order_by('timestamp')
       return render(request, 'chat.html', {'chat_name': chat_name, 'username': request.user.username, 'messages': messages})


@csrf_exempt
@login_required
def send_chat_message(request):
       if request.method == 'POST':
           data = json.loads(request.body)
           chat_name = data.get('chat_name')
           message = data.get('message')

           ChatMessage.objects.create(username=request.user, chat_name=chat_name, message=message)
           return JsonResponse({'status': 'success'})
       return JsonResponse({'status': 'fail'}, status=400)


def group_chats(request):
    chats = GroupChat.objects.all()  # Получаем все групповые чаты
    return render(request, 'group_chats.html', {'chats': chats})
@csrf_exempt
def create_chat(request):
       if request.method == 'POST':
           data = json.loads(request.body)
           chat_name = data.get('chat_name')

           chat, created = GroupChat.objects.get_or_create(name=chat_name)
           if created:
               return JsonResponse({'status': 'success', 'chat_name': chat.name})
           return JsonResponse({'status': 'fail', 'message': 'Чат уже существует.'}, status=400)
@csrf_exempt
def delete_chat(request, chat_id):
       try:
           chat = GroupChat.objects.get(id=chat_id)
           chat.delete()
           return JsonResponse({'status': 'success'})
       except GroupChat.DoesNotExist:
           return JsonResponse({'status': 'fail', 'message': 'Чат не найден.'}, status=404)
       except Exception as e:
           return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)


@login_required
def profile_page(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)  # Создаем профиль, если его нет

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'username': request.user.username, 'form': form})
@login_required
def user_list(request):
       users = User.objects.all()  # Получаем всех пользователей
       return render(request, 'user_list.html', {'users': users})


@csrf_exempt
@login_required
def send_direct_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        message = data.get('message')

        recipient = User.objects.filter(username=username).first()  # Найти пользователя по имени
        if recipient:
            DirectMessage.objects.create(sender=request.user, recipient=recipient, message=message)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'fail', 'message': 'Пользователь не найден.'}, status=404)
    return JsonResponse({'status': 'fail'}, status=400)


@login_required
def inbox(request):
    messages = DirectMessage.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'inbox.html', {'messages': messages})