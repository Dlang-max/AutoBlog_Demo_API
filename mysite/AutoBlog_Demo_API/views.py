import os
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import GenerateBlogForm
from .tasks import generate_and_post_blog

AUTOBLOG_DEMO_API_KEY = os.environ.get("AUTOBLOG_DEMO_API_KEY")

def home(request):
    """Endpoint that displays "AutoBlog Demo API" as an h2 HTML element
    on a webpage. Used to ensure API is running when in production.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return HttpResponse("<h2>AutoBlog Demo API</h2>")

@csrf_exempt
def create_blog(request):
    """API endpoint for generating a blog. If the POST request is formatted correctly,
    a blog will get generated and uploaded to WordPress.

    Args:
        request (HttpRequest): The HTTP request sent to this API endpoint. This request
        must be a POST request. 

    Returns:
        HttpResponse: The HTTP response returned by this endpoint. Returns a status code
        of 200 for POST requests. 
    """
    if request.method == "POST":
        form = GenerateBlogForm(request.POST)
        if form.is_valid():
            # Jotform won't send AUTOBLOG_DEMO_API_KEY in headers.
            # It needs to be a part of the POST request's body.  
            key = form.cleaned_data["AUTOBLOG_DEMO_API_KEY"]
            if(AUTOBLOG_DEMO_API_KEY == key):
                title = form.cleaned_data["title"]
                generate_and_post_blog.delay(title=title)
            return HttpResponse("Blog Generating", status=200)