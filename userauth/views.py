from django.utils import timezone


from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def register(request):
    # Handle user registration
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.email = request.POST['email']
        user.save()
        login(request, user)
        return redirect('pricetracker_home')   # Redirect to the website's home page

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pricetracker_home')   # Redirect to the website's home page

    return render(request, 'login.html')


from django.contrib.auth import logout
from django.shortcuts import render, redirect
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        print('logout')
        return redirect('pricetracker_home')   # Redirect to the website's home page

    return redirect('pricetracker_home')  # Handle GET request, redirect to the home page


from userauth.models import TrackList
from threading import Timer


# Dictionary to store timers
timers = {}



def home(request):
    if request.user.is_authenticated:
        # If the user is logged in
        username = request.user.username
        email = request.user.email
        user = request.user
        tracklist = TrackList.objects.filter(user=user)

        def callback(url, frequency, stop_flag):
            # Perform fetching prices
            # print(f"Checking price for {url}", stop_flag)

            if not stop_flag:
                create_timer(url, frequency, stop_flag)

        def create_timer(url, frequency, stop_flag):
            # Create and start a Timer object
            timer = Timer(frequency * 60, callback, args=[url, frequency, stop_flag])
            timer.start()
            return timer

        stop_flag = False
        for item in tracklist:
            # Get URL and frequency information
            url = item.url
            frequency = item.check_frequency
            # stop_flag = False

            if item.enable_auto_monitoring:

                # Check if a timer already exists to avoid duplicate starts
                if item.number not in timers:

                    timers[item.number] = create_timer(url, frequency, stop_flag)
                    print(f"Starting timer for {url}", timers[item.number])
            else:
                # If auto monitoring is disabled, stop the timer
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



        return render(request, 'home.html', {'username': username,  'email': email,  'tracklist': tracklist})
    else:
        # If the user is not logged in
        return render(request, 'home.html')


from django.shortcuts import redirect
from userauth.models import TrackList

def save_tracklist(request):
    if request.method == 'POST':
        # Get form data
        for item in request.POST:
            if item.startswith("url_"):
                # Get the item ID from the form data
                item_id = int(item.split("_")[1])
                url = request.POST[item]
                target_price = request.POST[f"target_price_{item_id}"]
                check_frequency = float (request.POST[f"check_frequency_{item_id}"])
                enable_auto_monitoring = request.POST.get(f"enable_auto_{item_id}")

                # Validate check_frequency
                if check_frequency < 10:
                    return HttpResponse("Error: Check frequency must be at least 10 minutes.")

                # convert web form data to bool data type
                enable_auto_monitoring = enable_auto_monitoring == 'on'

                # Update or create a TrackList entry in the database
                try:
                    tracklist_item = TrackList.objects.get(number=item_id)
                    tracklist_item.url = url
                    tracklist_item.target_price = target_price
                    tracklist_item.check_frequency = check_frequency
                    tracklist_item.enable_auto_monitoring = enable_auto_monitoring
                    tracklist_item.save()
                except TrackList.DoesNotExist:
                    # new tracklist item
                    tracklist_item = TrackList(
                        number=item_id,
                        url=url,
                        target_price=target_price,
                        check_frequency=check_frequency,
                        enable_auto_monitoring=enable_auto_monitoring
                    )
                    tracklist_item.save()

        return redirect('pricetracker_home')
    else:
        # Handle non-POST requests
        return redirect('pricetracker_home')

from userauth.utils import get_price, get_user_email, send_email_notification


def checknow(request):
    if request.method == 'POST':
        # Get URL
        url_to_check = request.POST.get('checknow_url', None)

        current_price = get_price(url_to_check)

        if current_price is not None:
            tracklist_item = TrackList.objects.get(url=url_to_check)
            tracklist_item.current_price = current_price
            tracklist_item.last_check_time = timezone.now()
            tracklist_item.save()
            print(tracklist_item.target_price)

            # Check if the current price is below the target price
            if float(current_price) < tracklist_item.target_price:
                # If yes, send an email notification
                user_email = get_user_email(tracklist_item)
                send_email_notification(user_email, tracklist_item.url, current_price)
                return HttpResponse(f"Checked {url_to_check}. Current Price: {current_price} is lower than target price. Email sent.")

            else:
                return HttpResponse(f"Checked {url_to_check}. Current Price: {current_price}")



        else:
            # Handle price retrieval failure
            return redirect('pricetracker_home')
    # If not a POST request, return an empty page
    return HttpResponse("Invalid request.")


# send_test_email

from django.core.mail import send_mail
from django.http import HttpResponse

def send_email(request):
    # Send a test email
    subject = 'Price Tracker Notification - Price met your target'
    message = 'This is a notification that the price of the item you watched have reduced to your target price.'
    from_email = 'Zhou0214algonquin@gmail.com'
    recipient_list = ['jet.ca@live.com']

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse('Test email sent successfully.')

