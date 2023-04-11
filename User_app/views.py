from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.


def profile_view(request, id):
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
