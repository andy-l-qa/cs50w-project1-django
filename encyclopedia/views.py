from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown

from . import util

class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Wiki'
        }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "search_form": SearchForm(),
        "entries": util.list_entries()
    })

def wiki(request, title):
    entry = util.get_entry(title)

    # If page doesn't exist
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page was not found."
        })

    return render(request, "encyclopedia/wiki.html", {
        "search_form": SearchForm(),
        "title": title,
        "entry": markdown.markdown(entry)
    })

def search(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            for entry in entries:
                if query.lower() == entry.lower():
                    # return redirect('wiki', entry)
                    return HttpResponseRedirect(reverse('wiki', args=[entry]))


    return render(request, "encyclopedia/search.html", {
        "search_form": SearchForm()
    })
