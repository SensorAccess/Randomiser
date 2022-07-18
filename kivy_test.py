
from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import partial
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
#import logging
#logging.Logger.manager.root = Logger
#Window.fullscreen = True

from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        self.factory.app.handle_message(data)

class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


class TwistedServerApp(App):
    label = None

    def build(self):
        layout = FloatLayout()
        self.label = Label(text="", font_size='64dp', pos_hint={'right': 1, 'top': 0.8})
        layout.add_widget(self.label)
        self.image = Image(source='black.jpg', size_hint=(0.5, 0.5),
                    pos_hint={'right': 0.75, 'top': 1})
        layout.add_widget(self.image)
        reactor.listenTCP(8000, EchoServerFactory(self))
        return layout

    def clear_screen(self, dt):
        Logger.info("Clear Screen")
        self.image.source = "black.jpg"
        self.label.text = ""
        return

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        msg = msg.split(':', 2)
        if(len(msg)>1):
            Logger.info(msg[0])
            if msg[0] == '0':
                Logger.info("image 0")
                self.image.source = 'guard.jpg'
                self.label.color = (1, 0, 0, 1)  # Red
                Clock.schedule_once(self.clear_screen, 10)
            else:
                Logger.info("image other")
                self.image.source='guard2.jpg'
                self.label.color = (0, 1, 0, 1) # Green
                Clock.schedule_once(self.clear_screen, 10)

            self.label.text = f"{msg[1]}"
        else:
            self.label.text = f"{msg[0]}"

        return

if __name__ == '__main__':
    TwistedServerApp().run()
