import paramiko
import urllib.request
import base64
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
print('Status:', run(f"{DOCKER} ps --filter name=Obsidian --format 'table {{{{.Names}}}}\t{{{{.Status}}}}\t{{{{.Ports}}}}'"))
client.close()

req = urllib.request.Request('http://192.168.1.100:3421/')
creds = base64.b64encode(b'admin:').decode()
req.add_header('Authorization', f'Basic {creds}')
try:
    with urllib.request.urlopen(req, timeout=5) as r:
        print('HTTP 3421 response code:', r.status)
except Exception as e:
    print('HTTP error:', e)
