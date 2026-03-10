import os
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex, platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
import threading
import requests
import hashlib
import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# --- APK FIX: ENSURE WE ARE IN THE RIGHT DIRECTORY FOR ASSETS ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- THE SACRED SETTINGS ---
MASTER_PEPPER = "global_unicode_spice_2026"
ROUNDS = 3
EMOJI_MAP = {'0':'🦄','1':'🍼','2':'🩷','3':'🧸','4':'🎀','5':'🍓','6':'🌈','7':'🌸','8':'💕','9':'🫐'}
REV_MAP = {v: k for k, v in EMOJI_MAP.items()}

# Lock in the background color globally
Window.clearcolor = get_color_from_hex('#DBDCFF')

# --- APK FIX: SECURE VAULT PATH LOGIC ---
def get_vault_path():
    data_dir = App.get_running_app().user_data_dir
    return os.path.join(data_dir, 'cypher_vault.json')

# --- CRYPTO HELPER FUNCTIONS ---
def to_emoji(val): 
    return "".join(EMOJI_MAP.get(d, d) for d in f"{val:03}")

def from_emoji(s):
    digits = [REV_MAP[ch] for ch in s if ch in REV_MAP]
    return int("".join(digits)) if len(digits) == 3 else None

def get_keys_and_perms(kw, pepper):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=64, salt=b"csprng_v3", iterations=100000, backend=default_backend())
    master_key = kdf.derive(kw.encode() + pepper.encode())
    rounds_params = []
    for i in range(ROUNDS):
        h = hashlib.sha256(master_key + i.to_bytes(4, 'big')).digest()
        a = ((int.from_bytes(h[:4], 'big') % 120) * 2 + 1) % 256
        b = int.from_bytes(h[4:8], 'big') % 256
        p_list = list(range(256))
        seed = int.from_bytes(h[8:16], 'big')
        import random
        r = random.Random(seed)
        r.shuffle(p_list)
        inv_p = [0]*256
        for idx, v in enumerate(p_list): inv_p[v] = idx
        rounds_params.append({'a': a, 'b': b, 'p': p_list, 'inv_p': inv_p})
    return rounds_params

