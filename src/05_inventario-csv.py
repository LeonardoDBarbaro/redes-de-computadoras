#!/usr/bin/env python3
import requests
import json
import csv
import datetime
from tabulate import tabulate
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NC_IP = "localhost:58000"
URL_BASE = f"http://{NC_IP}"

url_ticket = f"{URL_BASE}/api/v1/ticket"
payload_ticket = {
    "username": "admin",
    "password": "cisco"
}
headers_ticket = {
    "Content-Type": "application/json"
}

print("[*] Solicitando ticket de autenticación al Network Controller...")
response_ticket = requests.post(url_ticket, json=payload_ticket, headers=headers_ticket, verify=False)
data_ticket = response_ticket.json()

token = data_ticket["response"]["serviceTicket"]
print(f"[+] Token obtenido con éxito: {token}")

url_devices = f"{URL_BASE}/api/v1/network-device"
headers_devices = {
    "X-Auth-Token": token,
    "Content-Type": "application/json"
}

print("[*] Consultando dispositivos descubiertos en /api/v1/network-device...")
response_devices = requests.get(url_devices, headers=headers_devices, verify=False)
devices_data = response_devices.json()["response"]

# NUEVO DESDE ACÁ

print("\n" + "=" * 85)
print(f"  INVENTARIO DE RED - GENERADO EL {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 85)

archivo_csv = "inventario_red.csv"
headers_tabla = ["Hostname", "IP Gestión", "Familia / Tipo", "Plataforma", "Versión Soft", "Estado"]
filas_inventario = []

for dev in devices_data:
    hostname = dev.get("hostname", "N/A")
    mgmt_ip = dev.get("managementIpAddress", "N/A")
    family = dev.get("family", dev.get("type", "N/A"))
    platform = dev.get("platformId", "N/A")
    version = dev.get("softwareVersion", "N/A")
    status = dev.get("reachabilityStatus", "N/A")
    
    filas_inventario.append([hostname, mgmt_ip, family, platform, version, status])

print(tabulate(filas_inventario, headers=headers_tabla, tablefmt="grid"))

try:
    with open(archivo_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers_tabla)
        writer.writerows(filas_inventario)
    print(f"\n[✔] ÉXITO: Inventario exportado correctamente a '{archivo_csv}'.")
except Exception as e:
    print(f"\n[-] ERROR al guardar el archivo CSV: {e}")
