from skyfield.api import EarthSatellite, load
from datetime import datetime
from typing import Optional

class InvalidTLEError(Exception):
    pass

def compute_checksum(line: str) -> int:
    total = 0
    for char in line[:68]:
        if char.isdigit():
            total += int(char)
        elif char == '-':
            total += 1
    return total % 10

def validate_tle(line1: str, line2: str):
    if not line1.startswith('1') or len(line1.strip()) != 69:
        raise InvalidTLEError("Line 1 of the TLE must start with '1' and be exactly 69 characters long.")
    if not line2.startswith('2') or len(line2.strip()) != 69:
        raise InvalidTLEError("Line 2 of the TLE must start with '2' and be exactly 69 characters long.")
    
    for l in [line1, line2]:
        if l[-1].isdigit():
            if int(l[-1]) != compute_checksum(l):
                raise InvalidTLEError("Invalid checksum in TLE line: does not match expected digit.")
        else:
            raise InvalidTLEError("Last digit in line of the TLE is not a digit.")

def get_satellite_position(line1: str, line2: str, timestamp: Optional[datetime] = None):
    validate_tle(line1, line2)

    if timestamp is None:
        timestamp = datetime.now()

    try:
        ts = load.timescale()
        t = ts.utc(timestamp.year, timestamp.month, timestamp.day,
                   timestamp.hour, timestamp.minute, timestamp.second)
    except Exception as e:
        raise ValueError("Timestamp is invalid or could not be parsed.")

    try:
        satellite = EarthSatellite(line1, line2, 'SAT', ts)
        geocentric = satellite.at(t)
        position = geocentric.position.km
        return position
    except Exception as e:
        raise InvalidTLEError("Failed to compute position from the given TLE data.")
