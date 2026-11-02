import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')

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

print("=== WEB FILES IN /usr/share/kasmvnc/www/ ===")
print(run(f'{DOCKER} exec Obsidian find /usr/share/kasmvnc/www/ -maxdepth 2'))

print("\n=== NGINX / WEB ROOT IN CONTAINER ===")
print(run(f'{DOCKER} exec Obsidian cat /etc/nginx/nginx.conf 2>/dev/null || cat /etc/nginx/http.d/default.conf 2>/dev/null'))

print("\n=== RUNNING PROCESSES IN CONTAINER ===")
print(run(f'{DOCKER} exec Obsidian ps aux'))

client.close()
