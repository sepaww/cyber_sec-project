from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Note
from cryptography.fernet import Fernet
import sqlite3


def caesar_crypt(word):
    word=word.lower()
    enc=""
    turn=13
    maxi=ord("z")
    for ch in word:
        if ord(ch)+turn>maxi:
            val=maxi-ord(ch)+ord("a")+turn
        else:
            val=ord(ch)+turn
        enc=enc+chr(val)
    return enc

@login_required
def addView(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        #conn = sqlite3.connect('src/db.sqlite3')
        #conn.cursor().execute(f"INSERT INTO pages_note (owner, data) VALUES ({request.user}, {data})")
        Note.objects.create(owner=request.user, data=data)
        return redirect('/')
    return redirect('/')

@login_required
def homePageView(request):
    if caesar_crypt(request.user.username)!=request.session['valid']:
        return render(request, 'pages/bababooey.html')
    Notes = Note.objects.filter(owner=request.user)
    mynotes = [f.data for f in Notes]
    #mynotes = [str(f.data) for f in Notes]
    return render(request, 'pages/index.html', {'Notes': mynotes})

def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['valid']=caesar_crypt(username)
            request.session.modified = True
            return redirect('/')
        return HttpResponse('Login failed')

def registerView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).count() != 0:
            return HttpResponse('Name not available')
        candidates = [p.strip() for p in open("src\candidates.txt")]
        for psw in candidates:
            if psw==password:
                return HttpResponse('pls try harder with password')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        request.session['valid']=caesar_crypt(username)
        request.session.modified = True
        return redirect('/')
    return redirect('/')