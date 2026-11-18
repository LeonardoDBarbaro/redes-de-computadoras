# Pendientes para dejar el `.pkt` conforme a la consigna

Revisión del archivo contra `TP4_3643_2026_Integrador_v3.pdf`, con la solución de cada punto.

> Credencial del NC y de los equipos: `admin` / `cisco` · enable secret: `class`.
> Después de cada bloque: `end` → `write memory` en cada equipo y **Fast Forward Time**.

## ✅ Lo que ya cumple
- 6 routers en el AS (Borde, Piso A, Piso B y los tres 3650 con `ip routing` / `ipv6 unicast-routing`), con redundancia en el núcleo.
- 3 switches 2960 de acceso, ISP fuera del OSPF (serial a Borde), DNS/NTP/FTP en la intranet y web server colgado del ISP.
- Dual stack: `172.16.0.0/16` (/24 y /30) y `2001:DB8:10::/48` (/64 y /127, link-local estáticas). Web server `198.51.100.30` / `2001:DB8:FFFF:100::30`, con registros A y AAAA para `segundoparcial.test`.
- Router on a stick en Piso A y Piso B, SVIs en 3650-Servidores y SSH v2 en los 2960.
- OSPFv2 y OSPFv3 en el área 0 (router-ids `1.1.1.1` a `6.6.6.6`) y ruta default en Borde con `default-information originate`.
- NC secundario solo con IP (`172.16.250.70`).

---

## 1. DHCP en un 3650

**Problema:** solo Router-PisoB (4331) tiene DHCP; falta uno en un 3650.

**Solución:** usar **3650-Servidores**, que ya tiene la SVI de la VLAN 20 (`172.16.250.254/24`), y sumar una PC cliente en esa VLAN.

```
! 3650-Servidores
enable
configure terminal
ip dhcp excluded-address 172.16.250.1 172.16.250.99
ip dhcp excluded-address 172.16.250.254
ip dhcp pool VLAN20
 network 172.16.250.0 255.255.255.0
 default-router 172.16.250.254
 dns-server 172.16.250.20
 domain-name segundoparcial.test
end
write memory
```

Después:
1. Agregar una PC (ej. `PC-DHCP`) a un puerto libre de **2960-Servidores** y ponerle ese puerto en la VLAN 20:
   ```
   ! 2960-Servidores (cambiar Fa0/X por el puerto usado)
   configure terminal
   interface FastEthernet0/X
    switchport mode access
    switchport access vlan 20
    no shutdown
   end
   write memory
   ```
2. En la PC: *Desktop → IP Configuration → DHCP*. Tiene que recibir una IP `172.16.250.100` o mayor.

**Evidencia:** `show ip dhcp binding` en el 3650 + `ipconfig /all` en la PC.

(Opcional) Abrir el rango de Router-PisoB, que hoy solo deja libres `.30` y `.40`: `show running-config | include excluded` → `no ip dhcp excluded-address ...` → excluir solo `.1`–`.9` y `.254`.

## 2. Router ISP

**Problema:** tiene la credencial del AS (queda *Managed*) y usa rutas a la intranet en vez de default.

```
! ISP
enable
configure terminal
no username admin
no ip route 172.16.0.0 255.255.0.0 192.0.2.20
ip route 0.0.0.0 0.0.0.0 192.0.2.20
no ipv6 route 2001:DB8:10::/48 2001:DB8:FFFF::2
ipv6 route ::/0 2001:DB8:FFFF::2
no ip name-server 172.16.250.20
no ip domain-name SegundoParcial.test
no ntp server 172.16.250.30
end
write memory
```

> Si `ip domain-name` se usó para la llave RSA, sacarlo no rompe nada: el ISP no tiene que ser administrado por SSH.

**Verificación:** `show ip route` (tiene que aparecer `S* 0.0.0.0/0 [1/0] via 192.0.2.20`), `show ipv6 route`, y ping desde una PC al web server.

## 3. Switches 2960 (los tres)

**Problema:** `username admin` no tiene `privilege 15`, así que el NC no puede entrar a modo privilegiado.

```
! 2960-PisoA, 2960-PisoB y 2960-Servidores
enable
configure terminal
username admin privilege 15 secret cisco
end
write memory
```

