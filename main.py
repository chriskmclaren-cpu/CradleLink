from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import QPushButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
import json

class NexusLink(App):
    def build(self):
        # UI Configuration
        self.title = "NexusLink: Bloodfang"
        self.icon = 'Bloodfang.png' 
        self.current_user = "Chris"
        self.pc_ip = "192.168.4.32" # Static link to the Spire
        
        # Main Container
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        Window.clearcolor = (0.05, 0.05, 0.05, 1) # Dark Nexus Theme

        # 1. Identity Bar (The Pack Selection)
        id_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        users = ["Chris", "Gabbi", "Asher"]
        
        for name in users:
            btn = QPushButton(
                text=name.upper(),
                background_normal='',
                background_color=(0.15, 0.15, 0.15, 1)
            )
            btn.bind(on_press=self.set_user)
            id_layout.addWidget(btn)
        layout.addWidget(id_layout)

        # 2. Status Display
        self.status = Label(
            text=f"ACTIVE NERVE: {self.current_user.upper()}", 
            size_hint_y=0.1,
            color=(0, 1, 0.25, 1), # System Green
            font_size='18sp'
        )
        layout.addWidget(self.status)

        # 3. Input Field
        self.input = TextInput(
            hint_text="Transmit to the Spire...", 
            multiline=False,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            padding=(10, 10),
            font_size='16sp'
        )
        self.input.bind(on_text_validate=self.send_to_spire)
        layout.addWidget(self.input)

        # 4. Transmission Button
        send_btn = QPushButton(
            text="TRANSMIT", 
            size_hint_y=0.2, 
            background_normal='',
            background_color=(0.3, 0, 0, 1), # Bloodfang Crimson
            font_size='20sp',
            bold=True
        )
        send_btn.bind(on_press=self.send_to_spire)
        layout.addWidget(send_btn)

        return layout

    def set_user(self, instance):
        # Strip the newline/role if added in previous iterations
        self.current_user = instance.text.split('\n')[0].capitalize()
        self.status.text = f"ACTIVE NERVE: {self.current_user.upper()}"
        print(f"SYSTEM: Nerve identity shifted to {self.current_user}")

    def send_to_spire(self, instance):
        text = self.input.text.strip()
        if not text:
            return

        # Prepare payload for the FastAPI Mobile Bridge in the Cradle
        params = json.dumps({
            "user": self.current_user, 
            "text": text
        })
        
        headers = {'Content-type': 'application/json'}
        
        # Transmission Protocol
        url = f"http://{self.pc_ip}:8000/mobile_bridge"
        
        try:
            UrlRequest(
                url, 
                req_body=params, 
                req_headers=headers,
                on_success=self.on_tx_success,
                on_failure=self.on_tx_error,
                on_error=self.on_tx_error
            )
            self.input.text = "" # Clear after transmission
        except Exception as e:
            self.status.text = "BRIDGE ERROR: Spire Unreachable"

    def on_tx_success(self, req, result):
        self.status.text = f"TRANSMISSION SUCCESSFUL: {self.current_user.upper()}"

    def on_tx_error(self, req, result):
        self.status.text = "BRIDGE FAILURE: Check Spire Connection"

if __name__ == '__main__':
    NexusLink().run()