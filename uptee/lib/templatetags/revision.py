from django import template
from django.core.cache import cache

register = template.Library()

@register.simple_tag
def revision():
	rev = cache.get('current_revision')
	if rev == None:
		from lib.revision_hook import get_revision, set_cache
		rev = get_revision()
		set_cache(rev)
	return "r<a href=\"https://github.com/upTee/upTee/commit/{0}\">{1}</a>".format(rev, rev[:7])
