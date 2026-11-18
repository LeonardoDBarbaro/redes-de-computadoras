# Pendientes para dejar el `.pkt` conforme a la consigna

Revisión del archivo contra `TP4_3643_2026_Integrador_v3.pdf`.

## ✅ Lo que ya cumple
- 6 routers en el AS (Borde, Piso A, Piso B y los tres 3650 con `ip routing` / `ipv6 unicast-routing`), con redundancia en el núcleo.
- 3 switches 2960 de acceso, ISP fuera del OSPF (serial a Borde), DNS/NTP/FTP en la intranet y web server colgado del ISP.
- Dual stack: `172.16.0.0/16` (/24 y /30) y `2001:DB8:10::/48` (/64 y /127, link-local estáticas). Web server `198.51.100.30` / `2001:DB8:FFFF:100::30`, con registros A y AAAA para `segundoparcial.test`.
- Router on a stick en Piso A y Piso B, SVIs en 3650-Servidores y SSH v2 en los 2960.
- OSPFv2 y OSPFv3 en el área 0 (router-ids `1.1.1.1` a `6.6.6.6`) y ruta default en Borde con `default-information originate`.
- NC secundario solo con IP (`172.16.250.70`).

## ❌ Pendientes

### 1. DHCP en un 3650
- [ ] Configurar un pool DHCP (solo IPv4) en uno de los 3650, para una red directamente conectada, con al menos un host por DHCP.
- [ ] Evidencia: `show ip dhcp binding` en el 3650 + `ipconfig` en el host.
- [ ] (Opcional) Abrir el `excluded-address` de Router-PisoB, que hoy solo deja libres `.30` y `.40`.

### 2. Router ISP
- [ ] Quitar `username admin` → en el inventario del NC tiene que quedar **Wrong credential**.
- [ ] Reemplazar las rutas estáticas por default hacia Borde:
  ```
  no ip route 172.16.0.0 255.255.0.0 192.0.2.20
  ip route 0.0.0.0 0.0.0.0 192.0.2.20
  no ipv6 route 2001:DB8:10::/48 2001:DB8:FFFF::2
  ipv6 route ::/0 2001:DB8:FFFF::2
  ```
- [ ] Revisar `ip name-server` / `ntp server`, que apuntan a la intranet.

### 3. Switches 2960
- [ ] `username admin privilege 15 secret ...` en los 3 (hoy no tienen `privilege 15`).
- [ ] y/o cargar `class` como *enable password* en la credencial del NC (hoy está en `undefined`).

### 4. Network Controller Principal
- [ ] Corregir DNS → `172.16.250.20` y NTP → `172.16.250.30` (hoy tiene `.10` y `.20`).
- [ ] Borrar el inventario viejo (tiene IPs desactualizadas de los 2960 y del Secundario).
- [ ] Rehacer el discovery: los 9 equipos del AS en **Managed** y el ISP en **Wrong credential**.
- [ ] Push de DNS y NTP.

### 5. Place Notes
- [ ] Corregir las IPs de la nota:

  | Equipo | Dice la nota | Real |
  |---|---|---|
  | DNS | .10 | **.20** |
  | NTP | .20 | **.30** |
  | FTP | — | **.50** |
  | NC Principal | .30 | **.60** |
  | NC Secundario | .40 | **.70** |

- [ ] Agregar: dominio `segundoparcial.test`, redes IPv4/IPv6 con máscara/prefijo, interfaces de todos los routers (incluido Borde–ISP) y VLANs (`10 MGMT`, `20 SERVIDORES`, `30 USUARIOS-A`, `40 USUARIOS-B`).

## Verificación final
- [ ] Correr `scripts/script_inventario.py`: los 2960 tienen que salir **Reachable** y el ISP no tiene que estar gestionado.
