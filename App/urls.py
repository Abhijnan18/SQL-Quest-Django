from django.urls import path
from App import views

urlpatterns = [
    path('',views.index,name='indexVAR'),
    path('home',views.homepage,name='homeVAR'),
    path('help',views.helppage,name='helpVAR'),
    path('about',views.aboutpage,name='aboutVAR'),

    path('solve',views.solvepage,name='solveVAR'),
    path('question',views.questionspage,name='questionsVAR'),
    path('userquerysubmit',views.userquerysubmit_virtual,name='userquerysubmitVAR_virtual'),
    
    path('login',views.loginpage,name='loginVAR'),
    path('logout',views.logoutpage_virtual,name='logoutVAR_virtual'),
    path('signup',views.signuppage,name='signupVAR'),
]