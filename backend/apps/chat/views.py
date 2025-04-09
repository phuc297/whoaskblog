from django.shortcuts import render

def index(request):
    return render(request, "chat/messenger.html")

def room(request, conversation):
    return render(request, "chat/conversation.html", {"conversation": conversation})

