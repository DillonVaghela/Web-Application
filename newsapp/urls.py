from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index , name = 'index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^checklogin/$', views.loggedin, name='loggedin'),
    url(r'^addUser/$', views.addUser, name='addUser'),
    url(r'^updateDetails/$', views.updateDetails, name='updateUser'),
    url(r'^update/$', views.update, name='update'),
    url(r'^sport/$', views.sportsPage, name='sportsPage'),
    url(r'^business/$', views.businessPage, name='businessPage'),
    url(r'^technology/$', views.technologyPage, name='technologyPage'),
    #url(r'^comment/$', views.addComment, name='addComment'),
    url(r'^getComments/$', views.viewComments, name='viewComments'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^likeOrDislike/$', views.like, name='like'),
    url(r'^checklikeOrDislike/$', views.countLikes, name='countLikes'),
    url(r'^addArticle/$', views.addArticle, name='addArticle'),
    url(r'^addComment/$', views.addComment, name='addComment'),
    url(r'^deleteComment/$', views.deleteComment, name='deleteComment'),
    url(r'^getOldArticles/$', views.getOldArticles, name='getOldArticles'), 
    url(r'^getUserName/$', views.getUserName, name='getUserName'),
    url(r'^checkUserMatches/$', views.checkUserMatches, name='checkUserMatches'),
]
