from django.http.response import Http404
from django.shortcuts import render, redirect
from molten.models import *
from molten.forms import *


def new_visitor(request):
    """
    Randomly create a new room, and redirect to it.
    """
    print request
    if request.method == 'GET':
        form = VisitorForm()
        return render(request, "molten/new_visitor.html", {
            'form': form
        })

    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            handle = form.cleaned_data['handle']
            n_visitor, created = Visitor.objects.get_or_create(handle=handle)
            # Just send them to auto123 world for now
            return redirect(world_instance, visitor_handle=handle)
        else:
            raise Http404("Form invalid, mate!")


def world_instance(request, visitor_handle):
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    world, created = World.objects.get_or_create(label="auto123")
    visitor = Visitor.objects.get(handle=visitor_handle)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(world.messages.order_by('-timestamp')[:5])

    return render(request, "molten/world.html", {
        'world': world,
        'messages': messages,
        'visitor': visitor
    })