import requests

class IndicadoresEconomicos:
    def __init__(self):
        self.base_url = "https://mindicador.cl/api"

    def obtener_indicador(self, indicador: str, fecha: str = None):
        try:
            indicador = indicador.strip().lower()
            url = f"{self.base_url}/{indicador}/{fecha}" if fecha else f"{self.base_url}/{indicador}"

            resp = requests.get(url, timeout=10)
            resp.raise_for_status()

            data = resp.json()
            serie = data.get("serie", [])
            if not serie:
                return None

            return serie[0].get("valor")
        except Exception as e:
            print("Error al consumir la API:", e)
            return None
