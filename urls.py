import os
from django.contrib import admin
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from eddie.views import *
from captcha import urls
from robots import urls

admin.autodiscover()

site_media = os.path.join(
  os.path.dirname(__file__), 'site_media'
)

urlpatterns = patterns('',
  # Browsing
  (r'^$', main_page),
  (r'^user/(\w+)/$', user_page),
  (r'^search/', search_page),
  (r'^action/(\d+)/$', action_page),
  (r'^delete/(\d+)/$', delete_instance),
  (r'^actions/$', actions_list),
  (r'^update/(\d+)/$', update_instance),

  # Session management
  (r'^login/$', 'django.contrib.auth.views.login'),
  (r'^logout/$', logout_page),
  (r'^login/reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'password/password_reset.html'}),
  (r'^login/reset/confirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password/password_reset_confirm.html'}),
  (r'^login/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password/password_reset_done.html'}),    
  (r'^login/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password/password_reset_complete.html'}),    
  
  (r'^register/$', register_page),
  (r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),
  (r'^captcha/', include('captcha.urls')),
  
  # Account management
  (r'^save/', action_save_page),  

  # Site media
  (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),

  # Friends
  (r'^friends/(\w+)/$', friends_page),
  (r'^friend/add/$', friend_add),
  (r'^friend/remove/$', friend_remove),

  # Site admin
   (r'^admin/', include(admin.site.urls)),

   # Ajax
   (r'^ajax/action/autocomplete/$', ajax_action_autocomplete),
   
     (r'^robots.txt$', include('robots.urls')),
   
   
)
