import os
import sys
import requests

from kivy.app import App
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.properties import ObjectProperty

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen

import datetime


class MainWindow(Screen):
    egress = ObjectProperty(None)
    egress_value = ObjectProperty(None)
    egress_size = ""
    egress_days = ""

    @staticmethod
    def logOut():
        sm.current = "login"

    def on_enter(self, *args):
        self.egress.text = f'Egress Volume for last {self.egress_days} day(s) '
        self.egress_value.text = self.egress_size


class LoginWindow(Screen):
    access = ObjectProperty(None)
    secret = ObjectProperty(None)
    days = ObjectProperty(None)
    billing_data = None
    access_key = None
    secret_key = None

    def loginBtn(self):
        try:
            if self.access.text.strip() == "":
                return invalid("Access Key cannot be empty.")

            if self.secret.text.strip() == "":
                return invalid("Secret Key cannot be empty.")

            if self.days.text.strip() == "":
                return invalid("Days cannot be empty.")

            if self.days.text.strip().isnumeric() is False:
                return invalid("Days must be a number greater than 0.")

            if self.access.text.strip() != self.access_key and self.secret.text.strip() != self.secret_key:
                response = requests.get("https://billing.wasabisys.com/utilization/bucket/",
                                        headers={
                                            "Authorization": f'{self.access.text.strip()}:{self.secret.text.strip()}'})
                if response.status_code >= 400:
                    return invalid("Error: could not connect, please check your keys again.")
                self.billing_data = response.json()
                self.access_key = self.access.text.strip()
                self.secret_key = self.secret.text.strip()

            size, days = compute.get_egress(self.billing_data, int(self.days.text))
            MainWindow.egress_size = str(size)
            MainWindow.egress_days = str(days)

            self.reset()
            sm.current = "main"

        except Exception as e:
            invalid(str(e))

    def reset(self):
        self.days.text = ""


def invalid(text):
    pop = Popup(title='Invalid Form data',
                content=Label(text=text),
                size_hint=(None, None), size=(800, 800))
    pop.open()


class WindowManager(ScreenManager):
    pass


class MyMainApp(App):
    def build(self):
        return sm


class Compute:
    size_table = None

    def __init__(self):
        # Generate a table for SI units symbol table.
        self.size_table = {0: 'Bs', 1: 'KBs', 2: 'MBs', 3: 'GBs', 4: 'TBs', 5: 'PBs', 6: 'EBs'}

    @staticmethod
    def calculate_size(size, _size_table):
        """
        This function dynamically calculates the right base unit symbol for size of the object.
        :param size: integer to be dynamically calculated.
        :param _size_table: dictionary of size in Bytes. Created in wasabi-automation.
        :return: string of converted size.
        """
        count = 0
        while size // 1024 > 0:
            size = size / 1024
            count += 1
        return str(round(size, 2)) + ' ' + _size_table[count]

    def get_egress(self, json_data, days):
        # get json data for billing

        # initialize a dict for adding up numbers
        result = 0

        diff = days

        # get the initial time and check date only for this day.
        initial_time = datetime.datetime.now()

        # for each bucket add the the data to the dict
        for bucket in json_data:
            # check the time from the last day.
            time = datetime.datetime.strptime(bucket['StartTime'], '%Y-%m-%dT%H:%M:%SZ')
            # summing logic.
            diff = initial_time - time
            if diff.days <= days:
                result += bucket['DownloadBytes']
            else:
                break
        return self.calculate_size(result, self.size_table), diff.days - 1


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    Builder.load_file("my.kv")
    sm = WindowManager()
    screens = [LoginWindow(name="login"), MainWindow(name="main")]

    compute = Compute()

    for screen in screens:
        sm.add_widget(screen)

    sm.current = "login"

    MyMainApp().run()
