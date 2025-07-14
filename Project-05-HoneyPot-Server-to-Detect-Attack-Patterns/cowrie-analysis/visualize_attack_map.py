import json
import folium

def main():
    with open('attacker_ips_geo.json', 'r') as f:
        geo_data = json.load(f)

    m = folium.Map(location=[20,0], zoom_start=2)
    for entry in geo_data:
        if entry['lat'] is not None and entry['lon'] is not None:
            folium.CircleMarker(
                location=[entry['lat'], entry['lon']],
                radius=4,
                popup=f"{entry['ip']} ({entry['city']}, {entry['country']})",
                color='red',
                fill=True
            ).add_to(m)

    m.save('attack_map.html')
    print("Attack map saved as attack_map.html")

if __name__ == "__main__":
    main()