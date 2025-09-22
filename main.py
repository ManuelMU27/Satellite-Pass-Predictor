from skyfield.api import load, wgs84, EarthSatellite, utc
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo 

# To activate the environment: .venv\Scripts\Activate.ps1

# Fetches ISS TLE data
def get_iss_tle():
    url = "https://celestrak.org/NORAD/elements/stations.txt"
    response = requests.get(url)
    lines = response.text.strip().splitlines()
    # ISS is the first satellite in stations.txt
    return lines[0], lines[1], lines[2]

# Predicts next passes
def predict_passes(latitude, longitude, altitude_m = 0, hours = 24, local_tz = "America/New_York"):
    ts = load.timescale()
    line0, line1, line2 = get_iss_tle()
    satellite = EarthSatellite(line1, line2, line0, ts)

    location = wgs84.latlon(latitude, longitude, altitude_m)

    now = datetime.now(utc)
    end_time = now + timedelta(hours = hours)

    times, events = satellite.find_events(location, ts.utc(now), ts.utc(end_time), altitude_degrees = 10.0)

    print(f"\nPredicted ISS passes for the next {hours} hours at lat = {latitude}, lon = {longitude}:\n")

    current_pass = {}
    passes = [] # Stores results

    for t, event in zip(times, events):
        if event == 0: # Rise
            current_pass["rise"] = t.utc_datetime() # strftime('%Y-%m-%d %H:%M:%S')
        elif event == 1: # Peak
            current_pass["peak"] = t.utc_datetime() # strftime('%Y-%m-%d %H:%M:%S')
            # Computes altitude at peak
            difference = satellite - location
            topocentric = difference.at(t)
            alt, az, distance = topocentric.altaz()
            current_pass["max_altitude_deg"] = round(alt.degrees, 1)
        elif event == 2: # Set
            current_pass["set"] = t.utc_datetime() # strftime('%Y-%m-%d %H:%M:%S')

            # Converts to local timezone
            rise_local = current_pass["rise"].astimezone(ZoneInfo(local_tz))
            peak_local = current_pass["peak"].astimezone(ZoneInfo(local_tz))
            set_local = current_pass["set"].astimezone(ZoneInfo(local_tz))

            # Prints with format
            print(f"Pass:")
            print(f"  Rise: {rise_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"  Peak: {peak_local.strftime('%Y-%m-%d %H:%M:%S %Z')} (alt = {current_pass['max_altitude_deg']}°)")
            print(f"  Set: {set_local.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")

            # Saves to a list
            passes.append({
                "rise": rise_local,
                "peak": peak_local,
                "set": set_local,
                "max_altitude_deg": current_pass["max_altitude_deg"]
            })

            current_pass = {} # Resets for next pass
    
    return passes # Can be used for later (CSV, dashboard, etc.)

if __name__ == "__main__":
    # Example: Atlanta, GA (33.7490° N, -84.3880° W)
    predict_passes(latitude = 33.7490, longitude = -84.3880)
