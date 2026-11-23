# Pendientes para dejar el `.pkt` conforme a la consigna

Revisión contra la consigna **`TP4_3643_2026_Integrador_v4.pdf`**, con la solución de cada punto. Los puntos 1 a 5 son del `.pkt`; los 6 a 8, del repo, el informe y la entrega.

> Credencial del NC y de los equipos: `admin` / `cisco` · enable secret: `class`.
> Los bloques de CLI de los puntos 1–3 están también como archivos listos para pegar en [`configs/`](configs/).
> Después de cada bloque: `end` → `write memory` en cada equipo y **Fast Forward Time**.

## 🔁 Reentrega R1 — plazo miércoles 25/11

Correcciones de la cátedra sobre la primera entrega, y cómo se resuelven.

| # | Corrección | Estado | Qué hacer |
|---|---|---|---|
| 1 | **ISP administrado por el NC** | ✅ Resuelto en el `.pkt` del repo | Sin `username admin`, Discovery repetido y ISP en **Wrong credential**. Para el informe: captura del inventario (9 del AS en Managed + ISP en Wrong credential), del bloque de [`configs/ISP.txt`](configs/ISP.txt) y explicar por qué `no cdp run` no alcanzaba. |
| 2 | **Faltan conclusiones** | ❌ Informe | Sección con problemas reales (síntoma, causa, solución). |
| 3 | **Dos DHCP para 172.16.200.0/24** (3650 Switch Piso B y 4331 Piso B) | ✅ `.pkt` / ❌ informe | En el `.pkt` del repo, `show ip dhcp pool` en 3650-EdificioB **no muestra ningún pool** (verificado el 22/11). El DHCP del 3650 está en **3650-Servidores** (VLAN 20, PC3), y el del 4331 en Router Piso B (VLAN 40): redes distintas. **En el informe:** sacar cualquier mención o captura de un pool en el Switch Piso B y mostrar el de 3650-Servidores. Si hiciera falta, [`configs/3650-EdificioB_sacar-dhcp.txt`](configs/3650-EdificioB_sacar-dhcp.txt). |
| 4 | **Conectividad solo desde PC1** | ⚠️ IPv6 a Internet arreglado (PC0 → web server responde). Faltan capturas + informe | Tabla de pings entre todas las redes y a los servidores, en IPv4 e IPv6 (ver plantilla abajo). |
| 5 | **Postman sin contrastar con la doc de Cisco** | ❌ Informe | Por cada endpoint: qué hace, qué dice la doc de Cisco y epígrafe explicativo. |
| 6 | **Carátula** incompleta | ❌ Informe | Los 6 integrantes de MIeL y el número de grupo (11). Archivo: `TP4_3643_Grupo11_R1.pdf`. |
| 7 | **Un solo rótulo** en la topología | ✅ `.pkt` | Una nota por router con sus interfaces IPv4/IPv6 (ver [`configs/rotulos.md`](configs/rotulos.md)) y la nota general corregida. Captura: [`capturas/topologia-con-rotulos.webp`](capturas/topologia-con-rotulos.webp). |

**Entrega:** `TP4_3643_Grupo11_R1.zip` con `TP4_3643_Grupo11_R1.pdf` + el `.pkt` (link de GitHub en el informe).

### Plantilla de tabla de conectividad (punto 4)

| Origen → Destino | IPv4 | IPv6 |
|---|---|---|
| PC0 (Piso A) → PC2 (Piso B) | | |
| PC0 (Piso A) → PC3 (Servidores) | | |
| PC2 (Piso B) → PC3 (Servidores) | | |
| PC0 → DNS / NTP / FTP | | |
| PC2 → DNS / NTP / FTP | | |
| PC0 → Web server (198.51.100.30) | | |
| PC2 → Web server | | |
| PC3 → Web server | | |
| PC0 → `segundoparcial.test` | | |

