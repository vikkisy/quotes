# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def reg_validate(self, postData):
        errors = []
        if len(postData['name']) < 2:
            errors.append("First name cannot be less than 2 characters")
        if len(postData['alias']) < 2:
            errors.append("Alias cannot be less than 2 characters")
        if not re.match(EMAIL_REGEX, postData['email']):
            errors.append("Invalid email")
        if len(postData["password"]) < 8:
            errors.append("Password must be at least 8 characters")
        if postData["password"] != postData["pw_confirm"]:
            errors.append("Passwords must match")
        if len(self.filter(email=postData['email'])) > 1:
            errors.append("That email already exists")
        try:
            datetime.strptime(postData['bday'],'%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            errors.append("Please enter your birthday")
        today = datetime.now().date()
        birthday = datetime.strptime(postData['bday'],'%Y-%m-%d').date()
        print birthday
        print today
        if birthday > today:
            errors.append("Invalid birthday")

        return errors

    def log_validate(self, postData):
        errors = []
        if len(postData['email_login']) <1:
            errors.append("Email cannot be blank")
        if len(postData['pw_login']) <1:
            errors.append("Password cannot be blank")
        if len(self.filter(email=postData['email_login'])) > 0:
            user = self.filter(email=postData["email_login"])[0]
            if not bcrypt.checkpw(postData["pw_login"].encode(), user.password.encode()):
                errors.append("email/password incorrect")
        else:
            errors.append("email/password incorrect")
            return errors
        if not errors:
            return user

    def add_validate(self, postData):
        errors = []
        if len(postData['quoter']) < 3:
            errors.append("Quoted by must be more than 3 characters")
        if len(postData['quote']) < 10:
            errors.append("Quote must be more than 10 characters")
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.name, self.alias, self.email, self.password)

class Quote(models.Model):
    quoter = models.CharField(max_length = 255)
    quote = models.TextField()
    user = models.ForeignKey(User, related_name="quotes")
    favorites = models.ManyToManyField(User, blank=True, null=True, related_name="fav_quotes")
    def __repr__(self):
        return "<Quote object: {} {} {} {}>".format(self.quoter, self.quote, self.user, self.favorites)
