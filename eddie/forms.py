#!/usr/bin/env python
# encoding: utf-8
"""
forms.py

Created by Richard Eriksson on 2010-12-08.
Copyright (c) 2010 Ethical Detergent. All rights reserved.
"""

import re
from django.contrib.auth.models import User
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from captcha.fields import CaptchaField
from datetime import date

YEARS_CHOICES = range(date.today().year - 1, date.today().year + 1)

class RegistrationForm(forms.Form):    
  username = forms.CharField(label=u'Username', max_length=30)
  email = forms.EmailField(label=u'Email')
  password1 = forms.CharField(
    label=u'Password',
    widget=forms.PasswordInput()
  )
  password2 = forms.CharField(
    label=u'Password (Again)',
    widget=forms.PasswordInput()
  )
  captcha = CaptchaField(help_text=u'Are you human?')
  def clean_password2(self):
    if 'password1' in self.cleaned_data:
      password1 = self.cleaned_data['password1']
      password2 = self.cleaned_data['password2']
      if password1 == password2:
        return password2
      raise forms.ValidationError('Passwords do not match.')
  def clean_username(self):
    username = self.cleaned_data['username']
    if not re.search(r'^\w+$', username):
      raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
    try:
      User.objects.get(username=username)
    except User.DoesNotExist:
      return username
    raise forms.ValidationError('Username is already taken.')

class InstanceUpdateForm(forms.Form):
  when = forms.DateField(widget=SelectDateWidget(years=YEARS_CHOICES),required=False)

class ActionSaveForm(forms.Form):
  title = forms.CharField(
    label=u'Action',
    widget=forms.TextInput(attrs={'size': 64})
  )
  when = forms.DateField(widget=SelectDateWidget(years=YEARS_CHOICES),required=False)

class SearchForm(forms.Form):
  query = forms.CharField(
    label=u'Enter a keyword to search for',
    widget=forms.TextInput(attrs={'size': 32})
  )
