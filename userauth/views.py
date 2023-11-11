from django.utils import timezone


from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.email = request.POST['email']
        user.save()
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
from threading import Timer


# 存储定时器的字典
timers = {}



def home(request):
    if request.user.is_authenticated:
        # 用户已登录
        username = request.user.username
        email = request.user.email
        user = request.user
        tracklist = TrackList.objects.filter(user=user)  # 获取当前用户的 tracklist 数据

        def callback(url, frequency, stop_flag):
            # 这里可以执行你的操作，比如获取价格、保存到数据库等
            print(f"Checking price for {url}", stop_flag)

            if not stop_flag:
                create_timer(url, frequency, stop_flag)

        def create_timer(url, frequency, stop_flag):
            # 创建 Timer 对象并启动
            timer = Timer(frequency * 10, callback, args=[url, frequency, stop_flag])
            timer.start()
            return timer

        stop_flag = False
        for item in tracklist:
            # 获取用户设定的 URL、频率等信息
            url = item.url
            frequency = item.check_frequency
            # stop_flag = False
            # 如果 enable_auto_monitoring 启用，则启动定时器
            if item.enable_auto_monitoring:

                # 检查是否已有定时器，避免重复启动
                if item.number not in timers:

                    timers[item.number] = create_timer(url, frequency, stop_flag)
                    print(f"Starting timer for {url}", timers[item.number])
            else:
                # 如果 enable_auto_monitoring 取消，停止定时器

                if item.number in timers:
                    print(f"Stopping timer for {url}", timers[item.number])
                    stop_flag = True
                    timers[item.number].cancel()
                    del timers[item.number]
                    # print(f"end Stopping timer for {url}" ,timers[item.number])

        # Check if the form is submitted with new items
        if request.method == 'POST' and 'new_url' in request.POST:
            # Extract the values for the new item from the form

            new_url = request.POST['new_url']
            new_target_price = request.POST['new_target_price']
            new_check_frequency = request.POST['new_check_frequency']
            new_enable_auto = 'new_enable_auto' in request.POST

            # Create a new TrackList object and save it to the database
            new_item = TrackList(
                user=user,
                # number=new_number,
                url=new_url,
                target_price=new_target_price,
                check_frequency=new_check_frequency,
                enable_auto_monitoring=new_enable_auto
            )
            new_item.save()



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
                    tracklist_item = TrackList.objects.get(number=item_id)
                    tracklist_item.url = url
                    tracklist_item.target_price = target_price
                    tracklist_item.check_frequency = check_frequency
                    tracklist_item.enable_auto_monitoring = enable_auto_monitoring
                    tracklist_item.save()
                except TrackList.DoesNotExist:
                    # 如果没有找到该条目，可能是新创建的
                    # 创建新的 TrackList 条目
                    tracklist_item = TrackList(
                        number=item_id,
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

from django.http import HttpResponse
from userauth.utils import get_price
def checknow(request):
    if request.method == 'POST':


        # 获取提交的 URL
        url_to_check = request.POST.get('checknow_url', None)

        # 在这里执行检查的逻辑，可以使用相应的库或方法来获取 URL 的当前价格等信息
        # 这里仅作为演示，假设获取到的价格为 99.99
        current_price = get_price(url_to_check)

        # 更新数据库中的相关信息，例如更新 TrackList 表中的 current_price 和 last_check_time
        # 这里需要根据你的数据模型进行具体的实现
        # 以下仅作为示例，假设 TrackList 模型中有名为 current_price 和 last_check_time 的字段
        if current_price is not None:
            tracklist_item = TrackList.objects.get(url=url_to_check)
            tracklist_item.current_price = current_price
            tracklist_item.last_check_time = timezone.now()
            tracklist_item.save()

            # 返回一个简单的响应，也可以根据需要返回 JSON 数据等
            return HttpResponse(f"Checked {url_to_check}. Current Price: {current_price}")
        else:
            # 获取价格失败，你可以根据需要进行处理，这里简单返回 pricetracker_home 页面
            return redirect('pricetracker_home')
    # 如果不是 POST 请求，可以根据需要返回一个空的页面或其他响应
    return HttpResponse("Invalid request")
