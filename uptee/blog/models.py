from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db import models
from markdown import markdown


class Entry(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)
    content = models.TextField('Inhalt', help_text='You may use markdown.')
    content_html = models.TextField()

    PUBLISHED_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (PUBLISHED_STATUS, 'published'),
        (DRAFT_STATUS, 'draft'),
        (HIDDEN_STATUS, 'hidden'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS)

    def slugify_title(self):
        new_slug = slug = slugify(self.title) or "bad-title"
        # preventing slugs from being non-unique, wordpress-style
        n = 1
        while True:
            try:
                Entry.objects.get(slug=new_slug)
            except Entry.DoesNotExist:
                break
            n += 1
            if n != 1:
                new_slug = "{0}-{1}".format(slug, n)
        return new_slug

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = self.slugify_title()
        self.content_html = markdown(self.content)
        super(Entry, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return (
            'entry_detail',
            (),
            {'entry_id': self.id, 'slug': self.slug},
        )
