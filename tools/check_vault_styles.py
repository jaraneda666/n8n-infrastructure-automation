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

print("=== SEARCH FOR INLINE STYLES / COLORS IN MARKDOWN FILES ===")
print(run("grep -rnI -E '(color:|color=|#000|black)' /volume1/docker/obsidian/admin/ 2>/dev/null | head -n 40"))

print("\n=== HEAD OF INFORME COMPLETO ===")
print(run("head -n 50 /volume1/docker/obsidian/admin/Estudios/IACC/'Taller de Integracion en Seguridad de Datos'/'Semana 7'/'Informe_Completo_Semana_7.md' 2>/dev/null"))

print("\n=== HEAD OF FICHA TECNICA ===")
print(run("head -n 50 /volume1/docker/obsidian/admin/Estudios/IACC/'Taller de Integracion en Seguridad de Datos'/'Semana 7'/'Ficha_Tecnica_Semana_7.md' 2>/dev/null"))

client.close()
