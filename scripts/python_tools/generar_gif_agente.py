#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de GIF para Presentación - Agent.exe
Crea un GIF animado mostrando el comportamiento del agente
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.animation import FuncAnimation
try:
    from matplotlib.animation import PillowWriter as Writer
except ImportError:
    from matplotlib.animation import FFMpegWriter as Writer
import random
import time

class AgentGifGenerator:
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, 1, figsize=(12, 8))
        self.frames = []
        self.current_step = 0
        self.mouse_x = 640
        self.mouse_y = 400

        # Configurar el área de la pantalla simulada
        self.screen_width = 1280
        self.screen_height = 800

        # Colores
        self.bg_color = '#2b2b2b'
        self.text_color = '#00ff00'
        self.cursor_color = '#ff0000'
        self.action_color = '#ffff00'

    def setup_plot(self):
        """Configura la apariencia del plot"""
        self.ax.set_xlim(0, self.screen_width)
        self.ax.set_ylim(0, self.screen_height)
        self.ax.set_facecolor(self.bg_color)
        self.ax.set_title('AGENT.EXE - Simulador Autónomo',
                         color='white', fontsize=16, fontweight='bold')

        # Remover ejes
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Agregar borde
        for spine in self.ax.spines.values():
            spine.set_color('white')
            spine.set_linewidth(2)

    def draw_desktop_elements(self):
        """Dibuja elementos del escritorio simulado"""
        # Barra de tareas
        taskbar = patches.Rectangle((0, 0), self.screen_width, 50,
                                  facecolor='#1e1e1e', edgecolor='white')
        self.ax.add_patch(taskbar)

        # Iconos del escritorio
        icon_positions = [
            (100, 700, '📁 Documentos'),
            (200, 700, '🌐 Navegador'),
            (300, 700, '📝 Bloc de notas'),
            (400, 700, '📊 Excel'),
            (100, 600, '🎵 Música'),
            (200, 600, '🖼️ Imagen.png')
        ]

        for x, y, label in icon_positions:
            # Icono
            icon = patches.Rectangle((x-25, y-25), 50, 50,
                                   facecolor='#4a4a4a', edgecolor='white')
            self.ax.add_patch(icon)

            # Etiqueta
            self.ax.text(x, y-40, label, ha='center', va='center',
                        color='white', fontsize=8)

    def draw_cursor(self, x, y):
        """Dibuja el cursor del mouse"""
        # Cursor principal
        cursor = patches.Polygon([(x, y), (x+15, y-10), (x+8, y-8), (x+10, y-15)],
                               facecolor=self.cursor_color, edgecolor='white')
        return cursor

    def draw_action_indicator(self, x, y, action_type):
        """Dibuja indicador de acción"""
        # Círculo de acción
        circle = patches.Circle((x, y), 30, facecolor='yellow', alpha=0.5)

        # Texto de acción
        action_text = self.ax.text(x, y-50, action_type, ha='center', va='center',
                                 color=self.action_color, fontsize=12, fontweight='bold')

        return circle, action_text

    def draw_console_output(self, step_info):
        """Dibuja la salida de la consola simulada"""
        console_y = 150
        console_height = 120

        # Fondo de consola
        console_bg = patches.Rectangle((20, console_y), self.screen_width-40, console_height,
                                     facecolor='black', edgecolor=self.text_color, alpha=0.8)
        self.ax.add_patch(console_bg)

        # Texto de la consola
        console_lines = [
            f"[{self.current_step}] REASONING: {step_info['reasoning']}",
            f"[{self.current_step}] ACTION: {step_info['action']}",
            f"[{self.current_step}] COORDINATES: ({step_info['x']}, {step_info['y']})",
            f"[{self.current_step}] STATUS: {step_info['status']}"
        ]

        for i, line in enumerate(console_lines):
            self.ax.text(30, console_y + console_height - 20 - i*20, line,
                        color=self.text_color, fontsize=10, fontfamily='monospace')

    def generate_step_data(self):
        """Genera datos para cada paso de la animación"""
        actions = [
            ("Taking Screenshot", "Capturando pantalla actual..."),
            ("Moving Mouse", "Navegando a elemento objetivo..."),
            ("Left Click", "Haciendo clic en aplicación..."),
            ("Type Text", "Escribiendo contenido..."),
            ("Right Click", "Abriendo menú contextual..."),
            ("Double Click", "Ejecutando aplicación..."),
            ("Scroll", "Desplazando contenido..."),
            ("Key Press", "Presionando tecla Enter...")
        ]

        action, reasoning = random.choice(actions)
        x = random.randint(100, self.screen_width-100)
        y = random.randint(100, self.screen_height-100)

        return {
            'action': action,
            'reasoning': reasoning,
            'x': x,
            'y': y,
            'status': 'Ejecutando...' if self.current_step % 3 != 0 else 'Completado ✓'
        }

    def animate(self, frame):
        """Función de animación para cada frame"""
        self.ax.clear()
        self.setup_plot()
        self.draw_desktop_elements()

        # Generar datos del paso actual
        step_data = self.generate_step_data()

        # Animar movimiento del cursor
        target_x, target_y = step_data['x'], step_data['y']

        # Interpolación suave del cursor
        alpha = 0.3
        self.mouse_x += alpha * (target_x - self.mouse_x)
        self.mouse_y += alpha * (target_y - self.mouse_y)

        # Dibujar cursor
        cursor = self.draw_cursor(self.mouse_x, self.mouse_y)
        self.ax.add_patch(cursor)

        # Si estamos cerca del objetivo, mostrar acción
        distance = np.sqrt((self.mouse_x - target_x)**2 + (self.mouse_y - target_y)**2)
        if distance < 50:
            circle, action_text = self.draw_action_indicator(target_x, target_y, step_data['action'])
            self.ax.add_patch(circle)
            self.current_step += 1

        # Dibujar salida de consola
        self.draw_console_output(step_data)

        # Información en la esquina
        info_text = f"Paso: {self.current_step} | Agente: ACTIVO | Modo: AUTÓNOMO"
        self.ax.text(10, self.screen_height-20, info_text,
                    color='white', fontsize=12, fontweight='bold')

        return self.ax.patches + self.ax.texts

    def create_gif(self, filename='agent_demo.gif', duration=10, fps=5):
        """Crea el GIF animado"""
        print("🎬 Generando GIF para presentación...")
        print(f"📁 Archivo: {filename}")
        print(f"⏱️  Duración: {duration} segundos")
        print(f"🎞️  FPS: {fps}")

        # Configurar animación
        frames_total = duration * fps
        anim = FuncAnimation(self.fig, self.animate, frames=frames_total,
                           interval=1000/fps, blit=False, repeat=True)

        # Configurar writer
        writer = Writer(fps=fps)

        # Guardar GIF
        try:
            anim.save(filename, writer=writer)
            print(f"✅ GIF creado exitosamente: {filename}")
            print(f"📊 Frames generados: {frames_total}")
            return True
        except Exception as e:
            print(f"❌ Error creando GIF: {e}")
            return False

    def create_presentation_gif(self):
        """Crea GIF optimizado para presentación"""
        print("\n" + "="*60)
        print("🚀 AGENT.EXE - GENERADOR DE GIF PARA PRESENTACIÓN")
        print("="*60)

        # Configuraciones para diferentes tipos de presentación
        configs = {
            '1': {'file': 'agent_demo_corto.gif', 'duration': 15, 'fps': 4},
            '2': {'file': 'agent_demo_completo.gif', 'duration': 30, 'fps': 3},
            '3': {'file': 'agent_demo_rapido.gif', 'duration': 10, 'fps': 6}
        }

        print("\nSelecciona el tipo de GIF:")
        print("1. Corto (15s) - Para demos rápidas")
        print("2. Completo (30s) - Para presentaciones detalladas")
        print("3. Rápido (10s) - Para loops continuos")

        choice = input("\nOpción (1-3): ").strip()

        if choice in configs:
            config = configs[choice]
            success = self.create_gif(**config)

            if success:
                print(f"\n🎉 ¡GIF listo para tu presentación!")
                print(f"📂 Archivo creado: {config['file']}")
                print("💡 Tip: Inserta el GIF en PowerPoint/Google Slides")

        else:
            print("❌ Opción no válida")

def main():
    """Función principal"""
    try:
        generator = AgentGifGenerator()
        generator.create_presentation_gif()

    except KeyboardInterrupt:
        print("\n⏹️  Generación cancelada por el usuario")
    except ImportError as e:
        print(f"❌ Error: Instala las dependencias necesarias")
        print("pip install matplotlib numpy pillow")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