# --- KIVY UI LAYOUT ---
KV = '''
#:import utils kivy.utils

<WindowManager>:
    LockScreen:
        name: 'lock'
    MainScreen:
        name: 'main'

<LockScreen>:
    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        BoxLayout:
            orientation: 'vertical'
            padding: ['30dp', '10dp', '30dp', '30dp']
            spacing: '15dp'
            size_hint_y: None
            height: self.minimum_height

            Image:
                source: 'CYPHER.png'
                size_hint_y: None
                height: '350dp' 
                fit_mode: 'contain'

            Label:
                text: "VIP ACCESS REQUIRED"
                size_hint_y: None
                height: '40dp'
                font_size: '22sp'
                bold: True
                color: utils.get_color_from_hex('#B4A7D6')

            TextInput:
                id: name_input
                hint_text: "YOUR NAME FOR REQUEST"
                size_hint_y: None
                height: '60dp'
                background_color: utils.get_color_from_hex('#FFE1F9')
                foreground_color: utils.get_color_from_hex('#B4A7D6')
                hint_text_color: utils.get_color_from_hex('#B4A7D6')
                font_name: 'RobotoMono-Regular'
                font_size: '18sp'
                multiline: False

            TextInput:
                id: username_input
                hint_text: "SECURE USERNAME"
                size_hint_y: None
                height: '60dp'
                background_color: utils.get_color_from_hex('#FFE1F9')
                foreground_color: utils.get_color_from_hex('#B4A7D6')
                hint_text_color: utils.get_color_from_hex('#B4A7D6')
                font_name: 'RobotoMono-Regular'
                font_size: '18sp'
                multiline: False

            Button:
                text: "REQUEST ACCESS"
                size_hint_y: None
                height: '60dp'
                font_size: '20sp'
                bold: True
                color: utils.get_color_from_hex('#FFD4E5')
                background_normal: ''
                background_color: [0, 0, 0, 0]
                on_release: root.send_request()
                canvas.before:
                    Color:
                        rgba: utils.get_color_from_hex('#D1C4E9')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [20]

            Label:
                id: status_label
                text: root.status_msg
                size_hint_y: None
                height: '30dp'
                font_size: '14sp'
                bold: True
                color: utils.get_color_from_hex('#B4A7D6')

            Widget:
                size_hint_y: None
                height: '10dp'

            TextInput:
                id: vip_code_input
                hint_text: "ENTER VIP CODE"
                size_hint_y: None
                height: '60dp'
                background_color: utils.get_color_from_hex('#FFE1F9')
                foreground_color: utils.get_color_from_hex('#B4A7D6')
                hint_text_color: utils.get_color_from_hex('#B4A7D6')
                font_name: 'RobotoMono-Regular'
                font_size: '18sp'
                multiline: False

            Button:
                text: "UNLOCK CYPHER"
                size_hint_y: None
                height: '70dp'
                font_size: '26sp'
                bold: True
                color: utils.get_color_from_hex('#FFD4E5')
                background_normal: ''
                background_color: [0, 0, 0, 0]
                on_release: root.verify_code()
                canvas.before:
                    Color:
                        rgba: utils.get_color_from_hex('#B4A7D6')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [25]

<MainScreen>:
    ScrollView:
        size_hint: (1, 1)
        CypherLayout:

<CypherLayout>:
    orientation: 'vertical'
    padding: '20dp'
    spacing: '10dp' 
    size_hint_y: None
    height: self.minimum_height

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
        spacing: '-30dp' 

        Image:
            source: 'CYPHER.png'
            size_hint_y: None
            height: '350dp' 
            fit_mode: 'contain'

        Image:
            source: 'Lock Lips.png'
            size_hint_y: None
            height: '75dp' 
            fit_mode: 'contain'

    TextInput:
        id: key_input
        password: True
        hint_text: "SECRET KEY"
        size_hint_y: None
        height: '60dp'
        background_color: utils.get_color_from_hex('#FFE1F9')
        foreground_color: utils.get_color_from_hex('#B4A7D6')
        hint_text_color: utils.get_color_from_hex('#B4A7D6')
        font_name: 'RobotoMono-Regular'
        font_size: '18sp'
        multiline: False

    TextInput:
        id: hint_input
        hint_text: "KEY HINT (Optional)"
        size_hint_y: None
        height: '60dp'
        background_color: utils.get_color_from_hex('#FFE1F9')
        foreground_color: utils.get_color_from_hex('#B4A7D6')
        hint_text_color: utils.get_color_from_hex('#B4A7D6')
        font_name: 'RobotoMono-Regular'
        font_size: '18sp'
        multiline: False

    Image:
        source: 'Kiss Chemistry.png'
        size_hint_y: None
        height: '75dp' 
        fit_mode: 'contain'

    Button:
        id: input_toggle_btn
        text: "INPUT MODE: TEXT (TAP TO SWAP)"
        size_hint_y: None
        height: '30dp'
        font_size: '14sp'
        bold: True
        color: utils.get_color_from_hex('#B4A7D6')
        background_normal: ''
        background_color: [0, 0, 0, 0]
        on_release: root.toggle_input_font()

    TextInput:
        id: msg_input
        hint_text: "YOUR MESSAGE"
        size_hint_y: None
        height: max(self.minimum_height, dp(100))
        background_color: utils.get_color_from_hex('#FFE1F9')
        foreground_color: utils.get_color_from_hex('#B4A7D6')
        hint_text_color: utils.get_color_from_hex('#B4A7D6')
        font_name: 'RobotoMono-Regular'
        font_size: '18sp'
        multiline: True
        on_text: root.on_msg_text(self, self.text)

    Button:
        text: "KISS"
        size_hint_y: None
        height: '70dp'
        font_size: '34sp'
        bold: True
        on_release: root.kiss()
        color: utils.get_color_from_hex('#FFD4E5')
        background_normal: ''
        background_color: [0, 0, 0, 0]
        canvas.before:
            Color:
                rgba: utils.get_color_from_hex('#B4A7D6')
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [25]

    Button:
        text: "TELL"
        size_hint_y: None
        height: '70dp'
        font_size: '34sp'
        bold: True
        on_release: root.tell()
        color: utils.get_color_from_hex('#FFD4E5')
        background_normal: ''
        background_color: [0, 0, 0, 0]
        canvas.before:
            Color:
                rgba: utils.get_color_from_hex('#B4A7D6')
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [25]

    Button:
        text: "DESTROY CHEMISTRY"
        size_hint_y: None
        height: '50dp'
        font_size: '22sp'
        bold: True
        on_release: root.destroy_chemistry()
        color: utils.get_color_from_hex('#FFD4E5')
        background_normal: ''
        background_color: [0, 0, 0, 0]
        canvas.before:
            Color:
                rgba: utils.get_color_from_hex('#D1C4E9')
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [15]

    Button:
        id: output_toggle_btn
        text: "OUTPUT MODE: EMOJI (TAP TO SWAP)"
        size_hint_y: None
        height: '30dp'
        font_size: '14sp'
        bold: True
        color: utils.get_color_from_hex('#B4A7D6')
        background_normal: ''
        background_color: [0, 0, 0, 0]
        on_release: root.toggle_output_font()

    TextInput:
        id: output_display
        text: root.output_text
        readonly: True
        size_hint_y: None
        height: max(self.minimum_height, dp(100))
        background_color: utils.get_color_from_hex('#FFE1F9')
        foreground_color: utils.get_color_from_hex('#B4A7D6')
        font_name: 'NotoEmoji-Regular.ttf'
        font_size: '18sp'
        bold: True
        multiline: True

    Button:
        id: share_btn
        text: "SHARE CYPHER"
        size_hint_y: None
        height: '50dp'
        font_size: '22sp'
        bold: True
        on_release: root.share_output()
        color: utils.get_color_from_hex('#FFD4E5')
        background_normal: ''
        background_color: [0, 0, 0, 0]
        canvas.before:
            Color:
                rgba: utils.get_color_from_hex('#B4A7D6')
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [15]

    Image:
        source: 'LPB.png'
        size_hint_y: None
        height: '100dp'
        fit_mode: 'contain'

    Label:
        text: "CREATED BY LILPEACHBAT"
        size_hint_y: None
        height: '30dp'
        font_size: '16sp'
        bold: True
        color: utils.get_color_from_hex('#B4A7D6')
'''

