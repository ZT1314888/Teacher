from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.models import User

def api_root(request):
    return redirect('/admin/')

def favicon(request):
    """返回 Django 默认的 admin 图标"""
    return HttpResponseRedirect(settings.STATIC_URL + 'admin/img/icon-changelink.svg')



@csrf_exempt
def register_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, '两次密码不一致')
            return render(request, 'register_admin.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return render(request, 'register_admin.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, '邮箱已被注册')
            return render(request, 'register_admin.html')
        
        # 创建管理员账号
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        messages.success(request, '管理员账号创建成功，请登录')
        return redirect('/admin/')
    
    return render(request, 'register_admin.html')

urlpatterns = [
    path('', api_root, name='api_root'),
    path('favicon.ico', favicon, name='favicon'),
    path('register-admin/', register_admin, name='register_admin'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('apps.users.urls')),
    path('api/classrooms/', include('apps.classrooms.urls')),
    path('api/reservations/', include('apps.reservations.urls')),
    path('api/announcements/', include('apps.announcements.urls')),
    path('api/courses/', include('apps.courses.urls')),
]

# 开发环境下提供静态文件和媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root='backend/static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
