import os
from PIL import Image
import sys
from datetime import datetime
from moviepy.editor import VideoFileClip

def optimizar_imagenes():
    # Configuración
    config = {
        'calidad_webp': 70,               # 65-80
        'ancho_maximo': 1200,             # Redimensionar si es más ancha, no que sus 3000px :u
        'carpeta_salida': "optimized",
        'mantener_transparencia': True,    # Conservar canales alpha (PNG)
        'sobrescritura': False
    }

    stats = {
        'total': 0,
        'optimizadas': 0,
        'espacio_ahorrado': 0,
        'inicio': datetime.now()
    }

    ruta_actual = os.getcwd()
    carpeta_salida = os.path.join(ruta_actual, config['carpeta_salida'])
    os.makedirs(carpeta_salida, exist_ok=True)

    print(f"\n🔍 Procesando imágenes en: {ruta_actual}")
    print(f"⚙️ Config: WebP q{config['calidad_webp']}, Max {config['ancho_maximo']}px, Transparencia={'ON' if config['mantener_transparencia'] else 'OFF'}\n")

    for archivo in os.listdir(ruta_actual):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            stats['total'] += 1
            entrada = os.path.join(ruta_actual, archivo)
            nombre_base = os.path.splitext(archivo)[0]
            salida = os.path.join(carpeta_salida, f"{nombre_base}.webp")

            if not config['sobrescritura'] and os.path.exists(salida):
                print(f"⏭️  Saltada: {archivo}")
                continue

            try:
                with Image.open(entrada) as img:
                    if img.mode == 'RGBA' and config['mantener_transparencia']:
                        img = img.convert('RGBA')
                        params = {'lossless': False, 'method': 6, 'quality': config['calidad_webp']}
                    else:
                        img = img.convert('RGB')
                        params = {'method': 6, 'quality': config['calidad_webp']}

                    if img.width > config['ancho_maximo']:
                        ratio = config['ancho_maximo'] / img.width
                        nuevo_alto = int(img.height * ratio)
                        img = img.resize((config['ancho_maximo'], nuevo_alto), Image.LANCZOS)

                    img.save(salida, "WEBP", **params)

                    tam_original = os.path.getsize(entrada)
                    tam_optimizado = os.path.getsize(salida)
                    stats['espacio_ahorrado'] += (tam_original - tam_optimizado)
                    stats['optimizadas'] += 1

                    print(f"~ {archivo} | {tam_original/1024:.1f}KB → {tam_optimizado/1024:.1f}KB | -{(1-tam_optimizado/tam_original)*100:.1f}%")

            except Exception as e:
                print(f"X Error en {archivo}: {str(e)}")

    # Reporte final
    tiempo = (datetime.now() - stats['inicio']).total_seconds()
    print(f"\n🎉 Finalizado en {tiempo:.1f}s")
    print(f"📊 Imágenes: {stats['total']} | Procesadas: {stats['optimizadas']}")
    if stats['total'] > 0:
        print(f"💾 Ahorro total: {stats['espacio_ahorrado']/1024/1024:.2f}MB")

    input("\nPresiona Enter para salir...")

def convertir_gif_a_webm(ruta_gif, ruta_webm):
    try:
        clip = VideoFileClip(ruta_gif)
        clip.write_videofile(ruta_webm, codec='libvpx', audio=False)
        print(f"✅ Convertido: {os.path.basename(ruta_gif)} → {os.path.basename(ruta_webm)}")
    except Exception as e:
        print(f"X Error al convertir {ruta_gif}: {str(e)}")

if __name__ == "__main__":
    optimizar_imagenes()