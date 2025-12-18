from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import  LoginForm, VerifyForm, RegistrationForm
from .models import CustomUser, OTP
from .utils import generate_otp, send_otp_to_email

# Registration View+
def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # Using email as username
            user.save()

            # skipping OTP here and sending it after login

            return redirect("login")  # Redirect to login page after registration
    else:
        form = RegistrationForm()
    return render(request, "auth_service/register.html", {"form": form})


# Login View
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user, created = CustomUser.objects.get_or_create(username=email, email=email)

            otp = generate_otp()
            OTP.objects.update_or_create(user=user, defaults={"otp_code": otp})
            send_otp_to_email(email, otp)

            request.session["email"] = email
            return redirect("verify")

    return render(request, "auth_service/login.html", {"form": LoginForm()})

# OTP Verification View
def verify_view(request):
    email = request.session.get("email")
    if not email:
        return redirect("login")

    user = CustomUser.objects.get(email=email)
    otp_obj = OTP.objects.get(user=user)

    if request.method == "POST":
        form = VerifyForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data["otp"]
            if entered_otp == otp_obj.otp_code:
                login(request, user)
                return redirect("home")
            return render(request, "auth_service/verify.html", {"form": form, "error": "Invalid OTP"})

    return render(request, "auth_service/verify.html", {"form": VerifyForm()})
