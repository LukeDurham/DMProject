from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import  force_bytes, force_text
from . tokens import generate_token
from DMwebsite import settings
from django.core.mail import send_mail, EmailMessage
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

        if len(username)>10:
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

        messages.success(request, "Your account has been successfully created. Please confirm your account in the confirmation email to activate your account.")

        #Signup email
        subject = "Welcome to DMProject"
        message = "Hello " + myuser.first_name + ", \n" + "Thank you for choosing us for your project. \n We have sent you a confirmation email to confirm your sign-up request, please confirm your email to finish setting up your account. \n \n Sincerely, \n DMProject Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)




        # Email Address confirmation email

        current_site = get_current_site(request)
        email_subject = "Confirm your email @ DMProject"
        message2 = render_to_string('email_confirmation.html',{
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
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully.")
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated.")
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')


