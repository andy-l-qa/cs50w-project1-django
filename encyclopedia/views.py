from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown
import random

from . import util

class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'search',
            'placeholder': 'Search Wiki'
        }))
    
class CreateForm(forms.Form):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'create-form title', 
            'placeholder': 'Title'}))
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'create-form content', 
            'placeholder': 'Content'}))

class EditForm(forms.Form):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'create-form content', 
            'placeholder': 'Content'}))

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
    possible_entries = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            for entry in entries:
                if query.lower() == entry.lower():
                    return HttpResponseRedirect(reverse('wiki', args=[entry]))
                if query.lower() in entry.lower():
                    possible_entries.append(entry)

    return render(request, "encyclopedia/search.html", {
        "search_form": SearchForm(),
        "possible_entries": possible_entries
    })

def create(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            for entry in entries:
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/error.html", {
                        "message": "A page with the same title already exists."
                    })
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('wiki', args=[title]))            

    return render(request, "encyclopedia/create.html", {
        "search_form": SearchForm(),
        "create_form": CreateForm()
    })

def edit(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('wiki', args=[title])) 

    return render(request, "encyclopedia/edit.html", {
        "search_form": SearchForm(),
        "edit_form": EditForm(initial={'content': content}),
        "title": title
    })

def random_page(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('wiki', args=[entry]))