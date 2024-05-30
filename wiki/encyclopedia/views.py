from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import util
import random, markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = markdown2.markdown(util.get_entry(title))
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The requested page ({title}) was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": content,
        })

def search(request):
    query = request.GET.get("q","")
    if query:
        entries = util.list_entries()
        matchingEntries = [entry for entry in entries if query.lower() in entry.lower()]
        if len(matchingEntries) == 1 and matchingEntries[0].lower() == query.lower():
            title=matchingEntries[0]
            return HttpResponseRedirect(reverse("entry",kwargs={"title": title,
                                                                
                                                                }))
        else:
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "results": matchingEntries
            })
    else:
        return HttpResponseRedirect(reverse("index"))
    
def createPage(request):
    entries = util.list_entries()
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, 'encyclopedia/error.html', {
                    "message": f"Error: The file {title} already exists, please create something different"
                })
        content = f"#{title} \n{content}"
        #if title does not already exist
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse('entry', kwargs={
            "title": title,
            }))   
    else:
        return render(request, 'encyclopedia/createPage.html')
    

def editPage(request,title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse('entry', kwargs={
            "title": title,
            }))   
    else:
        content = util.get_entry(title)
        #if the user gets to the edit page by changing the URL rather than the edit page button
        if content == None:
            return render(request, "encyclopedia/error.html", {
            "title": title,
            "message": f"The page ({title}) you have requested to edit does not exist"
        })            
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "content": content
        })
    
def randomiser(request):
    entries = util.list_entries()
    title = entries[random.randint(0,len(entries)-1)]
    content = util.get_entry(title)
    return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": content
        })