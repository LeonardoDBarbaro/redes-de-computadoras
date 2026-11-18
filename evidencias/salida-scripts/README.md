# Salidas de los scripts

Ejecutados el 18/11/2026 contra el `.pkt` final (`pkt/TP-Integrador-Grupo11.pkt`), desde Windows (`localhost:58000`), con el usuario del NC del grupo (`admin` / `cisco`).

| Script | Resultado |
|---|---|
| `01_get-ticket.py` | ✅ [`01_get-ticket.txt`](01_get-ticket.txt) |
| `02_get-network-device.py` | ❌ `KeyError: 'hostname'` (ver nota) |
| `03_get-host.py` | ✅ [`03_get-host.txt`](03_get-host.txt) |
| `04_tabulate.py` | ❌ `KeyError: 'hostname'` (ver nota) |
| `05_inventario-csv.py` (propio) | ✅ [`05_inventario-csv.txt`](05_inventario-csv.txt) + [`inventario_red.csv`](inventario_red.csv) |

**Nota:** `02` y `04` (de la cátedra) leen `item["hostname"]` directamente. El NC secundario (`172.16.250.70`) aparece en el inventario como *Unsupported* y sin hostname, así que esos scripts cortan con `KeyError`. El script propio usa `dev.get("hostname", "N/A")` y no tiene ese problema.
