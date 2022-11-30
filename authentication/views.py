import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import generate_token
from DMwebsite import settings
from .models import Vehicle

from django.core.mail import send_mail, EmailMessage
from .forms import VehicleForm

from django.core.exceptions import ObjectDoesNotExist


def home(request):
    # return HttpResponse('homepage')
    return render(request, "authentication/index.html")


def about(request):
    # return HttpResponse('about')
    return render(request, 'about.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmedpassword = request.POST['confirmedpassword']

        '''
        these functions check for username already existing/email as well as 
        characteristics of username/email/password requirements.
        '''
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists.")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered.")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Username needs to be under 10 characters.")

        if password != confirmedpassword:
            messages.error(request, "Passwords don't match.")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-numeric")
            redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.is_active = False

        myuser.save()

        messages.success(request,
                         "Your account has been successfully created. Please confirm your account in the confirmation email to activate your account.")

        # Signup email
        subject = "Welcome to DMProject"
        message = "Hello " + myuser.first_name + ", \n" + "Thank you for choosing us for your project. \n We have sent you a confirmation email to confirm your sign-up request, please confirm your email to finish setting up your account. \n \n Sincerely, \n DMProject Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address confirmation email

        current_site = get_current_site(request)
        email_subject = "Confirm your email @ DMProject"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, "authentication/index.html", {'firstname': firstname})

        else:
            messages.error(request, "Invalid username or password")
            return redirect('home')
    # return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully.")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated.")
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')


def add_car(request):
    submitted = False
    if request.method =="POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            Cid = form.cleaned_data['CarID']
            y = form.cleaned_data['year']
            m = form.cleaned_data['make']
            mod = form.cleaned_data['model']
            mil = form.cleaned_data['miles']
            col = form.cleaned_data['color']
            loc = form.cleaned_data['location']
            stat = form.cleaned_data['status']
            DA = datetime.datetime.now()
            v = Vehicle(CarID=Cid, year=y, make=m, model=mod, miles=mil,
                        color=col, location=loc, status=stat, DateAdded=DA)
            v.save()


            return HttpResponseRedirect('/add_car?submitted=True')
    else:
        form = VehicleForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_car.html', {'form':form, 'submitted':submitted})


def removecar(request):
    if request.method == "POST":
        cid = request.POST['CarID']


        # entry.delete()
        if Vehicle.objects.filter(CarID=cid):
            obj = Vehicle.objects.get(pk=cid)
            obj.delete()
            messages.success(request, "Vehicle successfully removed")
            return redirect('home')
        else:
            messages.error(request, "Vehicle couldn't be removed.")
            return redirect('removecar.html')



    return render(request, 'removecar.html')


def showdb(request):
    cars = Vehicle.objects.all().values()
    # context= {'sortedCarID': cars_sorted}
    return render(request, 'showdb.html', {'cars': cars})

# def showusers(request):
#     users = User.objects.all().values()
#     return render(request, 'showusers.html', {'users': users})

def about(request):
    return render(request, 'about.html')

# def search_Cars(request):
#     cars = Vehicle.objects.all()
#     if request.method == "POST":
#         searched = request.POST['searched']
#         cars=Vehicle.objects.filter(year__contains = searched)
#
#         return render(request, 'searchCars.html', {'searched': searched, 'cars':cars})
#     # if 'searched' in request.GET:
#     #     searched = request.GET['searched']
#     #     cars = Vehicle.objects.filter( Q(CarID__icontains = searched) | Q(year__icontains =searched) | Q(make__icontains =searched) | Q(model__icontains  = searched) | Q(miles__icontains = searched) |
#     #                                    Q(color__icontains = searched)| Q(location__icontains = searched) | Q(status__icontains = searched) | Q(DateAdded__icontains =0))
#     #     context = {"cars": cars}
#     # else:
#     #     cars = Vehicle.objects.all()
#     #     context = {"cars": cars}
#     else:
#         return render(request, 'searchCars.html')
def search_Cars(request):
    cars = Vehicle.objects.all().values()
    if request.method == "GET":
        searched = request.GET['searched']
        cars = Vehicle.objects.filter( Q(CarID__icontains = searched) | Q(year__icontains =searched) | Q(make__icontains =searched) | Q(model__icontains  = searched) | Q(miles__icontains = searched) | Q(color__icontains = searched)| Q(location__icontains = searched) | Q(status__icontains = searched)).values()
        return render(request, 'searchCars.html', {'searched': searched, 'cars': cars})
    else:
        return render(request, 'searchCars.html')


def update_cars(request, CarID):
    car = Vehicle.objects.get(pk=CarID)
    form = VehicleForm(request.POST or None, instance=car)
    if form.is_valid():
        form.save()
        return redirect('showdb')
    return render(request, 'update_cars.html', {'car': car, 'form':form})
