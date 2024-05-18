from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def project_required(get_response):
    """
        If a user access a page but has no applicaiton registered, we redirect to the welcome page
    """
    def middleware(request):
        if not request.user.is_anonymous\
            and request.user.projects.count() == 0\
            and request.path != '/welcome/'\
            and request.path != '/logout/'\
            and request.path != '/settings/user/delete'\
            and not request.path.startswith('/admin/')\
            and request.path != '/restricted/':
            response = HttpResponseRedirect('/welcome/')
        else:
            response = get_response(request)
        return response

    return middleware
