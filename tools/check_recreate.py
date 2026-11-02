import paramiko

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
compose_path = '/volume1/docker/portainer/compose/70/docker-compose.yml'

print('=== STOP & RM OLD CONTAINER, THEN COMPOSE UP ===')
print('Stop:', run(f'{DOCKER} stop Obsidian'))
print('Rm:', run(f'{DOCKER} rm Obsidian'))
print('Compose up:', run(f'{DOCKER} compose -f {compose_path} up -d'))

print('=== INSPECT PRIVILEGED ===')
print('Privileged:', run(f"{DOCKER} inspect Obsidian --format '{{{{.HostConfig.Privileged}}}}'"))
print('SecurityOpt:', run(f"{DOCKER} inspect Obsidian --format '{{{{.HostConfig.SecurityOpt}}}}'"))
client.close()
