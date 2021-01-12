from kivy.config import Config
Config.set('graphics', 'position', 'custom') #implementing this in first place coz it should run first to display window in fixed size and postion,
from kivy.core.window import Window          #if we write this command below then another import statements could override it.
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.uix.actionbar import ActionButton
import cv2
Window.size = (1400, 885)
face_detection_count = 0
eyes_detection_count = 0
initial_label_for_face = 0
initial_label_for_eye = 0
camera_detected = 0
full_screen = 0
theme = 0
class CamApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        return KivyCamera().lay

    def Minus_app_button(self):
            MDApp.get_running_app().root_window.minimize()

    def close_app_button(self):
            CamApp().stop()

    def MaxiMin_app_button(self):
        global full_screen
        if full_screen == 0:
            full_screen = 1
            Window.size = (1910, 1030)
        else:
            full_screen = 0
            Window.size = (1600, 940)

class KivyCamera(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # print("p2")
        self.lay = GridLayout(cols=2)
        self.lay1 = BoxLayout()
        self.lay1.add_widget(camra())
        # print(getattr(camra.cam))
        if camera_detected == 0:
            self.lay2 = Screen()
            self.btn1 = MDRectangleFlatButton(text="Face", pos_hint={"center_x": 0.2, "center_y": 0.6},
                                              on_press=self.detect_face)
            self.btn2 = MDRectangleFlatButton(text="Wink", pos_hint={"center_x": 0.2, "center_y": 0.4},
                                              on_press=self.detect_eye)
            self.label0 = MDLabel(text=f"JUST WINK", pos_hint={"center_x": 0.23, "center_y": 0.88},
                                  theme_text_color="Error", font_style="H1")
            self.lay2.add_widget(self.label0)
            self.lay2.add_widget(self.btn1)
            self.lay2.add_widget(self.btn2)
            self.lay.add_widget(self.lay1)
            self.lay.add_widget(self.lay2)
        else:
            self.lay.remove_widget(self.lay1)
            self.lay2 = Screen()
            self.label0 = MDLabel(text=f"Ohps, NO Camera Detected !", pos_hint={"center_x": 0.5, "center_y": 0.5},
                                  theme_text_color="Error", font_style="H1")
            self.lay2.add_widget(self.label0)
            self.lay.add_widget(self.lay2)
        ################################################################
        # print("p1")                                                  #
        self.title_layout = FloatLayout()                              #
        self.title_layout.add_widget(TitleBar())                       #-----<This section is only for title bar>
        # Removing Current Bar                                         #
        Window.borderless = True                                       #
        self.lay2.add_widget(self.title_layout)                        #
        ################################################################
    def detect_face(self, obj):
        global initial_label_for_face
        #print("222222222222        "+str(initial_label))
        #print(face_detection_count)
        if initial_label_for_face == 1:
            #print("i m in face 1")
            self.lay2.remove_widget(self.label1)
        self.label1 = MDLabel(text=f"Number of faces detected : {str(face_detection_count)}", pos_hint={"center_x": 0.8, "center_y": 0.6}, theme_text_color="Error")
        self.lay2.add_widget(self.label1)
        initial_label_for_face = 1
    def detect_eye(self, obj):
        global initial_label_for_eye
        global theme
        if initial_label_for_eye == 1:
            #print("in detect_eye label 1")
            self.lay2.remove_widget(self.label2)
        if eyes_detection_count == 0 or eyes_detection_count == 2:
            self.label2 = MDLabel(text=f"Just wink and click a 'Wink' button.", pos_hint={"center_x": 0.8, "center_y": 0.4}, theme_text_color="Error")
            self.lay2.add_widget(self.label2)
        if eyes_detection_count > 2:
            self.label2 = MDLabel(text=f"Only one face is allowed.", pos_hint={"center_x": 0.8, "center_y": 0.4}, theme_text_color="Error")
            self.lay2.add_widget(self.label2)
        if eyes_detection_count == 1:
            if theme == 0:
                theme = 1
                self.label2 = MDLabel(text=f"Wink to LIGHT mode.", pos_hint={"center_x": 0.8, "center_y": 0.4}, theme_text_color="Error")
                self.lay2.add_widget(self.label2)
                Window.clearcolor = (0, 0, 0, 0)
            else:
                theme = 0
                self.label2 = MDLabel(text=f"Wink to DARK mode", pos_hint={"center_x": 0.8, "center_y": 0.4}, theme_text_color="Error")
                self.lay2.add_widget(self.label2)
                Window.clearcolor = (1, 1, 1, 1)
        initial_label_for_eye = 1
class camra(Image):
    def __init__(self, **kwargs):
        #print("in camra init")
        super().__init__(**kwargs)
        global camera_detected
        self.capture = cv2.VideoCapture(0)
        if self.capture.isOpened():
            Clock.schedule_interval(self.cam, 0)
        else:
            camera_detected = 1
    def cam(self, obj):
        #print("in564")
        ret, image = self.capture.read()
        if ret:
            #print("in2")
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.faces = face_cascade.detectMultiScale(grayImage, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            cv2.putText(image, "O", (10, image.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0, 0, 255), 11)
            cv2.putText(image, "LIVE", (25, image.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0, 0, 255), 1)
            global face_detection_count
            face_detection_count = len(self.faces)
            for (x, y, w, h) in self.faces:
                #print("in3")
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #cv2.rectangle(image, ((0, image.shape[0] - 25)), (270, image.shape[0]), (255, 0, 0), -1)
                cv2.putText(image, "Hey Bro !", (275, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                eyes = eye_cascade.detectMultiScale(grayImage, 1.3, 5, minSize=(50, 50))
                global eyes_detection_count
                eyes_detection_count = len(eyes)
                for (x, y, w, h) in eyes:
                    if eyes_detection_count == 1:
                        cv2.putText(image, "U can press Wink, now!", (200, image.shape[0] - 455), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 128), 2)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #print("in4")
        #print(type(image))
        buf1 = cv2.flip(image, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture
#For Title Bar
class HoverBehavior(object):
    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)
    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)
    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')
    def on_enter(self):
        pass
    def on_leave(self):
        pass
    def Minus_app_button(self):
        MDApp.get_running_app().root_window.minimize()
    def close_app_button(self):
        CamApp().stop()
    def MaxiMin_app_button(self):
        if Window.fullscreen:
            Window.fullscreen = False
        else:
            Window.fullscreen = True

from kivy.factory import Factory
Factory.register('HoverBehavior', HoverBehavior)
#Creating the Title Bar
Builder.load_string("""
<TitleBar>:
    ActionBar:
        size_hint_x: 2
        pos_hint: {'top':1, 'right':1}
        width: 400
        height: 40
        background_color:[0, 0, 0, 0]
        ActionView:
            use_separator: True
            ActionPrevious:
                title: '#justwink - Developed by AKASH.A (github: Akash-Peace, insta id: akash.a.2020)'
                app_icon: 'winkicon.png'
                with_previous: False
                color: [1, 0, 0, 1]
            ActionOverflow:
            MyActionButton:
                icon: '444.png' if self.hovered else "min1icon.png"
                width: 30 if self.hovered else 30
                on_press: app.Minus_app_button()
                border: 10,10,10,10
            MyActionButton:
                icon: '333.png' if self.hovered else "maxicon.png"
                width: 30 if self.hovered else 30
                on_press: app.MaxiMin_app_button()
                border: 10,10,10,10
            MyActionButton:
                icon: '222.png' if self.hovered else "exiticon.png"
                width: 30 if self.hovered else 30
                on_press: app.close_app_button()
                border: 10,10,10,10
""")
class MyActionButton(HoverBehavior,ActionButton):
    pass
class TitleBar(FloatLayout):
    pass

if __name__ == '__main__':
    CamApp().run()