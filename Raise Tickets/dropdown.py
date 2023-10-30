from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class MyApp(App):
    def build(self):
        self.selected_dish = "Favorite Dish: "

        layout = BoxLayout(orientation='vertical')

        self.label = Label(text=self.selected_dish, halign='center', size_hint=(1, None), height=40)
        layout.add_widget(self.label)

        button = Button(text="Select Favorite Dish", size_hint=(1, None), height=40)
        button.bind(on_release=self.open_dropdown)
        layout.add_widget(button)

        self.dropdown = DropDown()
        self.menu_items = [
            "Pizza",
            "Burger",
            "Sushi",
            "Pasta",
            "Tacos",
            "Salad",
        ]
        for dish in self.menu_items:
            btn = Button(text=dish, size_hint_y=None, height=40)
            btn.bind(on_release=self.select_dish)
            self.dropdown.add_widget(btn)

        return layout

    def open_dropdown(self, button):
        self.dropdown.open(button)

    def select_dish(self, button):
        self.selected_dish = "Favorite Dish: " + button.text
        self.label.text = self.selected_dish
        self.dropdown.dismiss()


if __name__ == "__main__":
    MyApp().run()
