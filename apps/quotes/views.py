# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.messages import error
from django.contrib import messages
from models import User, Quote
import bcrypt

def index(request):
    context = {
        "users": User.objects.all()
    }
    return render(request, 'quotes/index.html')

def process(request):
    errors = User.objects.reg_validate(request.POST)
    if errors:
        for err in errors:
            error(request, err)
        return redirect('/')
    else:
        new_user = User.objects.create(
        name=request.POST["name"],
        alias =  request.POST['alias'],
        email = request.POST['email'],
        birthday = request.POST['bday'],
        password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()))
        request.session['user_id'] = new_user.id
        return redirect('/success')

def login(request):
    errors = User.objects.log_validate(request.POST)
    if type(errors) == list:
        for error in errors:
            messages.error(request, error)
        return redirect('/')

    request.session['user_id'] = errors.id
    return redirect('/success')

def success(request):
    if not 'user_id' in request.session:
        return redirect('/')
    me = User.objects.get(id=request.session['user_id'])
    my_quotes = Quote.objects.filter(user=me)
    my_favorites = Quote.objects.filter(favorites=request.session['user_id'])
    all_quotes = Quote.objects.all()
    not_mine = all_quotes.difference(my_quotes, my_favorites)

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "my_favorites": my_favorites,
        "not_mine": not_mine,
        "all_quotes": Quote.objects.all(),
        "my_quotes": my_quotes
    }

    return render(request, 'quotes/quotes.html', context)

def add_quote(request):
    errors = User.objects.add_validate(request.POST)
    if errors:
        for err in errors:
            error(request, err)
    if not errors:
        user = User.objects.get(id=request.session['user_id'])
        new_quote = Quote.objects.create(
        quoter = request.POST['quoter'],
        quote = request.POST['quote'],
        user = user
        )
    return redirect('/success')

def favorite(request, quote_id):
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    quote.favorites.add(user)
    return redirect('/success')

def user(request, user_id):
    me = User.objects.get(id=user_id)
    count = Quote.objects.filter(user=me).count()
    context = {
        "user": User.objects.get(id=user_id),
        "user_quotes": Quote.objects.filter(user_id=user_id),
        "count": count,
    }
    return render(request, 'quotes/user.html', context)

def remove(request, quote_id):
    user = User.objects.get(id=request.session['user_id'])
    unfavorite = Quote.objects.get(id=quote_id)
    user.fav_quotes.remove(unfavorite)
    return redirect('/success')

def logout(request):
    del request.session['user_id']
    return redirect('/')

# Create your views here.
