from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.views.generic.edit import DeleteView
from django import forms
from allauth.account.views import SignupView, LoginView, PasswordResetView
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.contrib import messages
from .choices import subject_choices



class MySignupView(SignupView):
    template_name = 'registration/signup.html'

class MyPasswordReset(PasswordResetView):
    template_name = 'password_reset.html'

# User sign up
# class SignUp(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'

# User profile
class ProfileView(UserPassesTestMixin, DetailView):
    def test_func(self):
        return(self.request.user.id == int(self.kwargs['pk']))
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        id = int(self.kwargs['pk'])
        # Add in a QuerySet of all the books
        context['my_books'] = Posting.objects.all().filter(user=id)
        return context
    context_object_name = 'profile'
    queryset = User.objects.all()

# Profile edit
@login_required
def profile_edit(request, pk):
    if request.user.id != int(pk):
        return redirect('/login/')
    instance = User.objects.get(pk=pk)
    user_form = UserEditForm(request.POST or None, instance=request.user)
    profile_form = ProfileEditForm(request.POST or None, instance=request.user.profile)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, _('Your profile was successfully updated!'))
        return redirect(reverse_lazy('profile-detail', kwargs= {'pk': pk}))
    return render(request, 'profile_edit.html', {'user_form': user_form,'profile_form': profile_form,})

# Create a new post
class PostingCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Posting
    fields = ['book_title', 'subject_area', 'class_assoc', 'iSBN', 'price', 'rent_buy', 'image']
    template_name = 'posting_form.html'
    success_url = reverse_lazy('home')
    def post(self, request, *args, **kwargs):
        form = PostingForm(request.POST, request.FILES)
        user = self.request.user.id
        form.instance.user_id = user
        name =  self.request.user.username
        email =  self.request.user.email
        form.instance.seller_name = name
        form.instance.contact = email
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, form.instance.book_title+" was created successfully")
            return render(request, 'posting_form.html', {'form': form})
        return render(request, 'posting_form.html', {'form': form})
    def form_valid(self, form):
        return super().form_valid(form)

    def __str__(self):
        return 'post_form'

# List all posts
class PostDetailView(LoginRequiredMixin,DetailView):
    context_object_name = 'post'
    queryset = Posting.objects.all()

# Update a post
class PostingUpdate(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Posting
    template_name = 'posting_form.html'
    fields = ['book_title', 'subject_area', 'class_assoc', 'iSBN', 'price', 'contact', 'rent_buy', 'image']
    def test_func(self):
        book = Posting.objects.get(pk = self.kwargs['pk'])
        return(self.request.user.id == int(book.user_id))
    def get_success_url(self, **kwargs):
        if  kwargs != None:
            return reverse_lazy('profile-detail', kwargs = {'pk': self.request.user.id})
        else:
            return reverse_lazy('profile-detail', args = (self.request.user.id,))


# @login_required
def HomepageRender(request):
    posts_list = Posting.objects.all()
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'posts': posts})

@login_required
def my_books(request,pk):
    if request.user.id != int(pk):
        return redirect('/login/')
    my_books=Posting.objects.all().filter(user=pk)
    return render(request,"my_books.html",{'my_books':my_books})

@login_required
def search_result(request):
    if request.method == 'GET':
        title = request.GET.get('book_title')
        class_assoc = request.GET.get('class')
        iSBN = request.GET.get('iSBN')
        result = Posting.objects.all()
        if (title):
            result = result.filter(book_title__icontains = title)
        if (class_assoc):
            result = result.filter(class_assoc__icontains = class_assoc)
        if (iSBN):
            result = result.filter(iSBN__icontains = iSBN)
        return render(request, 'search_result.html', {'result': result})
    else:
        return render(request, 'search_result.html', {'result': []})

@login_required
def search(request):
    if request.method == 'GET':
        book_name =  request.GET.get('usr_query')
        status = {}
        try:
            posts = Posting.objects.filter(book_title__icontains = book_name)
        except:
            pass
        return render(request,"home.html",{'posts': posts})
    else:
        return render(request,"home.html",{})

class PostingDelete(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Posting
    def test_func(self):
        book = Posting.objects.get(pk = self.kwargs['pk'])
        return(self.request.user.id == int(book.user_id))
    success_url = reverse_lazy('home')
