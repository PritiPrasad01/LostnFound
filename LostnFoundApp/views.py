from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignUpForm,UserUpdateForm,UserProfileUpdateForm,PostForm,CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .models import Post,Profile,UserOtp,Comment,Reply
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import random
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.db.models import Q

# Create your views here.

def home(request):
    lost = Post.objects.filter(category='L')
    found = Post.objects.filter(category="F")
    context = {'lost':lost,'found':found}
    return render(request,'app/home.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
                get_user = request.POST.get('user')
                user = User.objects.get(username=get_user)
                if int(get_otp) == UserOtp.objects.filter(user=user).last().otp:
                    user.is_active=True
                    user.save()
                    login(request, user)
                    return redirect('home')
                else:
                    messages.warning(request, f"Wrong Otp")
                    return render(request,'app/login.html',{'otp':True,'user':user})

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        elif not User.objects.filter(username=username).exists():
            messages.success(request, f"Please enter a correct username and password. Note that both fields may be case-sensitive.")
            return redirect('login')
        elif not User.objects.get(username=username).is_active:
            user = User.objects.get(username=username)
            user.is_active = False
            user.save()
            user_otp = random.randint(100000,999999)
            UserOtp.objects.create(user=user,otp=user_otp)
            mess = f"Hello {user.first_name},\n\nYour Otp is {user_otp}\n\n\nRegards,\nLostnFound"

            send_mail(
                "Welcome to LostnFound - Verify Your Email",
                 mess, 
                 settings.EMAIL_HOST_USER, 
                 [user.email],
                 fail_silently=False
                 )
            return render(request, 'app/login.html',{'otp':True,'user':user})
        else:
            messages.success(request, f"Please enter a correct username and password. Note that both fields may be case-sensitive.")
            return redirect('login')

    form = AuthenticationForm()
    return render(request, 'app/login.html',{'form':form})

def signup(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)
            if int(get_otp) == UserOtp.objects.filter(user=user).last().otp:
                user.is_active=True
                user.save()
                messages.success(request, "Congratulations!! Registered Successfully")
                return redirect('login')
            else:
                messages.warning(request, f"Wrong Otp")
                return render(request,'app/signup.html',{'otp':True,'user':user})     
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() 
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.phone_num = form.cleaned_data.get('phone_num')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.profile_pic = form.cleaned_data.get('profile_pic')
            user.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            user.is_active = False
            user.save()
            user_otp = random.randint(100000,999999)
            UserOtp.objects.create(user=user,otp=user_otp)
            mess = f"Hello {user.first_name},\nYour Otp is {user_otp}\n\n\nRegards,\nLostnFound"

            send_mail(
                "Welcome to LostnFound - Verify Your Email",
                 mess, 
                 settings.EMAIL_HOST_USER, 
                 [user.email],
                 fail_silently=False
                 )
            return render(request,'app/signup.html',{'otp':True,'user':user})
    else:
        form = SignUpForm()
    return render(request,'app/signup.html',{'form':form})

def addpost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                data = Post()
                data.user = request.user
                data.title= form.cleaned_data['title']
                data.location= form.cleaned_data['location']
                data.description= form.cleaned_data['description']
                data.category = form.cleaned_data['category']
                data.product_image = form.cleaned_data['product_image']
                data.save()
                messages.success(request, "Post added successfully.")
                return redirect('posts')
        else:
            form = PostForm()
        context = {'form':form}
        return render(request,'app/addpost.html',context)
    else:
        return HttpResponse("Please login to add new posts")

def lost(request):
    lost = Post.objects.filter(category='L')
    context = {'lost':lost}
    return render(request,'app/lost.html',context)

def found(request):
    found = Post.objects.filter(category="F")
    context = {'found':found}
    return render(request,'app/found.html',context)

def posts(request):
    lost = Post.objects.filter(category='L')
    found = Post.objects.filter(category="F")
    context = {'lost':lost,'found':found}
    return render(request,'app/posts.html',context)

def about(request):
    return render(request,'app/about.html')

def details(request, pk):
    detail = Post.objects.get(pk=pk)
    comment_list = Comment.objects.filter(post=detail).order_by('-created_at')
    paginator = Paginator(comment_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/details.html', {'detail': detail, 'page_obj': page_obj})

@login_required(login_url='/login/')
def profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.all().filter(user = request.user)
        posts = Post.objects.filter(user=request.user)
        context = {'profile':profile,
                   'posts':posts
                   }
        return render(request,'app/profile.html',context)
    return redirect('login')

@login_required(login_url='/login/')
def editprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = UserProfileUpdateForm(request.POST,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.profile)
    context = {
        'form': u_form,
        'p_form':p_form
    }
    return render(request,'app/editprofile.html',context)

def search(request):
    query = request.GET.get('query', '').strip()
    if len(query) > 78:
        posts = Post.objects.none()
        users = User.objects.none()
    else:
        postTitle = Post.objects.filter(title__icontains=query)
        postDescription = Post.objects.filter(description__icontains=query)
        postLocation = Post.objects.filter(location__icontains=query)
        posts = postTitle.union(postDescription,postLocation)
        users = User.objects.filter(username__icontains=query)
    if (posts.exists() or users.exists()):
        context = {'posts': posts, 'users': users, 'query': query}
        return render(request, 'app/search.html', context)
    else:
        # messages.warning(request, "No search results found. Please refine your query.")
        context = {'query': query}
        return render(request, 'app/search.html', context)

@login_required(login_url='/login/')
def change_password(request):
    return render(request, 'app/changepassword.html')

@login_required(login_url='/login/')
def resend_otp(request):
    if request.method == "GET":
        get_user = request.GET['user']
        if User.objects.filter(username=get_user).exists() and not User.objects.get(username=get_user).is_active:
            user =  User.objects.get(username=get_user)
            user_otp = random.randint(100000,999999)
            UserOtp.objects.create(user=user,otp=user_otp)
            mess = f"Hello {user.first_name},\n\nYour Otp is {user_otp}\n\n\nRegards,\LostnFound"

            send_mail(
                "Welcome to LostnFound - Verify Your Email",
                 mess, 
                 settings.EMAIL_HOST_USER, 
                 [user.email],
                 fail_silently=False
                 )
            return HttpResponse("Resend")
    return HttpResponse("Can't Send")

@login_required(login_url='/login/')
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():   
            text = request.POST['text']
            comment = Comment.objects.create(
                user=request.user,
                post=post,
                text=text,
                created_at=timezone.now()
            )
            comment.save()
            messages.success(request,"Comment added successfully.")
            return redirect('details', pk=post.pk)
    context = {'form':form,"pk":pk}
    return render(request,'app/commentForm.html', context)
        
@login_required(login_url='/login/')
def reply_create_view(request, comment_pk):
    parent_comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        text = request.POST['text']
        reply = Reply.objects.create(
            user=request.user,
            comment=parent_comment,
            text=text,
            created_at=timezone.now()
        )
        reply.save()
        return redirect('details', pk=parent_comment.post.pk)
    return render(request, 'app/details.html')
    

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'app/userdetail.html', context)

@login_required(login_url='/login/')
def alert_owner(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if post:
        email = post.user.email
    mess = f"{request.user.first_name} have raised alert for your post {post.title}. His/Her email address is {request.user.email} and mobile number is {request.user.profile.phone_num}. Thank you."
    send_mail(
        "Greeting from LostnFound ",
            mess, 
            settings.EMAIL_HOST_USER, 
            [email],
            fail_silently=False
            )
    messages.success(request,"Alerted Owner Successfully.")
    return redirect(details,pk=pk)