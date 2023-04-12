from django.shortcuts import render, redirect
from .models import Posting
# Create your views here.

    
    
def post(request):
    if request.method == 'GET':
        all_post = Posting.objects.all().order_by('-created_at')
        return render(request, 'posting/post.html', {'posts':all_post})
    
    elif request.method == 'POST':
        # user = request.user
        my_post = Posting()
        # my_post.author = user
        my_post.content = request.POST.get('my-content', '')
        my_post.save()
        return redirect('/post')
    
def delete_post(request, id):
    my_post = Posting.objects.get(id=id)
    my_post.delete()
    return redirect('/post')