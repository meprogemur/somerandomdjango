from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    text = util.get_entry(title)
    if text is None:
        return HttpResponse("no such file")
    md = markdown.Markdown()
    text = md.convert(text)
 #   return HttpResponse(f"hello {title}")
    return render(request, "encyclopedia/info.html", {
        "text":text,
        "title":title
    })

def page(request):
    if request.method == "POST":
        title = request.POST["title"]
        if title in util.list_entries():
            return HttpResponse("already exist")
        elif title =="" or request.POST['content'] =="":
            return HttpResponse("please feel all")
        
        with open(f"entries/{title}.md", 'w') as f:
            f.write(request.POST["content"])
        url = reverse('title', kwargs={'title': title})
        return HttpResponseRedirect(url)
        #return HttpResponseRedirect(reverse("title"))

    return render(request, "encyclopedia/new.html")