### Ideas para conclusiones (punto 2)
- **ISP administrado por el NC.** Síntoma: aparecía Managed. Causa: tenía la misma credencial CLI que el AS; `no cdp run` solo lo ocultaba de CDP. Solución: `no username admin` y nuevo Discovery → Wrong credential.
- **2960 sin gestión.** Síntoma: Unreachable/no Managed. Causa: faltaba la IP en la VLAN de administración y `privilege 15` en el usuario. Solución: SVI de gestión + default-gateway + `username admin privilege 15`.
- **Vecinos OSPF.** Síntoma: tablas de ruteo incompletas. Causa: redes no publicadas/vecinos no formados. Solución: revisar `network` y `show ip ospf neighbor` equipo por equipo.
- **API del NC no respondía.** Síntoma: Postman sin conexión y `REST_API_NO_EXTERNAL_ACCESS`. Causa: acceso externo deshabilitado. Solución: *Preferences → Misc* y *Access Enable* en el NC.
- **IPv6 entre Borde e ISP.** Síntoma: sin respuesta IPv6 hacia el web server; la ruta default IPv6 no se instalaba. Causa: Borde `2001:DB8:FFFF::2/127` e ISP `::1/127` quedaban en subredes /127 distintas, y el Borde no tenía ruta default IPv6. Solución: ISP a `::3/127` (misma subred que `::2`), `ipv6 route ::/0 2001:DB8:FFFF::3` en el Borde y `::/0` por la serial en el ISP. Se probó usar `::0` en el Borde, pero Packet Tracer no respondió (es la dirección anycast de la subred).
- **Scripts 02 y 04 de la cátedra.** Síntoma: `KeyError: 'hostname'`. Causa: equipos sin hostname en el inventario (ISP en Wrong credential). Solución: el script propio usa `.get()`.
- **DHCP duplicado.** Dos pools para la misma LAN (172.16.200.0/24); se dejó solo el del 4331 (Router Piso B) y el del 3650 se configuró en 3650-Servidores para la VLAN 20, con PC3 como cliente.

---

## 📌 Estado al 22/11/2026

| Punto | Estado |
|---|---|
| 1 · DHCP en un 3650 | ✅ Pool `VLAN20` en 3650-Servidores. **PC3** (Access Servidores Fa0/3, VLAN 20) recibió `172.16.250.100` por DHCP. IPv6 por SLAAC (`2001:DB8:10:250::/64`). |
| 2 · ISP | ✅ Sin `username admin`, rutas default IPv4 e IPv6 hacia Borde. En el NC figura **Wrong credential**. Enlace IPv6 Borde–ISP corregido (`::2/127` – `::3/127`): PC0 llega al web server por IPv6. |
| 3 · Switches 2960 | ✅ Los tres en **Managed**. |
| 4 · Network Controller | ✅ 9 equipos del AS en Managed, ISP en Wrong credential, inventario sin entradas viejas. NC secundario sacado del `.pkt` (se agrega para la oral: `172.16.250.70/24`, GW `.254`). |
| 5 · Place Notes | ✅ Nota general corregida y una nota por router con sus interfaces IPv4/IPv6 ([`configs/rotulos.md`](configs/rotulos.md)). |
| 6 · Repo GitHub | ✅ Scripts de la cátedra + propio, README y evidencias. |
| 7 · Postman | ⚠️ Confirmar que los endpoints no repiten los del TP3. |
| 8 · Informe y entrega | ❌ Pendiente. |

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
ipv6 route ::/0 Serial0/1/0
interface Serial0/1/0
 no ipv6 address 2001:DB8:FFFF::1/127
 ipv6 address 2001:DB8:FFFF::3/127
 exit
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

Además, en el NC: **Provisioning → Credentials → CLI** → editar `SSH-admin` y cargar **Enable Password: `class`**. ✅ *Hecho por la API (`PUT /global-credential/cli`); guardar el `.pkt` para que quede.*

**Verificación:** desde un router, `ssh -l admin 172.16.11.10`: tiene que entrar directo con el prompt `#`.

## 4. Network Controller Principal

**Problema:** DNS y NTP mal cargados, y un inventario viejo con IPs desactualizadas.

