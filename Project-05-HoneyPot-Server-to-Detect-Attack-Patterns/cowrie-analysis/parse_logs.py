import json
from collections import Counter, defaultdict

LOG_PATH = '../cowrie/var/log/cowrie/cowrie.json'

def main():
    ip_counter = Counter()
    cmd_counter = Counter()
    ip_cmds = defaultdict(list)

    with open(LOG_PATH, 'r') as f:
        for line in f:
            try:
                event = json.loads(line)
                src_ip = event.get('src_ip')
                if src_ip:
                    ip_counter[src_ip] += 1
                if event.get('eventid') == 'cowrie.command.input':
                    cmd = event.get('input')
                    cmd_counter[cmd] += 1
                    ip_cmds[src_ip].append(cmd)
            except Exception as e:
                continue

    print("Top Attacking IPs:")
    for ip, count in ip_counter.most_common(10):
        print(f"{ip}: {count} attempts")

    print("\nTop Attempted Commands:")
    for cmd, count in cmd_counter.most_common(10):
        print(f"{cmd}: {count} times")

    with open('attacker_ips.txt', 'w') as f:
        for ip in ip_counter:
            f.write(ip + '\n')

    with open('ip_to_commands.json', 'w') as f:
        json.dump(ip_cmds, f, indent=2)

if __name__ == "__main__":
    main()
