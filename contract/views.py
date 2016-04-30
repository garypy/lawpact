# coding=gbk

from django.http import HttpResponse
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http.response import HttpResponseRedirect
from contract.form import RegisterForm
from contract.models import UserProfile
from django.contrib.auth.models import User
from django.core.mail import send_mail
import hashlib

def index(request):
    return HttpResponse("Welcome to LawPact")

def user_login(request):
    #context = RequestContext(request)
    error_msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            #Remove is_active check since user may not using email validation code and he can login correctly
            #if user.is_active:
                print "login success!"
                login(request, user) #produce session
                #return render(request, 'contract/index.html')
                return HttpResponseRedirect('/')
            #else:
                #error_msg = "User was not active!"
                #return render(request, "User account is disabled!")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            error_msg = "Wrong username or password!"
            #render(request, "Invalid detailed provided.")
    return render(request, 'contract/login.html', {'err_msg' : error_msg})

def register(request):
    #err_msg = ""
    if request.method == 'POST':
        rf = RegisterForm(request.POST)
        #profile_form = UserProfileForm(data = request.POST)
        if rf.is_valid():
            print "#########is_valid check sucessful!"
            #user = register_form.save()
            #user.save()
            dt = request.POST
            #username = dt.get('username')
            username = rf.cleaned_data['username']
            #email = dt.get('email')
            email = rf.cleaned_data['email']
            #password = dt.get('password')
            password = rf.cleaned_data['password']
            user = User.objects.create_user(username, email, password) 
            if user is not None:
                user.is_active = False
                user.save()
                
                #save UserProfile
                activekey = hashlib.sha1(username).hexdigest()[:15]
                user.activation_key = activekey

                user_profile = UserProfile(user=user,)
                user_profile.activation_key = activekey
                user_profile.save()

                ##send email##
                mail_title = u'��ʦ���˺ż���'
                mail_content = u'�װ��ģ���л����ע�ᣬ�����������Ӽ����˺�\n'
                active_link = 'http://localhost:8000/activate/' + activekey
                mail_content += active_link
                mail_from = 'imblues@126.com'
                mail_to = [user.email]
                send_mail(mail_title,
                          mail_content,
                          mail_from,
                          mail_to)
                
                print "success to register"
            else:
                print "failed to register"

                        
            msg = "ע��ɹ������¼"
            return render(request, 'contract/regSuccess.html')
        else:
            print "fail to validate"
            #print rf.cleaned_data['username']
            return render(request, 'contract/register.html', {'form' : rf})
    
    return render(request, 'contract/register.html')

def activation(request, key):
    #print 'key=%s' % key
    profile = get_object_or_404(UserProfile, activation_key=key)
    if profile is not None:
        if profile.user.is_active == False:
            print "����ɹ�"
            profile.user.is_active = True
            profile.user.save()
        return HttpResponse(u'�˺ż���ɹ�')
    return HttpResponse(u'���˺Ų�����')
    
    
    