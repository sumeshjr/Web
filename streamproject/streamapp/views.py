
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,redirect,HttpResponse
from .models import *
from pyexpat.errors import messages
from django.contrib.auth.models import *
from django.db.models import Q
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Count


def index(request):
    screen=Home.objects.all()
    view=Video.objects.all().order_by('-id')[:4]
    return render (request, "index.html", {"view":view,"screen":screen})



def register(request):
    msg=""
    if request.POST:
        
        name=request.POST.get("name")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        profileimage=request.POST.get("image")

        if UserReg.objects.filter(email=email).exists():
            msg="Already Registered"
        
        else :
            insert=UserReg.objects.create(name=name,email=email,password=password,phone=phone,address=address,profileimage=profileimage)
            insert.save()
            msg="Registered Successfully"
            return HttpResponseRedirect("/?msg="+msg)
        
    
    return render(request,"signup.html",{"msg":msg})

def login(request):
    if request.POST:
        email=request.POST.get("email")
        password=request.POST.get("password")
        log=UserReg.objects.filter(email=email,password=password)
        if log:
            request.session['u_id']=log[0].id
            return HttpResponseRedirect('/home')
      
    else:       
        return render(request, "login.html")


def videoview(request):
    view=Video.objects.all()
    return render (request, "videoview.html", {"view":view})


def recentvideo(request):
    recent=Video.objects.all().order_by("-id")[:10]

    return render(request,"recentvideo.html",{"recent":recent})


def home(request):
    user_id = request.session.get("u_id")
    if not user_id:
        return redirect("login")
    try:
        user = UserReg.objects.get(id=user_id)
    except UserReg.DoesNotExist:
        return redirect("login")
    
    comm=Comment.objects.all().order_by('-id')
    screen=Home.objects.all()
    videos = Video.objects.all().order_by('-id') 
    context = {
        "user": user,
        "videos": videos,
        "screen":screen,
        'comm':comm
    }
    
    return render(request, "home.html", context)



def recent_updates(request):
    updates = RecentUpdate.objects.all().order_by('-date_created')
    return render(request, 'recent_updates.html', {'updates': updates})


   

def stream(request):
    id=request.GET.get("id")
    video=Video.objects.filter(category_id=id)
    return render (request,"streaming.html",{"video":video})



def category(request):
    ct=Category.objects.all()
    return render(request,"categoryview.html",{"ct":ct})



def add_to_favorites(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if 'u_id' in request.session:
        user_id = request.session['u_id']
        if video.fav.filter(id=user_id).exists():
            message = "Already exists"
        else:
            video.fav.add(user_id)
            message = "Video added to favorites."
    else:
        message = "You need to be logged in to add videos to favorites."
        messages.error(request, message)
        return redirect('login') 
    
    context = {'message': message}
    return render(request, 'home.html', context)

#Remove Fav
def remove_from_fav(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if 'u_id' in request.session:
        user_id=request.session['u_id']
        if video.fav.filter(id=user_id).exists():
            video.fav.remove(user_id)
            message="Video Removed From Favourites"
        else:
            messages="No Video in Favourites"
    else:
        message = "You need to be logged in to add videos to favorites."
        messages.error(request, message)
        return redirect('login') 
    
    context = {'message': message}
    return render(request, 'home.html', context)
    



def favorites_list(request):
    if 'u_id' in request.session:
        user_id = request.session['u_id']
        favorites = Video.objects.filter(fav=user_id)
        return render(request, 'favlist.html', {'favorites': favorites})
    else:
        return render(request, 'favlist.html', {'favorites': None})







def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if 'u_id' in request.session:
        user_id = request.session['u_id']
        if video.likes.filter(id=user_id).exists():
            video.likes.remove(user_id)
            liked = False
        else:
            video.likes.add(user_id)
            liked = True
    else:
        return JsonResponse({'error': 'You need to be logged in to like videos.'})

    like_count = video.likes.count()

    return JsonResponse({'liked': liked, 'like_count': like_count})



def my_profile(request):
    # Retrieve the Sign_up record for the currently logged-in user
  id= request.session["u_id"]
  sign_up = UserReg.objects.get(id=id) 
  return render(request, 'profile.html', {'sign_up': sign_up})


def edit_profile(request):
    user_id = request.session.get("u_id")
    user = UserReg.objects.get(id=user_id)

    if request.method == "POST":
        # Update the user profile based on the submitted data
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.address = request.POST.get("address")
        profile_image = request.FILES.get("profileimage")

        if profile_image:
            
            if user.profileimage:
                user.profileimage.delete(save=False)
            user.profileimage = profile_image
        user.save()
        message="Video Removed From Favourites"
        return redirect("userprofile/",{'message':message})

    return render(request, "edit_profile.html", {"user": user})



def contact(request):
    msg=""
    if request.POST:
        email = request.POST.get('email')
        name = request.POST.get('name')
        suggestion = request.POST.get('suggestion')

        contact=ContactUs.objects.create(name=name,email=email,suggestion=suggestion)
        contact.save()

        msg="Thanks for your Feedback"
        return HttpResponseRedirect("/?msg="+msg)
    return render(request, 'contact.html')



def addcomment(request):
    if request.method == 'POST':
        user_id = request.session.get('u_id')
        if user_id:
            user = UserReg.objects.get(id=user_id)
            text = request.POST.get('comment_text')

            comment = Comment(user=user, text=text)
            comment.save()

            return HttpResponseRedirect('/home')
    return HttpResponse('Error: Unable to add comment')


    

def search_videos(request):
    query = request.GET.get('query')
    videos = Video.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'search.html', {'videos': videos, 'query': query})



def user_logout(request):
    logout(request)
    return redirect('/')

# Create your views here.
