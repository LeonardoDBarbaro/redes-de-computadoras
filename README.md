# TP N° 4 Integrador · Redes de Computadoras (3643) · Grupo 11

**Universidad Nacional de La Matanza.** Este repositorio tiene los scripts de Python del TP: los **suministrados por la cátedra** (incorporados con su historial desde [redes-computadoras/api-python-redes-cisco](https://github.com/redes-computadoras/api-python-redes-cisco)) y el **script propio** del grupo. También suma la documentación de la topología y de la API.

## Scripts (actividad 4)

Todos hablan con la API REST del Network Controller de Packet Tracer en `http://localhost:58000/api/v1`.

| Script | Origen | Qué hace |
|---|---|---|
| [`src/01_get-ticket.py`](src/01_get-ticket.py) | Cátedra | Pide un *service ticket* (`POST /ticket`) y lo muestra. |
| [`src/02_get-network-device.py`](src/02_get-network-device.py) | Cátedra | Lista los dispositivos de red (`GET /network-device`): hostname, plataforma e IP de gestión. Hay que pegarle a mano el ticket del 01. |
| [`src/03_get-host.py`](src/03_get-host.py) | Cátedra | Lista los hosts (`GET /host`): nombre, IP, MAC e interfaz donde están conectados. Hay que pegarle a mano el ticket del 01. |
| [`src/04_tabulate.py`](src/04_tabulate.py) | Cátedra | Pide el ticket solo y muestra dispositivos y hosts en tablas con `tabulate`. |
| [`src/05_inventario-csv.py`](src/05_inventario-csv.py) | **Grupo 11** | Pide el ticket solo, arma un **inventario de los dispositivos** (hostname, IP de gestión, tipo, plataforma, versión de software y estado de alcance) con fecha y hora, lo muestra en una tabla y lo **exporta a `inventario_red.csv`**. Le agrega a los suministrados un registro persistente que se puede abrir en Excel y comparar entre ejecuciones. |

### Cómo ejecutarlos

1. En Packet Tracer:
   - abrir el `.pkt`;
   - activar *Options → Preferences → Miscellaneous → Enable External Access for Network Controller REST API*;
   - en el Network Controller, activar *Config → Access Enable*.
2. Crear el entorno e instalar las dependencias:
   ```bash
   python -m venv venv
   venv\Scripts\activate          # Windows  (Linux: source venv/bin/activate)
   pip install -r requirements.txt
   ```
3. Ejecutar:
   ```bash
   python src/05_inventario-csv.py
   ```

> **Credenciales:** los scripts de la cátedra usan `cisco` / `cisco123!`. El script propio usa el usuario del controlador del grupo, `admin` / `cisco`. Si el NC tiene otro usuario, cambialo al principio de cada script.

## Documentación

- [Network Controller](NETWORK-CONTROLLER.md): discovery, inventario, topología y path trace.
- [API REST con Postman](API-REST.md): endpoints CRUD (POST, GET, PUT, DELETE) con sus capturas.
- [Pendientes](PENDIENTES.md): lo que falta para cumplir la consigna (`.pkt`, informe y entrega).

## Resumen del diseño

- Campus con dos edificios: Borde, núcleo con tres 3650 (Edificio A, Edificio B y Servidores) y routers de piso con router on a stick.
- 6 routers en el AS. El ISP queda afuera, conectado por serial al Borde.
- Ruteo OSPFv2 + OSPFv3 en el área 0, con ruta default propagada desde el Borde.
- IPv4 `172.16.0.0/16` (RFC 1918). IPv6 `2001:DB8:10::/48` (RFC 3849).
- Web server `198.51.100.30` / `2001:DB8:FFFF:100::30`, dominio `segundoparcial.test`, conectado al ISP.

| VLAN | Nombre | Red IPv4 |
|---|---|---|
| 10 | MGMT | 172.16.11.0/24 (Piso A) · 172.16.12.0/24 (Piso B) · 172.16.10.0/24 (Servidores) |
| 20 | SERVIDORES | 172.16.250.0/24: DNS .20 · NTP .30 · FTP .50 · NC .60 · NC secundario .70 |
| 30 | USUARIOS-A | 172.16.100.0/24 |
| 40 | USUARIOS-B | 172.16.200.0/24 |

## Contenido

| Ruta | Qué hay |
|---|---|
| `src/` | Scripts de Python (cátedra + propio) |
| `pkt/` | Archivo de Packet Tracer |
| `capturas/` | Capturas de Postman y del Network Controller |
