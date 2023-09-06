from kivy import platform
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import Clock, StringProperty
import time

class MainWidget(BoxLayout):
    actual_time_str = StringProperty("00:00:00")

    cronometro_time = 0
    cronometro_time_str = StringProperty("00:00:00") 
    cronometro_is_on = False

    temporizador_time = 0
    temporizador_time_str = StringProperty("00:00:00") 
    temporizador_is_on = False
    temporizador_started_before = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.instant_update()
        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, dt):
        print(str(dt))
        actual_time = time.strftime("%H:%M:%S", time.localtime())
        self.actual_time_str = str(actual_time)
        if self.cronometro_is_on:
            self.cronometro_time_str = self.elapsed_time_formater(self.cronometro_time)
            self.cronometro_time += 1
        if self.temporizador_is_on:
            self.temporizador_time_str = self.elapsed_time_formater(self.temporizador_time)
            if self.temporizador_time <= 1:
                self.temporizador_is_on = False
            else:
                self.temporizador_time -= 1

    def instant_update(self):
        actual_time = time.strftime("%H:%M:%S", time.localtime())
        self.actual_time_str = str(actual_time)
        self.cronometro_time_str = self.elapsed_time_formater(self.cronometro_time)
        self.temporizador_time_str = self.elapsed_time_formater(self.temporizador_time)

    def cronometro_start_stop(self, widget):
        if widget.state == "normal":
            self.cronometro_is_on = False
        else:
            self.cronometro_is_on = True

    def reset_cronometro(self):
        self.cronometro_time = 0
        self.instant_update()

    def temporizador_time_to_seconds(self, entered_hr, entered_min, entered_sec):
        try:
            return int(entered_sec) + int(entered_min)*60 + int(entered_hr)*3600
        except Exception as e:
            print(str(e))
            return 0

    def temporizador_start_stop(self, widget, entered_hr, entered_min, entered_sec):
        if widget.state == "normal":
            self.temporizador_is_on = False
        else:
            self.temporizador_is_on = True
            if not self.temporizador_started_before:
                self.temporizador_time = self.temporizador_time_to_seconds(entered_hr, entered_min, entered_sec)
                self.temporizador_started_before = True
            
    def reset_temporizador(self,entered_hr, entered_min, entered_sec):
        self.temporizador_time = self.temporizador_time_to_seconds(entered_hr, entered_min, entered_sec)
        self.instant_update()
        

    def two_digit_formater(self, number_to_format):
        if number_to_format < 10:
            return "0" + str(number_to_format)
        return str(number_to_format)
    
    def elapsed_time_formater(self, time_to_format_on_seconds):
        hour_holder = 0
        minuts_holder = 0
        seconds_holder = 0

        if time_to_format_on_seconds < 60:
            seconds_holder = time_to_format_on_seconds
            return "00:00:" + self.two_digit_formater(seconds_holder)
        elif 60 <= time_to_format_on_seconds < 3600:
            seconds_holder = time_to_format_on_seconds % 60
            minuts_holder = time_to_format_on_seconds // 60
            return "00:" + self.two_digit_formater(minuts_holder) + ":" + self.two_digit_formater(seconds_holder)
        hour_holder = time_to_format_on_seconds // 3600
        minuts_holder = (time_to_format_on_seconds % 3600) // 60
        seconds_holder = (time_to_format_on_seconds % 3600) % 60
        return self.two_digit_formater(hour_holder) + ":" + self.two_digit_formater(minuts_holder) + ":" + self.two_digit_formater(seconds_holder)

class Cronometro_Container(BoxLayout):
    pass

class Temporizador_Container(BoxLayout):
    pass

class TimerApp(App):
    pass

TimerApp().run()