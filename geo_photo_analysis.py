import piexif
from fractions import Fraction
from geopy.geocoders import Nominatim

def convert_to_degrees(coord):
    degrees = coord[0][0] / coord[0][1]
    minutes = coord[1][0] / coord[1][1]
    seconds = coord[2][0] / coord[2][1]
    return degrees + minutes / 60 + seconds / 3600

def extract_location_from_image(image_path):
    try:
        exif_data = piexif.load(image_path)

        if "GPS" in exif_data:
            gps_info = exif_data["GPS"]
            lat = convert_to_degrees(gps_info[2])
            lon = convert_to_degrees(gps_info[4])

            if gps_info[3] == 83:  # Check for 'S'
                lat = -lat

            if gps_info[1] == 87:  # Check for 'W'
                lon = -lon

            location = (lat, lon)

            # Reverse geocoding
            geolocator = Nominatim(user_agent="reverse_geocoding_example")
            location_name = geolocator.reverse(location)

            return location, location_name
        else:
            raise ValueError("No GPS data found in the image")

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage with the new image path
image_path = r"D:\project\geo1.jpg"
result = extract_location_from_image(image_path)

if result:
    location, location_name = result
    print(f"Location extracted from image: Latitude {location[0]}, Longitude {location[1]}")
    print(f"Location in words: {location_name}")
else:
    print("Failed to extract location from image.")