class LockScreen(Screen):
    status_msg = StringProperty("")

    def send_request(self):
        name = self.ids.name_input.text.strip()
        user = self.ids.username_input.text.strip().lower()
        if not name or not user:
            self.status_msg = "Please enter Name & Username!"
            return
        self.status_msg = "Sending request to ledger..."
        def ping_google_form():
            try:
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLScss8ZphhCVfMkw14f4Ijr9Gk8YdBOX2bJG_Dp3JSCDc6qCnQ/formResponse"
                entry_data = {"entry.1136846679": name, "entry.464222339": user} 
                requests.post(form_url, data=entry_data)
                self.status_msg = "Request sent! Wait for code."
            except Exception:
                self.status_msg = "No internet! Can't send request."
        threading.Thread(target=ping_google_form).start()

    def verify_code(self):
        user = self.ids.username_input.text.strip().lower()
        input_code = self.ids.vip_code_input.text.strip().upper()
        if not user or not input_code:
            self.status_msg = "Need Username & VIP Code!"
            return
        raw = f"{user}:{MASTER_PEPPER}"
        correct_hash = hashlib.sha256(raw.encode()).hexdigest()[:6].upper()
        if input_code == correct_hash:
            store = JsonStore(get_vault_path())
            store.put('vip_status', approved=True)
            self.manager.current = 'main'
        else:
            self.status_msg = "Invalid Code for this User."

class MainScreen(Screen):
    pass

