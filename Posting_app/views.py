
from django.shortcuts import render, redirect
from .models import Posting, PostingComment, PostingImage
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.


def home(request):
    return redirect('/api/posts')


def post_view(request):
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
    
def search(request):
    if request.method == 'GET':
        searched = request.GET.get("searched","")     
        posts = Posting.objects.filter(content__contains=searched).order_by('-created_at')
        if posts.exists() == False:
            return render(request, 'posting/searched.html', {'searched': searched, 'error': "찾으시는 검색어를 가진 글은 존재하지 않습니다."}) 
        count = posts.count()
        page = int(request.GET.get('page','1'))
        paginator = Paginator(posts,5)
        post_list = paginator.get_page(page)
        return render(request, 'posting/searched.html', {'searched': searched, "post_list": post_list, 'count':count})
    else:
        return render(request, 'posting/searched.html', {})

@login_required
def delete_posting_view(request, id):
    my_post = Posting.objects.get(id=id)
    if my_post.author == request.user:
        my_post.delete()
    go_to = request.GET.get('from', '/')
    print(go_to)
    return redirect(go_to)

    # return HttpResponse('글 삭제 완료')


def posting_detail_view(request, id):
    my_posting = Posting.objects.get(id=id)
    posting_comment = PostingComment.objects.filter(posting_id=id)
    return render(request, 'posting/post_detail.html', {'posting': my_posting, 'comment': posting_comment})


@login_required
def posting_edit_view(request, id):
    print(request.FILES)
    # 1. id가 0 인지 확인
    if id == 0:
        my_posting = Posting()
        my_posting.title = ""
        my_posting.content = ""
        my_posting.category = "recipe"
        my_posting.author = request.user

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
        category = request.POST.get("category", "recipe")
        my_posting.title = title
        my_posting.content = content
        # title, content 내용 없으면 다시 랜더링
        if (title.strip() == "") or (content.strip() == ""):
            return render(request, 'posting/post_edit.html', {'posting': my_posting, 'error': "please write title and content!"})
        my_posting.category = category
        my_posting.save()
        for post_image in my_posting.embed.all():
            delete_check = request.POST.get(str(post_image.id), '')
            if delete_check == 'on':
                post_image.image.delete(save=False)
                post_image.delete()

        for img in request.FILES.getlist('images'):
            print(my_posting.title, img)
            photo = PostingImage()
            # 외래키로 현재 생성한 Post의 기본키를 참조한다.
            photo.posting = my_posting
            # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            photo.image = img
            # 데이터베이스에 저장
            photo.save()
        my_posting.save()
        return redirect('/api/posts/'+str(id)) if id else redirect('/api/posts')
    else:
        return render(request, 'posting/post_edit.html', {'posting': my_posting})


def write_comment_view(request, id: int) -> HttpResponse:
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
def comment_modify_view(request, id):
    comment = PostingComment.objects.get(id=id)
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
    comment = PostingComment.objects.get(id=id)
    current_posting = comment.posting.id
    if comment.author == request.user:
        comment.delete()
    return redirect('/api/posts/'+str(current_posting))

