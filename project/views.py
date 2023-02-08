from django.shortcuts import render
from django.template import RequestContext

def error404(request, exception, template_name="404.html"):
    return render(request, "bilti/404.html", {})

def error500(request,  *args, **argv):
    return render(request, "bilti/500.html", {})
    
def index(request):
    if request.user.is_authenticated:
        print(request.user)
        return render(request, "bilti/index.html", {})
    return render(request, "user/auth.html", {})
    # response = render_to_response(
    #     '400.html',
    #     context_instance=RequestContext(request)
    #     )

    # response.status_code = 400

    # return response