class CypherLayout(BoxLayout):
    output_text = StringProperty("")

    def on_msg_text(self, instance, value):
        if "[" in value and "]" in value:
            try:
                start = value.find("[") + 1
                end = value.find("]")
                hint_line = value[start:end].strip()
                emoji_part = value[end+1:].strip()
                
                self.ids.hint_input.text = hint_line
                Clock.schedule_once(lambda dt: setattr(self.ids.msg_input, 'text', emoji_part), 0)
            except Exception:
                pass

    def toggle_input_font(self):
        current_font = self.ids.msg_input.font_name
        if current_font == 'RobotoMono-Regular':
            self.ids.msg_input.font_name = 'NotoEmoji-Regular.ttf'
            self.ids.input_toggle_btn.text = "INPUT MODE: EMOJI (TAP TO SWAP)"
        else:
            self.ids.msg_input.font_name = 'RobotoMono-Regular'
            self.ids.input_toggle_btn.text = "INPUT MODE: TEXT (TAP TO SWAP)"

    def toggle_output_font(self):
        current_font = self.ids.output_display.font_name
        if current_font == 'RobotoMono-Regular':
            self.ids.output_display.font_name = 'NotoEmoji-Regular.ttf'
            self.ids.output_toggle_btn.text = "OUTPUT MODE: EMOJI (TAP TO SWAP)"
        else:
            self.ids.output_display.font_name = 'RobotoMono-Regular'
            self.ids.output_toggle_btn.text = "OUTPUT MODE: TEXT (TAP TO SWAP)"

    def share_output(self):
        if self.output_text:
            shared = False
            if platform == 'android':
                try:
                    from jnius import autoclass, cast
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    Intent = autoclass('android.content.Intent')
                    String = autoclass('java.lang.String')
                    intent = Intent()
                    intent.setAction(Intent.ACTION_SEND)
                    java_text = String(self.output_text.encode('utf-8'), 'UTF-8')
                    intent.putExtra(Intent.EXTRA_TEXT, java_text)
                    intent.setType("text/plain")
                    currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
                    chooser_title = cast('java.lang.CharSequence', String("Share Cypher Chemistry"))
                    chooser = Intent.createChooser(intent, chooser_title)
                    currentActivity.startActivity(chooser)
                    shared = True
                except Exception:
                    pass
            
            if not shared:
                Clipboard.copy(self.output_text)
                self.ids.share_btn.text = "COPIED INSTEAD!"
                Clock.schedule_once(lambda dt: setattr(self.ids.share_btn, 'text', 'SHARE CYPHER'), 2)

    def kiss(self):
        kw = self.ids.key_input.text.strip()
        user_input = self.ids.msg_input.text.strip()
        hint = self.ids.hint_input.text.strip()
        
        if not kw or not user_input:
            self.output_text = "Enter key & message."
            return
            
        self.ids.output_display.font_name = 'NotoEmoji-Regular.ttf'
        self.ids.output_toggle_btn.text = "OUTPUT MODE: EMOJI (TAP TO SWAP)"
        
        params = get_keys_and_perms(kw, MASTER_PEPPER)
        data = user_input.encode('utf-8')
        tag = hashlib.sha256(data).digest()[:4]
        payload = data + tag
        
        nonce_bytes = [secrets.randbelow(256) for _ in range(4)]
        prev = int.from_bytes(hashlib.sha256(bytes(nonce_bytes)).digest()[:1], 'big')
        
        res_list = [to_emoji(b) for b in nonce_bytes]
        for byte in payload:
            current = byte ^ prev
            for r in range(ROUNDS):
                current = params[r]['p'][current]
                current = (params[r]['a'] * current + params[r]['b']) % 256
            res_list.append(to_emoji(current))
            prev = current
            
        cipher_text = " ".join(res_list)
        
        if hint:
            self.output_text = f"[{hint}]\n\n{cipher_text}"
        else:
            self.output_text = cipher_text

    def tell(self):
        kw = self.ids.key_input.text.strip()
        user_input = self.ids.msg_input.text.strip()
        
        if not kw or not user_input:
            self.output_text = "Enter key & message."
            return
            
        self.ids.output_display.font_name = 'RobotoMono-Regular'
        self.ids.output_toggle_btn.text = "OUTPUT MODE: TEXT (TAP TO SWAP)"
        
        params = get_keys_and_perms(kw, MASTER_PEPPER)
        try:
            parts = []
            for chunk in user_input.split():
                val = from_emoji(chunk)
                if val is not None:
                    parts.append(val)
                    
            if len(parts) < 9: raise ValueError("Format invalid")
            
            nonce_ints, ciphertext_payload = parts[:4], parts[4:]
            prev = int.from_bytes(hashlib.sha256(bytes(nonce_ints)).digest()[:1], 'big')
            decoded_bytes = []
            
            for current_cipher in ciphertext_payload:
                temp = current_cipher
                for r in reversed(range(ROUNDS)):
                    a_inv = pow(params[r]['a'], -1, 256)
                    temp = (a_inv * (temp - params[r]['b'])) % 256
                    temp = params[r]['inv_p'][temp]
                original_byte = temp ^ prev
                decoded_bytes.append(original_byte)
                prev = current_cipher
                
            final_data, received_tag = bytes(decoded_bytes[:-4]), bytes(decoded_bytes[-4:])
            if hashlib.sha256(final_data).digest()[:4] != received_tag:
                self.output_text = "Chemistry Error! Check Key."
            else:
                self.output_text = f"Cypher Whispers: {final_data.decode('utf-8')}"
        except Exception:
            self.output_text = "Chemistry Error! Check Key."

    def destroy_chemistry(self):
        self.ids.key_input.text = ""
        self.ids.hint_input.text = ""
        self.ids.msg_input.text = ""
        self.output_text = ""
        self.ids.msg_input.font_name = 'RobotoMono-Regular'
        self.ids.input_toggle_btn.text = "INPUT MODE: TEXT (TAP TO SWAP)"
        self.ids.output_display.font_name = 'NotoEmoji-Regular.ttf'
        self.ids.output_toggle_btn.text = "OUTPUT MODE: EMOJI (TAP TO SWAP)"

class WindowManager(ScreenManager):
    pass

class CypherApp(App):
    def build(self):
        Builder.load_string(KV)
        wm = WindowManager()
        store = JsonStore(get_vault_path())
        if store.exists('vip_status') and store.get('vip_status')['approved']:
            wm.current = 'main'
        else:
            wm.current = 'lock'
        return wm

if __name__ == '__main__':
    CypherApp().run()
