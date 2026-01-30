try:
    import swisseph as swe
    SWISSEPH_AVAILABLE = True
except ImportError:
    SWISSEPH_AVAILABLE = False
    print("Warning: PySwisseph not installed. Panchang calculations will show placeholder values.")

from datetime import datetime, timedelta
import math

# Nakshatra names (27 nakshatras)
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Nakshatra names in Tamil
NAKSHATRAS_TAMIL = [
    "அஸ்வினி", "பரணி", "கிருத்திகை", "ரோகிணி", "மிருகசீரிடம்", "திருவாதிரை",
    "புனர்பூசம்", "பூசம்", "ஆயில்யம்", "மகம்", "பூரம்", "உத்திரம்",
    "அஸ்தம்", "சித்திரை", "சுவாதி", "விசாகம்", "அனுஷம்", "கேட்டை",
    "மூலம்", "பூராடம்", "உத்திராடம்", "திருவோணம்", "அவிட்டம்", "சதயம்",
    "பூரட்டாதி", "உத்திரட்டாதி", "ரேவதி"
]

# Tithi names (30 tithis - 15 for waxing, 15 for waning)
TITHIS = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima"
]

TITHIS_KRISHNA = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
]

# Tithi names in Tamil
TITHIS_TAMIL = [
    "பிரதமை", "துவிதியை", "திருதியை", "சதுர்த்தி", "பஞ்சமி",
    "சஷ்டி", "சப்தமி", "அஷ்டமி", "நவமி", "தசமி",
    "ஏகாதசி", "துவாதசி", "திரயோதசி", "சதுர்த்தசி", "பௌர்ணமி"
]

TITHIS_KRISHNA_TAMIL = [
    "பிரதமை", "துவிதியை", "திருதியை", "சதுர்த்தி", "பஞ்சமி",
    "சஷ்டி", "சப்தமி", "அஷ்டமி", "நவமி", "தசமி",
    "ஏகாதசி", "துவாதசி", "திரயோதசி", "சதுர்த்தசி", "அமாவாசை"
]

# Yoga names (27 yogas)
YOGAS = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shoola", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti"
]

# Yoga names in Tamil
YOGAS_TAMIL = [
    "விஷ்கம்பம்", "ப்ரீதி", "ஆயுஷ்மான்", "சௌபாக்யம்", "சோபனம்", "அதிகண்டம்",
    "சுகர்மா", "திருதி", "சூலம்", "கண்டம்", "வ்ருத்தி", "துருவம்",
    "வியாகாதம்", "ஹர்ஷணம்", "வஜ்ரம்", "சித்தி", "வியதீபாதம்", "வரியான்",
    "பரிகம்", "சிவம்", "சித்தம்", "சாத்யம்", "சுபம்", "சுக்லம்",
    "பிரம்மா", "இந்திரா", "வைத்ருதி"
]

# Karana names (11 karanas)
KARANAS = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja",
    "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
]

# Karana names in Tamil
KARANAS_TAMIL = [
    "பவ", "பாலவ", "கௌலவ", "தைதில", "கரஜ",
    "வணிஜ", "விஷ்டி", "சகுனி", "சதுஷ்பாத", "நாக", "கிம்ஸ்துக்ன"
]

# Weekday names in Sanskrit
WEEKDAYS_SANSKRIT = [
    "Soma Vasara",      # Monday
    "Mangala Vasara",   # Tuesday
    "Budha Vasara",     # Wednesday
    "Guru Vasara",      # Thursday
    "Shukra Vasara",    # Friday
    "Shani Vasara",     # Saturday
    "Ravi Vasara"       # Sunday
]

# Weekday names in Tamil
WEEKDAYS_TAMIL = [
    "திங்கள்",    # Monday
    "செவ்வாய்",   # Tuesday
    "புதன்",      # Wednesday
    "வியாழன்",    # Thursday
    "வெள்ளி",     # Friday
    "சனி",        # Saturday
    "ஞாயிறு"      # Sunday
]

# Tamil Month names
TAMIL_MONTHS = [
    "சித்திரை",      # Chithirai (Apr-May)
    "வைகாசி",        # Vaikasi (May-Jun)
    "ஆனி",           # Aani (Jun-Jul)
    "ஆடி",           # Aadi (Jul-Aug)
    "ஆவணி",          # Aavani (Aug-Sep)
    "புரட்டாசி",      # Purattasi (Sep-Oct)
    "ஐப்பசி",        # Aippasi (Oct-Nov)
    "கார்த்திகை",     # Karthigai (Nov-Dec)
    "மார்கழி",        # Margazhi (Dec-Jan)
    "தை",            # Thai (Jan-Feb)
    "மாசி",           # Maasi (Feb-Mar)
    "பங்குனி"         # Panguni (Mar-Apr)
]

