from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect

from .models import room,Topic,Messages,User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import RoomForm,Userform,myusercreationform
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')


        try:

            user = User.objects.get(email=email)

        except:
            messages.error(request, "User Does not exist Please check again ")

        user = authenticate(email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password is Not right")









    context= {}
    return render(request,template_name='chat/login.html',context=context)







def registerpage(request):
    page = 'registration'
    form = myusercreationform()

    if request.method=="POST":
        form = myusercreationform(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "You have been Successfully Registered Please Enter you Credentials")

            return redirect('login')
        else:
            messages.error(request,"Your Password Did not match!")

    ctx = {'form':form,'page':page}

    return render(request,template_name='chat/login.html',context=ctx)







def home(request):
    page = 'page'
    members = User.objects.all()
    total_rooms = room.objects.count()
    if request.user not in members:
        messages.error(request,"You are not logged In Please Register yourself!")


    q = request.GET.get('q') if request.GET.get('q') != None  else ''


    room_messages = Messages.objects.filter(Q(Room__topic__name__icontains=q))
    rooms = room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))

    room_count = rooms.count()
    topics = Topic.objects.all()


    ctx = {'rooms':rooms,'topics':topics,"room_count":room_count,
           'room_messages':room_messages,'total_rooms':total_rooms,'page':page
           }
    return render(request,'chat/home.html',context=ctx)



def user_profile(request,pk):
    total_rooms = room.objects.count()
    user = User.objects.get(id  =pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.messages_set.all()
    context = {'user':user,"rooms":rooms,'topics':topics,'room_messages':room_messages,'total_rooms':total_rooms}

    return render(request,"chat/user_profile.html",context)























def room_view(request,pk):

    Room = room.objects.get(id=pk)


    message_room = Room.messages_set.all().order_by('created')


    participants = Room.participants.all()



    if request.method=="POST":


        comment_object = Messages.objects.create(user=request.user,Room=Room,body=request.POST.get('comment'))
        Room.participants.add(request.user)
        return redirect('room',pk=Room.id)


    ctx = {'room':Room,'message_room':message_room,'participants':participants}
    return render(request,'chat/room.html',context=ctx)


@login_required(login_url='login')
def room_create(request):
    form = RoomForm()

    topics = Topic.objects.all()
    if request.method=="POST":
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)

        room.objects.create(
            name=request.POST.get('room_name'),
            topic=topic,
            description=request.POST.get('room_about'),
            host=request.user,


        )
        return redirect('home')

    ctx = {"form":form,'topics':topics}
    return render(request,"chat/room_form.html",context=ctx)



@login_required(login_url='login')
def update_room(request,pk):
    value = 'value'

    room_a = room.objects.get(id=pk)



    form = RoomForm(instance=room_a)
    if request.user != room_a.host:
        return HttpResponse("You are not allowed to be here")
    if request.method=="POST":
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)

        name = request.POST.get('room_name')
        description = request.POST.get('room_about')
        room_a.name=name
        room_a.description=description
        room_a.topic=topic
        room_a.save()

        return redirect('home')


    ctx = {'form':form,'room_a':room_a,'value':value}

    return render(request,"chat/room_form.html",context=ctx)


@login_required(login_url='login')
def delete_room(request,pk):

    Room = room.objects.get(id=pk)

    if request.user != Room.host:
        return HttpResponse("You are not allowed to be here")
    if request.method=="POST":


        Room.delete()
        return redirect("home")

    ctx = {'obj':Room}
    return render(request,"chat/delete_confirmation.html",context=ctx)




@login_required(login_url='login')
def delete_message(request,pk):
    comment = Messages.objects.get(id=pk)


    room_id = comment.Room.id
    Room = room.objects.get(id=room_id)


    if request.user != comment.user:
        return HttpResponse("You are not allowed to be here")
    if request.method=="POST":

        Room.participants.remove(request.user)
        comment.delete()

        return redirect("room",pk=room_id)

    ctx = {'obj':comment}
    return render(request,"chat/delete_confirmation.html",context=ctx)






def logout_user(request):

    logout(request)
    return redirect('home')




def update_message(request,pk):

    page = 'update'
    comment = Messages.objects.get(id=pk)


    Room = room.objects.get(id=comment.Room.id)

    message_room = Room.messages_set.all()


    participants = Room.participants.all()



    if request.method=="POST":

        comment.body = request.POST.get('body')
        comment.save()


        return redirect('room',pk=Room.id)


    ctx = {'room':Room,'message_room':message_room,'participants':participants,'comment':comment,'page':page}
    return render(request,'chat/room.html',context=ctx)


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = Userform(instance=user)
    if request.method=="POST":
        form = Userform(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

    ctx = {'form':form}
    return render(request,'chat/update-user.html',ctx)