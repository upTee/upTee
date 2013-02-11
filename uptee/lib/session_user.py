from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


def get_user(request):
    sessions = Session.objects.filter(session_key=request.COOKIES.get('sessionid'))
    if not sessions:
        return None
    uid = sessions[0].get_decoded().get('_auth_user_id')
    if not uid:
        return None
    users = User.objects.filter(pk=uid)
    if not users:
        return None
    return users[0]
