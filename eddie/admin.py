from django.contrib import admin
from eddie.models import *

class ActionAdmin(admin.ModelAdmin):
  pass
admin.site.register(Action, ActionAdmin)
