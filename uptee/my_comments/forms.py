from django_comments.forms import CommentForm
from django.utils.html import escape
from markdown import markdown


class CommentMarkdownForm(CommentForm):

    def clean_comment(self):
        comment = super(CommentMarkdownForm, self).clean_comment()
        comment = escape(comment)
        comment = markdown(comment)
        return comment
