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


from userauth.models import TrackList
def home(request):
    if request.user.is_authenticated:
        # 用户已登录
        username = request.user.username
        email = request.user.email
        user = request.user
        tracklist = TrackList.objects.filter(user=user)  # 获取当前用户的 tracklist 数据
        # 然后将 tracklist 数据传递给模板
        return render(request, 'home.html', {'username': username,  'email': email,  'tracklist': tracklist})
    else:
        # 用户未登录
        return render(request, 'home.html')


from django.shortcuts import redirect
from userauth.models import TrackList  # 导入 TrackList 模型

def save_tracklist(request):
    if request.method == 'POST':
        # 获取表单数据
        for item in request.POST:
            if item.startswith("url_"):
                # 解析 item 的编号
                item_id = int(item.split("_")[1])
                url = request.POST[item]
                target_price = request.POST[f"target_price_{item_id}"]
                check_frequency = request.POST[f"check_frequency_{item_id}"]
                enable_auto_monitoring = request.POST.get(f"enable_auto_{item_id}")

                # 将字符串转换为布尔值
                enable_auto_monitoring = enable_auto_monitoring == 'on'  # 如果值为 'on'，则为 True，否则为 False

                # 在数据库中更新或创建 TrackList 条目
                try:
                    tracklist_item = TrackList.objects.get(id=item_id)
                    tracklist_item.url = url
                    tracklist_item.target_price = target_price
                    tracklist_item.check_frequency = check_frequency
                    tracklist_item.enable_auto_monitoring = enable_auto_monitoring
                    tracklist_item.save()
                except TrackList.DoesNotExist:
                    # 如果没有找到该条目，可能是新创建的
                    # 创建新的 TrackList 条目
                    tracklist_item = TrackList(
                        id=item_id,
                        url=url,
                        target_price=target_price,
                        check_frequency=check_frequency,
                        enable_auto_monitoring=enable_auto_monitoring
                    )
                    tracklist_item.save()

        # 可以添加成功消息或重定向到其他页面
        return redirect('pricetracker_home')
    else:
        # 处理非 POST 请求
        return redirect('pricetracker_home')
