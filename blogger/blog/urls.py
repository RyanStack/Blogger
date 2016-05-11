from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    # ex: /blog/
    url(r'^$', views.PostList.as_view(), name='list'),
    # ex: /blog/5/
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetails.as_view(), name='details'),
    # ex: /blog/create/
    url(r'^create/$', views.PostCreate.as_view(), name='create'),
    # ex: /blog/5/edit/
    url(r'^(?P<pk>[0-9]+)/update/$', views.PostUpdate.as_view(), name='update'),
    # ex: /blog/5/delete
    url(r'^(?P<pk>[0-9]+)/delete/$', views.PostDelete.as_view(), name='delete'),
]

