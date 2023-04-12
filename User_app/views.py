from django.shortcuts import render, redirect
from .models import UserModel


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
