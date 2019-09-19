"""src URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
import nextbook.views as views
from django import forms
from django.conf import settings
from nextbook.views import PostingUpdate, PostingDelete
from django.conf.urls.static import static
from allauth.account.views import SignupView, LoginView, PasswordResetView

class MySignupView(SignupView):
    template_name = 'signup.html'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.HomepageRender, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # new
    path('signup/', views.MySignupView.as_view(template_name = 'account_signup.html'), name='account_signup'),
    path('search/', views.search, name='search'),
    path('posting/', views.PostingCreate.as_view(), name='posting_form'),
    url(r'^accounts/password/reset/', views.MyPasswordReset.as_view(template_name = 'password_reset.html'), name='password_reset'),
    url(r'^accounts/social/signup/', views.MySignupView.as_view(template_name = 'signup.html'), name='account_signup'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^post/(?P<pk>\d+)/', views.PostDetailView.as_view(template_name='post_detail.html'), name='post-detail'),
    # url('^signup/', CreateView.as_view(
    #     template_name='signup.html',
    #     form_class=forms.Form,
    #     success_url='/'
    # ), name='signup'),
    url(r'^profile/(?P<pk>\d+)/', views.ProfileView.as_view(template_name='profile_detail.html'),
        name='profile-detail'),
    url(r'^profile_edit/(?P<pk>\d+)/', views.profile_edit,
        name='profile-edit'),
    #url(r'^mybooks/(?P<pk>\d+)/', views.my_books, name="my_books"),
    url(r'^update/(?P<pk>\d+)/', PostingUpdate.as_view(), name='post-update'),
    path('search_result/', views.search_result, name='search_result'),
    url(r'^search/$', views.search, name='search'),
    url(r'^delete/(?P<pk>\d+)/$', PostingDelete.as_view(template_name='posting_confirm_delete.html'), name = 'post-delete'),
    # path('post/<int:pk>', views.PostDetailView.as_view(template_name='post_detail.html'), name='post_detail')
    # re_path(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(template_name='post_detail.html'), name='post-detail'),
    # The django.contrib.auth.urls allows access to:
    # -/login/ [name='login']
    # -/logout/ [name='logout']
    # -/password_change/ [name='password_change']
    # -/password_change/done/ [name='password_change_done']
    # -/password_reset/ [name='password_reset']
    # -/password_reset/done/ [name='password_reset_done']
    # -/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # -/reset/done/ [name='password_reset_complete']
    # The html files should be under src/templates/, if not, default will be used
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
