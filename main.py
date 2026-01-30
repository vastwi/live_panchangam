from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from datetime import datetime, timedelta
import calendar

# Import calculation modules
try:
    from location_data import get_location_coordinates, get_all_locations
    from sun_calculator import calculate_sunrise_sunset, format_time_12hr
    from panchang_calculator import calculate_panchang
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False

# Set window size for testing on desktop
Window.size = (400, 700)
Window.clearcolor = (0.95, 0.95, 0.97, 1)  # Light background

class TamilPanchangApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = 'en'
        self.current_location = 'Chennai'
        self.current_date = datetime.now()
        self.current_time = datetime.now().time()
        self.is_today = True
        
        self.translations = {
            'en': {
                'title': 'Live Thirukanitha Panchangam',
                'location': 'Location',
                'date': 'Date',
                'time': 'Time',
                'sunrise': 'Sunrise',
                'sunset': 'Sunset',
                'panchang_details': 'Panchang Details',
                'year': 'Year',
                'ayana': 'Ayana',
                'ritu': 'Ritu',
                'month': 'Month',
                'paksha': 'Paksha',
                'tithi': 'Tithi',
                'weekday': 'Weekday',
                'nakshatra': 'Nakshatra',
                'yoga': 'Yoga',
                'karana': 'Karana',
                'select_location': 'Select Location',
                'confirm': 'Confirm',
                'cancel': 'Cancel',
                'disclaimer': 'Note: Uses Drik Panchang (Modern Astronomical)',
            },
            'ta': {
                'title': 'நேரலை திருகணித பஞ்சாங்கம்',
                'location': 'இடம்',
                'date': 'தேதி',
                'time': 'நேரம்',
                'sunrise': 'சூரிய உதயம்',
                'sunset': 'சூரிய அஸ்தமனம்',
                'panchang_details': 'பஞ்சாங்க விவரங்கள்',
                'year': 'வருடம்',
                'ayana': 'அயனம்',
                'ritu': 'ருது',
                'month': 'மாதம்',
                'paksha': 'பக்ஷம்',
                'tithi': 'திதி',
                'weekday': 'வாரம்',
                'nakshatra': 'நட்சத்திரம்',
                'yoga': 'யோகம்',
                'karana': 'கரணம்',
                'select_location': 'இடத்தைத் தேர்ந்தெடுக்கவும்',
                'confirm': 'உறுதிப்படுத்து',
                'cancel': 'ரத்து',
                'disclaimer': 'குறிப்பு: திரிக் பஞ்சாங்கம் (நவீன வானியல் கணிப்பு)',
            }
        }
    
    def build(self):
        # Set theme colors
        self.theme_colors = {
            'primary': (1, 0.6, 0, 1),      # Orange
            'primary_dark': (0.9, 0.4, 0, 1),  # Dark Orange
            'accent': (1, 0.8, 0.2, 1),     # Golden
            'background': (0.95, 0.95, 0.97, 1),  # Light Gray
            'card': (1, 1, 1, 1),           # White
            'text': (0.2, 0.2, 0.2, 1),     # Dark Gray
            'text_light': (0.5, 0.5, 0.5, 1),  # Medium Gray
        }
        
        self.root_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # Add background
        with self.root_layout.canvas.before:
            Color(*self.theme_colors['background'])
            self.bg_rect = Rectangle(size=self.root_layout.size, pos=self.root_layout.pos)
        self.root_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # Create UI
        self.create_header()
        self.create_location_section()
        self.create_date_section()
        self.create_time_section()
        self.create_sun_timings()
        self.create_panchang_section()
        
        # Update display every second if today
        Clock.schedule_interval(self.update_live_data, 1)
        
        # Initial calculation
        self.update_panchang()
        
        return self.root_layout
    
    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def create_card(self, content_widget, height='auto'):
        """Helper to create a styled card"""
        card = BoxLayout(orientation='vertical', padding=[10, 5, 10, 5], spacing=0)
        
        if height != 'auto':
            card.size_hint_y = None
            card.height = height
        
        # White background with shadow effect
        with card.canvas.before:
            Color(*self.theme_colors['card'])
            card.rect = Rectangle(size=card.size, pos=card.pos)
        
        card.bind(size=lambda i, v: setattr(i.rect, 'size', v),
                 pos=lambda i, v: setattr(i.rect, 'pos', v))
        
        card.add_widget(content_widget)
        
        # Add spacing wrapper
        wrapper = BoxLayout(orientation='vertical', padding=[10, 5, 10, 5], size_hint_y=None)
        wrapper.height = height if height != 'auto' else 100
        wrapper.add_widget(card)
        
        return wrapper
    
    def create_header(self):
        header = BoxLayout(size_hint_y=0.10, spacing=0, padding=[10, 8, 10, 3])
        
        # Add gradient background
        with header.canvas.before:
            Color(*self.theme_colors['primary'])
            self.header_rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=lambda i, v: setattr(self.header_rect, 'size', v),
                   pos=lambda i, v: setattr(self.header_rect, 'pos', v))
        
        self.title_label = Label(
            text=self.get_text('title'),
            font_size='15sp',
            bold=True,
            size_hint_x=0.75,
            color=(1, 1, 1, 1),  # White text
            halign='left',
            valign='middle',
            text_size=(None, None)  # Will be set dynamically
        )
        self.title_label.bind(size=self._update_title_text_size)
        
        self.lang_button = Button(
            text='EN/TA',
            size_hint_x=0.25,
            background_color=self.theme_colors['accent'],
            color=(0.2, 0.2, 0.2, 1),
            bold=True,
            on_release=self.toggle_language
        )
        
        header.add_widget(self.title_label)
        header.add_widget(self.lang_button)
        self.root_layout.add_widget(header)
    
    def _update_title_text_size(self, instance, value):
        instance.text_size = (instance.width, None)
    
    def create_location_section(self):
        content = BoxLayout(orientation='vertical', spacing=5, padding=[5, 5, 5, 5])
        
        loc_header = Button(
            text=f"📍 {self.get_text('location')}",
            on_release=self.show_location_picker,
            background_color=self.theme_colors['primary_dark'],
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.4
        )
        
        self.location_label = Label(
            text=self.current_location,
            font_size='18sp',
            bold=True,
            color=self.theme_colors['primary'],
            size_hint_y=0.6
        )
        
        content.add_widget(loc_header)
        content.add_widget(self.location_label)
        
        card = self.create_card(content, height=85)
        self.root_layout.add_widget(card)
    
    def create_date_section(self):
        content = BoxLayout(orientation='vertical', spacing=5, padding=[5, 5, 5, 5])
        
        date_header = Button(
            text=f"📅 {self.get_text('date')}",
            on_release=self.reset_to_today,
            background_color=self.theme_colors['primary_dark'],
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.35
        )
        
        date_controls = BoxLayout(size_hint_y=0.65, spacing=5)
        
        prev_btn = Button(
            text='◀',
            background_color=self.theme_colors['accent'],
            color=(0.2, 0.2, 0.2, 1),
            bold=True,
            on_release=lambda x: self.change_date(-1)
        )
        
        self.date_button = Button(
            text=self.current_date.strftime('%d-%m-%Y'),
            background_color=self.theme_colors['card'],
            color=self.theme_colors['primary'],
            font_size='16sp',
            bold=True,
            on_release=self.show_date_picker
        )
        
        next_btn = Button(
            text='▶',
            background_color=self.theme_colors['accent'],
            color=(0.2, 0.2, 0.2, 1),
            bold=True,
            on_release=lambda x: self.change_date(1)
        )
        
        date_controls.add_widget(prev_btn)
        date_controls.add_widget(self.date_button)
        date_controls.add_widget(next_btn)
        
        content.add_widget(date_header)
        content.add_widget(date_controls)
        
        card = self.create_card(content, height=95)
        self.root_layout.add_widget(card)
    
    def create_time_section(self):
        content = BoxLayout(orientation='vertical', spacing=5, padding=[5, 5, 5, 5])
        
        time_header = Button(
            text=f"🕐 {self.get_text('time')}",
            on_release=self.reset_time_smart,
            background_color=self.theme_colors['primary_dark'],
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.35
        )
        
        time_controls = BoxLayout(size_hint_y=0.65, spacing=5)
        
        minus_btn = Button(
            text='−1h',
            background_color=self.theme_colors['accent'],
            color=(0.2, 0.2, 0.2, 1),
            bold=True,
            on_release=lambda x: self.change_time(-1)
        )
        
        self.time_button = Button(
            text=self.format_time(self.current_time),
            background_color=self.theme_colors['card'],
            color=self.theme_colors['primary'],
            font_size='16sp',
            bold=True,
            on_release=self.show_time_picker
        )
        
        plus_btn = Button(
            text='+1h',
            background_color=self.theme_colors['accent'],
            color=(0.2, 0.2, 0.2, 1),
            bold=True,
            on_release=lambda x: self.change_time(1)
        )
        
        reset_btn = Button(
            text='↻',
            background_color=self.theme_colors['accent'],
            color=(0.2, 0.2, 0.2, 1),
            bold=True,
            on_release=self.reset_time_smart
        )
        
        time_controls.add_widget(minus_btn)
        time_controls.add_widget(self.time_button)
        time_controls.add_widget(plus_btn)
        time_controls.add_widget(reset_btn)
        
        content.add_widget(time_header)
        content.add_widget(time_controls)
        
        card = self.create_card(content, height=95)
        self.root_layout.add_widget(card)
    
    def create_sun_timings(self):
        content = BoxLayout(orientation='vertical', spacing=5, padding=[8, 8, 8, 8])
        
        header = Label(
            text='☀️ Sun Timings',
            font_size='16sp',
            bold=True,
            size_hint_y=0.25,
            color=self.theme_colors['primary']
        )
        
        timings = BoxLayout(size_hint_y=0.75, spacing=10)
        
        # Sunrise box
        sunrise_box = BoxLayout(orientation='vertical', spacing=3, padding=[5, 5, 5, 5])
        with sunrise_box.canvas.before:
            Color(1, 0.95, 0.8, 1)  # Light orange
            sunrise_box.rect = Rectangle(size=sunrise_box.size, pos=sunrise_box.pos)
        sunrise_box.bind(size=lambda i, v: setattr(i.rect, 'size', v),
                        pos=lambda i, v: setattr(i.rect, 'pos', v))
        
        self.sunrise_label = Label(
            text=self.get_text('sunrise'),
            font_size='11sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        self.sunrise_time = Label(
            text='--:--',
            font_size='16sp',
            bold=True,
            color=(1, 0.5, 0, 1)  # Orange
        )
        sunrise_box.add_widget(self.sunrise_label)
        sunrise_box.add_widget(self.sunrise_time)
        
        # Sunset box
        sunset_box = BoxLayout(orientation='vertical', spacing=3, padding=[5, 5, 5, 5])
        with sunset_box.canvas.before:
            Color(0.9, 0.85, 1, 1)  # Light purple
            sunset_box.rect = Rectangle(size=sunset_box.size, pos=sunset_box.pos)
        sunset_box.bind(size=lambda i, v: setattr(i.rect, 'size', v),
                       pos=lambda i, v: setattr(i.rect, 'pos', v))
        
        self.sunset_label = Label(
            text=self.get_text('sunset'),
            font_size='11sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        self.sunset_time = Label(
            text='--:--',
            font_size='16sp',
            bold=True,
            color=(0.4, 0.2, 0.6, 1)  # Purple
        )
        sunset_box.add_widget(self.sunset_label)
        sunset_box.add_widget(self.sunset_time)
        
        timings.add_widget(sunrise_box)
        timings.add_widget(sunset_box)
        
        content.add_widget(header)
        content.add_widget(timings)
        
        card = self.create_card(content, height=95)
        self.root_layout.add_widget(card)
    
    def create_panchang_section(self):
        scroll_content = BoxLayout(orientation='vertical', padding=[5, 5, 5, 5])
        
        # Header
        header = Label(
            text=self.get_text('panchang_details'),
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=35,
            color=self.theme_colors['primary']
        )
        scroll_content.add_widget(header)
        
        # Panchang grid
        layout = GridLayout(cols=2, spacing=5, size_hint_y=None, padding=[3, 3, 3, 3])
        layout.bind(minimum_height=layout.setter('height'))
        
        # Store labels for updating
        self.panchang_labels = {}
        
        fields = ['year', 'ayana', 'ritu', 'month', 'paksha', 'tithi', 'weekday', 'nakshatra', 'yoga', 'karana']
        
        colors = [
            (1, 0.95, 0.9, 1),   # Light peach
            (0.95, 0.98, 1, 1),  # Light blue
        ]
        
        for idx, field in enumerate(fields):
            # Label box
            label_box = BoxLayout(padding=[5, 3, 5, 3])
            with label_box.canvas.before:
                Color(*colors[idx % 2])
                label_box.rect = Rectangle(size=label_box.size, pos=label_box.pos)
            label_box.bind(size=lambda i, v: setattr(i.rect, 'size', v),
                          pos=lambda i, v: setattr(i.rect, 'pos', v))
            
            label = Label(
                text=f"{self.get_text(field)}:",
                font_size='12sp',
                bold=True,
                size_hint_y=None,
                height=32,
                halign='right',
                valign='middle',
                color=(0.3, 0.3, 0.3, 1)
            )
            label.bind(size=label.setter('text_size'))
            label_box.add_widget(label)
            
            # Value box
            value_box = BoxLayout(padding=[5, 3, 5, 3])
            with value_box.canvas.before:
                Color(*self.theme_colors['card'])
                value_box.rect = Rectangle(size=value_box.size, pos=value_box.pos)
            value_box.bind(size=lambda i, v: setattr(i.rect, 'size', v),
                          pos=lambda i, v: setattr(i.rect, 'pos', v))
            
            value = Label(
                text='--',
                font_size='12sp',
                size_hint_y=None,
                height=32,
                halign='left',
                valign='middle',
                color=self.theme_colors['primary']
            )
            value.bind(size=value.setter('text_size'))
            value_box.add_widget(value)
            
            layout.add_widget(label_box)
            layout.add_widget(value_box)
            
            self.panchang_labels[field] = value
        
        scroll_content.add_widget(layout)
        
        # Disclaimer
        self.disclaimer_label = Label(
            text=self.get_text('disclaimer'),
            font_size='9sp',
            size_hint_y=None,
            height=30,
            color=self.theme_colors['text_light'],
            italic=True,
            halign='center',
            valign='middle'
        )
        self.disclaimer_label.bind(size=self.disclaimer_label.setter('text_size'))
        scroll_content.add_widget(self.disclaimer_label)
        
        scroll = ScrollView(size_hint_y=None)
        scroll.height = Window.height * 0.45  # Take remaining space
        scroll.add_widget(scroll_content)
        
        card = self.create_card(scroll, height=Window.height * 0.48)
        self.root_layout.add_widget(card)
    
    def get_text(self, key):
        return self.translations[self.language].get(key, key)
    
    def toggle_language(self, instance):
        self.language = 'ta' if self.language == 'en' else 'en'
        self.update_ui_language()
        self.update_panchang()
    
    def update_ui_language(self):
        self.title_label.text = self.get_text('title')
        self.sunrise_label.text = self.get_text('sunrise')
        self.sunset_label.text = self.get_text('sunset')
        self.disclaimer_label.text = self.get_text('disclaimer')
    
    def show_location_picker(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        if MODULES_AVAILABLE:
            locations = get_all_locations()
        else:
            locations = ['Chennai', 'Coimbatore', 'Madurai']
        
        spinner = Spinner(
            text=self.current_location,
            values=locations,
            size_hint_y=0.8
        )
        
        buttons = BoxLayout(size_hint_y=0.2, spacing=10)
        
        popup = Popup(
            title=self.get_text('select_location'),
            content=content,
            size_hint=(0.9, 0.7)
        )
        
        confirm = Button(
            text=self.get_text('confirm'),
            on_release=lambda x: self.set_location(spinner.text, popup)
        )
        cancel = Button(
            text=self.get_text('cancel'),
            on_release=popup.dismiss
        )
        
        buttons.add_widget(confirm)
        buttons.add_widget(cancel)
        
        content.add_widget(spinner)
        content.add_widget(buttons)
        
        popup.open()
    
    def show_date_picker(self, instance):
        """Show date picker popup"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Year, Month, Day selectors
        selectors = BoxLayout(size_hint_y=0.7, spacing=10)
        
        # Year spinner (100 years past to 10 years future)
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 100, current_year + 11)]
        year_spinner = Spinner(
            text=str(self.current_date.year),
            values=years
        )
        
        # Month spinner
        months = [str(m).zfill(2) for m in range(1, 13)]
        month_spinner = Spinner(
            text=str(self.current_date.month).zfill(2),
            values=months
        )
        
        # Day spinner
        days = [str(d).zfill(2) for d in range(1, 32)]
        day_spinner = Spinner(
            text=str(self.current_date.day).zfill(2),
            values=days
        )
        
        selectors.add_widget(day_spinner)
        selectors.add_widget(month_spinner)
        selectors.add_widget(year_spinner)
        
        # Buttons
        buttons = BoxLayout(size_hint_y=0.3, spacing=10)
        
        popup = Popup(
            title='Select Date',
            content=content,
            size_hint=(0.9, 0.5)
        )
        
        confirm = Button(
            text=self.get_text('confirm'),
            on_release=lambda x: self.set_date(
                int(year_spinner.text),
                int(month_spinner.text),
                int(day_spinner.text),
                popup
            )
        )
        cancel = Button(
            text=self.get_text('cancel'),
            on_release=popup.dismiss
        )
        
        buttons.add_widget(confirm)
        buttons.add_widget(cancel)
        
        content.add_widget(selectors)
        content.add_widget(buttons)
        
        popup.open()
    
    def show_time_picker(self, instance):
        """Show time picker popup"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Hour and Minute selectors
        selectors = BoxLayout(size_hint_y=0.7, spacing=10)
        
        # Hour spinner (00-23)
        hours = [str(h).zfill(2) for h in range(24)]
        hour_spinner = Spinner(
            text=str(self.current_time.hour).zfill(2),
            values=hours
        )
        
        # Minute spinner (00-59)
        minutes = [str(m).zfill(2) for m in range(60)]
        minute_spinner = Spinner(
            text=str(self.current_time.minute).zfill(2),
            values=minutes
        )
        
        colon = Label(text=':', font_size='24sp', size_hint_x=0.2)
        
        selectors.add_widget(hour_spinner)
        selectors.add_widget(colon)
        selectors.add_widget(minute_spinner)
        
        # Buttons
        buttons = BoxLayout(size_hint_y=0.3, spacing=10)
        
        popup = Popup(
            title='Select Time',
            content=content,
            size_hint=(0.8, 0.4)
        )
        
        confirm = Button(
            text=self.get_text('confirm'),
            on_release=lambda x: self.set_time(
                int(hour_spinner.text),
                int(minute_spinner.text),
                popup
            )
        )
        cancel = Button(
            text=self.get_text('cancel'),
            on_release=popup.dismiss
        )
        
        buttons.add_widget(confirm)
        buttons.add_widget(cancel)
        
        content.add_widget(selectors)
        content.add_widget(buttons)
        
        popup.open()
    
    def set_location(self, location, popup):
        self.current_location = location
        self.location_label.text = location
        popup.dismiss()
        self.update_panchang()
    
    def set_date(self, year, month, day, popup):
        """Set date from date picker"""
        try:
            self.current_date = datetime(year, month, day)
            self.date_button.text = self.current_date.strftime('%d-%m-%Y')
            
            # Check if it's today
            today = datetime.now().date()
            self.is_today = (self.current_date.date() == today)
            
            if not self.is_today:
                self.current_time = datetime.strptime("06:00", "%H:%M").time()
                self.time_button.text = self.format_time(self.current_time)
            
            popup.dismiss()
            self.update_panchang()
        except ValueError:
            # Invalid date
            pass
    
    def set_time(self, hour, minute, popup):
        """Set time from time picker"""
        try:
            self.current_time = datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
            
            # If user manually sets time for today, stop live updates
            if self.is_today:
                self.is_today = False  # Treat as "frozen" time, not live
            
            self.time_button.text = self.format_time(self.current_time)
            popup.dismiss()
            self.update_panchang()
        except ValueError:
            pass
    
    def change_date(self, days):
        self.current_date += timedelta(days=days)
        self.date_button.text = self.current_date.strftime('%d-%m-%Y')
        
        # Check if it's today
        today = datetime.now().date()
        self.is_today = (self.current_date.date() == today)
        
        if not self.is_today:
            self.current_time = datetime.strptime("06:00", "%H:%M").time()
            self.time_button.text = self.format_time(self.current_time)
        
        self.update_panchang()
    
    def reset_to_today(self, instance):
        self.current_date = datetime.now()
        self.current_time = datetime.now().time()
        self.date_button.text = self.current_date.strftime('%d-%m-%Y')
        self.is_today = True
        self.update_panchang()
    
    def change_time(self, hours):
        current = datetime.combine(datetime.today(), self.current_time)
        new_time = (current + timedelta(hours=hours)).time()
        self.current_time = new_time
        
        # If user manually adjusts time for today, stop live updates
        today = datetime.now().date()
        if self.current_date.date() == today:
            self.is_today = False  # Treat as "frozen" time
        
        self.time_button.text = self.format_time(self.current_time)
        self.update_panchang()
    
    def reset_time_smart(self, instance):
        """Smart reset: Current time if today, 6 AM otherwise"""
        today = datetime.now().date()
        if self.current_date.date() == today:
            # Reset to live current time for today
            self.is_today = True
            self.current_time = datetime.now().time()
            self.time_button.text = f"🔴 {datetime.now().strftime('%I:%M:%S %p')}"
        else:
            # Reset to 6 AM (sunrise) for past/future dates
            self.is_today = False
            self.current_time = datetime.strptime("06:00", "%H:%M").time()
            self.time_button.text = self.format_time(self.current_time)
        
        self.update_panchang()
    
    def format_time(self, time_obj):
        return datetime.combine(datetime.today(), time_obj).strftime('%I:%M %p')
    
    def update_live_data(self, dt):
        if self.is_today:
            now = datetime.now()
            self.current_time = now.time()
            self.time_button.text = f"🔴 {now.strftime('%I:%M:%S %p')}"
            # Update panchang every minute
            if now.second == 0:
                self.update_panchang()
    
    def update_panchang(self):
        if not MODULES_AVAILABLE:
            return
        
        coords = get_location_coordinates(self.current_location)
        if not coords:
            return
        
        latitude, longitude, timezone = coords
        
        # Calculate sunrise/sunset
        sunrise, sunset = calculate_sunrise_sunset(latitude, longitude, self.current_date)
        self.sunrise_time.text = format_time_12hr(sunrise)
        self.sunset_time.text = format_time_12hr(sunset)
        
        # Calculate panchang
        calc_datetime = datetime.combine(self.current_date.date(), self.current_time)
        panchang = calculate_panchang(calc_datetime, latitude, longitude, self.language)
        
        # Update labels
        for field in ['year', 'ayana', 'ritu', 'month', 'paksha', 'tithi', 'weekday', 'nakshatra', 'yoga', 'karana']:
            if field in self.panchang_labels and field in panchang:
                self.panchang_labels[field].text = str(panchang[field])

if __name__ == '__main__':
    TamilPanchangApp().run()
