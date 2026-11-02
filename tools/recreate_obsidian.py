import paramiko
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

# 1. Read compose file from NAS
compose_path = '/volume1/docker/portainer/compose/70/docker-compose.yml'
content = run(f'cat {compose_path}')

# 2. Replace privileged with security_opt
old_line = '    privileged: true # <--- BYPASS DE RESTRICCIONES DE SYNOLOGY'
new_line = '    security_opt:\n      - seccomp:unconfined'

if old_line not in content:
    lines = content.splitlines()
    new_lines = []
    for l in lines:
        if 'privileged: true' in l:
            new_lines.append(new_line)
        else:
            new_lines.append(l)
    new_content = '\n'.join(new_lines)
else:
    new_content = content.replace(old_line, new_line, 1)

# Write back via base64
b64 = base64.b64encode(new_content.encode('utf-8')).decode('ascii')
client.exec_command(f'echo "{b64}" | base64 -d > /tmp/new_compose.yml')
run(f'cp /tmp/new_compose.yml {compose_path}')
print('Compose actualizado en NAS. Verificando diff:')
print(run(f'diff -u {compose_path}.bak_20261007 {compose_path}'))

# 3. Recreate container
DOCKER = '/var/packages/ContainerManager/target/usr/bin/docker'
print('Recreando contenedor Obsidian...')
recreate_out = run(f'{DOCKER} compose -f {compose_path} up -d --force-recreate')
print('Salida recreate:\n', recreate_out)

# 4. Verify privileged status
insp = run(f"{DOCKER} inspect Obsidian --format '{{{{.HostConfig.Privileged}}}} | {{{{.State.Status}}}}'")
print('\nNuevo estado Obsidian (Privileged | Status):', insp)

client.close()
