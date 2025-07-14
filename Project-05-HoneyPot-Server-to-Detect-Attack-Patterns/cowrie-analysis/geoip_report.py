import geoip2.database
import json

def main():
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    with open('attacker_ips.txt', 'r') as f:
        ips = [line.strip() for line in f]

    geo_data = []
    for ip in ips:
        try:
            response = reader.city(ip)
            geo_data.append({
                'ip': ip,
                'country': response.country.name,
                'city': response.city.name,
                'lat': response.location.latitude,
                'lon': response.location.longitude
            })
        except Exception:
            continue

    with open('attacker_ips_geo.json', 'w') as f:
        json.dump(geo_data, f, indent=2)

    print(f"Geolocated {len(geo_data)} IPs.")

if __name__ == "__main__":
    main()