# Sanskrit Month names
SANSKRIT_MONTHS = [
    "Chaitra",     # Mar-Apr
    "Vaishakha",   # Apr-May
    "Jyeshtha",    # May-Jun
    "Ashadha",     # Jun-Jul
    "Shravana",    # Jul-Aug
    "Bhadrapada",  # Aug-Sep
    "Ashvina",     # Sep-Oct
    "Kartika",     # Oct-Nov
    "Margashirsha",# Nov-Dec
    "Pausha",      # Dec-Jan
    "Magha",       # Jan-Feb
    "Phalguna"     # Feb-Mar
]

# Ritu (Seasons) names
RITU_NAMES = [
    "Vasanta",    # Spring (Mar-May)
    "Grishma",    # Summer (May-Jul)
    "Varsha",     # Monsoon (Jul-Sep)
    "Sharad",     # Autumn (Sep-Nov)
    "Hemanta",    # Pre-winter (Nov-Jan)
    "Shishira"    # Winter (Jan-Mar)
]

RITU_NAMES_TAMIL = [
    "வசந்த",      # Spring
    "கிரீஷ்ம",     # Summer
    "வர்ஷா",       # Monsoon
    "சரத்",        # Autumn
    "ஹேமந்த",      # Pre-winter
    "சிசிர"        # Winter
]

# Ayana (Solstice period) names
AYANA_NAMES = ["Uttarayana", "Dakshinayana"]
AYANA_NAMES_TAMIL = ["உத்தராயண", "தக்ஷிணாயன"]

# 60-year cycle names (Samvatsara)
SAMVATSARA_NAMES = [
    "Prabhava", "Vibhava", "Shukla", "Pramoda", "Prajapati",
    "Angirasa", "Shrimukha", "Bhava", "Yuva", "Dhatri",
    "Ishvara", "Bahudhanya", "Pramathi", "Vikrama", "Vrisha",
    "Chitrabhanu", "Svabhanu", "Tarana", "Parthiva", "Vyaya",
    "Sarvajit", "Sarvadharin", "Virodhi", "Vikrita", "Khara",
    "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukhi",
    "Hevilambi", "Vilambi", "Vikari", "Sharvari", "Plava",
    "Shubhakrit", "Shobhana", "Krodhi", "Vishvavasu", "Parabhava",
    "Plavanga", "Kilaka", "Saumya", "Sadharana", "Virodhikrit",
    "Paridhavi", "Pramadi", "Ananda", "Rakshasa", "Nala",
    "Pingala", "Kalayukta", "Siddharthi", "Raudra", "Durmati",
    "Dundubhi", "Rudhirodgari", "Raktaksha", "Krodhana", "Akshaya"
]

def calculate_julian_day(dt):
    """Convert datetime to Julian Day Number"""
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour + dt.minute/60.0 + dt.second/3600.0
    
    if month <= 2:
        year -= 1
        month += 12
    
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    
    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + hour/24.0 + B - 1524.5
    
    return JD

