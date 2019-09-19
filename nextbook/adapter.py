from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adaptor import DefaultSocialAccountAdapter

# class MySocialAccount(DefaultSocialAccountAdapter):
#     def pre_social_login(self, request, sociallogin):
#         u = sociallogin.user
#         if not u.email.split('@')[1] == "virginia.edu"
#             raise ImmediateHttpResponse(render_to_response('error.html'))
