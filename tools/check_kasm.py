import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.1.100', 22, os.environ.get("ADMIN_USER", "admin"), os.environ.get("ADMIN_PASS", ""), timeout=10)

def run(cmd):
    stdin, stdout, stderr = client.exec_command(f'echo "$ADMIN_PASS" | sudo -S {cmd}')
    raw = stdout.read().decode('utf-8', errors='replace').strip()
    if raw.startswith('Password:'):
        raw = raw[len('Password:'):].strip()
    return raw

DOCKER = '/var/packages/ContainerManager/target/usr/bin/docker'
print("=== DEFAULTS ===")
print(run(f"{DOCKER} exec Obsidian ls -la /defaults/ 2>/dev/null"))

print("\n=== KASMVNC IN CONTAINER ===")
print(run(f"{DOCKER} exec Obsidian ls -la /etc/kasmvnc/ 2>/dev/null"))

print("\n=== KASM / VNC CONFIG IN /CONFIG ===")
print(run("find /volume1/docker/obsidian/ -name '*kasm*' -o -name '*vnc*' -o -name '*openbox*' 2>/dev/null"))

print("\n=== GTK / THEME SETTINGS IN /CONFIG ===")
print(run("find /volume1/docker/obsidian/ -name '*gtk*' 2>/dev/null"))

client.close()
