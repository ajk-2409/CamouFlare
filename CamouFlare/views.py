from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import EncodeForm, DecodeForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .steganography import Steganography

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            return render(
                request, "CamouFlare/signup.html", {"error": "Username already exists"}
            )
        user = User.objects.create_user(username=username, password=password)
        return redirect("login")
    return render(request, "CamouFlare/signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            return render(
                request,
                "CamouFlare/login.html",
                {"error": "Invalid username or password"},
            )
        else:
            login(request, user)
            return redirect("home")
    return render(request, "CamouFlare/login.html")

@login_required
def home_view(request):
    encode_form = EncodeForm()
    decode_form = DecodeForm()
    return render(
        request,
        "CamouFlare/steg.html",
        {"encode_form": encode_form, "decode_form": decode_form},
    )

@login_required
def encode_message(request):
    if request.method == "POST":
        form = EncodeForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            message = form.cleaned_data["message"]
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            img_path = os.path.join(settings.MEDIA_ROOT, filename)
            try:
                steganography = Steganography(1, img_path, message)
                output_filename = os.path.join(settings.MEDIA_ROOT, "encoded.png")
                with open(output_filename, "rb") as f:
                    response = HttpResponse(f.read(), content_type="image/png")
                    response["Content-Disposition"] = (
                        f'attachment; filename="encoded.png"'
                    )
                os.remove(img_path)
            except Exception as e:
                context = {
                    "encode_form": EncodeForm(),
                    "decode_form": DecodeForm(),
                    "error": f"Failed to decode message: {e}",
                }
                return render(request, "CamouFlare/steg.html", context)
            fs.delete(filename)
            return response
    context = {
        "encode_form": EncodeForm(),
        "decode_form": DecodeForm(),
        "error": "Failed to encode message.",
    }
    return render(request, "CamouFlare/steg.html")

@login_required
def decode_message(request):
    if request.method == "POST":
        form = DecodeForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            img_path = os.path.join(settings.MEDIA_ROOT, filename)
            try:
                obj = Steganography(0, img_path)
                context = {
                    "encode_form": EncodeForm(),
                    "decode_form": DecodeForm(),
                    "decoded_message": obj.decoded_message,
                }
            except Exception as e:
                context = {
                    "encode_form": EncodeForm(),
                    "decode_form": DecodeForm(),
                    "error": f"Failed to decode message: {e}",
                }
                return render(request, "CamouFlare/steg.html", context)
            fs.delete(filename)
            return render(request, "CamouFlare/steg.html", context)
    context = {
        "encode_form": EncodeForm(),
        "decode_form": DecodeForm(),
        "error": "Failed to decode message.",
    }
    return render(request, "CamouFlare/steg.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
