
from django.shortcuts import render, redirect
from .models import Posting, PostingComment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return redirect('/api/posts')


def post_view(request):
    if request.method == 'GET':
        category = request.GET.get('category', '')
        all_post = []
        if category:
            all_post = Posting.objects.filter(
                category=category).order_by('-created_at')
        else:
            all_post = Posting.objects.all().order_by('-created_at')
        return render(request, 'posting/post.html', {'posts': all_post})
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
    my_post = Posting.objects.get(id=id)
    if my_post.author == request.user:
        my_post.delete()
    return redirect('/api/posts')

    # return HttpResponse('글 삭제 완료')


def posting_detail_view(request, id):
    my_posting = Posting.objects.get(id=id)
    posting_comment = PostingComment.objects.filter(posting_id = id)
    return render(request,'posting/post_detail.html',{'posting':my_posting,'comment':posting_comment})
   
@login_required
def posting_edit_view(request, id):
    # 1. id가 0 인지 확인
    if id==0:
        my_posting=Posting()
        my_posting.title=""
        my_posting.content=""
        my_posting.category="recipe"
        my_posting.author=request.user
    
    # 2. id가 0 이면, 새로운 포스팅 모델 객체를 만들면 됩니다.
    # 3. 0이 아니라면, 바로 여기아래 있는 코드한줄이 실행되면 됩니다.
    else:
        my_posting = Posting.objects.get(id=id)
    # 4. 작성자와 동일한 사용자인지 체크하고 아니면 되돌려보내기
    if request.user != my_posting.author:
        return redirect('/api/posts/'+str(id)) if id else redirect('/api/posts')
    if request.method == 'POST':
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        category=request.POST.get("category", "recipe")
        my_posting.title = title
        my_posting.content = content
        # title, content 내용 없으면 다시 랜더링
        if (title.strip() == "")or(content.strip()==""):
            return render(request, 'posting/post_edit.html', {'posting':my_posting,'error':"please write title and content!"})
        my_posting.category=category
        my_posting.save()
        return redirect('/api/posts/'+str(id)) if id else redirect('/api/posts')
    else:
        return render(request, 'posting/post_edit.html', {'posting':my_posting})


def write_comment_view(request,id:int) -> HttpResponse:
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

        return redirect('/api/posts/'+str(id))


@login_required
def delete_comment_view(request, id):
    comment = PostingComment.objects.get(id=id)
    current_posting = comment.posting.id
    if comment.author == request.user:
        comment.delete()
    return redirect('/api/posts/'+str(current_posting))