Además, en el NC: **Provisioning → Credentials → CLI** → editar `SSH-admin` y cargar **Enable Password: `class`**.

**Verificación:** desde un router, `ssh -l admin 172.16.11.10`: tiene que entrar directo con el prompt `#`.

## 4. Network Controller Principal

**Problema:** DNS y NTP mal cargados, y un inventario viejo con IPs desactualizadas.

1. **Provisioning → Network Settings**:
   - DNS Server: `172.16.250.20`
   - NTP Server: `172.16.250.30`
   - **Save**
2. **Provisioning → Inventory**: borrar todos los dispositivos (ícono de engranaje → *Delete*).
3. **Provisioning → Discovery**: editar `Discovery-general` (CDP, semilla `172.16.50.5` o la IP de Borde, credencial `SSH-admin`) → **Apply** y esperar a que termine (Fast Forward).
4. Controlar en **Inventory**:
   - 9 equipos del AS (Borde, Piso A, Piso B, tres 3650, tres 2960) en **Managed**
   - ISP en **Wrong credential**
5. **Provisioning → Network Settings → Push** de DNS y NTP a todos los dispositivos.
6. Verificar en un equipo: `show running-config | include name-server|ntp` y `show clock`.

> Si un 2960 queda *Unreachable*, revisar desde el 3650 o el router que haya ping a su SVI de gestión (`172.16.11.10`, `172.16.12.20`, `172.16.10.30`) y que el usuario tenga `privilege 15` (punto 3).

## 5. Place Notes

**Problema:** las IPs de la nota están cruzadas y faltan rótulos obligatorios.

**Solución:** editar la nota existente (doble clic) y reemplazar el texto. Para sacar las IPs reales de cada router: `show ip interface brief` y `show ipv6 interface brief`.

Plantilla (completar los `?` con lo que muestran los comandos):

```
DOMINIO WEB: segundoparcial.test

SERVIDORES (VLAN 20 – 172.16.250.0/24 – 2001:DB8:10:250::/64)
  DNS          172.16.250.20   2001:DB8:10:250::20
  NTP          172.16.250.30   2001:DB8:10:250::30
  FTP          172.16.250.50   2001:DB8:10:250::50
  NC Principal 172.16.250.60   2001:DB8:10:250::60
  NC Secundario 172.16.250.70  2001:DB8:10:250::70
  Gateway      172.16.250.254

WEB SERVER (detrás del ISP)  198.51.100.30/24   2001:DB8:FFFF:100::30/64

VLANs
  10 MGMT        Piso A 172.16.11.0/24 · Piso B 172.16.12.0/24 · Servidores 172.16.10.0/24
  20 SERVIDORES  172.16.250.0/24
  30 USUARIOS-A  172.16.100.0/24  (GW .254)
  40 USUARIOS-B  172.16.200.0/24  (GW .254)

ENLACE BORDE – ISP (serial)
  Borde Se0/1/0  192.0.2.20/24   2001:DB8:FFFF::2
  ISP   Se0/1/0  192.0.2.10/24   2001:DB8:FFFF::1

ENLACES INTERNOS (/30 – /127)
  Borde ? – 3650-EdificioA ?   172.16.50.?/30   2001:DB8:10:50::?/127
  ...
```

> ⚠️ Verificar con `show ip interface brief` los prefijos IPv6 de servidores y VLANs antes de pegarlos: los de la plantilla siguen el esquema `2001:DB8:10::/48` pero pueden variar.

Alternativa más prolija: una nota chica al lado de cada router con sus interfaces, y una nota general con servidores, VLANs y dominio.

---

## Verificación final
- [ ] Ping y `tracert` de PC0 / PC2 al web server (IPv4 e IPv6) y `ping segundoparcial.test`.
- [ ] `show ip ospf neighbor` y `show ipv6 ospf neighbor` en Borde.
- [ ] Correr `scripts/script_inventario.py`: los 2960 tienen que salir **Reachable** y el ISP no tiene que figurar como gestionado.
- [ ] Guardar el `.pkt` y reemplazar `pkt/TP-Integrador-Grupo11.pkt` en el repo.
