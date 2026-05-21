from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import product ,login , student
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
#  صلاحيات
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

class ProductAPI(APIView):

 def get(self, request):

    products = product.objects.all()

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)
# ------------------------
# REGISTER
# ------------------------

# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             form.save()
#             messages.success(request, "تم إنشاء الحساب بنجاح")
#             return redirect("login")

#     else:
#         form = UserCreationForm()

#     return render(request, "pages/sin_up.html", {"form": form})
# in the hand
def register(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            error = "اسم المستخدم مستخدم بالفعل"
        else:
            User.objects.create_user(username=username, password=password)
            return redirect("login")

    return render(request, "pages/sin_up.html", {"error": error})

# ------------------------
# LOGIN
# ------------------------
# shortes
# def user_login(request):

#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)

#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)
#             return redirect("index")

#     else:
#         form = AuthenticationForm()

#     return render(request, "pages/login.html", {"form": form})
def user_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("index")
        else:
            error = "اسم المستخدم أو كلمة المرور غير صحيحة"

    return render(request, "pages/login.html", {"error": error})

# ------------------------
# LOGOUT
# ------------------------
def user_logout(request):
    logout(request)
    return redirect("login")


# ------------------------
# INDEX (محمي) يمنع أي شخص يدخل الصفحة إلا إذا كان مسجل دخول
# ------------------------
@login_required
def index(request):
    # return HttpResponse('hellow')
    return render(request, "pages/home.html")

# class IndexView(View):
    
#     def get(self, request):
#         return render(request, "pages/home.html")
# ------------------------
# PRODUCTS PAGE (CRUD)
# ------------------------

@login_required
def podectpage(request):

    if request.method == "POST":

        action = request.POST.get("action")

        n = request.POST.get('name')
        d = request.POST.get('description')
        p = request.POST.get('price')

        # ---------------- ADD ----------------
        if action == "save":

            # أي مستخدم مسجل يقدر يضيف
            product.objects.create(
                name=n,
                description=d,
                price=p
            )

        # ---------------- EDIT ----------------
        elif action == "edit":

            # فقط الأدمن يقدر يعدل
            if not request.user.is_superuser:
            # if not (request.user.is_superuser or request.user.username == "kamall"):
                raise PermissionDenied()

            obj = product.objects.filter(name=n).first()

            if obj:
                obj.description = d
                obj.price = p
                obj.save()

        # ---------------- DELETE ----------------
        elif action == "delete":

            # فقط الأدمن يقدر يحذف
            if not request.user.is_superuser:
                raise PermissionDenied()

            product.objects.filter(name=n).delete()

    return render(request, "pages/prodect.html")

# class ProductPageView(LoginRequiredMixin, View):

#     login_url = 'login'

#     def get(self, request):
#         return render(request, "pages/prodect.html")


#     def post(self, request):

#         action = request.POST.get("action")

#         n = request.POST.get('name')
#         d = request.POST.get('description')
#         p = request.POST.get('price')

#         if action == "save":

#             if request.user.has_perm('app1.add_product'):

#                 product.objects.create(
#                     name=n,
#                     description=d,
#                     price=p
#                 )

#         elif action == "edit":

#             if request.user.has_perm('app1.change_product'):

#                 obj = product.objects.filter(name=n).first()

#                 if obj:
#                     obj.description = d
#                     obj.price = p
#                     obj.save()

#         elif action == "delete":

#             if request.user.has_perm('app1.delete_product'):

#                 product.objects.filter(name=n).delete()

#         return render(request, "pages/prodect.html")
# ------------------------
# ADMIN CHECK (اختياري)
# ------------------------
def is_admin(user):
    return user.is_superuser


# ------------------------
# (اختياري لو تفصل delete لوحده)
# ------------------------
@user_passes_test(is_admin)
def delete_product(request, name):
    product.objects.filter(name=name).delete()
    return redirect("product_page")


# ------------------------
# SAVE INFORMATION (كما هو عندك)
# ------------------------
def saveinformation(request):

    f = product.objects.all()

    if request.method == "POST":

        action = request.POST.get("action")
        u = request.POST.get('username')
        p = request.POST.get('password')

        if action == "save":
            login.objects.create(username=u, passwored=p)

        elif action == "edit":
            user = login.objects.filter(username=u).first()
            if user:
                user.passwored = p
                user.save()

        elif action == "delete":
            login.objects.filter(username=u).delete()

    return render(request, "pages/login.html", {'login': f})

def display(request) :
    f = product.objects.all()
    return render(request,"pages/display.html",{'display': f})
# class DisplayView(LoginRequiredMixin, View):

#     login_url = 'login'

#     def get(self, request):

#         f = product.objects.all()

#         return render(request, "pages/display.html", {
#             'display': f
#         })

def student_list(request):
    data = student.objects.all()
    return render(request,"pages/student.html",{'student':data})

def add_student(request):
    if request.method == "POST":
        x = request.POST.get('nu')
        y = request.POST.get('name')
        a = request.POST.get('phon')
        d = request.POST.get('adress')
        data = student(nu = x ,name =y , number = a , adress = d)
        data.save()
    return render(request,"pages/add_student.html")


def edit_student(request, id):

    # جلب الطالب حسب الـ id
    data = get_object_or_404(student, id=id)

    if request.method == "POST":

        data.nu = request.POST.get('nu')
        data.name = request.POST.get('name')
        data.number = request.POST.get('phon')
        data.adress = request.POST.get('adress')

        data.save()

        return redirect('/a/student_list')

    return render(request, "pages/edite_student.html", {'data': data})
  
            