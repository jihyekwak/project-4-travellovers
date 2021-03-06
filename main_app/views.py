from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser, Travel, Itinerary, Destination, Comment, Tag, List
from .forms import CustomUserCreationForm, CustomUserChangeForm, ItineraryForm, CommentForm, TravelForm, ListForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model


# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.order_by('?')[:4]
        context['travels'] = Travel.objects.order_by('?')[:4]
        return context

class Travel_List(TemplateView):
    template_name = 'travel_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['users'] = CustomUser.objects.all()
        title = self.request.GET.get("title")
        tag = self.request.GET.get("tag")
        if title != None:
            context['travels'] = Travel.objects.filter(title__icontains=title)
            context['header'] = f"Searching for {title}"
        elif tag !=None:
            context['travels'] = Travel.objects.filter(tags__name__icontains=tag)
            context['header'] = f"Searching for {tag}"
        else:
            context['travels'] = Travel.objects.all()
            context['header'] = "All Travels"
        return context

@login_required
def travel_create(request):
    form = TravelForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            form.instance.travelers.add(str(request.user.pk))
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                tag=tag.strip().lower()
                if '#' in tag:
                    tag = tag.replace('#', '')
                if len(tag) != 0:
                    tag, created = Tag.objects.get_or_create(name=tag)
                    form.instance.tags.add(tag)
            destinations = form.cleaned_data['destinations']
            for destination in destinations:
                form.instance.destinations.add(destination)
            return HttpResponseRedirect("/travels/")
    return render(request, 'travel_create.html', {'form':form})

def travel_detail(request, pk):
    travel = Travel.objects.get(pk = pk)
    lists = List.objects.filter(travel = pk)
    packing_list = lists.filter(category__icontains= 'Packing')
    confirm_list = lists.filter(category__icontains = 'confirm')
    todo_list = lists.filter(category__icontains = 'to do')
    list_form = ListForm(request.POST)
    comment_form = CommentForm(request.POST)
    if request.method == "POST":
        if list_form.is_valid():
            list_form.instance.travel = travel
            list_form.save()
            return HttpResponseRedirect("/travels/"+str(pk))
        if comment_form.is_valid():
            comment_form.instance.author = request.user
            comment_form.instance.travel = travel
            comment_form.save()
            return HttpResponseRedirect("/travels/"+str(pk))
    return render(request, 'travel_detail.html', {'travel': travel, 'list_form':list_form, 'comment_form':comment_form, 'packing_list': packing_list, 'confirm_list': confirm_list, 'todo_list':todo_list})

@login_required
def comment_update(request, pk, comment_id):
    comment = Comment.objects.get(id=comment_id)
    form = CommentForm(request.POST or None, instance = comment)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/travels/"+str(pk))
    return render(request, 'comment_update.html', {'comment':comment, 'form':form})

