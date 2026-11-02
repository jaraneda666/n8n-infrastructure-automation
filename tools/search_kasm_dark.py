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
cmd = f"{DOCKER} exec Obsidian grep -rnI 'dark' /usr/share/kasmvnc/www/public/ 2>/dev/null | head -n 30"
print(run(cmd))

print("--- CSS FILES ---")
cmd2 = f"{DOCKER} exec Obsidian ls -la /usr/share/kasmvnc/www/public/css/"
print(run(cmd2))

client.close()
