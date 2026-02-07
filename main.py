import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest # Native Kivy Network Tool
from kivy.core.window import Window

# --- CONFIGURATION ---
# Default IP. You can change this in the app.
DEFAULT_SPIRE_URL = "http://192.168.1.XX:8000/mobile_bridge" 

class NexusLink(App):
    def build(self):
        self.icon = "Bloodfang.png" 
        Window.clearcolor = (0.05, 0.05, 0.05, 1) # Dark Background
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # --- HEADER ---
        self.status_label = Label(text="NEXUS LINK: OFFLINE", size_hint=(1, 0.1), color=(1, 0, 0, 1), bold=True)
        layout.add_widget(self.status_label)
        
        # --- IP CONFIG ---
        ip_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        self.ip_input = TextInput(text=DEFAULT_SPIRE_URL, multiline=False, foreground_color=(0, 1, 0, 1), background_color=(0.1, 0.1, 0.1, 1))
        ip_layout.add_widget(Label(text="SPIRE URL:", size_hint=(0.3, 1)))
        ip_layout.add_widget(self.ip_input)
        layout.add_widget(ip_layout)

        # --- CHAT HISTORY ---
        self.history = Label(size_hint_y=None, markup=True, color=(0.8, 0.8, 0.8, 1))
        self.scroll = ScrollView(size_hint=(1, 0.6))
        self.scroll.add_widget(self.history)
        layout.add_widget(self.scroll)

        # --- INPUT AREA ---
        input_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        self.user_name = TextInput(text="Asher", size_hint=(0.3, 1), multiline=False, hint_text="Name")
        self.msg_input = TextInput(size_hint=(0.5, 1), multiline=False, hint_text="Message...")
        send_btn = Button(text="SEND", size_hint=(0.2, 1), background_color=(0, 0.5, 0, 1))
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.user_name)
        input_layout.add_widget(self.msg_input)
        input_layout.add_widget(send_btn)
        layout.add_widget(input_layout)
        
        return layout

    def send_message(self, instance):
        user = self.user_name.text
        text = self.msg_input.text
        url = self.ip_input.text
        
        if not text: return
        
        # Update UI instantly
        self.update_history(f"[b]{user}:[/b] {text}")
        self.msg_input.text = ""
        
        # Send to Spire using Native Kivy Request (Async)
        headers = {'Content-type': 'application/json'}
        body = json.dumps({"user": user, "text": text})
        
        UrlRequest(url, req_body=body, req_headers=headers, 
                  on_success=self.on_success, on_failure=self.on_failure, on_error=self.on_error)

    def on_success(self, req, result):
        Clock.schedule_once(lambda dt: self.set_status("LINK ESTABLISHED", (0, 1, 0, 1)))

    def on_failure(self, req, result):
        Clock.schedule_once(lambda dt: self.set_status("CONNECTION FAILED (400/500)", (1, 0, 0, 1)))

    def on_error(self, req, error):
        Clock.schedule_once(lambda dt: self.set_status("CONNECTION ERROR (Check IP)", (1, 0, 0, 1)))
        Clock.schedule_once(lambda dt: self.update_history(f"[color=ff0000]Error: {str(error)}[/color]"))

    def set_status(self, text, color):
        self.status_label.text = text
        self.status_label.color = color

    def update_history(self, text):
        self.history.text += f"\n{text}"
        self.history.height = self.history.texture_size[1]
        self.scroll.scroll_to(self.history)

if __name__ == "__main__":
    NexusLink().run()
