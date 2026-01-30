import math
from datetime import datetime, timedelta

def calculate_sunrise_sunset(latitude, longitude, date):
    """
    Calculate sunrise and sunset times for a given location and date
    
    Args:
        latitude: Latitude in degrees (positive for North)
        longitude: Longitude in degrees (positive for East)
        date: datetime object
    
    Returns:
        tuple: (sunrise_time, sunset_time) as datetime objects
    """
    
    # Julian day calculation
    year = date.year
    month = date.month
    day = date.day
    
    if month <= 2:
        year -= 1
        month += 12
    
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    
    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    
    # Calculate time
    n = JD - 2451545.0 + 0.0008
    
    # Mean solar time
    J_star = n - (longitude / 360)
    
    # Solar mean anomaly
    M = (357.5291 + 0.98560028 * J_star) % 360
    
    # Equation of center
    C = 1.9148 * math.sin(math.radians(M)) + 0.0200 * math.sin(math.radians(2 * M)) + 0.0003 * math.sin(math.radians(3 * M))
    
    # Ecliptic longitude
    lambda_val = (M + C + 180 + 102.9372) % 360
    
    # Solar transit
    J_transit = 2451545.0 + J_star + 0.0053 * math.sin(math.radians(M)) - 0.0069 * math.sin(math.radians(2 * lambda_val))
    
    # Declination of the sun
    sin_delta = math.sin(math.radians(lambda_val)) * math.sin(math.radians(23.44))
    cos_delta = math.cos(math.asin(sin_delta))
    
    # Hour angle
    cos_omega = (math.sin(math.radians(-0.83)) - math.sin(math.radians(latitude)) * sin_delta) / (math.cos(math.radians(latitude)) * cos_delta)
    
    # Check if sun rises/sets
    if cos_omega > 1:
        # Polar night - sun doesn't rise
        return None, None
    elif cos_omega < -1:
        # Polar day - sun doesn't set
        return None, None
    
    omega = math.degrees(math.acos(cos_omega))
    
    # Calculate sunrise and sunset
    J_rise = J_transit - (omega / 360)
    J_set = J_transit + (omega / 360)
    
    # Convert to datetime
    def julian_to_datetime(jd, date):
        # Calculate time from Julian date
        time_decimal = (jd - math.floor(jd)) * 24
        hours = int(time_decimal)
        minutes = int((time_decimal - hours) * 60)
        seconds = int(((time_decimal - hours) * 60 - minutes) * 60)
        
        return datetime(date.year, date.month, date.day, hours, minutes, seconds)
    
    sunrise = julian_to_datetime(J_rise, date)
    sunset = julian_to_datetime(J_set, date)
    
    # The calculation gives UTC time, need to convert to IST (UTC+5:30)
    ist_offset = timedelta(hours=5, minutes=30)
    
    sunrise = sunrise + ist_offset
    sunset = sunset + ist_offset
    
    return sunrise, sunset

def format_time_12hr(dt):
    """
    Format datetime to 12-hour format string
    """
    if dt is None:
        return "--:--"
    return dt.strftime("%I:%M %p")

def format_time_24hr(dt):
    """
    Format datetime to 24-hour format string
    """
    if dt is None:
        return "--:--"
    return dt.strftime("%H:%M")
