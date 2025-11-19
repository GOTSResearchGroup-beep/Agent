#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de GIF Simple para Presentación - Agent.exe
Versión simplificada que funciona con cualquier instalación de Python
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import os
from datetime import datetime

class SimpleAgentVisualizer:
    def __init__(self):
        # Configuración básica
        self.screen_width = 1280
        self.screen_height = 800
        self.step_count = 0

        # Colores
        self.bg_color = '#1a1a1a'
        self.text_color = '#00ff41'
        self.cursor_color = '#ff4444'
        self.action_color = '#ffaa00'

        plt.style.use('dark_background')

    def create_static_demo_frames(self, num_frames=20):
        """Crea frames estáticos para mostrar el comportamiento del agente"""

        print("🎬 Generando frames de demo...")

        # Crear directorio para frames
        if not os.path.exists('agent_frames'):
            os.makedirs('agent_frames')

        actions_sequence = [
            ("Taking Screenshot", "📸", "Capturando estado actual de la pantalla"),
            ("Analyzing Screen", "🧠", "Procesando elementos visuales detectados"),
            ("Mouse Move", "🖱️", "Navegando a coordenadas objetivo"),
            ("Left Click", "👆", "Ejecutando clic en elemento identificado"),
            ("Typing Text", "⌨️", "Escribiendo contenido requerido"),
            ("Keyboard Shortcut", "⌨️", "Ejecutando comando de teclado"),
            ("Scroll Action", "📜", "Desplazando contenido de la pantalla"),
            ("Right Click", "👆", "Abriendo menú contextual"),
            ("Double Click", "👆", "Ejecutando aplicación seleccionada"),
            ("Task Complete", "✅", "Tarea completada exitosamente")
        ]

        for frame_num in range(num_frames):
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))

            # Configurar plot
            ax.set_xlim(0, self.screen_width)
            ax.set_ylim(0, self.screen_height)
            ax.set_facecolor(self.bg_color)
            ax.set_title('AGENT.EXE - Demostración de Funcionamiento',
                        color='white', fontsize=18, fontweight='bold', pad=20)

            # Remover ejes
            ax.set_xticks([])
            ax.set_yticks([])

            # Dibujar escritorio simulado
            self.draw_desktop(ax)

            # Generar acción actual
            action_idx = frame_num % len(actions_sequence)
            action_name, icon, description = actions_sequence[action_idx]

            # Coordenadas aleatorias para esta acción
            x = random.randint(200, self.screen_width - 200)
            y = random.randint(200, self.screen_height - 200)

            # Dibujar cursor y acción
            self.draw_cursor_and_action(ax, x, y, action_name, icon)

            # Dibujar consola de logs
            self.draw_console(ax, frame_num, action_name, x, y, description)

            # Información del sistema
            self.draw_system_info(ax, frame_num)

            # Guardar frame
            filename = f'agent_frames/frame_{frame_num:03d}.png'
            plt.tight_layout()
            plt.savefig(filename, dpi=100, bbox_inches='tight',
                       facecolor=self.bg_color, edgecolor='none')
            plt.close()

            print(f"✅ Frame {frame_num + 1}/{num_frames} generado")

        print(f"\n🎉 {num_frames} frames generados en la carpeta 'agent_frames'")
        self.create_gif_instructions()

    def draw_desktop(self, ax):
        """Dibuja elementos del escritorio"""
        # Barra de tareas
        taskbar = patches.Rectangle((0, 0), self.screen_width, 60,
                                  facecolor='#333333', edgecolor='white', linewidth=2)
        ax.add_patch(taskbar)

        # Iconos del escritorio
        icons = [
            (120, 720, "📁", "Documentos"),
            (250, 720, "🌐", "Browser"),
            (380, 720, "📝", "Notepad"),
            (510, 720, "📊", "Excel"),
            (640, 720, "🖼️", "Imagen.png"),
            (120, 600, "⚙️", "Settings"),
            (250, 600, "🎵", "Media"),
            (380, 600, "📂", "Files")
        ]

        for x, y, emoji, label in icons:
            # Fondo del icono
            icon_bg = patches.Rectangle((x-35, y-35), 70, 70,
                                      facecolor='#2d2d2d', edgecolor='white', linewidth=1)
            ax.add_patch(icon_bg)

            # Emoji del icono
            ax.text(x, y+5, emoji, ha='center', va='center', fontsize=24)

            # Label del icono
            ax.text(x, y-50, label, ha='center', va='center',
                   color='white', fontsize=9, fontweight='bold')

    def draw_cursor_and_action(self, ax, x, y, action_name, icon):
        """Dibuja el cursor y la acción actual"""
        # Cursor del mouse
        cursor_points = np.array([[x, y], [x+20, y-15], [x+10, y-10], [x+15, y-25]])
        cursor = patches.Polygon(cursor_points, facecolor=self.cursor_color,
                               edgecolor='white', linewidth=2)
        ax.add_patch(cursor)

        # Círculo de acción
        action_circle = patches.Circle((x, y), 50, facecolor=self.action_color,
                                     alpha=0.3, edgecolor=self.action_color, linewidth=3)
        ax.add_patch(action_circle)

        # Texto de acción
        ax.text(x, y-80, f"{icon} {action_name}", ha='center', va='center',
                color=self.action_color, fontsize=14, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.5", facecolor='black', alpha=0.8))

        # Coordenadas
        ax.text(x, y-110, f"({x}, {y})", ha='center', va='center',
                color='white', fontsize=11,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#333333', alpha=0.8))

    def draw_console(self, ax, step, action, x, y, description):
        """Dibuja la ventana de consola con logs"""
        console_x, console_y = 50, 50
        console_width, console_height = self.screen_width - 100, 150

        # Fondo de consola
        console_bg = patches.Rectangle((console_x, console_y), console_width, console_height,
                                     facecolor='black', edgecolor=self.text_color,
                                     linewidth=2, alpha=0.9)
        ax.add_patch(console_bg)

        # Header de consola
        ax.text(console_x + 10, console_y + console_height - 20,
                "AGENT.EXE - Console Output",
                color='white', fontsize=12, fontweight='bold')

        # Logs simulados
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        logs = [
            f"[{step+1:02d}] {timestamp} - REASONING: {description}",
            f"[{step+1:02d}] {timestamp} - ACTION: {action}",
            f"[{step+1:02d}] {timestamp} - COORDINATES: Moving to ({x}, {y})",
            f"[{step+1:02d}] {timestamp} - STATUS: {'Executing...' if step % 3 else 'Completed ✓'}"
        ]

        for i, log in enumerate(logs):
            ax.text(console_x + 15, console_y + console_height - 50 - i*25, log,
                   color=self.text_color, fontsize=10, fontfamily='monospace')

    def draw_system_info(self, ax, step):
        """Dibuja información del sistema"""
        info_y = self.screen_height - 30

        # Información del agente
        info_items = [
            f"👁️ Step: {step + 1}",
            f"🤖 Agent: ACTIVE",
            f"🎯 Mode: AUTONOMOUS",
            f"⚡ Status: RUNNING"
        ]

        info_text = " | ".join(info_items)
        ax.text(20, info_y, info_text, color='white', fontsize=12, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.5", facecolor='#1a1a1a', alpha=0.8))

    def create_gif_instructions(self):
        """Muestra instrucciones para crear GIF"""
        print("\n" + "="*60)
        print("📋 INSTRUCCIONES PARA CREAR GIF:")
        print("="*60)
        print("Los frames están guardados en la carpeta 'agent_frames/'")
        print("\n💡 OPCIONES PARA CREAR GIF:")
        print("\n1. 🌐 ONLINE (más fácil):")
        print("   • Ve a: https://ezgif.com/maker")
        print("   • Sube todos los archivos PNG")
        print("   • Ajusta velocidad: 0.5-1 segundo por frame")
        print("   • Descarga tu GIF")

        print("\n2. 💻 FFMPEG (si lo tienes instalado):")
        print("   ffmpeg -framerate 2 -i agent_frames/frame_%03d.png -y agent_demo.gif")

        print("\n3. 🐍 PYTHON (si tienes PIL):")
        print("   pip install pillow")
        print("   # Luego ejecuta el método create_gif_from_frames()")

        print("\n🎬 Tu GIF estará listo para la presentación!")
        print("="*60)

    def create_gif_from_frames(self):
        """Crea GIF desde los frames (requiere PIL)"""
        try:
            from PIL import Image
            import glob

            frames = []
            frame_files = sorted(glob.glob('agent_frames/frame_*.png'))

            for frame_file in frame_files:
                img = Image.open(frame_file)
                frames.append(img)

            if frames:
                frames[0].save(
                    'agent_demo.gif',
                    save_all=True,
                    append_images=frames[1:],
                    duration=800,  # 0.8 segundos por frame
                    loop=0
                )
                print("✅ GIF creado: agent_demo.gif")
            else:
                print("❌ No se encontraron frames")

        except ImportError:
            print("❌ PIL no está instalado. Usa las opciones online.")
        except Exception as e:
            print(f"❌ Error creando GIF: {e}")

def main():
    """Función principal"""
    try:
        print("🚀 AGENT.EXE - GENERADOR DE DEMO VISUAL")
        print("="*50)

        visualizer = SimpleAgentVisualizer()

        # Preguntar cuántos frames
        try:
            num_frames = int(input("¿Cuántos frames generar? (recomendado 15-30): ") or "20")
        except ValueError:
            num_frames = 20

        # Generar frames
        visualizer.create_static_demo_frames(num_frames)

        # Preguntar si crear GIF automáticamente
        create_gif = input("\n¿Intentar crear GIF automáticamente? (y/n): ").lower().strip()
        if create_gif == 'y':
            visualizer.create_gif_from_frames()

    except KeyboardInterrupt:
        print("\n⏹️ Generación cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