1. **Provisioning → Network Settings**:
   - DNS Server: `172.16.250.20`
   - NTP Server: `172.16.250.30`
   - **Save**
2. **Provisioning → Inventory**: borrar los dispositivos con IP vieja. ✅ *Hecho por la API: se borraron el `172.16.250.40` sin hostname y los 2960 con `.10.1`, `.100.1` y `.200.1`, y se descubrieron los 2960 en sus IPs actuales (`172.16.10.30`, `.11.10`, `.12.20`). Siguen **Unreachable** hasta aplicar el punto 3 en los 2960.*
3. **Provisioning → Discovery**: editar `Discovery-general` (CDP, semilla `172.16.50.5` o la IP de Borde, credencial `SSH-admin`) → **Apply** y esperar a que termine (Fast Forward).
4. Controlar en **Inventory**:
   - 9 equipos del AS (Borde, Piso A, Piso B, tres 3650, tres 2960) en **Managed**
   - ISP en **Wrong credential**
5. **Provisioning → Network Settings → Push** de DNS y NTP a todos los dispositivos.
6. Verificar en un equipo: `show running-config | include name-server|ntp` y `show clock`.

> Si un 2960 queda *Unreachable*, revisar desde el 3650 o el router que haya ping a su SVI de gestión (`172.16.11.10`, `172.16.12.20`, `172.16.10.30`) y que el usuario tenga `privilege 15` (punto 3).

## 5. Place Notes

**Problema:** las IPs de la nota están cruzadas y faltan rótulos obligatorios. La consigna (pág. 8) pide como mínimo: IPv4/IPv6 de cada red y de las interfaces de los routers (incluido el enlace con el ISP), número y nombre de cada VLAN, IPs de los servidores y del NC, dominio del HTTP y **las credenciales** (SSH, enable y NC).

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

CREDENCIALES
  SSH (routers, 3650 y 2960): admin / cisco
  Enable secret: class
  Network Controller: admin / cisco

WEB SERVER (detrás del ISP)  198.51.100.30/24   2001:DB8:FFFF:100::30/64

VLANs
  10 MGMT        Piso A 172.16.11.0/24 · Piso B 172.16.12.0/24 · Servidores 172.16.10.0/24
  20 SERVIDORES  172.16.250.0/24
  30 USUARIOS-A  172.16.100.0/24  (GW .254)
  40 USUARIOS-B  172.16.200.0/24  (GW .254)

ENLACE BORDE – ISP (serial)
  Borde Se0/1/0  192.0.2.20/24   2001:DB8:FFFF::2/127
  ISP   Se0/1/0  192.0.2.10/24   2001:DB8:FFFF::3/127

ENLACES INTERNOS (/30 – /127)
  Borde ? – 3650-EdificioA ?   172.16.50.?/30   2001:DB8:10:50::?/127
  ...
