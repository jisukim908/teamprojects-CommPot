
from django.shortcuts import render, redirect
from .models import Posting, PostingComment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def post_view(request):
    if request.method == 'GET':
        all_post = Posting.objects.all().order_by('-created_at')
        return render(request, 'posting/post.html', {'posts': all_post})

    elif request.method == 'POST':
        user = request.user.is_authenticated
        if not user:
            return redirect('/api/user/login')

        # user = request.user
        my_post = Posting()
        # my_post.author = user
        my_post.content = request.POST.get('my-content', '')
        my_post.save()
        return redirect('/post')


@login_required
def delete_posting_view(request, id):
    my_post = Posting.objects.get(id=id)
    if my_post.author == request.user:
        my_post.delete()
    return redirect('/api/posts')
    # return HttpResponse('글 삭제 완료')


def posting_detail_view(request, id):
    # 수정하기
    if request.method == 'POST':
        my_posting = Posting.objects.get(id=id)
        if request.user != my_posting.author:
            return redirect('/api/posts/'+str(id))
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        my_posting.title = title
        my_posting.content = content
        my_posting.save()
        # return redirect('/api/posts/'+str(id))
        return HttpResponse('수정완료')
    elif request.method == 'GET':
        my_posting = Posting.objects.get(id=id)
        posting_comment = PostingComment.objects.filter(posting_id=id)
        # return render(request,'posting/posting_detail.html',{'posting':my_posting,'comment':posting_comment})
        return HttpResponse('업로드 완료')


def write_comment_view(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        current_posting = Posting.objects.get(id=id)
        user = request.user.is_authenticated
        if not user:
            return redirect('/api/user/login')

        PC = PostingComment()
        PC.comment = comment
        PC.author = request.user
        PC.posting = current_posting
        PC.save()

        # return redirect('/api/posts'+str(id))
        return HttpResponse('댓글 저장 완료')


@login_required
def delete_comment_view(request, id):
    comment = PostingComment.objects.get(id=id)
    current_posting = comment.posting.id
    if comment.author == request.user:
        comment.delete()

    # return redirect('/api/posts'+str(current_posting))
    return HttpResponse('댓글 삭제 완료')
