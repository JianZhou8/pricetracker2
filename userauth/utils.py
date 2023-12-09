import requests
from bs4 import BeautifulSoup

def get_price(url):
    try:
        # Send a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200 indicates success)
        if response.status_code == 200:
            # Parse the page content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the parent element containing price information
            price_parent_element = soup.find('div', class_='price__current--hidden')

            # If the parent element is found, further locate the price element within it
            if price_parent_element:
                # Find the span element containing the price information under the parent element
                price_element = price_parent_element.find('span', class_='money')

                # If the price element is found, extract the price value
                if price_element:
                    # Get the text content containing the price
                    price_text = price_element.text.strip()

                    # Extract the numeric part, assuming the price format is like "$639.20 CAD"
                    price = price_text.split(' ')[0].replace('$', '').replace(',', '')

                    return price
                else:
                    # If the price element is not found, return a default value
                    return None
            else:
                # If the price element is not found
                return None
        else:
            # If the request fails, return None
            return None
    except Exception as e:
        # Handle exceptions; return a default value
        print(f"Error while getting price for {url}: {e}")
        return None


import threading
import time

def set_timer(url, frequency, callback):
    def run():
        while not stop_event.is_set():
            callback(url)
            stop_event.wait(frequency * 60)  # # Wait for the specified frequency, in seconds

    stop_event = threading.Event()
    timer_thread = threading.Thread(target=run)
    timer_thread.start()

    return stop_event

# utils.py
import threading




def stop_timer(timer_id):
    # Stop the thread corresponding to the specified timer identifier
    print("stop_timer begin", timer_id)
    for thread in threading.enumerate():
        if str(id(thread)) == timer_id:
            print(f"Before join - Thread {timer_id} is alive: {thread.is_alive()}")
            thread.join()
            print(f"After join - Thread {timer_id} is alive: {thread.is_alive()}")

# send_test_email

from django.core.mail import send_mail
from django.http import HttpResponse

def send_email_notification(user_email, url, current_price):
    # Send an email notification
    subject = 'Price Tracker Notification - Price met your target'
    message = f'This is a notification that the price of the item at {url} has reduced to your target price. ' \
              f'Current Price: {current_price}'
    from_email = 'Zhou0214algonquin@gmail.com'
    recipient_list = [user_email] if user_email else []  # Use the user's email from the TrackList model

    send_mail(subject, message, from_email, recipient_list)



def get_user_email(tracklist_item):
    # Get the user's email from the TrackList item
    return tracklist_item.user.email if tracklist_item.user else None