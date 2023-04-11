from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def profile_view(request, id: int) -> HttpResponse | HttpResponseRedirect:
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
        return redirect('/api/proflie/'+id)
