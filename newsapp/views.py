from django.shortcuts import render
from newsapp.models import *
from django.http import HttpResponse, Http404, JsonResponse
# Create your views here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.utils import dateformat

@csrf_exempt
def loggedin(request):
    if 'username' in request.session:
        #return f(request)
        data = [{"success":"true", "username":request.session['username']}]
        return JsonResponse(data, safe=False)
    else:
        data = [{"success":"false"}]
        return JsonResponse(data, safe=False)


def index(request):
    #print("murad is roight")
    context ={"page": "home"}
    return render(request,'newsapp/index.html', context)


def signup(request):
    return render(request,'newsapp/register.html')

def updateDetails(request):
    return render(request,'newsapp/update.html')


def technologyPage(request):
    return render(request,'newsapp/technology.html')


def sportsPage(request):
    return render(request,'newsapp/sports.html')


def businessPage(request):
    return render(request,'newsapp/business.html')


@csrf_exempt
def login(request):
    uname = request.POST['uname']
    password = request.POST['password']
    try:
        #print('getting user object from email')
        user = User.objects.get(username=uname)
       # print(user.password)
       # print(password)
        if user.check_password(password):
         #print('check if password matches')
            request.session['username'] =uname
            request.session['password'] = password
          #  print('success')
            data = [{"success":"true","username":uname}]
            return JsonResponse(data, safe=False)

        else:
            data = [{"success":"false"}]
            return JsonResponse(data, safe=False)
            #print('Has not worked')
            #fail = 'fail'
            #return JsonResponse({"success": fail}, safe=False)
    except User.DoesNotExist:
        data = [{"success":"nonExistent"}]
        return JsonResponse(data, safe=False)


@csrf_exempt
def logout(request):
    if 'username' in request.session:
        u=request.session['username']
        request.session.flush()
        data = [{"success":"true"}]
        return JsonResponse(data, safe=False)
    else:
        data = [{"success":"false"}]
        return JsonResponse(data, safe=False)



@csrf_exempt
def like(request):
    if 'username' in request.session:
        like = request.POST['iflike']
        username = request.session['username']
        user = User.objects.get(username=username)
        theuser = Users.objects.get(user=user)
        articleID = request.POST['articleurl']
        theArticle = Article.objects.get(link = articleID)
        count = Like.objects.filter(article = theArticle, UserFK=theuser).count()
        if count != 0:
            likeO = Like.objects.get(article = theArticle, UserFK=theuser)
            if like == "True":
                isLike = True
            else:
                isLike = False
            if likeO.likeOrDislike is isLike :
                likeO.delete()
                data = [{"success":"false"}]
                return JsonResponse(data, safe=False)
            likeO.likeOrDislike = like
            likeO.save()
            data = [{"success":"true"}]
            return JsonResponse(data, safe=False)
        Like.objects.create(article = theArticle, UserFK = theuser, likeOrDislike= like)
        data = [{"success":"true"}]
        return JsonResponse(data, safe=False)
    else:
        data = [{"success":"false"}]
        return JsonResponse(data, safe=False)

@csrf_exempt
def countLikes(request):
    like = request.POST['iflike']
    articleID = request.POST['articleurl']
    theArticle = Article.objects.get(link=articleID)
    count = Like.objects.filter(article=theArticle, likeOrDislike=like).count()
    data = [{"count": count}]
    return JsonResponse(data, safe=False)

@csrf_exempt
def viewComments(request):
    articleID = request.POST['articleurl']
    theArticle = Article.objects.get(link=articleID)
    comments_list = list(Comment.objects.filter(article=theArticle).values('text', 'user', 'Date'))
    return JsonResponse(comments_list, safe=False)


@csrf_exempt
def addUser(request):
    email = request.POST["email"]
    try:
        User.objects.filter(username=email).exists()
        name = request.POST["fname"]
        pwd = request.POST["password"]
        u_number = request.POST["number"]
        nuser = User.objects.create_user(email, email, pwd, first_name=name)
        nuser.save()
        Users.objects.create(user=nuser, number=u_number)
        request.session['username'] = email
        request.session['password'] = pwd
        data = [{"success":"true"}]
        return JsonResponse(data, safe=False)
    except:
        data = [{"success":"false"}]
        return JsonResponse(data, safe=False)




@csrf_exempt
def update(request):
    old_password = request.POST['password']
    new_password = request.POST['new_password']
    new_firstname = request.POST['new_name']
    uname = request.POST['username']
    number = request.POST['number']
    user = User.objects.get(username=uname)
    news_user = Users.objects.get(user = user)
    if user.check_password(old_password):
        user.set_password(new_password)
        user.first_name = new_firstname
        news_user.number = number
        user.save()
        news_user.save()
        updated = 'updated'
        return JsonResponse({'success': updated}, safe=False)
    else:
        fail = 'fail'
        return JsonResponse({'success': fail}, safe=False)


@csrf_exempt
def addArticle(request):
    link = request.POST['link']
    try:
        prevArt = Article.objects.get(link=link)
        data = [{"success": "already exists"}]
        return JsonResponse(data, safe=False)
    except:
        title = request.POST['title']
        text = request.POST['description']
        aType = request.POST['cat']
        imageurl = request.POST['imagelink']
        article = Article(text=text, title=title, link=link, published=timezone.now(), cat=aType, imagelink=imageurl)
        article.save()
        data = [{"success": "added"}]
        return JsonResponse(data, safe=False)

@csrf_exempt
def addComment(request):
    comment = request.POST['text']
    url = request.POST['articleurl']
    username = request.session['username']
    user = User.objects.get(username=username)
    theuser = Users.objects.get(user = user)
    theArticle = Article.objects.get(link = url)
    newComment = Comment(user=theuser, article=theArticle, text=comment, Date=timezone.now())
    newComment.save()
    data = [{"success": "added"}]
    return JsonResponse(data, safe=False)

@csrf_exempt
def deleteComment(request):
    comment = request.POST['text']
    url = request.POST['articleurl']
    username = request.session['username']
    user = User.objects.get(username=username)
    theuser = Users.objects.get(user = user)
    theArticle = Article.objects.get(link = url)
    Comment.objects.filter(user=theuser, article=theArticle, text=comment).delete()
    data = [{"success": "deleted"}]
    return JsonResponse(data, safe=False)

@csrf_exempt
def getUserName(request):
    userid = request.POST['user']
    users = Users.objects.get(id=userid)
    user = User.objects.get(id = users.user_id)
    name = user.first_name
    data = [{"name": name}]
    return JsonResponse(data, safe=False)

@csrf_exempt
def checkUserMatches(request):
    userid = request.POST['user']
    users = Users.objects.get(id=userid)
    user = User.objects.get(id = users.user_id)
    match = False;
    #print(request.session['username'])
    #print(user.username)
    if request.session['username'] == user.username:
        match = True
    data = [{"match": match}]
    return JsonResponse(data, safe=False)


@csrf_exempt
def getOldArticles(request):
    cat = request.POST['cat']
    article_list = list(Article.objects.filter(cat=cat).values('text', 'title','link','published','imagelink'))
    return JsonResponse(article_list, safe=False)
