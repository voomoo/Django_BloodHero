from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import DonorSignupForm, DonorAuthenticationForm, ProfileForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'home.html')

def signup_user(request):
    context = {}
    if request.POST:
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password2')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('dashboard')
        else:
            context['form'] = form
    else:
        form = DonorSignupForm()
        context['form'] = form
    return render(request, 'authentication/signup.html', context)


def login_user(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("dashboard")

    if request.POST:
        form = DonorAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if Profile.objects.filter(donor=request.user).exists():
                    return redirect("dashboard")
                else:
                    return redirect('profile')

    else:
        form = DonorAuthenticationForm()

    context['form'] = form
    return render(request, 'authentication/login.html', context)

@login_required
def profile(request):
    # return render(request, 'navigation/profile.html', {'form':ProfileForm})
    if Profile.objects.filter(donor=request.user).exists():
        data = get_object_or_404(Profile, donor=request.user)
        if request.method == 'GET':
            form = ProfileForm(instance=data)
            return render(request, 'navigation/profile.html', {'form': form})

        else:
            try:
                form = ProfileForm(request.POST, instance=data)
                form.save()
                return redirect('dashboard')
            except ValueError:
                return redirect('profile')

    else:
        if request.method == 'GET':
            form = ProfileForm()
            return render(request, 'navigation/profile.html', {'form': form})

        else:
            try:
                form = ProfileForm(request.POST)
                new_profile = form.save(commit=False)
                new_profile.donor = request.user
                new_profile.email = request.user.email
                new_profile.save()
                return redirect('dashboard')
            except ValueError:
                return redirect('profile')

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    print(request.GET.get('bl_group'))
    if(request.GET.get('bl_group') == 'all'):
        data = Profile.objects.all()
    elif(request.GET.get('bl_group') is None):
        data = Profile.objects.all()
    else:
        data = Profile.objects.filter(blood_group=request.GET.get('bl_group'))
    if Profile.objects.filter(donor=request.user).exists():
        return render(request, 'navigation/dashboard.html', {'data':data})
    else:
        return redirect('profile')

@login_required
def mail_user(request, donor_pk):
    user_email = get_object_or_404(Profile, pk = donor_pk)
    if request.POST:
        form = MessageForm(request.POST)
        new_msg = form.save(commit=False)
        new_msg.email_from = request.user.email
        new_msg.save()
        #print(address,msg, request.user.email)
        return redirect('dashboard')
    else:
        address = user_email.email
        name = Profile.objects.filter(email=request.user.email)[0].name
        phone = Profile.objects.filter(email=request.user.email)[0].phone
        info = Profile.objects.filter(email=request.user.email)[0].info
        msg = 'Hello {},<br><br>I am {}. I am in emergency need of {} blood group. So it would be wonderful if you can call me at {} or mail me at {}. <br><br>Thank you'.format(user_email.name,name, user_email.blood_group, phone, request.user.email)
        form = MessageForm({'email_to': address, 'message': msg})
        return render(request, 'navigation/mail.html', {'form':form, 'info': info})

@login_required
def messages(request):
    data = Messages.objects.filter(email_to=request.user.email).order_by('-id')
    return render(request, 'navigation/messages.html', {'data': data})

