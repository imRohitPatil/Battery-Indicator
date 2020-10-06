import psutil
import time
import tkinter as tk
from tkinter import ttk
from win10toast import ToastNotifier
from threading import Thread


def show_warning(title, battery_level_text, message_text, suggestion_text):
    font10 = "-family {Segoe UI} -size 14"
    font9 = "-family {Segoe UI} -size 14 -weight bold"

    top = tk.Tk()
    width = 400
    height = 200
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    top.geometry("%dx%d+%d+%d" % (width, height, x, y-50))
    top.resizable(0, 0)
    top.title(title)
    top.configure(background="#3a3a3a")
    top.wm_iconbitmap('battery_icon.ico')

    top.attributes('-topmost', True)
    top.update()

    battery_level = tk.Label(top)
    battery_level.place(relx=0.15, rely=0.1, height=31, width=274)
    battery_level.configure(background="#3a3a3a")
    battery_level.configure(font=font9)
    battery_level.configure(foreground="#ffffff")
    battery_level.configure(text=f'Battery Level: {battery_level_text}%')

    message = tk.Label(top)
    message.place(relx=0.0, rely=0.25, height=41, width=394)
    message.configure(background="#3a3a3a")
    message.configure(font=font9)
    message.configure(foreground="#82f733")
    message.configure(text=message_text)

    suggestion = tk.Label(top)
    suggestion.place(relx=0.0, rely=0.45, height=31, width=394)
    suggestion.configure(background="#3a3a3a")
    suggestion.configure(font=font10)
    suggestion.configure(foreground="#ffff00")
    suggestion.configure(text=suggestion_text)

    close_btn = ttk.Button(top, command=top.destroy)
    close_btn.place(relx=0.325, rely=0.75, height=35, width=146)
    close_btn.configure(text='''Okay''')
    close_btn.configure(takefocus="")

    top.mainloop()


def monitor_battery_level():
    notify_count = 0
    while(True):
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        battery_level = battery.percent

        if plugged:

            if battery_level < 90 or battery_level == 99:
                notify_count = 0

            elif battery_level == 90 and notify_count == 0:
                th = Thread(target=show_warning, args=('Battery Status', battery_level,
                                                       'Your battery is charged 90%.', 'I\'m suggesting to unplug charger!',))
                th.start()
                notify_count = 1

            elif battery_level == 100 and notify_count == 0:
                th = Thread(target=show_warning, args=('Battery Charged', battery_level,
                                                       'Your battery is fully charged!', 'Unplug charger immediately!',))
                th.start()
                notify_count = 1

        else:
            if battery_level > 15:
                notify_count = 0

            elif battery_level <= 15 and notify_count == 0:  # 15
                th = Thread(target=show_warning, args=('Low Battery', battery_level,
                                                       'Your battery is running low!', 'Plug the charger immediately!',))
                th.start()
                notify_count = 1

        time.sleep(60)


# execution starts here
monitor_battery_level()
