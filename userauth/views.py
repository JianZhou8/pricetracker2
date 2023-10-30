from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('pricetracker_home')  # 重定向到网站的首页

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pricetracker_home')  # 重定向到网站的首页

    return render(request, 'login.html')


from django.contrib.auth import logout
from django.shortcuts import render, redirect
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        print('logout')
        return redirect('pricetracker_home')  # 重定向到网站的首页

    return redirect('pricetracker_home')  # 处理 GET 请求，重定向到首页



def home(request):
    if request.user.is_authenticated:
        # 用户已登录
        username = request.user.username
        password = request.user.password  # 请注意，不建议直接显示密码
        return render(request, 'home.html', {'username': username, 'password': password})
    else:
        # 用户未登录
        return render(request, 'home.html')
