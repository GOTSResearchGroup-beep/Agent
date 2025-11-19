#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modificador de píxeles para crear ataque adversarial visual
Selecciona un área de 50x50 píxeles y modifica aleatoriamente algunos píxeles
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
import os

class PixelModifier:
    def __init__(self, image_path):
        """Inicializa con la ruta de la imagen"""
        self.image_path = image_path
        self.original_image = None
        self.modified_image = None
        self.saturated_image = None
        self.modified_pixels = []

    def load_image(self):
        """Carga la imagen desde el archivo"""
        try:
            # Cargar imagen
            img = Image.open(self.image_path)
            # Convertir a RGB si no lo está
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Convertir a array numpy
            self.original_image = np.array(img)
            print(f"✅ Imagen cargada: {self.original_image.shape}")
            return True
        except Exception as e:
            print(f"❌ Error cargando imagen: {e}")
            return False

    def select_center_area(self, area_size=50):
        """Selecciona un área cuadrada del centro de la imagen"""
        if self.original_image is None:
            print("❌ Primero debes cargar la imagen")
            return None

        h, w = self.original_image.shape[:2]

        # Calcular centro
        center_y, center_x = h // 2, w // 2

        # Calcular límites del área
        half_size = area_size // 2
        start_y = max(0, center_y - half_size)
        end_y = min(h, center_y + half_size)
        start_x = max(0, center_x - half_size)
        end_x = min(w, center_x + half_size)

        print(f"📍 Área seleccionada: ({start_x}, {start_y}) a ({end_x}, {end_y})")
        print(f"📏 Tamaño real del área: {end_x - start_x} x {end_y - start_y}")

        return (start_x, start_y, end_x, end_y)

    def modify_pixels_randomly(self, area_coords, modification_percentage=30, intensity_range=(0, 10)):
        """Modifica aleatoriamente un porcentaje de píxeles en el área"""
        if self.original_image is None:
            print("❌ Primero debes cargar la imagen")
            return False

        start_x, start_y, end_x, end_y = area_coords

        # Crear copia de la imagen original (convertir a int32 para evitar overflow)
        self.modified_image = self.original_image.astype(np.int32)

        # Calcular número de píxeles en el área
        area_width = end_x - start_x
        area_height = end_y - start_y
        total_pixels = area_width * area_height
        pixels_to_modify = int(total_pixels * modification_percentage / 100)

        print(f"🎯 Píxeles totales en área: {total_pixels}")
        print(f"🔧 Píxeles a modificar: {pixels_to_modify} ({modification_percentage}%)")

        # Generar posiciones aleatorias para modificar
        self.modified_pixels = []

        for _ in range(pixels_to_modify):
            # Posición aleatoria dentro del área
            x = random.randint(start_x, end_x - 1)
            y = random.randint(start_y, end_y - 1)

            # Modificación aleatoria de intensidad
            intensity_change = random.randint(intensity_range[0], intensity_range[1])

            # Decidir si sumar o restar
            if random.choice([True, False]):
                intensity_change = -intensity_change

            # Aplicar modificación a cada canal RGB
            for channel in range(3):
                original_value = int(self.modified_image[y, x, channel])
                new_value = original_value + intensity_change
                # Mantener en rango válido [0, 255]
                new_value = max(0, min(255, new_value))
                self.modified_image[y, x, channel] = new_value

            # Guardar información del píxel modificado
            self.modified_pixels.append((x, y, intensity_change))

        # Convertir de vuelta a uint8
        self.modified_image = self.modified_image.astype(np.uint8)

        print(f"✅ {len(self.modified_pixels)} píxeles modificados")
        return True

    def create_saturated_version(self):
        """Crea versión saturada donde los píxeles modificados se ven claramente"""
        if self.modified_image is None or not self.modified_pixels:
            print("❌ Primero debes modificar píxeles")
            return False

        # Crear copia de la imagen modificada
        self.saturated_image = self.modified_image.copy()

        # Saturar los píxeles modificados
        for x, y, _ in self.modified_pixels:
            # Hacer el píxel completamente rojo para que sea visible
            self.saturated_image[y, x] = [255, 0, 0]  # Rojo intenso

        print(f"🔴 {len(self.modified_pixels)} píxeles saturados en rojo")
        return True

    def create_subplot_comparison(self):
        """Crea subplot con las 3 imágenes para comparación"""
        if any(img is None for img in [self.original_image, self.modified_image, self.saturated_image]):
            print("❌ Faltan imágenes para crear el subplot")
            return False

        # Crear figura con 3 subplots
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        # Imagen original
        axes[0].imshow(self.original_image)
        axes[0].set_title('Original', fontsize=14, fontweight='bold')
        axes[0].axis('off')

        # Imagen modificada (ataque adversarial sutil)
        axes[1].imshow(self.modified_image)
        axes[1].set_title('Modificada (Ataque Adversarial)', fontsize=14, fontweight='bold')
        axes[1].axis('off')

        # Imagen con píxeles modificados saturados
        axes[2].imshow(self.saturated_image)
        axes[2].set_title('Píxeles Modificados (Saturados)', fontsize=14, fontweight='bold')
        axes[2].axis('off')

        # Título general
        fig.suptitle('Comparación: Ataque Adversarial de Píxeles',
                    fontsize=16, fontweight='bold', y=0.98)

        # Información adicional
        info_text = f"Área modificada: 50x50 píxeles | {len(self.modified_pixels)} píxeles alterados | Intensidad: 0-10%"
        fig.text(0.5, 0.02, info_text, ha='center', fontsize=12, style='italic')

        # Ajustar layout
        plt.tight_layout()
        plt.subplots_adjust(top=0.9, bottom=0.1)

        # Guardar imagen
        output_filename = 'pixel_attack_comparison.png'
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
        print(f"💾 Comparación guardada como: {output_filename}")

        # Mostrar
        plt.show()

        return True

    def analyze_changes(self):
        """Analiza los cambios realizados"""
        if not self.modified_pixels:
            print("❌ No hay píxeles modificados para analizar")
            return

        print("\n" + "="*60)
        print("📊 ANÁLISIS DE MODIFICACIONES")
        print("="*60)

        # Estadísticas de intensidad
        intensities = [abs(change) for _, _, change in self.modified_pixels]
        avg_intensity = np.mean(intensities)
        max_intensity = max(intensities)
        min_intensity = min(intensities)

        print(f"🔢 Píxeles modificados: {len(self.modified_pixels)}")
        print(f"📈 Intensidad promedio: {avg_intensity:.2f}")
        print(f"📊 Intensidad máxima: {max_intensity}")
        print(f"📉 Intensidad mínima: {min_intensity}")

        # Distribución de cambios
        positive_changes = sum(1 for _, _, change in self.modified_pixels if change > 0)
        negative_changes = len(self.modified_pixels) - positive_changes

        print(f"⬆️ Aumentos de intensidad: {positive_changes}")
        print(f"⬇️ Reducciones de intensidad: {negative_changes}")

        print("="*60)

    def run_complete_process(self):
        """Ejecuta el proceso completo"""
        print("🚀 INICIANDO MODIFICACIÓN DE PÍXELES")
        print("="*50)

        # 1. Cargar imagen
        if not self.load_image():
            return False

        # 2. Seleccionar área central
        area_coords = self.select_center_area(50)
        if area_coords is None:
            return False

        # 3. Modificar píxeles aleatoriamente
        if not self.modify_pixels_randomly(area_coords, modification_percentage=30, intensity_range=(0, 10)):
            return False

        # 4. Crear versión saturada
        if not self.create_saturated_version():
            return False

        # 5. Analizar cambios
        self.analyze_changes()

        # 6. Crear subplot de comparación
        if not self.create_subplot_comparison():
            return False

        print("\n🎉 ¡Proceso completado exitosamente!")
        return True

def main():
    """Función principal"""
    try:
        # Buscar imagen.png en la raíz
        image_path = "imagen.png"

        if not os.path.exists(image_path):
            print(f"❌ No se encontró la imagen: {image_path}")
            print("🔍 Buscando archivos de imagen...")

            # Buscar otros archivos de imagen
            image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
            found_images = []

            for file in os.listdir('.'):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    found_images.append(file)

            if found_images:
                print("📸 Imágenes encontradas:")
                for i, img in enumerate(found_images, 1):
                    print(f"  {i}. {img}")

                try:
                    choice = int(input("\nSelecciona una imagen (número): ")) - 1
                    if 0 <= choice < len(found_images):
                        image_path = found_images[choice]
                    else:
                        print("❌ Selección inválida")
                        return
                except ValueError:
                    print("❌ Entrada inválida")
                    return
            else:
                print("❌ No se encontraron archivos de imagen")
                return

        # Crear modificador y ejecutar proceso
        modifier = PixelModifier(image_path)
        modifier.run_complete_process()

    except KeyboardInterrupt:
        print("\n⏹️ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
