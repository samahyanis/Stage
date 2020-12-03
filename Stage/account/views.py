from pyexpat.errors import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print('c bon')
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('$/affaires/affaires')

    else:
        return render(request, 'login.html')


def register(request):
    print('c bon')
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                email=email, password=password1)
                user.save()
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'password not matching...')
            return redirect('register')
        return redirect('/')

    else:
        return render(request, 'register.html')

"""def register(request):
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=username, email=email, password=password1,
                                                    first_name=first_name, last_name=last_name)
                    return redirect('/')
    else:
        return render(request, 'register.html')
"""
