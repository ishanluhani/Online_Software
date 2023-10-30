from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class PhotoChangingButton(Button):
    def __init__(self, x, root):
        super(PhotoChangingButton, self).__init__()
        self.size_hint = (1, .93)
        self.background_normal = x
        self.root = root

    def on_release(self):
        print('clicked')

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        button = PhotoChangingButton('//RASPBERRYPI/128gbSSD/returns ex - Copy/Group 6/1689935715188.jpg', self)
        layout.add_widget(button)
        return layout

if __name__ == '__main__':
    MyApp().run()
