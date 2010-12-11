# Create your views here.
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from eddie.forms import *
from eddie.models import *

def main_page(request):
    return render_to_response(
      'main_page.html', RequestContext(request)
    )

def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')


def user_page(request, username):
  try:
    user = User.objects.get(username=username)
  except User.DoesNotExist:
    raise Http404(u'Requested user not found.')

  actions = user.action_set.all().order_by('-when')

  variables = RequestContext(request, {
    'username': username,
    'actions': actions
  })
  return render_to_response('user_page.html', variables)

def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password1'],
        email=form.cleaned_data['email']
      )
      return HttpResponseRedirect('/register/success/')
  else:
    form = RegistrationForm()
  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response('registration/register.html', variables)

@login_required
def action_save_page(request):
  if request.method == 'POST':
    form = ActionSaveForm(request.POST)
    if form.is_valid():
      # Update the date and person who did the action
      action, created = Action.objects.get_or_create(
        title=form.cleaned_data['title'],
        when=form.cleaned_data['when'],
        person = request.user       
      )
      if not created:
        pass
      action.save
      return HttpResponseRedirect(
        '/user/%s/' % request.user.username
      )
  else:
    form = ActionSaveForm()
  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response('action_save.html', variables)
  
def search_page(request):
  form = SearchForm();
  actions = []
  show_results = False
  if 'query' in request.GET:
    show_results = True
    query = request.GET['query'].strip()
    if query:
      form = SearchForm({'query': query})
      actions = Action.objects.order_by('-when').filter(
        title__icontains=query
      )[:10]
  variables = RequestContext(request, {
    'form': form,
    'actions': actions,
    'show_results': show_results,
    'show_user': True,
  })
  if request.GET.has_key('ajax'):
    return render_to_response('actions_list.html', variables)
  else:
    return render_to_response('search.html', variables)
  