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

print("=== FIND WEB ASSETS IN CONTAINER ===")
print(run(f"{DOCKER} exec Obsidian find /usr/ /var/ /etc/ -name '*kclient*' 2>/dev/null"))

print("\n=== KASMVNC WWW DIR ===")
print(run(f"{DOCKER} exec Obsidian find /usr/share/kasmvnc/www/ -maxdepth 3 2>/dev/null"))

print("\n=== CURRENT LOGS OF OBSIDIAN / X11 ===")
print(run("cat /volume1/docker/obsidian/.cache/openbox/openbox.log 2>/dev/null | tail -n 20"))
print(run("cat /volume1/docker/obsidian/.config/obsidian/obsidian.log 2>/dev/null | tail -n 20"))

client.close()