```

> ⚠️ Verificar con `show ip interface brief` los prefijos IPv6 de servidores y VLANs antes de pegarlos: los de la plantilla siguen el esquema `2001:DB8:10::/48` pero pueden variar.

Alternativa más prolija: una nota chica al lado de cada router con sus interfaces, y una nota general con servidores, VLANs y dominio.

---

## 6. Repositorio de GitHub (actividad 4) — ✅ resuelto
- [x] Contiene los **scripts suministrados** por la cátedra (`src/01` a `src/04`, traídos con su historial) y el **script propio** (`src/05_inventario-csv.py`).
- [x] README que explica qué hace cada script.
- [x] `requirements.txt` y `.gitignore` de la cátedra (excluyen `venv/`, `cisco/`, `.env`).
- [x] Repositorio público.
- [ ] Ejecutar los 4 scripts suministrados. ⚠️ `02` y `04` fallan con `KeyError: 'hostname'` mientras haya en el inventario un equipo sin hostname (los 2960 todavía Unreachable): correrlos después de que todo quede Managed.
- [ ] Ejecutar los 4 scripts suministrados y el propio, y sacar captura de la salida para el informe. Los de la cátedra usan `cisco` / `cisco123!`: crear ese usuario en el NC o cambiarlo en `01` y `04`. En `02` y `03` hay que pegar el ticket que da el `01`.
- [ ] Hacer el último commit **antes de la fecha de entrega**.

## 7. Postman (actividad 3)
- [ ] Los 4 endpoints (POST, GET, PUT, DELETE) tienen que ser **distintos de los que usaron en el TP3**. Los actuales son `POST /ticket`, `GET` y `PUT /global-credential/cli`, y `POST` y `DELETE /flow-analysis`: confirmar contra lo entregado en el TP3.
- [ ] Por cada endpoint, en el informe: método, URL, headers, body, respuesta con código de estado, y **la parte de la documentación de Cisco** (*Northbound API for Network Controller Device*) con la que se contrasta.
- [ ] (Opcional) Exportar la colección de Postman a `.json` y sumarla al `.zip`.

## 8. Entrega (MIEL)
- [ ] Un único `TP4_3643_Grupo11.zip` con:
  - `TP4_3643_Grupo11.pdf` (informe)
  - `TP4_3643_Grupo11.pkt`, guardado **al final**, con el NC completo: usuario creado, credenciales, Discovery con todo en Managed, y NTP y DNS enviados.
- [ ] Los scripts **no** van en el zip: va el link al repo en el informe (apartado de la actividad 4).
- [ ] Plazo: 15 días corridos desde la 2° clase de práctica.
- [ ] NC secundario: la consigna lo pide **solo para la presentación oral** (solo IP, máscara y gateway). Ya está en el `.pkt` con `172.16.250.70`: dejarlo así y ponerlo en un rótulo.

### Estructura del informe
1. Carátula: universidad, asignatura (3643), TP N° 4, comisión, Grupo 11, apellido y nombre de cada integrante, fecha.
2. Índice.
3. Diseño: captura de la topología con rótulos visibles, tablas IPv4 e IPv6 (con el enlace al ISP), tabla de VLANs y justificación de las subredes.
4. Desarrollo: un apartado por actividad, con las evidencias de abajo.
5. Conclusiones: problemas y cómo se resolvieron (ej.: vecinos OSPF, acceso externo del NC deshabilitado, 2960 sin `privilege 15`, ISP descubierto por el NC).

### Evidencias mínimas
- [ ] **Conectividad:** tabla de pings entre hosts de distintas redes y al HTTP, en IPv4 e IPv6; `tracert` de un host al HTTP en IPv4 e IPv6.
- [ ] **DHCP:** `show ip dhcp binding` en el 3650 **y** en el 4331, e `ipconfig` de un host de cada uno.
- [ ] **VLANs:** `show vlan brief` y `show interfaces trunk` en los 2960; `show ip interface brief` en el 4331 con subinterfaces.
- [ ] **Ruteo:** `show ip protocols`, `show ipv6 protocols`, `show ip route` y `show ipv6 route` en **cada** router del AS (señalando la default), y `show running-config | section ospf` en cada uno.
- [ ] **NC:** credenciales, Discovery, lista en Managed, topología en Assurance; en cada 2960, `show ip interface brief` (VLAN de administración up/up) y `show running-config | include default-gateway`; `show running-config | include ntp` en al menos dos equipos, y `show clock`.
- [ ] **API y scripts:** las 4 peticiones de Postman y la salida de los scripts (ver 6 y 7).
- [ ] Cada captura con el prompt visible, recortada (usar `section` / `include`), con número de figura, epígrafe y 2–3 líneas de explicación.

## Verificación final
- [ ] Ping y `tracert` de PC0 / PC2 al web server (IPv4 e IPv6) y `ping segundoparcial.test`.
- [ ] `show ip ospf neighbor` y `show ipv6 ospf neighbor` en Borde.
- [ ] Correr `src/05_inventario-csv.py`: los 2960 tienen que salir **Reachable** y el ISP no tiene que figurar como gestionado.
- [ ] Guardar el `.pkt` y reemplazar `pkt/TP-Integrador-Grupo11.pkt` en el repo (en el zip va como `TP4_3643_Grupo11.pkt`).
