from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Action(models.Model):
  title = models.CharField(unique=True,max_length=200)
  def __unicode__(self):
    return self.title

class ActionInstance(models.Model):
  person = models.ForeignKey(User) # person who did the action  
  when = models.DateTimeField() # when that person did the action
  action = models.ForeignKey(Action) # what action this is an instance of
  
  def __unicode__(self):
    return u'%s, %s, %s' % (self.person.username, self.when.isoformat(), self.action.title)
  
class Tag(models.Model):
  name = models.CharField(max_length=64, unique=True)
  actions = models.ManyToManyField(Action)
  def __unicode__(self):
    return self.name

class ActionLike(models.Model):
  instance = models.ForeignKey(ActionInstance, unique=True)
  when = models.DateTimeField(auto_now_add=True)
  likes = models.IntegerField(default=1)
  users_liked = models.ManyToManyField(User)
  
  def __unicode__(self):
    return u'%s, %s' % (self.instance, self.likes)

class Friendship(models.Model):
  from_friend = models.ForeignKey(
    User, related_name='friend_set'
  )
  to_friend = models.ForeignKey(
    User, related_name='to_friend_set'
  )
  def __unicode__(self):
    return u'%s, %s' % (self.from_friend.username, self.to_friend.username)

class Meta:
  unique_together = (('to_friend', 'from_friend'), )