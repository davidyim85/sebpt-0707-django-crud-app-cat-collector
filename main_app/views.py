from django.shortcuts import render, redirect
from .models import Cat, Toy

# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# Add the following import
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import FeedingForm
from django.contrib.auth.views import LoginView
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# Define the home view function
# def home(request):
#     # Send a simple HTML response
#     return render(request, "home.html")


def about(request):
    # Send a simple HTML response
    return render(request, "about.html")


# views.py
@login_required
def cat_index(request):
    # Render the cats/index.html template with the cats data
    # cats = Cat.objects.all()  # look familiar?
    cats = Cat.objects.filter(user=request.user) #give me all the cat for the user
    return render(request, "cats/index.html", {"cats": cats})

@login_required
def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # instantiate FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    # toys = Toy.objects.all()  # Fetch all toys
    # Only get the toys the cat does not have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list("id"))
    return render(
        request,
        "cats/detail.html",
        {
            # include the cat and feeding_form in the context
            "cat": cat,
            "feeding_form": feeding_form,
            "toys": toys_cat_doesnt_have,  # Pass toys to the template
        },
    )

@login_required
def add_feeding(request, cat_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect("cat-detail", cat_id=cat_id)

@login_required
def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect("cat-detail", cat_id=cat_id)

@login_required
def remove_toy(request, cat_id, toy_id):
    # Look up the cat
    # Look up the toy
    # Remove the toy from the cat
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect("cat-detail", cat_id=cat_id)


class CatCreate(
    LoginRequiredMixin,
    CreateView
):  # Now we can inherit from CreateView to create our own CBV used to create catscreate:
    model = Cat
    # fields = '__all__' # We’ve taken advantage of the special '__all__' value to specify that the form should contain all of the Cat Model’s attributes. Alternatively, we could have listed the fields in a list like this: fields = ['name', 'breed', 'description', 'age']
    fields = ["name", "breed", "description", "age"]

    # This inherited method is called when a
    # valid cat form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )


class CatUpdate(LoginRequiredMixin,UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ["breed", "description", "age"]


class CatDelete(DeleteView):
    model = Cat
    success_url = "/cats/"


class ToyCreate(
    LoginRequiredMixin,
    CreateView
):  # Now we can inherit from CreateView to create our own CBV used to create catscreate:
    model = Toy
    fields = "__all__"  # We’ve taken advantage of the special '__all__' value to specify that the form should contain all of the Cat Model’s attributes. Alternatively, we could have listed the fields in a list like this: fields = ['name', 'breed', 'description', 'age']


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(DeleteView):
    model = Toy
    success_url = "/toys/"


class Home(LoginView):
    template_name = "home.html"
