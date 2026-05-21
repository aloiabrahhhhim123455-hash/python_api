from django.urls import path
from .  import views 

urlpatterns = [
path('index',views.index,name='index'),
path('save',views.saveinformation,name='save'),
path('prodect',views.podectpage,name='product_page'),
path('register', views.register, name='register'),
path('login', views.user_login, name='login'),
path('logout', views.user_logout, name='logout'),
path('display', views.display, name='display'),
# path('index', views.IndexView.as_view(), name='index'),
# path('display', views.DisplayView.as_view(), name='display'),
# path('product', views.ProductPageView.as_view(), name='product_page'),
path('api/products/', views.ProductAPI.as_view()),
path('student_list',views.student_list,name='s'),
path('add_student',views.add_student,name = 'student'),
path('student_edit/<int:id>/', views.edit_student, name='edit_student')

]