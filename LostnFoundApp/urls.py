from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

urlpatterns =[
    path('',views.home,name = 'home'),

    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view,name='login'),
    path('user/resendOTP/',views.resend_otp),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name="logout"),
    
    path('profile/',views.profile,name ='profile'),
    path('editprofile/',views.editprofile,name ='editprofile'),
    path('addpost/',views.addpost,name='addpost'),
    path('lost/',views.lost,name='lost'),
    path('found/',views.found,name='found'),
    path('posts/',views.posts,name = 'posts'),
    path('about/',views.about,name='about'),
    path('privacy/',views.privacy,name='privacy'),
    path('instructions/',views.instructions,name='instructions'),
    path('search/',views.search,name = 'search'),

    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name = 'passwordchangedone'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='passwordchange'),


    path('password-rest/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name="password_reset"),
    path('password-rest/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name="password_reset_done"),
    path('password-rest-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name="password_reset_confirm"),
    path('password-rest-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name="password_reset_complete"),

    path('details/<int:pk>',views.details,name='details'),
    path('add_comment_to_post/<int:pk>/', views.add_comment_to_post, name='add_comment_to_post'),
    path('search/',views.search,name = 'search'),
    path('add_reply_to_comment/<int:comment_pk>/', views.reply_create_view, name='add_reply_to_comment'),
    path('<str:username>/', views.user_detail, name='user_detail'),

    path('alert_owner/<int:pk>/',views.alert_owner,name="alert_owner"),


] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)