def calculate_panchang(date, latitude, longitude, language='en'):
    """
    Calculate Panchang for a given date and location
    
    Args:
        date: datetime object
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        language: 'en' for English, 'ta' for Tamil
    
    Returns:
        dict with all panchang details
    """
    
    if not SWISSEPH_AVAILABLE:
        # Return placeholder values if swisseph is not available
        return {
            'tithi': 'Pratipada (Shukla)' if language == 'en' else 'பிரதமை (சுக்ல)',
            'nakshatra': 'Ashwini' if language == 'en' else 'அஸ்வினி',
            'yoga': 'Vishkambha' if language == 'en' else 'விஷ்கம்பம்',
            'karana': 'Bava' if language == 'en' else 'பவ',
            'weekday': 'Soma Vasara' if language == 'en' else 'திங்கள்',
            'month': 'Chaitra' if language == 'en' else 'சித்திரை',
            'paksha': 'Shukla Paksha' if language == 'en' else 'சுக்ல பக்ஷம்',
            'ritu': 'Vasanta' if language == 'en' else 'வசந்த',
            'ayana': 'Uttarayana' if language == 'en' else 'உத்தராயண',
            'year': 'Prabhava'
        }
    
    # Calculate Julian Day for the given date
    jd = calculate_julian_day(date)
    
    # Calculate Moon position
    moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]  # Moon longitude
    
    # Calculate Sun position
    sun_pos = swe.calc_ut(jd, swe.SUN)[0][0]  # Sun longitude
    
    # Calculate Nakshatra (based on Moon position)
    nakshatra_index = int(moon_pos / 13.333333)
    nakshatra_name = NAKSHATRAS_TAMIL[nakshatra_index] if language == 'ta' else NAKSHATRAS[nakshatra_index]
    
    # Calculate Tithi (based on Moon-Sun angle)
    moon_sun_diff = (moon_pos - sun_pos) % 360
    tithi_index = int(moon_sun_diff / 12)
    
    # Determine paksha (waxing or waning)
    if tithi_index < 15:
        # Shukla Paksha (waxing moon)
        tithi_name = TITHIS_TAMIL[tithi_index] if language == 'ta' else TITHIS[tithi_index]
        paksha = "சுக்ல பக்ஷம்" if language == 'ta' else "Shukla Paksha"
    else:
        # Krishna Paksha (waning moon)
        tithi_name = TITHIS_KRISHNA_TAMIL[tithi_index - 15] if language == 'ta' else TITHIS_KRISHNA[tithi_index - 15]
        paksha = "கிருஷ்ண பக்ஷம்" if language == 'ta' else "Krishna Paksha"
    
    # Calculate Yoga (based on Moon + Sun position)
    yoga_value = (moon_pos + sun_pos) % 360
    yoga_index = int(yoga_value / 13.333333)
    yoga_name = YOGAS_TAMIL[yoga_index] if language == 'ta' else YOGAS[yoga_index]
    
    # Calculate Karana (half of tithi)
    karana_index = int((moon_sun_diff / 6) % 60)
    if karana_index < 57:
        karana_name_idx = karana_index % 7
    else:
        karana_name_idx = 7 + (karana_index - 57)
    karana_name = KARANAS_TAMIL[karana_name_idx] if language == 'ta' else KARANAS[karana_name_idx]
    
    # Weekday calculation
    weekday_index = date.weekday()  # 0=Monday, 6=Sunday
    weekday_name = WEEKDAYS_TAMIL[weekday_index] if language == 'ta' else WEEKDAYS_SANSKRIT[weekday_index]
    
    # Tamil/Sanskrit Month calculation (approximate based on sun position)
    # Tamil calendar starts when sun enters Aries (Mesha)
    month_index = int(sun_pos / 30) % 12
    if language == 'ta':
        # Tamil months start from Chithirai (when sun enters Aries around April 14)
        tamil_month_index = (month_index - 0) % 12  # Mesha = Chithirai
        month_name = TAMIL_MONTHS[tamil_month_index]
    else:
        # Sanskrit months (Chaitra starts around Mar-Apr)
        month_name = SANSKRIT_MONTHS[month_index]
    
    # Ritu (Season) calculation - based on month
    ritu_index = int(month_index / 2) % 6
    ritu_name = RITU_NAMES_TAMIL[ritu_index] if language == 'ta' else RITU_NAMES[ritu_index]
    
    # Ayana (Solstice period)
    # Uttarayana: Sun moving north (approx Jan 14 - Jul 14)
    # Dakshinayana: Sun moving south (approx Jul 14 - Jan 14)
    if 270 <= sun_pos or sun_pos < 90:
        ayana_name = AYANA_NAMES_TAMIL[0] if language == 'ta' else AYANA_NAMES[0]  # Uttarayana
    else:
        ayana_name = AYANA_NAMES_TAMIL[1] if language == 'ta' else AYANA_NAMES[1]  # Dakshinayana
    
    # Samvatsara (60-year cycle) calculation
    # Tamil year starts around April 14
    base_year = 1987  # Known Prabhava year
    year_diff = date.year - base_year
    samvatsara_index = year_diff % 60
    year_name = SAMVATSARA_NAMES[samvatsara_index]
    
    return {
        'tithi': tithi_name,
        'nakshatra': nakshatra_name,
        'yoga': yoga_name,
        'karana': karana_name,
        'weekday': weekday_name,
        'month': month_name,
        'paksha': paksha,
        'ritu': ritu_name,
        'ayana': ayana_name,
        'year': year_name
    }
