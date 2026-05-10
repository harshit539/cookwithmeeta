from django.shortcuts import render
from .models import Video
from django.core.paginator import Paginator

def home(request):
    query = request.GET.get('q', '')

    videos = Video.objects.only(
        'title', 'thumbnail', 'video_id', 'category', 'published_at'
    ).order_by('-published_at')

    # search
    if query:
        videos = videos.filter(title__icontains=query)

    # pagination add
    paginator = Paginator(videos, 25)   # 25 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'videos': page_obj,
        'page_obj': page_obj,
        'query': query,
        'latest_video': Video.objects.order_by('-published_at').first(),
    }

    return render(request, 'index.html', context)
