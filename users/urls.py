from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user,create_group,assign_role,respond,cancel_response,group_list,CustomLoginView,GroupView,CustomSignUp,profile,EditProfileView,ProfileView,ChangePassword,CustomPasswordResetView,CustomPasswordResetConfirmView,CreateGroupView
from django.contrib.auth.views import LogoutView,PasswordChangeDoneView

urlpatterns = [
    # path('sign_up/',sign_up,name='sign-up'),
    path('sign_up/',CustomSignUp.as_view(),name='sign-up'),
    # path('sign_in/',sign_in,name='sign-in'),
    path('sign_in/',CustomLoginView.as_view(),name='sign-in'),
    # path('sign_out/',sign_out,name='sign-out'),
    path('sign_out/',LogoutView.as_view(),name='sign-out'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    # path('create_group/',create_group,name='create-group'),
    path('create_group/',CreateGroupView.as_view(),name='create-group'),
    path('assign_role/<int:user_id>/',assign_role,name='assign-role'),
    path('respond/<int:e_id>/',respond,name='respond'),
    path('cancel/<int:e_id>/', cancel_response, name='cancel-response'),
    # path('group_list/',group_list,name='group-list'),
    path('group_list/',GroupView.as_view(),name='group-list'),
    # path('profile/',profile,name='profile'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('edit_profile/',EditProfileView.as_view(),name='edit_profile'),
    path('password_change/',ChangePassword.as_view(),name='password_change'),
    path('password_change/done',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
    path('password_reset/',CustomPasswordResetView.as_view(),name="password-reset"),
    path('password_reset/confirm/<uidb64>/<token>',CustomPasswordResetConfirmView.as_view(),name="password_reset_confirm"),
]
