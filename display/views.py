from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from posts.models import Post, Likes, Comments

def index(request):
    return render(request, 'display/index.html')

def cadastro(request):
    return render(request, "display/cadastro.html")

def createUser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        verifyUser = User.objects.get(username=username)
    except:
        verifyUser = None
    if verifyUser:
        return render(request, "display/userAlreadyExists.html")
    else:
        user = User.objects.create_user(username=username,password=password)
        user.save()
    return HttpResponseRedirect("/")

def loginUser(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username,password=password)
    if user:
        login(request,user)
        return HttpResponseRedirect("/socialMedia")
    else:
        return HttpResponseRedirect("/")

def socialMedia(request):
    objetos = Post.objects.all()
    if request.user.is_authenticated:
        return render(request,"display/socialMedia.html", { 'objetos': objetos })
    else:
        return render(request, "display/needLogin.html")

def post(request):
    if request.user.is_authenticated:
        return render(request,"display/post.html")
    else:
        return render(request, "display/needLogin.html")
    
def createPost(request):
    title = request.POST.get('title')
    author = request.user
    body = request.POST.get('body')
    slug = request.POST.get('title').replace(' ', '-')
    
    verifyPost = Post.objects.filter(title=title).first()

    if verifyPost:
        return render(request, "display/postAlreadyExists.html")
    else:
        newPost = Post(title=title,author=author,body=body,slug=slug)
        newPost.save()
        return render(request,"display/postCreated.html")

def selectedPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    likes = Likes.objects.filter(post=Post.objects.filter(slug=slug).first().id).all()
    comment = Comments.objects.filter(post=post).all()
    numLikes = 0
    for like in likes:
        numLikes = numLikes + like.likes
    getIsLiked = Likes.objects.filter(post=Post.objects.filter(slug=slug).first().id,likedBy=request.user).first()
    isLiked = False
    if getIsLiked:
        isLiked = True
    if post.author == request.user:
        isLiked = True
    var = {"post": post, "likes": likes, "isLiked":isLiked, "llikes":numLikes, "comment":comment}
    return render(request,"display/selectedPost.html", var)

def addLike(request, slug):
    '''
    verifyLikedBy = Likes.objects.filter(post=Post.objects.filter(slug=slug).first(), likedBy=request.user).first()
    verifyLike = Likes.objects.filter(post=Post.objects.filter(slug=slug).first()).first()
    if verifyLike:
        verifyLike.likes = verifyLike.likes+1
        verifyLike.save()
    else:
        newLike = Likes(likes=1,post=Post.objects.filter(slug=slug).first(), likedBy=request.user)
        newLike.save()
    '''
    verifyLikedBy = Likes.objects.filter(post=Post.objects.filter(slug=slug).first(), likedBy=request.user).first()
    if verifyLikedBy:
        pass
    else:
        newLike = Likes(likes=1,post=Post.objects.filter(slug=slug).first(), likedBy=request.user)
        newLike.save()

    return HttpResponseRedirect("/posts/"+slug)

def logoutSystem(request):
    logout(request)
    return HttpResponseRedirect("/")

def createComment(request):
    comment = request.POST.get("comment")
    author = request.user
    slug = request.POST.get("post")
    post = Post.objects.filter(slug=slug).first()
    newComment = Comments(comment=comment,author=author,post=post)
    newComment.save()
    #return render(request, "posts/"+post.slug)
    return HttpResponseRedirect("/posts/"+post.slug)