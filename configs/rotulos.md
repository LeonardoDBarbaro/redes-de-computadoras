# Rótulos (Place Notes) para la topología

Una nota por router. Se pegan al lado de cada equipo: herramienta **Place Note** (tecla **N**) → clic → pegar.
Todos los enlaces internos son **/30** en IPv4 y **/127** en IPv6 (`2001:DB8:10:50::/64` repartido en /127).

## Borde
```
BORDE (ISR4331) - LL FE80::1
Gi0/0/0 > Sw Piso A: 172.16.50.1/30 | 2001:DB8:10:50::/127
Gi0/0/1 > Sw Piso B: 172.16.50.5/30 | 2001:DB8:10:50::2/127
Se0/1/0 > ISP: 192.0.2.20/24 | 2001:DB8:FFFF::2/127
Default: 0.0.0.0/0 > 192.0.2.10 | ::/0 > 2001:DB8:FFFF::3
```

## ISP
```
ISP (ISR4331) - fuera del AS
Se0/1/0 > Borde: 192.0.2.10/24 | 2001:DB8:FFFF::3/127
Gi0/0/0 > Web: 198.51.100.1/24 | 2001:DB8:FFFF:100::1/64
Sin credencial CLI (Wrong credential en el NC)
```

## Switch Piso A
```
SWITCH PISO A (3650) - LL FE80::2
Gi1/0/1 > Borde: 172.16.50.2/30 | 2001:DB8:10:50::1/127
Gi1/0/2 > Sw Piso B: 172.16.50.9/30 | 2001:DB8:10:50::4/127
Gi1/0/3 > Servidores: 172.16.50.13/30 | 2001:DB8:10:50::6/127
Gi1/0/4 > Piso A: 172.16.50.21/30 | 2001:DB8:10:50::A/127
```

## Switch Piso B
```
SWITCH PISO B (3650) - LL FE80::3
Gi1/0/1 > Borde: 172.16.50.6/30 | 2001:DB8:10:50::3/127
Gi1/0/2 > Sw Piso A: 172.16.50.10/30 | 2001:DB8:10:50::5/127
Gi1/0/3 > Servidores: 172.16.50.17/30 | 2001:DB8:10:50::8/127
Gi1/0/4 > Piso B: 172.16.50.25/30 | 2001:DB8:10:50::C/127
```

## Servidores
```
SERVIDORES (3650) - LL FE80::4
Gi1/0/1 > Sw Piso B: 172.16.50.18/30 | 2001:DB8:10:50::9/127
Gi1/0/2 > Sw Piso A: 172.16.50.14/30 | 2001:DB8:10:50::7/127
Gi1/0/3 > Access Servidores (troncal)
Vlan10 MGMT: 172.16.10.254/24 | 2001:DB8:10:10::254/64
Vlan20 SERVIDORES: 172.16.250.254/24 | 2001:DB8:10:250::254/64
DHCP: pool VLAN20 (PC3)
```

## Piso A
```
PISO A (ISR4331) - LL FE80::5
Gi0/0/0 > Sw Piso A: 172.16.50.22/30 | 2001:DB8:10:50::B/127
Gi0/0/1.10 VLAN 10 MGMT: 172.16.11.254/24 | 2001:DB8:10:11::254/64
Gi0/0/1.30 VLAN 30 USUARIOS-A: 172.16.100.254/24 | 2001:DB8:10:100::254/64
```

## Piso B
```
PISO B (ISR4331) - LL FE80::6
Gi0/0/0 > Sw Piso B: 172.16.50.26/30 | 2001:DB8:10:50::D/127
Gi0/0/1.10 VLAN 10 MGMT: 172.16.12.254/24 | 2001:DB8:10:12::254/64
Gi0/0/1.40 VLAN 40 USUARIOS-B: 172.16.200.254/24 | 2001:DB8:10:200::254/64
DHCP: pool POOL-PISO-B
```
