from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError 
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.core.cache import cache

from .models import *

import json
from . import util
# Create your views here.

def index(request):
    if request.method == 'GET':

        number = request.GET.get('page')
        page, pageLinks =  util.nav_page( number ,File.objects.order_by('-downloadsCount'))
        if pageLinks is None and page is not None:
            return render(request, "fastFile/index.html",{
                'page':page,
            })
        elif pageLinks is None and page is None:
            return render(request, "fastFile/index.html", {
                "message": 'Page not exist'  
            })
        else:
            return render(request,"fastFile/index.html",{
                'page':page,
                'linkPages':pageLinks
            })
    
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,'fastFile/login.html',{
                'message':'Invalid username and/or password'
            })
    else:
        return render(request,'fastFile/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):

    if request.method == "POST":
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        #
        if password != confirmation or len(password) < 8:
            return render(request,'fastFile/register.html',{
                'message':'The passwords must match and/or Password must be 8 chars'
            })
        
        userExist = User.objects.filter(Q(username=username) | Q(email=email))
        if userExist.exists():
            if userExist.first().username == username:
                return render(request,'fastFile/register.html',{
                'message':'This username exist'
            })
            else:
                return render(request,'fastFile/register.html',{
                'message':'This email exist'
            })
        
        user = User.objects.create_user(username, email, password)
        user.save()
        
            
        login(request,user)
        return redirect('index')
    else:
        return render(request,'fastFile/register.html')

def search(request):
    if request.method !='GET':
        return render(request,'fastFile/index.html',{
                    'message':'This method not allow'
        }) 
    q = request.GET.get('q',None)
    if q is None:
        return render(request,'fastFile/index.html',{
                    'message':'where is the query?'
        })
    number = request.GET.get('page')
    files = File.objects.filter(name__icontains=q).order_by('-downloadsCount')
    
    page, pageLinks =  util.nav_page( number,files)
    if pageLinks is None and page is not None:
            return render(request, "fastFile/index.html",{
                'page':page,
            })
    elif pageLinks is None and page is None:
            return render(request, "fastFile/index.html", {
                "message": 'Page not exist'  
            })
    else:
            return render(request,"fastFile/index.html",{
                'page':page,
                'linkPages':pageLinks
            })

def fileName(request,fileName):
    file = File.objects.filter(name=fileName)
    if file.exists():
        file = file.first()

        if file.userPermition or file.password != None:
            if request.user in file.allowedUsers.all():
                return render(request, 'fastFile/file.html',{
                    'name':file.name,
                    'author':file.postedBy,
                    'dateAndTime':file.postedAt,
                    'downloads':file.downloadsCount
                })
            
            else:
                return render(request,'fastFile/index.html',{
                    'message':'You not have permition'
                }) 
        else:
            return render(request, 'fastFile/file.html',{
                    'name':file.name,
                    'author':file.postedBy,
                    'dateAndTime':file.postedAt,
                    'downloads':file.downloadsCount
                })
    
    else:
        return render(request,'fastFile/index.html',{
            'message':'This file not exist'
        })    

def download_file(request,fileName):
    
    file = File.objects.filter(name=fileName)
    
    if file.exists():
        file = file.first()
        if file.userPermition or file.password != None:
            if request.user in file.allowedUsers.all():
            
                content = open(file.file.path,'rb')
                response = FileResponse(content)
                response['Content-Disposition'] = 'attachment; filename="%s"' % file.file.name

                
            else:
                #change after to redirect('search' filename=fileName)
                return render(request,'fastFile/index.html',{
                    'message':'You not have permition'
                })
        else:
            content = open(file.file.path,'rb')
            response = FileResponse(content)
            response['Content-Disposition'] = 'attachment; filename="%s"' % file.file.name

            
        if request.session.get('lastDownload', None) == None or request.session.get('lastDownload', None) != file.file.name:
            file.downloadsCount += 1
            file.save()
        request.session['lastDownload'] = file.file.name

        return response
    else:
        return render(request,'fastFile/index.html',{
            'message':'This file not exist'
        })

@login_required
def perfil(request,username):
    if request.method == "GET":

        number = request.GET.get('page')
        user = User.objects.filter(username=username)
        if not user.exists():
            return render(request, "fastFile/perfil.html")
        user = user.first()
        if request.user == user:
            inbox = True
            requests = user.requestsMessages.all()
            messages = user.messages.all()
            
            
        else:
            
            inbox = False
            messages = False
        page, pageLinks =  util.nav_page( number ,File.objects.filter(postedBy=user).order_by('-downloadsCount'))
        if pageLinks is None and page is not None:
            return render(request, "fastFile/perfil.html",{
                'user':user,
                'inbox':inbox,
                'page':page,
                'messages': messages,
                'requests':requests
            })
        elif pageLinks is None and page is None:
            return render(request, "fastFile/perfil.html", {
                'user':user,
                'inbox':inbox,
                "message": 'Page not exist',
                'messages': messages,
                'requests':requests
            })
        else:
            return render(request,"fastFile/perfil.html",{
                'user':user,
                'inbox':inbox,
                'page':page,
                'linkPages':pageLinks,
                'messages': messages,
                'requests':requests
            })

@login_required
def upload(request):
    if request.method == "GET":
        return render(request,"fastFile/upload.html")
    
    fileName = request.POST.get('fileName', None)
    password = request.POST.get('password', None)
    confirmation = request.POST.get('confirmation', None)
    file = request.FILES.get('file',None)
    creatorPermition = request.POST.get('creatorPermition','off')
    #confirm datas
    if len(fileName) > 100:
        return render(request,'fastFile/upload.html',{
            'message':'file name must be less than 30 characters'
        })
    if len(password)  > 100:
        return render(request,'fastFile/upload.html',{
            'message':'password must be less than 20 characters'
        })
    if (password is not None and confirmation is not None) and (password != confirmation):
        return render(request,'fastFile/upload.html',{
            'message':'passwords must be the same'
        })
    if fileName is None or file is None:
        return render(request,'fastFile/upload.html',{
            'message':'The file name and file are nescessary'
        })
    if File.objects.filter(name=fileName).exists():
        return render(request,'fastFile/upload.html',{
            'message':'This file name exist'
        }) 
    
    #creat file
    
    if password is not None and (password != '' and password != ' ' ):
        if creatorPermition == 'on':
            fileInfo = File.objects.create(
            name=fileName,
            postedBy=request.user,
            file=file,
            password=make_password(password),
            userPermition=True,
            )
        else:
            fileInfo = File.objects.create(
            name=fileName,
            postedBy=request.user,
            file=file,
            password=make_password(password),
            )
        fileInfo.allowedUsers.add(request.user)
    else:
        if creatorPermition == 'on':
            fileInfo = File.objects.create(
            name=fileName,
            postedBy=request.user,
            file=file,
            userPermition=True,
            )
        else:
            fileInfo = File.objects.create(
            name=fileName,
            postedBy=request.user,
            file=file,
            )
        fileInfo.allowedUsers.add(request.user)

        
    fileInfo.save()
    
    return redirect('fileName', fileName=fileName)

@login_required
def settings_perfil(request):
    if request.method == "GET":
        return render(request,'fastFile/settings.html')
    DECISIONS = ['username','password','email','delete']
    decision = request.POST.get('decision', None)
    
    if decision not in DECISIONS:
        return render(request,'fastFile/settings.html',{
            'message':'decision not allow'
        })
    password = request.POST.get('password-hash') 
    user = User.objects.get(pk=request.user.id)
    

    if check_password(password,user.password):
        
        if decision != 'delete':
            change = request.POST.get('change', None)
            
            if not util.check_inputs(decision,change):
                if decision == 'email' or decision == 'username':
                    return render(request,'fastFile/settings.html',{
                        'message':f'This {decision} exist'
                    })
                else:
                    return render(request,'fastFile/settings.html',{
                        'message':'Password must be 8 chars'
                    })

            setattr(user, decision, change) if decision != 'password' else user.set_password(change)
            user.save()
            login(request,user)
            return render(request,'fastFile/settings.html',{
                        'message':f' change {decision} '
            })
        #delete perfil 
        uploads = user.posteds.all()
        for upload in uploads:
            if upload.file.path:
                upload.file.delete(save=False)
            upload.delete()
        user.delete()
        return redirect('index')

    else:
        return render(request,'fastFile/settings.html',{
            'message':'wrong password'
        })
#APIs
#user can request permition to download the file
@login_required
def requests(request):
    if request.method != "POST":
        return JsonResponse({"respost":"POST required "}, status=405)
    
    data = json.loads(request.body)
    
    type = data.get('type')
    if type == 'lock':
        title = data.get('name')
        password = data.get('password')
        file = File.objects.filter(name=title)
        if file.exists():
            file = file.first()
                
            if request.user in file.allowedUsers.all():
                return JsonResponse({"respost":"you already have permission "}, status=302)
                
            if check_password(password,file.password):
                file.allowedUsers.add(request.user)
                alert = Message.objects.create(
                    caller = request.user,
                    reciver = file.postedBy,
                    message = f"{request.user.username} can download your {file.name} file",
                )
                alert.save()
                file.save()
                return JsonResponse({"respost":"ok"}, status=202)
            else:
                return JsonResponse({"respost":"password incorrect"}, status=200)
                    
        else:
            return JsonResponse({"respost":"This file not exist "}, status=404)
    elif type == 'admin-permition':
        title = data.get('name')
        file = File.objects.filter(name=title)
        if file.exists():
            file = file.first()
            if request.user in file.allowedUsers.all():
                return JsonResponse({"respost":"has permission"}, status=200)
            
            alert = RequestMessage.objects.create(
                caller = request.user,
                reciver = file.postedBy,
                file = file,
                message = f'Can {request.user.username}  download your "{file.name}" file?',
                )
            alert.save()
            return JsonResponse({"respost":"ok"}, status=200)
        else:
            return JsonResponse({"respost":"This file not exist"}, status=404)

#Author can allow users
@login_required
def allowUser(request):
    if request.method != "POST":
        return JsonResponse({"respost":"POST required"}, status=405)
    data = json.loads(request.body)
    idUpload = int(data.get('id'))
    decision = bool(data.get('decision'))
    userMessages = request.user.requestsMessages.all()
    ids = []
    for message in userMessages:
        ids.append(message.id)

    if idUpload in ids:
        rqst = userMessages.filter(id=idUpload)
        if rqst.exists():
            caller = data.get('caller')
            caller = User.objects.get(username=caller)

            rqst = rqst.first()
            if decision:
                file = rqst.file
                file.allowedUsers.add(caller)

                message = Message(
                    caller=request.user,
                    reciver=caller,
                    message=f'{request.user.username} accept your request to {rqst.file.name} file'
                )
                message.save()
            else:
                message = Message(
                    caller=request.user,
                    reciver= caller,
                    message=f'{request.user.username} rejected your request to {rqst.file.name} file'
                )
                message.save()
                
            rqst.delete()
            return JsonResponse({"respost":"made"}, status=200)
        else:
            return JsonResponse({"respost":"this id not exist"}, status=400)
    else:
        return JsonResponse({"respost":"id is not your"}, status=401)
    
@login_required
def delete_messages(request):
    
    user = request.user
    messages = Message.objects.filter(reciver=user)
    messages.delete()
    return JsonResponse({"respost":"deleted"}, status=200)
    