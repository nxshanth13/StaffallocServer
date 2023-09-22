from django.shortcuts import render
from .models import *
from django.db.models import Q
from Logic.logic import superlogic
user=''
date=[]
tot=0
exam=''
mselected_staff=[]
fselected_staff=[]
rooms=[]
single=[]
girl=[]
def login(request):
    return render(request,"login.html")

def register(request):
    name=request.POST['name']
    password=request.POST['password']
    confirmation=request.POST['confirmation']
    department=request.POST['department']
    email=request.POST['email']
    names=Users.objects.values_list('name')
    if name!='' and password==confirmation and name not in names[0]:
        user=Users(name=name,password=password,department=department,email=email)
        user.save()
    print(name,password,confirmation,email,names,department)
    return render(request,"login.html")

def logins(request):
    name=request.POST['name']
    global mselected_staff,user,fselected_staff
    password=request.POST['password']
    names=Users.objects.filter(name=name).values()
    if (names[0]['name']=='admin4' and names[0]['password']==password):
        staff1=Staff.objects.exclude(Q(name__in=mselected_staff)&Q(name__in=fselected_staff)&Q(gender='M')).values()
        staff2=Staff.objects.exclude(Q(name__in=mselected_staff)&Q(name__in=fselected_staff)&Q(gender='F')).values()
        user='all'
        print(staff1,staff2)
        return render(request,"staff.html",{'mstaff':staff2,'fstaff':staff1})
    elif (names[0]['name']==name and names[0]['password']==password):
        staff1=Staff.objects.filter(Q(department=names[0]['department'].upper())&Q(gender='M')).exclude(Q(name__in=mselected_staff)).values()
        staff2=Staff.objects.filter(Q(department=names[0]['department'].upper())&Q(gender='F')).exclude(Q(name__in=fselected_staff)).values()
        user=names[0]['department']
        return render(request,"staff.html",{'mstaff':staff1,'fstaff':staff2})
    return render(request,"login.html")
def staffselection(request):
    global mselected_staff,fselected_staff
    selected=request.POST.getlist('staff_name')
    for i in selected:
        staff=Staff.objects.filter(id=i).values()
        if staff[0]['gender']=='M':
            mselected_staff.append(staff[0]['name'])
            mselected_staff=list(set(mselected_staff))
        else:
            fselected_staff.append(staff[0]['name'])
            fselected_staff=list(set(fselected_staff))
    print(mselected_staff,fselected_staff)
    return render(request,"viewstaff.html",{'mstaff':mselected_staff,'fstaff':fselected_staff})

def edit(request):
    global user,mselected_staff,fselected_staff
    mselectedstaff=[]
    fselectedstaff=[]
    if user=='all':
        return render(request,'edit.html',{'mstaff':mselected_staff,'fstaff':fselected_staff})
    for i in mselected_staff:
        if user in i.lower():
            mselectedstaff.append(i)
    for i in fselected_staff:
        if user in i.lower():
            fselectedstaff.append(i)
    return render(request,'edit.html',{'mstaff':mselectedstaff,'fstaff':fselectedstaff})

def edition(request):
    global mselected_staff,fselected_staff
    sel1=request.POST.getlist('mstaff_name')
    sel2=request.POST.getlist('fstaff_name')
    for i in sel1:
        mselected_staff.remove(i)
    for i in sel2:
        fselected_staff.remove(i)
    return render(request,'viewstaff.html',{'mstaff':mselected_staff,'fstaff':fselected_staff})

def rooms(request):
    if user=='all':
        rooms=Rooms.objects.all().values()
        return render(request,'rooms.html',{'rooms':rooms})
    return render(request,'finished.html')

def roomselect(request):
    global rooms,single,girl
    rooms=request.POST.getlist('roomInput')
    single=request.POST.getlist('singlestaff')
    girl=request.POST.getlist('girlroom')
    print(rooms,single,girl)
    return render(request,'examtype.html')
    pass

def examdate(request):
    global date,exam,tot
    date=request.POST['date'].split()
    exam=request.POST['exam']
    tot=int(request.POST['tot'])
    print('views')
    print(date,exam,tot,mselected_staff,fselected_staff,single,girl,rooms)
    print('aftre')
    superlogic(date,rooms,single,girl,mselected_staff,fselected_staff)
    return render(request,'examtype.html')