# Salidas de los scripts

Ejecutados el 22/11/2026 contra el `.pkt` final (`pkt/TP-Integrador-Grupo11.pkt`), desde Windows (`localhost:58000`), con el usuario del NC del grupo (`admin` / `cisco`).

| Script | Resultado |
|---|---|
| `01_get-ticket.py` | ✅ [`01_get-ticket.txt`](01_get-ticket.txt) |
| `02_get-network-device.py` | ❌ `KeyError: 'hostname'` (ver nota) |
| `03_get-host.py` | ✅ [`03_get-host.txt`](03_get-host.txt) |
| `04_tabulate.py` | ❌ `KeyError: 'hostname'` (ver nota) |
| `05_inventario-csv.py` (propio) | ✅ [`05_inventario-csv.txt`](05_inventario-csv.txt) + [`inventario_red.csv`](inventario_red.csv) |

**Nota:** `02` y `04` (de la cátedra) leen `item["hostname"]` directamente. Cualquier equipo del inventario **sin hostname** los hace cortar con `KeyError`. Con la topología correcta eso pasa siempre, porque la consigna exige que el **ISP** quede en *Wrong credential*: el NC no puede entrar y no conoce su hostname. El NC secundario se sacó del `.pkt` de la entrega (la consigna lo pide solo para la oral).

El script propio (`05`) usa `dev.get("hostname", "N/A")` y lista todo el inventario sin errores, incluido el ISP. Es una de las mejoras que le agrega a los suministrados.
