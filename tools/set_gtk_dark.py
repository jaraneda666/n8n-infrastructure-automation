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

content = "[Settings]\\ngtk-application-prefer-dark-theme=1\\n"
print("Setting GTK3 settings.ini...")
print(run(f"bash -c 'printf \"[Settings]\\ngtk-application-prefer-dark-theme=1\\n\" > /volume1/docker/obsidian/.config/gtk-3.0/settings.ini && chown admin:users /volume1/docker/obsidian/.config/gtk-3.0/settings.ini'"))
print("Verify:")
print(run("cat /volume1/docker/obsidian/.config/gtk-3.0/settings.ini"))

client.close()
