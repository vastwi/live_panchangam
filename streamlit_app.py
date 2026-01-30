import streamlit as st
from datetime import datetime, timedelta

# Import our calculation modules
# Note: You need to have location_data.py, sun_calculator.py, and panchang_calculator.py in the same folder
try:
    from location_data import get_location_coordinates
    from sun_calculator import calculate_sunrise_sunset, format_time_12hr
    from panchang_calculator import calculate_panchang
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False
    st.warning("⚠️ Calculation modules not found. Please ensure location_data.py, sun_calculator.py, and panchang_calculator.py are in the same folder.")

# Page config
st.set_page_config(
    page_title="Tamil Panchang",
    page_icon="📅",
    layout="centered"
)

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.now()
if 'location' not in st.session_state:
    st.session_state.location = 'Chennai'
if 'show_location_select' not in st.session_state:
    st.session_state.show_location_select = False
if 'date_input_key' not in st.session_state:
    st.session_state.date_input_key = 0
if 'selected_time' not in st.session_state:
    st.session_state.selected_time = datetime.now().time()
if 'show_time_select' not in st.session_state:
    st.session_state.show_time_select = False

# Translations
translations = {
    'en': {
        'title': 'Tamil Panchang',
        'location': 'Location',
        'date': 'Date',
        'time': 'Time',
        'sunrise': 'Sunrise',
        'sunset': 'Sunset',
        'panchang_details': 'Panchang Details',
        'additional_details': 'Additional Details',
        'tithi': 'Tithi',
        'nakshatra': 'Nakshatra',
        'yoga': 'Yoga',
        'karana': 'Karana',
        'weekday': 'Weekday',
        'month': 'Month',
        'paksha': 'Paksha',
        'ritu': 'Ritu',
        'ayana': 'Ayana',
        'year': 'Year Name',
        'select_location': 'Select Location',
        'confirm': 'Confirm',
        'cancel': 'Cancel',
        'edit_time': 'Edit Time',
    },
    'ta': {
        'title': 'தமிழ் பஞ்சாங்கம்',
        'location': 'இடம்',
        'date': 'தேதி',
        'time': 'நேரம்',
        'sunrise': 'சூரிய உதயம்',
        'sunset': 'சூரிய அஸ்தமனம்',
        'panchang_details': 'பஞ்சாங்க விவரங்கள்',
        'additional_details': 'கூடுதல் விவரங்கள்',
        'tithi': 'திதி',
        'nakshatra': 'நட்சத்திரம்',
        'yoga': 'யோகம்',
        'karana': 'கரணம்',
        'weekday': 'வாரம்',
        'month': 'மாதம்',
        'paksha': 'பக்ஷம்',
        'ritu': 'ருது',
        'ayana': 'அயனம்',
        'year': 'வருட பெயர்',
        'select_location': 'இடத்தைத் தேர்ந்தெடுக்கவும்',
        'confirm': 'உறுதிப்படுத்து',
        'cancel': 'ரத்து',
        'edit_time': 'நேரத்தை மாற்று',
    }
}

# Tamil Nadu locations
tn_locations = [
    'Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore',
    'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram',
    'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Mayiladuthurai',
    'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai',
    'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi',
    'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli',
    'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur',
    'Vellore', 'Viluppuram', 'Virudhunagar',
    'Hosur', 'Kumbakonam', 'Nagercoil', 'Ooty', 'Pollachi', 
    'Tambaram', 'Tiruchengode'
]

def get_text(key):
    """Get translated text"""
    return translations[st.session_state.language][key]

def toggle_language():
    """Toggle between English and Tamil"""
    st.session_state.language = 'ta' if st.session_state.language == 'en' else 'en'

def change_date(days):
    """Change date by specified days"""
    st.session_state.current_date += timedelta(days=days)

def reset_to_today():
    """Reset date to today"""
    st.session_state.current_date = datetime.now()

def toggle_location_select():
    """Toggle location selection panel"""
    st.session_state.show_location_select = not st.session_state.show_location_select

def get_panchang_data(location, date, selected_time, language):
    """
    Get all panchang data for given location, date and time
    """
    if not MODULES_AVAILABLE:
        return {
            'sunrise': '--:--',
            'sunset': '--:--',
            'tithi': '--',
            'nakshatra': '--',
            'yoga': '--',
            'karana': '--',
            'weekday': '--',
            'month': '--',
            'paksha': '--',
            'ritu': '--',
            'ayana': '--',
            'year': '--'
        }
    
    # Get coordinates
    coords = get_location_coordinates(location)
    if not coords:
        return {
            'sunrise': '--:--',
            'sunset': '--:--',
            'tithi': '--',
            'nakshatra': '--',
            'yoga': '--',
            'karana': '--',
            'weekday': '--',
            'month': '--',
            'paksha': '--',
            'ritu': '--',
            'ayana': '--',
            'year': '--'
        }
    
    latitude, longitude, timezone = coords
    
    # Create datetime with selected time
    calculation_datetime = datetime.combine(date.date(), selected_time)
    
    # Calculate sunrise/sunset for the selected date
    sunrise, sunset = calculate_sunrise_sunset(latitude, longitude, date)
    sunrise_str = format_time_12hr(sunrise)
    sunset_str = format_time_12hr(sunset)
    
    # Calculate panchang for the specific date and time
    panchang = calculate_panchang(calculation_datetime, latitude, longitude, language)
    
    return {
        'sunrise': sunrise_str,
        'sunset': sunset_str,
        'tithi': panchang['tithi'],
        'nakshatra': panchang['nakshatra'],
        'yoga': panchang['yoga'],
        'karana': panchang['karana'],
        'weekday': panchang['weekday'],
        'month': panchang['month'],
        'paksha': panchang['paksha'],
        'ritu': panchang['ritu'],
        'ayana': panchang['ayana'],
        'year': panchang['year']
    }

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title(get_text('title'))
with col2:
    if st.button('EN/TA', key='lang_toggle'):
        toggle_language()
        st.rerun()

