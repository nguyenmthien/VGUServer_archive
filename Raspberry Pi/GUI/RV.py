from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
import email2

Builder.load_string("""
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    #value: ''
    font_size: '23sp'

<Test>:
    rv: rv
    error_msg: error_msg
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: .2
        orientation: 'horizontal'
        TextInput:
            id: email_input
            hint_text: "Email"
            font_size: '23sp'
            multiline: False
            #on_text_validate: root.insert(email_input.text)
        Button:
            text: 'Add'
            font_size: '23sp'
            size_hint_x: .3
            on_release: 
                root.insert(email_input.text)
                email_input.text = ""
    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(20)
        viewclass: 'SelectableLabel'
        SRBL:
            default_size: None, dp(65)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)
            multiselect: True
            touch_multiselect: True
    BoxLayout:
        size_hint_y: .2
        Label:
            id: error_msg
            font_size: '23sp'
        Button:
            text: "Send"
            font_size: '23sp'
            size_hint_x: .2
            on_release: root.send()    
        Button:
            text: "Delete"
            font_size: '24sp'
            size_hint_x: .2
            on_release: root.delete()   
""")

class SRBL(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''''''

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        #kek = rv.data[index]
        if is_selected:
            rv.data[index]['select'] = True
            print("selection changed to {0}".format(rv.data[index]))
        else:
            try:
                rv.data[index]['select'] = False
                print("selection removed for {0}".format(rv.data[index]))
            except:
                pass

class Test(BoxLayout):
    def insert(self, value):
        if len(self.rv.data) == 6:
            self.error_msg.text = "Maximum emails is 6"
        else:
            self.rv.data.insert(0, {'text': value or 'lul'})

    def random(self):
        self.rv.data = [{'text': str(x)} for x in range(100)]

    def delete(self):
        for x in reversed(self.rv.data):
            if x['select'] == True:
                self.rv.data.pop(self.rv.data.index(x))
        self.rv.layout_manager.clear_selection()
    
    def send(self):
        '''f = open("contacts.txt", "w")
        for x in self.rv.data:
            f.write(x['text'] + " ")
        f.close()
        email2.send_email("contacts.txt")'''
        select_list = []
        for x in reversed(self.rv.data):
            if x['select'] == True:
                select_list.append(x['text'])
        if len(select_list):
            email2.send_email_list(select_list)
            print(select_list)

class TestApp(App):
    def build(self):
        return Test()

if __name__ == '__main__':
    TestApp().run()