@login_required
def comment_delete(request, pk, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponseRedirect("/travels/"+str(pk))

@method_decorator(login_required, name='dispatch')
class Travel_Update(UpdateView):
    model = Travel
    # fields = '__all__'
    form_class = TravelForm
    template_name = 'travel_update.html'
    # form_class = TravelForm
    
    def get_success_url(self):
        return reverse('travel_detail', kwargs={'pk': self.object.pk})

    def get_initial(self):
        taglist = Tag.objects.filter(travel = self.object.pk).values_list('name', flat=True)
        return {"tags": ', '.join(taglist)}

    def form_valid(self, form):
        self.object.tags.clear()
        self.object = form.save(commit=False)
        tags = form.cleaned_data['tags'].split(',')
        for tag in tags:
            tag=tag.strip().lower()
            if '#' in tag:
                tag = tag.replace('#', '')
            if len(tag) != 0:
                tag, created = Tag.objects.get_or_create(name=tag)
                self.object.tags.add(tag)
        self.object.save()
        return super(Travel_Update, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Travel_Delete(DeleteView):
    model = Travel
    template_name = 'travel_delete_confirmation.html'
    success_url = '/travels/'

@method_decorator(login_required, name='dispatch')
class Itinerary_Create(CreateView):
    model = Itinerary
    fields = '__all__'
    template_name = 'itinerary_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        travel = self.kwargs.get("pk")
        context['travel'] = Travel.objects.get(pk=travel)
        return context

    def get_initial(self):
        return {"travel": self.kwargs.get("pk")}

    def get_success_url(self):
        return reverse('travel_detail', kwargs={'pk': self.object.travel.id})
    
    def from_valid(self, form):
        self.object = form.save(commit = False)
        self.object.travel = self.request.travel
        self.object.save()

@login_required
def itinerary_update(request, pk, itinerary_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    travel = Travel.objects.get(pk=pk)
    form = ItineraryForm(request.POST or None, instance = itinerary)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/travels/"+str(pk))
    return render(request, 'itinerary_update.html', {'itineray':itinerary, 'form':form, 'travel':travel})

@login_required
def itinerary_delete(request, pk, itinerary_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    if request.method == "POST":
        itinerary.delete()
        return HttpResponseRedirect("/travels/"+str(pk))
    return render(request, "itinerary_delete_confirmation.html", {'itinerary':itinerary})

class Destination_List(TemplateView):
    template_name = 'destination_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get("city")
        continent = self.request.GET.get("continent")
        if city != None:
            context['destinations'] = Destination.objects.filter(city__icontains=city)
            context['header'] = f"Searching for {city}"
            context['nav'] = f"{city}"
        elif continent !=None:
            context['destinations'] = Destination.objects.filter(continent__icontains=continent)
            context['header'] = f"Searching for {continent}"
            context['nav'] = f"{continent}"
        else:
            context['destinations'] = Destination.objects.all()
            context['header'] = "All Destinations"
            context['nav'] = "All"
        return context

@method_decorator(login_required, name='dispatch')
class Destination_Create(CreateView):
    model = Destination
    fields = '__all__'
    template_name = 'destination_create.html'
    success_url = "/destinations/"

class Destination_Detail(DetailView):
    model = Destination
    template_name = 'destination_detail.html'

@method_decorator(login_required, name='dispatch')
class Destination_Update(UpdateView):
    model = Destination
    fields = '__all__'
    template_name = 'destination_update.html'
    
    def get_success_url(self):
        return reverse('destination_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class Destination_Delete(DeleteView):
    model = Destination
    template_name = 'destination_delete_confirmation.html'
    success_url = "/destinations/"

def checklist_list(request, pk):
    travel = Travel.objects.get(pk = pk)
    lists = List.objects.filter(travel = pk)
    packing_list = lists.filter(category__icontains= 'Packing')
    confirm_list = lists.filter(category__icontains = 'Confirm')
    todo_list = lists.filter(category__icontains = 'to do')
    list_form = ListForm(request.POST)
    if request.method == "POST":
        if list_form.is_valid():
            list_form.instance.travel = travel
            list_form.save()
            return HttpResponseRedirect("/travels/"+str(pk)+"/checklists")
    return render(request, 'checklist_list.html', {'travel': travel, 'list_form':list_form, 'packing_list': packing_list, 'confirm_list': confirm_list, 'todo_list':todo_list})

@login_required
def is_completed(request, pk, item_id):
    list_item = List.objects.get(id= item_id)
    list_item.is_completed = True
    list_item.save()
    return HttpResponseRedirect('/travels/'+str(pk)+"/checklists")

def is_not_done(request, pk, item_id):
    list_item = List.objects.get(id= item_id)
    list_item.is_completed = False
    list_item.save()
    return HttpResponseRedirect('/travels/'+str(pk)+"/checklists")

def checklist_delete(request, pk, item_id):
    list_item = List.objects.get(id= item_id)
    list_item.delete()
    return HttpResponseRedirect('/travels/'+str(pk)+"/checklists")

def checklist_update(request, pk, item_id):
    list = List.objects.get(id=item_id)
    # travel = Travel.objects.get(pk=pk)
    form = ListForm(request.POST or None, instance = list)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/travels/"+str(pk)+"/checklists")
    return render(request, 'checklist_update.html', {'list':list, 'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    return render(request, 'login.html', {'form': form})
            else:
                return render(request, 'login.html', {'form': form})
        else: 
            return render(request, 'signup.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('Hi', user.username)
            return HttpResponseRedirect('/user/' + str(user))
        else:
            return render(request, 'signup.html', {'form':form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form':form})

@login_required
def profile(request, username):
    user = get_user_model().objects.get(username = username)
    travels = Travel.objects.filter(travelers__username = username)
    tags = Tag.objects.filter(travel__travelers__username = username).distinct()
    tag = request.GET.get("tag")
    if tag != None:
        travels = travels.filter(tags__name__icontains = tag)
        nav = f"{tag}"
    else:
        nav = "All Travels"
    return render(request, 'profile.html', {'user':user, 'travels':travels, 'tags':tags, 'tag':tag, 'nav':nav})

@method_decorator(login_required, name='dispatch')
class Profile_Update(UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = 'profile_update.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.object.username})


# class Users(TemplateView):
#     template_name='users.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['users'] = CustomUser.objects.all()
#         return context
