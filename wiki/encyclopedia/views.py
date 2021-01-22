from django.shortcuts import render
from django.http import HttpResponse
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
