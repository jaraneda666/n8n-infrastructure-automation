import paramiko
import json
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
insp_raw = run(f'{DOCKER} inspect Obsidian')
data = json.loads(insp_raw)[0]

hc = data.get('HostConfig', {})
cfg = data.get('Config', {})

print("=== OBSIDIAN CONTAINER AUDIT ===")
print("Image:", cfg.get('Image'))
print("Privileged:", hc.get('Privileged'))
print("CapAdd:", hc.get('CapAdd'))
print("Devices:", hc.get('Devices'))
print("Binds:", hc.get('Binds'))
print("PortBindings:", hc.get('PortBindings'))
print("NetworkMode:", hc.get('NetworkMode'))
print("RestartPolicy:", hc.get('RestartPolicy'))
print("Env:", cfg.get('Env'))
print("Labels:", json.dumps(cfg.get('Labels', {}), indent=2))

print("\n=== COMPOSE / DOCKER DIR SEARCH ===")
print(run("find /volume1/docker/ -name '*compose*' -o -name '*obsidian*' 2>/dev/null"))

client.close()
