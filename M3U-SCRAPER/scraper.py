import os
import re
import requests

def obtener_codigo_del_dia():
    print("Buscando el código dinámico directamente en admincode.php...")
    # La URL del archivo JS que descubriste en tu captura image_880ddf.jpg
    url_js = "https://tecnotv.club/admincode.php"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://spinoff.link/"
    }
    
    try:
        # Traemos el archivo JavaScript pelado
        response = requests.get(url_js, headers=headers, timeout=20)
        
        if response.status_code == 200:
            texto_codigo = response.text
            
            # Usamos una expresión regular para buscar: window.CARPETA = "cualquier_cosa";
            match = re.search(r'window\.CARPETA\s*=\s*"([^"]+)"', texto_codigo)
            
            if match:
                codigo_detectado = match.group(1).strip()
                print(f"¡Éxito! Código detectado para hoy: {codigo_detectado}")
                return codigo_detectado
            else:
                print("No se encontró la variable window.CARPETA dentro del archivo.")
        else:
            print(f"No se pudo acceder al archivo JS (Código HTTP: {response.status_code})")
            
    except Exception as e:
        print(f"Ocurrió un error al conectar con el servidor de códigos: {e}")
        
    return None

def descargar_lista(url, nombre_archivo):
    print(f"Descargando desde: {url}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            os.makedirs("listas", exist_ok=True)
            path_destino = f"listas/{nombre_archivo}"
            with open(path_destino, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"✓ Guardado con éxito en: {path_destino}")
            return True
        else:
            print(f"❌ Error al descargar la lista (Código HTTP: {response.status_code})")
    except Exception as e:
        print(f"Ocurrió un error durante la descarga: {e}")
    return False

# --- PROCESO PRINCIPAL ---
if __name__ == "__main__":
    # 1. Obtenemos la parte variable gracias a tu investigación
    codigo_dia = obtener_codigo_del_dia()
    
    if codigo_dia:
        # 2. Armamos las listas por partes tal cual sugeriste
        url_principal = f"https://tecnotv.club/{codigo_dia}/lista.m3u"
        url_deportes = f"https://tecnotv.club/{codigo_dia}/deportes.m3u"
        
        print(f"--> URL Principal armada: {url_principal}")
        print(f"--> URL Deportes armada: {url_deportes}")
        
        # 3. Descargamos los archivos finales
        descargar_lista(url_principal, "principal.m3u")
        descargar_lista(url_deportes, "deportes.m3u")
    else:
        print("No se pudo armar ninguna lista porque falló la extracción del código.")
