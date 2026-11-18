# Network Controller

## Configuración
1. **User setup**: usuario `admin`.
2. **Credencial CLI** `SSH-admin` (admin).
3. **Discovery** `Discovery-general`: tipo CDP, IP semilla `172.16.50.1` (Borde), CDP level 16, timeout 5, retry 3.

| | |
|---|---|
| ![](capturas/network-controller/02-nueva-credencial.png) | ![](capturas/network-controller/03-discovery.png) |

## Inventario
Todos los equipos en **Managed**:

| Hostname | Tipo | IP de gestión |
|---|---|---|
| Borde | Router | 192.0.2.2 |
| ISP | Router | 192.0.2.1 |
| Router-PisoA | Router | 172.16.100.254 |
| Router-PisoB | Router | 172.16.200.254 |
| 3650-EdificioA | MultiLayerSwitch | 172.16.50.21 |
| 3650-EdificioB | MultiLayerSwitch | 172.16.50.25 |
| 3650-Servidores | MultiLayerSwitch | 172.16.50.18 |
| 2960-PisoA | Switch | 172.16.100.1 |
| 2960-PisoB | Switch | 172.16.200.1 |
| 2960-Servidores | Switch | 172.16.10.1 |
| *(server)* | — | 172.16.250.40 → *Unsupported* |

![](capturas/network-controller/04-inventario.png)

## Topología
![](capturas/network-controller/06-topologia.png)

## Path trace: PC1 → Web server
`172.16.100.10` → Router-PisoA → 3650-EdificioA → Borde (Se0/1/0) → ISP → Web server `198.51.100.30`. Estado: **COMPLETED**.

Los 2960 aparecen como *UNKNOWN* en el path trace porque el trazado es de capa 3 y los 2960 trabajan en capa 2.

![](capturas/network-controller/07-path-trace-pc1-webserver.png)
