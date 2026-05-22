from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment, Reply
from .forms import PostForm

from .forms import CleanLoginForm, CleanSignupForm

#def home_landing(request):
#    login_form = CleanLoginForm()
#    signup_form = CleanSignupForm()

#    if request.method == 'POST':
#        if 'action_login' in request.POST:
#            login_form = CleanLoginForm(data=request.POST)
#            if login_form.is_valid():
#                login(request, login_form.get_user())
#                return redirect('dashboard')
#        elif 'action_signup' in request.POST:
#            signup_form = CleanSignupForm(request.POST)
#            if signup_form.is_valid():
#                user = signup_form.save()
#                login(request, user)
#                return redirect('dashboard')

#    return render(request, 'home.html', {
#        'login_form': login_form,
#        'signup_form': signup_form
#    })

from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CleanLoginForm, CleanSignupForm

def home_landing(request):
    login_form = CleanLoginForm()
    signup_form = CleanSignupForm()
    
    if request.method == 'POST':
        # HANDLE LOGIN
        if 'action_login' in request.POST:
            login_form = CleanLoginForm(data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                return redirect('dashboard')
        
        # HANDLE SIGNUP
        elif 'action_signup' in request.POST:
            signup_form = CleanSignupForm(request.POST)
            if signup_form.is_valid():
                # 1. Save the user first
                user = signup_form.save()
                # 2. Force the login after signup
                login(request, user)
                # 3. Redirect to dashboard
                return redirect('dashboard')
    
    return render(request, 'home.html', {
        'login_form': login_form,
        'signup_form': signup_form
    })

@login_required
def dashboard(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('dashboard')

    return render(request, 'dashboard.html', {'posts': posts, 'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('dashboard')

# --- REAL-TIME ASYNC ENDPOINTS (JSON) ---

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get('text')
        if text:
            comment = Comment.objects.create(post=post, user=request.user, text=text)
            return JsonResponse({
                'status': 'success',
                'comment_id': comment.id,
                'user': comment.user.username,
                'text': comment.text
            })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def add_reply(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        text = request.POST.get('text')
        if text:
            reply = Reply.objects.create(comment=comment, user=request.user, text=text)
            return JsonResponse({
                'status': 'success',
                'user': reply.user.username,
                'text': reply.text
            })
    return JsonResponse({'status': 'error'}, status=400)

def user_logout(request):
    logout(request)
    return redirect('home')
