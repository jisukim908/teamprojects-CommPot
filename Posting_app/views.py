
from django.shortcuts import render, redirect
from .models import Posting, PostingComment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.


def home(request):
    return redirect('/api/posts')


def post_view(request):
    if request.method == 'GET':
        category = request.GET.get('category', '')
        subscribe = request.GET.get('subscribed', '')
        all_post = []
        if category:
            all_post = Posting.objects.filter(category=category)
        elif subscribe == 'only':
            all_post = Posting.objects.filter(
                author__in=request.user.follow.all())
            pass
        else:
            all_post = Posting.objects.all()
        all_post = all_post.order_by('-created_at')
        page = int(request.GET.get('page', '1'))
        paginator = Paginator(all_post, 5)
        post_list = paginator.get_page(page)
        return render(request, 'posting/post.html', {'post_list': post_list})
    elif request.method == 'POST':
        user = request.user.is_authenticated
        if not user:
            return redirect('/api/user/login')

        # user = request.user

        my_post = Posting()
        my_post.author = user
        my_post.content = request.POST.get('my-content', '')
        my_post.save()
        return redirect('/api/posts/')


@login_required
def delete_posting_view(request, id):
    go_to = request.GET.get('from', '/')
    try:
        my_post = Posting.objects.get(id=id)
    except:
        return render(go_to)
    if my_post.author == request.user or request.user.is_superuser:
        my_post.delete()
    print(go_to)
    return redirect(go_to)

    # return HttpResponse('글 삭제 완료')


def posting_detail_view(request, id):
    try:
        my_posting = Posting.objects.get(id=id)
    except:
        return render(request, '404.html')
    posting_comment = PostingComment.objects.filter(posting_id=id)
    return render(request, 'posting/post_detail.html', {'posting': my_posting, 'comment': posting_comment})


@login_required
def posting_edit_view(request, id):
    # 1. id가 0 인지 확인
    if id == 0:
        my_posting = Posting()
        my_posting.title = ""
        my_posting.content = ""
        my_posting.category = "recipe"
        my_posting.author = request.user
        my_posting.author_name = request.user.username

    # 2. id가 0 이면, 새로운 포스팅 모델 객체를 만들면 됩니다.
    # 3. 0이 아니라면, 바로 여기아래 있는 코드한줄이 실행되면 됩니다.
    else:
        try:
            my_posting = Posting.objects.get(id=id)
        except:
            return render(request, '404.html')
    # 4. 작성자와 동일한 사용자인지 체크하고 아니면 되돌려보내기
    if request.user != my_posting.author:
        return redirect('/api/posts/'+str(id)) if id else redirect('/api/posts')
    if request.method == 'POST':
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        category = request.POST.get("category", "recipe")
        my_posting.title = title
        my_posting.content = content
        # title, content 내용 없으면 다시 랜더링
        if (title.strip() == "") or (content.strip() == ""):
            return render(request, 'posting/post_edit.html', {'posting': my_posting, 'error': "please write title and content!"})
        my_posting.category = category
        my_posting.save()
        return redirect('/api/posts/'+str(id)) if id else redirect('/api/posts')
    else:
        return render(request, 'posting/post_edit.html', {'posting': my_posting})


def write_comment_view(request, id: int) -> HttpResponse:
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        try:
            current_posting = Posting.objects.get(id=id)
        except:
            return render(request, '404.html')
        user = request.user.is_authenticated
        if not user:
            return redirect('/api/user/login')
        PC = PostingComment()
        PC.comment = comment
        PC.author = request.user
        PC.author_name = request.user.username
        PC.posting = current_posting
        PC.save()

        return redirect('/api/posts/'+str(id))


@login_required
def comment_modify_view(request, id):
    try:
        comment = PostingComment.objects.get(id=id)
    except:
        return render(request, 'no_comment.html')
    current_posting = comment.posting.id
    if request.method == 'POST':
        my_comment = request.POST.get("comment", "")
        if (my_comment.strip() == ""):
            return render(request, 'posting/comment_edit.html', {'comment': comment, 'error': "please write comment!"})
        comment.comment = my_comment
        comment.save()
        return redirect('/api/posts/'+str(current_posting))
    else:
        return render(request, 'posting/comment_edit.html', {'comment': comment})


@login_required
def delete_comment_view(request, id):
    try:
        comment = PostingComment.objects.get(id=id)
    except:
        return redirect(request.GET.get('from', '/'))
    current_posting = comment.posting.id
    if comment.author == request.user or request.user.is_superuser:
        comment.delete()
    return redirect(request.GET.get('from', '/'))
