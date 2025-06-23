import os
import json

# Ruta a tu carpeta de imágenes (debe estar en la misma carpeta que este script)
IMAGES_FOLDER = 'imagenes'

def generate_gallery_data():
    image_files = []
    # Obtenemos todos los archivos .png de la carpeta de imágenes
    for filename in os.listdir(IMAGES_FOLDER):
        if filename.endswith('.png') and filename.startswith('imagen'): # Aseguramos que sea imagenX.png
            try:
                # Extraemos el número para ordenar
                num = int(filename.replace('imagen', '').replace('.png', ''))
                image_files.append((num, filename))
            except ValueError:
                # Ignoramos archivos que no sigan el patrón imagenX.png
                continue

    # Ordenamos las imágenes por número de forma descendente (las más nuevas arriba)
    # Por ejemplo, imagen120 primero, luego imagen119, etc.
    image_files.sort(key=lambda x: x[0], reverse=True)

    gallery_data = []
    for i, (num, filename) in enumerate(image_files):
        # Generamos un título a partir del nombre del archivo (quitar 'imagen', quitar '.png')
        # Ejemplo: "imagen120.png" -> "Creación AI #120"
        # Si renombraste tus imágenes a algo como "paisaje-urbano.png", el título será "Paisaje urbano"
        title_from_filename = filename.replace('.png', '').replace('imagen', 'Creación AI #').replace('_', ' ').replace('-', ' ').strip()
        if title_from_filename.lower().startswith('creacion ai #'): # Si sigue el patron imagenX.png
            final_title = f"Creación AI #{num}"
        else: # Si renombraste tus imagenes, usara el nombre del archivo mas bonito
            final_title = title_from_filename.replace('  ', ' ').title() # Capitaliza cada palabra

        # Este prompt será genérico, deberías editarlo después si quieres uno específico por imagen
        generic_prompt = f"Prompt: Descripción detallada de la imagen {num} generada con IA."

        gallery_data.append({
            "filename": filename,
            "title": final_title,
            "prompt": generic_prompt
        })

    # Imprimimos la lista de JavaScript
    print("const galleryImages = [")
    for i, entry in enumerate(gallery_data):
        # Usamos json.dumps para formatear correctamente los strings con comillas
        print(f"    {json.dumps(entry, indent=4).replace('    ', '        ').strip()},") # Formato bonito con 8 espacios
    print("];")

if __name__ == "__main__":
    generate_gallery_data()