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

print("=== APPEARANCE.JSON ===")
print(run("cat /volume1/docker/obsidian/admin/.obsidian/appearance.json 2>/dev/null"))

print("\n=== THEMES AND SNIPPETS ===")
print(run("ls -la /volume1/docker/obsidian/admin/.obsidian/themes 2>/dev/null"))
print(run("ls -la /volume1/docker/obsidian/admin/.obsidian/snippets 2>/dev/null"))

print("\n=== GTK SETTINGS ===")
print(run("cat /volume1/docker/obsidian/.config/gtk-3.0/settings.ini 2>/dev/null"))

print("\n=== OPENBOX RC.XML ===")
print(run("grep -i 'theme' /volume1/docker/obsidian/.config/openbox/rc.xml 2>/dev/null"))

client.close()
