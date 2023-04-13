
from .models import Profile, UserModel
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
# User_app/views.py
def sign_up_view(request):
    if request.method == "GET":  # GET 메서드로 요청이 들어 올 경우
        return render(request, "user/signup.html")
    elif request.method == "POST":  # POST 메서드로 요청이 들어 올 경우
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        password2 = request.POST.get("password2", None)
        bio = request.POST.get("bio", None)

        if password != password2:
            return render(request, "user/signup.html")
        else:
            new_user = UserModel()
            new_user.username = username
            new_user.password = password
            new_user.bio = bio
            new_user.save()
        return redirect("/sign-in")


def sign_in_view(request):
    return render(request, "user/signin.html")


def profile_view(request, id: int) -> HttpResponse or HttpResponseRedirect:
    '''
    모든 사용자가 프로필 페이지를 조회할 수 있습니다. 프로필과 프로필 소유자의 글 목록이 주어집니다.
    오직 프로필 소유자 일때만 프로필의 수정을 할 수 있습니다.
    '''
    # 프로필 가져오기
    opened_profile = Profile.objects.get(id=id)
    if request.method == 'GET':
        # 역참조로 지정된 사용자의 글만 가져오기
        posts = opened_profile.username.posting_set.order_by('-created_at')
        return render('', {'profile': opened_profile, 'posts': posts})
    if request.method == 'POST':
        if request.user != opened_profile.username:
            return redirect('/')
        locate = request.POST.get('locate', '')
        description = request.POST.get('description', '')
        opened_profile.locate = locate
        opened_profile.description = description
        opened_profile.save()
        return redirect('/api/proflie/'+str(id))

