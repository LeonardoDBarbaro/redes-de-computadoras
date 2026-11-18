# TP Integrador — Redes de Computadoras (Grupo 11)
n**Autor del repo:** Leo Barbaro

Diseño propio: **Edificio A**, **Edificio B**, **granja de servidores**, **router de borde** e **ISP**. Ruteo con **OSPF** (RIP descartado por los profes). IPv4 + IPv6. Network Controller + Postman + Python.

## Plan de direccionamiento IPv4 (RFC 1918, 172.16.0.0)

| Segmento | Red | Notas |
|---|---|---|
| Switches 2960 (gestión) | 172.16.10.X/24 | VLAN administrativa para el NC |
| Enlaces entre routers | 172.16.50.X/30 | +4 por cada enlace |
| Edificio A | 172.16.100.X/24 | hosts de 10 en 10 |
| Edificio B | 172.16.200.X/24 | |
| Granja de servidores | 172.16.250.X/24 | DNS, NTP, FTP |
| WAN Borde ↔ ISP | 192.0.2.X/24 | IPs "reales" de documentación (RFC 5737) |

Default gateway: `.254`.

| Web server (detrás del ISP) | 198.51.100.30 | RFC 5737 |

## VLANs

| VLAN | Uso |
|---|---|
| 10 | Switches (administrativa / NC) |
| 20 | Edificio A |
| 30 | Servidores |
| 40 | Edificio B |

## Decisiones
- El **web server HTTP** cuelga del **ISP** (simula Internet), no de la granja.
- DNS / NTP / FTP en la granja (la versión nueva del TP permite que estén en un solo server).
- Borde ↔ ISP por **cable serial** → módulo **NIM-2T** en ambos routers.
- El **ISP no es nuestro**: no debe ser descubierto por el NC (en el inventario debería figurar *wrong credentials*):
  ```
  no cdp run
  no router ospf 10
  ```
- Dominio de prueba: `SegundoParcial.test` (registro A al web server).

## Documentación

- [Network Controller](NETWORK-CONTROLLER.md): discovery, inventario, topología y path trace
- [API REST con Postman](API-REST.md): ticket, credenciales y flow-analysis
- [Pendientes](PENDIENTES.md): checklist de lo que falta en el `.pkt` según la consigna

## Contenido

| Carpeta | Qué hay |
|---|---|
| `pkt/` | Archivo de Packet Tracer |
| `scripts/` | Script de Python contra la API del Network Controller |
| `capturas/` | Capturas de Postman y del Network Controller |

## Script de inventario

[`scripts/script_inventario.py`](scripts/script_inventario.py): pide un ticket al Network Controller, consulta `/api/v1/network-device` y muestra el inventario en una tabla (hostname, IP de gestión, tipo, plataforma, versión y estado). También lo exporta a `inventario_red.csv`.

```bash
pip install -r requirements.txt
python scripts/script_inventario.py
```

> El script apunta al NC en `172.16.250.60` con el usuario `admin` / `cisco`. Si lo corrés contra otro NC, cambiá `NC_IP` y las credenciales al principio del archivo (desde la PC host es `127.0.0.1:58000`).
