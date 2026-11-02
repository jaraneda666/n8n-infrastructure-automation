# n8n Infrastructure Automation Suite

Colección de flujos de trabajo de n8n y utilitarios de soporte para supervisión de servicios, sincronización de bóvedas de documentación y alertas de infraestructura.

---

## Arquitectura y Componentes

- **Orquestador:** n8n en contenedor Docker con acceso a APIs locales.
- **Supervisión:** Verificación de estado de proxies inversos y contenedores en Synology DSM.
- **Integración:** Nodos HTTP Request y webhooks con autenticación por clave.

---

## Instrucciones de Uso

Importe las definiciones de flujo de trabajo `.json` en su consola de n8n y configure las variables de entorno locales.

---

## Consideraciones de Seguridad

- Este repositorio almacena código fuente, utilitarios de prueba y documentación técnica de ingeniería.
- Todas las credenciales, llaves privadas y variables de entorno deben suministrarse de forma local mediante archivos no versionados.
- Las herramientas de auditoría contenidas deben utilizarse exclusivamente en entornos autorizados y laboratorios de prueba.

---

**Autor:** Security Analyst  
**Licencia:** Uso Privado / Propietario
