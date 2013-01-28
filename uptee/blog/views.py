from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from blog.models import Entry


def blog_home(request):
    if request.user.is_staff or request.user.is_superuser:
        entries = Entry.objects.exclude(status=Entry.DRAFT_STATUS)
    else:
        entries = Entry.objects.filter(status=Entry.PUBLISHED_STATUS)
    return render_to_response('blog/home.html', {'entry_list': entries}, context_instance=RequestContext(request))


def entry_detail(request, slug):
    if request.user.is_staff or request.user.is_superuser:
        entries = Entry.objects.exclude(status=Entry.DRAFT_STATUS)
    else:
        entries = Entry.objects.filter(status=Entry.PUBLISHED_STATUS)
    entry = get_object_or_404(
        entries.select_related(),
        slug=slug
    )
    return render_to_response('blog/entry_detail.html', {'entry': entry}, context_instance=RequestContext(request))
