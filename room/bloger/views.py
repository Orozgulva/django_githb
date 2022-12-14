from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post
from .forms import  CommentForm
from taggit.models import Tag
from django.db.models import Count




class PostListView(ListView):
    queryset=Post.objects.all()
    context_object_name = 'posts' 
    paginate_by = 3
    template_name = 'bloger/post/list.html'

def post_list(request, tag_slug=None): 
    object_list = Post.objects.all() 
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug) 
        object_list = object_list.filter(tags__in=[tag])
   
    paginator = Paginator(object_list, 3) # По 3 статьи на каждой странице. page = request.GET.get('page')
    page = request.GET.get('page')
    try:
        posts = paginator.page(page) 
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1) 
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)
    return render(request,'bloger/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)
            # Список активных комментариев для этой статьи. 
    comments = post.comments.filter(active=True) 
    new_comment = None
    if request.method == 'POST':
            # Пользователь отправил комментарий. 
        comment_form = CommentForm(data=request.POST) 
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных. 
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье. 
            new_comment.post = post
                # Сохраняем комментарий в базе данных.
            new_comment.save()
    else:
        comment_form = CommentForm()

    
# Формирование списка похожих статей.
        post_tags_ids = post.tags.values_list('id', flat=True) 
        similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]    
    return render(request,'bloger/post/detail.html',{'post': post, 'comments': comments,'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts })
                                                                                                    