# Create your views here.
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.utils.translation import ugettext as _

from forms import *
from models import *

def main_page(request):
    return render_to_response(
      'main_page.html', RequestContext(request)
    )

def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')

def action_page(request, action_id):
  action = get_object_or_404(Action, id=action_id)
  instances = ActionInstance.objects.filter(action=action)

  variables = RequestContext(request, {
    'show_user': True,
    'instances': instances,
    'action': action
  })
  return render_to_response('instances_page.html', variables)

def user_page(request, username):
  user = get_object_or_404(User, username=username)
  if request.user.is_authenticated():
    is_friend = Friendship.objects.filter(
      from_friend=request.user,
      to_friend=user
    )
  else:
    is_friend = False
  try:
    user = User.objects.get(username=username)
  except User.DoesNotExist:
    raise Http404(u'Requested user not found.')

  instances = user.actioninstance_set.all().order_by('-when')

  variables = RequestContext(request, {
    'username': username,
    'instances': instances,
    'is_friend': is_friend,
    'link_action': True,
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
      action, created = Action.objects.get_or_create(
        title=form.cleaned_data['title']
      )
      action.save()
      instance = ActionInstance(
        person=request.user,
        when=form.cleaned_data['when'] or datetime.now(),
        action=action
      )
      instance.save()      
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
      actions = Action.objects.order_by('-id').filter(
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

def actions_list(request):
  actions = Action.objects.order_by('-id')
  variables = RequestContext(request, {
    'actions': actions
  })
  return render_to_response('actions_page.html', variables)

def friends_page(request, username):
  person = get_object_or_404(User, username=username)
  friends = [friendship.to_friend for friendship in person.friend_set.all()]
  friend_actions = Action.objects.filter(
    person__in=friends
  ).order_by('-id')
  variables = RequestContext(request, {
    'username': username,
    'friends': friends,
    'actions': friend_actions[:10],
    'show_tags': True,
    'show_user': True,
  })
  return render_to_response('friends_page.html', variables)

@permission_required('eddie.change_actioninstance', '/login/')
def update_instance(request, instance_id):
  instance = get_object_or_404(ActionInstance, id=instance_id)
  if request.user.username == instance.person.username:
    if request.method == 'POST':
      form = InstanceUpdateForm(request.POST)
      if form.is_valid():
        instance = ActionInstance.objects.get(id=instance_id)
        instance.when = form.cleaned_data['when']
        instance.save()
        request.user.message_set.create(
          message=_(u'Instance ID %s was updated.') % instance_id
        )
    else:
      initial = {'title': instance.action.title, 'when': instance.when}
      form = InstanceUpdateForm(initial=initial)
      variables = RequestContext(request, {
        'instance': instance,   
        'form': form,    
      })
      return render_to_response('instance_update.html', variables)
  request.user.message_set.create(
    message=_(u'You don\'t have access to update this instance.')
  )
  return HttpResponseRedirect('/user/%s/' % request.user.username)

@permission_required('eddie.delete_actioninstance', '/login/')
def delete_instance(request, instance_id):
  instance = get_object_or_404(ActionInstance, id=instance_id)
  if request.user.username == instance.person.username:
    if request.method == 'POST':
      instance.delete()
      request.user.message_set.create(
        message=_(u'Instance ID %s was deleted.') % instance_id
      )
      return HttpResponseRedirect('/user/%s/' % request.user.username)
    else:
      variables = RequestContext(request, {
        'when': instance.when,
        'action': instance.action,
      })
      return render_to_response('delete_confirmation.html', variables)
  else:
    request.user.message_set.create(
      message=_(u'Delete not allowed.')
    )
    if 'HTTP_REFERER' in request.META:
      return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/user/%s/' % request.user.username)

@login_required
def friend_remove(request):
  if 'username' in request.GET:
    try:
      friend = get_object_or_404(
        User, username=request.GET['username']
      )
      friendship = Friendship.objects.get(
        from_friend=request.user,
        to_friend=friend
      )
      friendship.delete()
      if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
      return HttpResponseRedirect('/user/%s/' % request.user.username)
    except friend.DoesNotExist:
      raise Http404('Friendship does not exist.')

def ajax_action_autocomplete(request):
  if 'q' in request.GET:
    actions = Action.objects.filter(
      title__icontains=request.GET['q']
    )[:10]
    return HttpResponse(u'\n'.join(action.title for action in actions))
  return HttpResponse()

@login_required
def friend_add(request):
  if 'username' in request.GET:
    friend = get_object_or_404(
      User, username=request.GET['username']
    )
    friendship, created = Friendship.objects.get_or_create(
      from_friend=request.user,
      to_friend=friend
    )
    if created: 
      friendship.save()
      request.user.message_set.create(
        message=u'%s was added to your friend list.' % friend.username
      )
    else:
      request.user.message_set.create(
        message=u'%s is already a friend of yours.' % friend.username
      )
    return HttpResponseRedirect('/friends/%s/' % request.user.username)
  else:
    raise Http404