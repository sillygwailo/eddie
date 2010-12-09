from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Action(models.Model):
  when = models.DateTimeField()
  title = models.CharField(max_length=200)
  person = models.ForeignKey(User)