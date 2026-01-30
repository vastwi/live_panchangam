# Tamil Nadu Districts and Cities with Coordinates
# Format: 'Location': (latitude, longitude, timezone)

TN_LOCATIONS = {
    # Districts
    'Ariyalur': (11.1401, 79.0770, 'Asia/Kolkata'),
    'Chengalpattu': (12.6922, 79.9758, 'Asia/Kolkata'),
    'Chennai': (13.0827, 80.2707, 'Asia/Kolkata'),
    'Coimbatore': (11.0168, 76.9558, 'Asia/Kolkata'),
    'Cuddalore': (11.7480, 79.7714, 'Asia/Kolkata'),
    'Dharmapuri': (12.1211, 78.1582, 'Asia/Kolkata'),
    'Dindigul': (10.3673, 77.9803, 'Asia/Kolkata'),
    'Erode': (11.3410, 77.7172, 'Asia/Kolkata'),
    'Kallakurichi': (11.7394, 78.9594, 'Asia/Kolkata'),
    'Kanchipuram': (12.8342, 79.7036, 'Asia/Kolkata'),
    'Kanyakumari': (8.0883, 77.5385, 'Asia/Kolkata'),
    'Karur': (10.9601, 78.0766, 'Asia/Kolkata'),
    'Krishnagiri': (12.5186, 78.2137, 'Asia/Kolkata'),
    'Madurai': (9.9252, 78.1198, 'Asia/Kolkata'),
    'Mayiladuthurai': (11.1025, 79.6536, 'Asia/Kolkata'),
    'Nagapattinam': (10.7672, 79.8449, 'Asia/Kolkata'),
    'Namakkal': (11.2189, 78.1677, 'Asia/Kolkata'),
    'Nilgiris': (11.4102, 76.6950, 'Asia/Kolkata'),
    'Perambalur': (11.2324, 78.8793, 'Asia/Kolkata'),
    'Pudukkottai': (10.3833, 78.8000, 'Asia/Kolkata'),
    'Ramanathapuram': (9.3639, 78.8377, 'Asia/Kolkata'),
    'Ranipet': (12.9222, 79.3333, 'Asia/Kolkata'),
    'Salem': (11.6643, 78.1460, 'Asia/Kolkata'),
    'Sivaganga': (9.8433, 78.4809, 'Asia/Kolkata'),
    'Tenkasi': (8.9597, 77.3152, 'Asia/Kolkata'),
    'Thanjavur': (10.7870, 79.1378, 'Asia/Kolkata'),
    'Theni': (10.0104, 77.4977, 'Asia/Kolkata'),
    'Thoothukudi': (8.7642, 78.1348, 'Asia/Kolkata'),
    'Tiruchirappalli': (10.7905, 78.7047, 'Asia/Kolkata'),
    'Tirunelveli': (8.7139, 77.7567, 'Asia/Kolkata'),
    'Tirupathur': (12.4989, 78.5731, 'Asia/Kolkata'),
    'Tiruppur': (11.1085, 77.3411, 'Asia/Kolkata'),
    'Tiruvallur': (13.1436, 79.9119, 'Asia/Kolkata'),
    'Tiruvannamalai': (12.2253, 79.0747, 'Asia/Kolkata'),
    'Tiruvarur': (10.7729, 79.6345, 'Asia/Kolkata'),
    'Vellore': (12.9165, 79.1325, 'Asia/Kolkata'),
    'Viluppuram': (11.9401, 79.4861, 'Asia/Kolkata'),
    'Virudhunagar': (9.5881, 77.9624, 'Asia/Kolkata'),
    
    # Major Cities/Towns
    'Hosur': (12.7409, 77.8253, 'Asia/Kolkata'),
    'Kumbakonam': (10.9617, 79.3881, 'Asia/Kolkata'),
    'Nagercoil': (8.1778, 77.4345, 'Asia/Kolkata'),
    'Ooty': (11.4102, 76.6950, 'Asia/Kolkata'),
    'Pollachi': (10.6581, 77.0089, 'Asia/Kolkata'),
    'Tambaram': (12.9249, 80.1000, 'Asia/Kolkata'),
    'Tiruchengode': (11.3797, 77.8940, 'Asia/Kolkata'),
}

def get_location_coordinates(location_name):
    """
    Get coordinates for a given location
    Returns: (latitude, longitude, timezone) or None if not found
    """
    return TN_LOCATIONS.get(location_name)

def get_all_locations():
    """
    Get list of all available locations
    """
    return sorted(TN_LOCATIONS.keys())
