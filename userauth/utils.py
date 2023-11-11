import requests
from bs4 import BeautifulSoup

def get_price(url):
    try:
        # 发送 GET 请求
        response = requests.get(url)

        # 检查请求是否成功 (状态码 200 表示成功)
        if response.status_code == 200:
            # 使用 BeautifulSoup 解析页面内容
            soup = BeautifulSoup(response.content, 'html.parser')

            # 查找包含价格信息的父元素
            price_parent_element = soup.find('div', class_='price__current--hidden')

            # 如果找到了父元素，进一步查找其中的价格元素
            if price_parent_element:
                # 在父元素下查找包含价格信息的 span 元素
                price_element = price_parent_element.find('span', class_='money')

                # 如果找到了价格元素，提取价格值
                if price_element:
                    # 获取包含价格的文本内容
                    price_text = price_element.text.strip()

                    # 提取数字部分，这里假设价格的格式是 "$639.20 CAD"
                    price = price_text.split(' ')[0].replace('$', '')

                    return price
                else:
                    # 如果没有找到价格元素，可以返回一个默认值或者抛出异常
                    return None
            else:
                # 如果没有找到父元素，可以返回一个默认值或者抛出异常
                return None
        else:
            # 如果请求失败，返回 None 或者抛出异常
            return None
    except Exception as e:
        # 处理异常，可以根据实际情况返回默认值或者抛出详细的异常信息
        print(f"Error while getting price for {url}: {e}")
        return None


import threading
import time

def set_timer(url, frequency, callback):
    def run():
        while not stop_event.is_set():
            callback(url)
            stop_event.wait(frequency * 10)  # 等待指定的频率，单位是秒

    stop_event = threading.Event()
    timer_thread = threading.Thread(target=run)
    timer_thread.start()

    return stop_event

# utils.py
import threading

# def create_timer(url, frequency, callback):
#     def run_timer():
#         while True:
#             callback(url)
#             # 间隔 frequency 秒执行一次
#             threading.Event().wait(frequency * 10)
#
#     # 创建线程并启动
#     timer_thread = threading.Thread(target=run_timer)
#     timer_thread.start()
#
#     # 返回定时器的标识符
#     return str(id(timer_thread))

from threading import Timer

# def create_timer(url, frequency, callback):
#     def timer_function():
#         # 执行定时操作
#         callback(url)
#
#     # 创建 Timer 对象并启动
#     timer = Timer(frequency * 10, timer_function)
#     timer.start()
#
#     return timer


def stop_timer(timer_id):
    # 根据定时器标识符停止对应的线程
    print("stop_timer begin", timer_id)
    for thread in threading.enumerate():
        if str(id(thread)) == timer_id:
            print(f"Before join - Thread {timer_id} is alive: {thread.is_alive()}")
            thread.join()
            print(f"After join - Thread {timer_id} is alive: {thread.is_alive()}")

