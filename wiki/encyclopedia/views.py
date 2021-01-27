from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown
import random

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

def ran(request):
    title = random.choice(util.list_entries())
    url = reverse('title', kwargs={'title': title})
    return HttpResponseRedirect(url)    

def page(request):
    if request.method == "POST":
        title = request.POST["title"]
        if title in util.list_entries():
            return HttpResponse("already exist")
        elif title =="" or request.POST['content'] =="":
            return HttpResponse("please fill all")
        
        with open(f"entries/{title}.md", 'w') as f:
            f.write(request.POST["content"])
        url = reverse('title', kwargs={'title': title})
        return HttpResponseRedirect(url)
        #return HttpResponseRedirect(reverse("title"))

    return render(request, "encyclopedia/new.html")

def search(request):
    result = []
    if request.method == "GET":
        for title in util.list_entries():
            tit = title.lower()
            check = request.GET["q"].lower()
            if (tit.find(check) == -1):
                pass
            else:
                result.append(title)
            if title.lower() == check:
                return HttpResponseRedirect(reverse("title", kwargs={'title': title}))
        return render(request, "encyclopedia/slist.html", {
            "q": check,
            "match": result
        })

def edit(request, ed):
    if request.method == "POST":
        if request.POST["edited"] == "":
            return HttpResponse("can't be blank")
        with open("entries/" + ed + ".md", 'w') as f:
            f.write(request.POST["edited"])
        return HttpResponseRedirect(reverse('title', kwargs={'title': ed}))
    with open("entries/" + ed + ".md", 'r') as f:
        txt = f.read()
    
    return render(request, "encyclopedia/edit.html", {
        "text":txt,
        "title":ed
    })