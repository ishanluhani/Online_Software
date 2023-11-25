from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.dropdown import DropDown
import file_grouper, img_to_text
from tkinter.filedialog import askopenfilename
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import choose_type_of_ticket
import upload_file
import video_compress_two
import subprocess
from kivy.config import Config
from tkinter.messagebox import askyesno


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


# Builder.load_file('main.kv')


class PhotoChangingButton(Button):
    def __init__(self, x, root):
        super(PhotoChangingButton, self).__init__()
        self.size_hint = (1, .93)
        self.background_normal = x
        self.root = root

    def on_release(self):
        new = askopenfilename()
        if new and askyesno():
            new = new.replace('/', '\\', 1)
            # new = new.replace('/', '\\')
            # new = new.replace('\\\\', '\\')
            print(self.root.coordinate_data[self])
            self.root.data[1][self.root.coordinate_data[self][0]].remove(self.root.coordinate_data[self][1])
            self.root.data[1][self.root.coordinate_data[self][0]].append(new)
            self.background_normal = new


class ScreenManagers(ScreenManager):
    pass


class MenuScreen(Screen):
    pass


class Dropdown(DropDown):
    def __init__(self, i_path, current, root1, button):
        super(Dropdown, self).__init__()
        self.dismiss()
        self.menu_items = [
            'packet id',
            'product img',
            'waybill'
        ]
        self.last = current
        self.root1 = root1
        self.i_path = i_path
        self.button = button
        for dish in self.menu_items:
            btn = Button(text=dish, size_hint_y=None, height=40)
            btn.bind(on_release=self.select_dish)
            self.add_widget(btn)

    def select_dish(self, button):
        self.root1.data[1][self.last].remove(self.i_path)
        self.root1.data[1][button.text].append(self.i_path)
        self.button.text = button.text
        self.last = button.text


class GroupScreen(Screen):
    def __init__(self, **kwargs):
        super(GroupScreen, self).__init__()
        self.name = kwargs['name']
        self.ids.mainest_layout.add_widget(Label(text=self.name, size_hint=(1, .05)))
        # self.data = kwargs['data']
        self.data = img_to_text.data[self.name]

        print(self.data, 'gg')
        self.ids.Suborder.text = self.data[0][0]
        self.ids.AWB.text = self.data[0][1]
        self.ids.Packet.text = self.data[0][2]
        lst = MDList()
        for i in choose_type_of_ticket.tickets:
            lst.add_widget(OneLineListItem(text=i, on_release=self.call_ticket_maker))
        self.scroll = MDScrollView(lst, size_hint=(0, 1))
        self.ids.main_layout.add_widget(self.scroll)
        video_link = self.data[1]['video'][0]
        # video_link = video_link.replace('/', '\\$')
        # video_link = video_link.replace('$', '')
        out_path = '/'.join(video_link.split('/')[:-1]) + '/output.mp4'
        video_compress_two.compress_video(video_link, out_path, 20*1000)
        self.data[1]['video'][0] = '/'.join(self.data[1]['video'][0].split('/')[:-1]) + '/output.mp4'
        video_link = self.data[1]['video'][0]
        print(video_link, 'gk')
        self.video_button = Button(text='Show Video', on_release=lambda x: subprocess.call(['start', '', self.data[1]['video'][0]], shell=True), size_hint=(1, .05))
        self.ids.data_layout.add_widget(self.video_button)
        self.coordinate_data = {}
        for i in self.data[1]:
            for x in self.data[1][i]:
                if i != 'video':
                    a = BoxLayout(orientation='vertical')
                    # a.add_widget(Label(text=i, size_hint=(1, .07)))
                    button_drop = Button(text=i, size_hint=(1, .07))
                    drop = Dropdown(i_path=x, current=i, root1=self, button=button_drop)
                    button_drop.bind(on_release=drop.open)
                    a.add_widget(drop)
                    a.add_widget(button_drop)
                    button = PhotoChangingButton(x, self)
                    self.coordinate_data[button] = [i, x]
                    a.add_widget(button)
                    self.ids.img_layout.add_widget(a)

    def change_video(self):
        a = askopenfilename()
        if a:
            self.data[1]['video'][0] = a


    def available_options(self):
        self.scroll.size_hint = (.3, 1)

    def call_ticket_maker(self, x):
        self.data[0][0] = self.ids.Suborder.text
        self.data[0][1] = self.ids.AWB.text
        self.data[0][2] = self.ids.Packet.text
        a, description = choose_type_of_ticket.run(x.text, self.data[1])
        data = description.to_dict()
        description = list(data['description'].values())[0]
        link = list(data['link'].values())[0]
        print(description)
        upload_file.run_file(self.data, description, link)


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.manager = ScreenManager()
        self.menuscreen = MenuScreen(name='Menu')
        self.manager.add_widget(self.menuscreen)
        return self.manager

    def on_start(self):
        file_grouper.ask_and_group()
        data = file_grouper.group
        print('iuyiggikug', data)
        img_to_text.calibrate(data)
        print(img_to_text.data)
        # try:
        for i in img_to_text.data:
            self.menuscreen.ids.ListofGroups.add_widget(OneLineListItem(text=i, on_press=lambda x: self.change_screen(x)))
            print(i)
            self.groupscreen = GroupScreen(name=i)
            self.manager.add_widget(self.groupscreen)
        # except Exception as e:
        #     print(e, 'errorrrr')

    def change_screen(self, x):
        self.manager.transition.direction = 'left'
        self.manager.current = x.text


MainApp().run()