st.divider()

# Combined Location and Date Section
col1, col2 = st.columns(2)

# Location Section
with col1:
    # Make location heading clickable to toggle edit mode
    if st.button(f"📍 {get_text('location')}", key='location_heading', use_container_width=True, type="secondary"):
        toggle_location_select()
        st.rerun()
    
    # Show current location or dropdown based on edit mode
    if not st.session_state.show_location_select:
        st.markdown(f"**{st.session_state.location}**")
    else:
        # Show searchable dropdown directly
        selected_location = st.selectbox(
            get_text('select_location'),
            sorted(tn_locations),
            index=sorted(tn_locations).index(st.session_state.location) if st.session_state.location in tn_locations else 0,
            label_visibility='collapsed',
            key='location_dropdown'
        )
        
        # Confirm and Cancel buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button(f"✓ {get_text('confirm')}", key='confirm_location', use_container_width=True):
                st.session_state.location = selected_location
                st.session_state.show_location_select = False
                st.rerun()
        with btn_col2:
            if st.button(f"✗ {get_text('cancel')}", key='cancel_location', use_container_width=True):
                st.session_state.show_location_select = False
                st.rerun()

# Date Section
with col2:
    # Make date heading clickable to reset to today
    if st.button(f"📅 {get_text('date')}", key='date_heading', use_container_width=True, type="secondary"):
        reset_to_today()
        st.rerun()
    
    # Date display with arrows - clickable to open date picker
    date_col1, date_col2, date_col3 = st.columns([1, 4, 1])
    
    with date_col1:
        if st.button("◀", key='prev_date', use_container_width=True):
            change_date(-1)
            st.rerun()
    
    with date_col2:
        # Calculate date range (100 years past to 10 years future)
        min_date = datetime.now() - timedelta(days=365*100)
        max_date = datetime.now() + timedelta(days=365*10)
        
        # Date picker directly in place - no button needed
        new_date = st.date_input(
            "Date",
            value=st.session_state.current_date,
            min_value=min_date,
            max_value=max_date,
            label_visibility='collapsed',
            key='date_picker',
            format="DD-MM-YYYY"
        )
        
        # Update date if changed
        if new_date != st.session_state.current_date.date():
            st.session_state.current_date = datetime.combine(new_date, datetime.min.time())
            st.rerun()
    
    with date_col3:
        if st.button("▶", key='next_date', use_container_width=True):
            change_date(1)
            st.rerun()

st.divider()

# Calculate panchang data
panchang_data = get_panchang_data(
    st.session_state.location,
    st.session_state.current_date,
    st.session_state.selected_time,
    st.session_state.language
)

# Show calculation time info
now = datetime.now()
if st.session_state.current_date.date() == now.date():
    st.success(f"🔴 **LIVE** - Panchang at current time: {now.strftime('%I:%M:%S %p')} IST")
else:
    calc_time = st.session_state.selected_time.strftime('%I:%M %p')
    st.info(f"📅 Panchang for {st.session_state.current_date.strftime('%d-%m-%Y')} at {calc_time}")

# Sun Timings Section
st.subheader("☀️ Sun Timings")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label=get_text('sunrise'),
        value=panchang_data['sunrise']
    )

with col2:
    st.metric(
        label=get_text('sunset'),
        value=panchang_data['sunset']
    )

st.divider()

# Panchang Details Section
st.subheader(get_text('panchang_details'))

col1, col2 = st.columns(2)

with col1:
    st.write(f"**{get_text('year')}:** {panchang_data['year']}")
    st.write(f"**{get_text('ayana')}:** {panchang_data['ayana']}")
    st.write(f"**{get_text('ritu')}:** {panchang_data['ritu']}")
    st.write(f"**{get_text('month')}:** {panchang_data['month']}")
    st.write(f"**{get_text('paksha')}:** {panchang_data['paksha']}")

with col2:
    st.write(f"**{get_text('tithi')}:** {panchang_data['tithi']}")
    st.write(f"**{get_text('weekday')}:** {panchang_data['weekday']}")
    st.write(f"**{get_text('nakshatra')}:** {panchang_data['nakshatra']}")
    st.write(f"**{get_text('yoga')}:** {panchang_data['yoga']}")
    st.write(f"**{get_text('karana')}:** {panchang_data['karana']}")

st.divider()

# Footer
st.caption("✅ Phase 2 Complete: Panchang Calculations Active!")
st.caption("📍 Location-based sunrise/sunset | 🌙 Tithi, Nakshatra, Yoga, Karana")
st.caption("⚠️ Note: This app uses Drik Panchang (Modern Astronomical Calculations)")

# Display current state (for debugging)
with st.expander("🔧 Debug Info"):
    st.write(f"Language: {st.session_state.language}")
    st.write(f"Location: {st.session_state.location}")
    st.write(f"Date: {st.session_state.current_date.strftime('%d-%m-%Y')}")
    st.write(f"Modules Available: {MODULES_AVAILABLE}")
    if MODULES_AVAILABLE:
        from location_data import get_location_coordinates
        coords = get_location_coordinates(st.session_state.location)
        if coords:
            st.write(f"Coordinates: {coords[0]:.4f}°N, {coords[1]:.4f}°E")
    st.write("Panchang Type: Drik (Modern Astronomical)")
    st.write("Ayanamsa: Not Applied")
