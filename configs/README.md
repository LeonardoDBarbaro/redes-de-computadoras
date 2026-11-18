# Configs para corregir el `.pkt`

Bloques listos para pegar en la **CLI** de cada equipo en Packet Tracer (pestaña CLI → `enable` → pegar todo el bloque). Cada uno corresponde a un punto de [PENDIENTES.md](../PENDIENTES.md).

| Archivo | Equipo | Punto |
|---|---|---|
| [`3650-Servidores_dhcp.txt`](3650-Servidores_dhcp.txt) | 3650-Servidores | 1 · DHCP en un 3650 |
| [`2960-Servidores_puerto-dhcp.txt`](2960-Servidores_puerto-dhcp.txt) | 2960-Servidores | 1 · puerto para la PC cliente DHCP |
| [`ISP.txt`](ISP.txt) | ISP | 2 · sin credencial CLI y rutas default |
| [`2960_privilege15.txt`](2960_privilege15.txt) | 2960-PisoA, 2960-PisoB y 2960-Servidores | 3 · usuario con privilege 15 |
| [`verificacion.txt`](verificacion.txt) | todos | comandos para las evidencias del informe |

> Antes de pegar, confirmar con `show running-config` que los nombres de interfaces e IPs coinciden con el equipo.
> Los pasos del Network Controller (punto 4) y de las Place Notes (punto 5) se hacen en la interfaz gráfica: ver PENDIENTES.md.
