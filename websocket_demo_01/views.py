from django.shortcuts import render


# Create your views here.
def chat_room(request):
    chat_room_num = request.GET.get('room')
    return render(request, 'chat_room.html', {'chat_room_num': chat_room_num})
