#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador del Agent.exe para presentación
Simula el comportamiento del agente con pasos animados
"""

import time
import random
import os
from datetime import datetime

class AgentSimulator:
    def __init__(self):
        self.step_count = 0
        self.actions = [
            "Move to",
            "Left click",
            "Right click",
            "Double click",
            "Screenshot",
            "Type text",
            "Key press",
            "Scroll",
            "Wait"
        ]

    def generate_coordinates(self):
        """Genera coordenadas aleatorias realistas"""
        x = random.randint(50, 1200)
        y = random.randint(50, 800)
        return x, y

    def print_action(self, action, coords=None, extra_info=""):
        """Imprime una acción del agente con formato similar al real"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.step_count += 1

        print(f"[{self.step_count}] {timestamp} - ", end="")

        if coords:
            x, y = coords
            print(f"🎯 {action} ({x}, {y})")
        else:
            print(f"⚡ {action}")

        if extra_info:
            print(f"    💭 {extra_info}")
        print()

    def simulate_screenshot(self):
        """Simula tomar captura de pantalla"""
        self.print_action("📸 Taking Screenshot", extra_info="Analyzing current screen state...")
        time.sleep(1.5)

    def simulate_mouse_move(self):
        """Simula movimiento del mouse"""
        coords = self.generate_coordinates()
        self.print_action("🖱️  Move to", coords, f"Moving mouse to coordinates {coords}")
        time.sleep(0.8)

    def simulate_click(self):
        """Simula clic del mouse"""
        coords = self.generate_coordinates()
        click_type = random.choice(["Left click", "Right click", "Double click"])
        self.print_action(f"👆 {click_type}", coords, f"Clicking at {coords}")
        time.sleep(1.2)

    def simulate_typing(self):
        """Simula escritura de texto"""
        texts = [
            "Análisis completado",
            "Documento creado exitosamente",
            "Procesando información...",
            "Tarea ejecutada correctamente",
            "Navegando a sitio web",
            "Abriendo aplicación",
            "Guardando archivo"
        ]
        text = random.choice(texts)
        self.print_action("⌨️  Type text", extra_info=f'Writing: "{text}"')
        time.sleep(2)

    def simulate_reasoning(self):
        """Simula el razonamiento del agente"""
        reasonings = [
            "Evaluando la situación actual en pantalla...",
            "Identificando elementos interactivos disponibles...",
            "Analizando la mejor estrategia para completar la tarea...",
            "Verificando que la acción anterior se ejecutó correctamente...",
            "Determinando el próximo paso a realizar...",
            "Comprobando el estado de la aplicación objetivo...",
            "Procesando la respuesta del sistema..."
        ]
        reasoning = random.choice(reasonings)
        print(f"🧠 REASONING: {reasoning}")
        time.sleep(1.8)

    def simulate_task_completion(self):
        """Simula completar una tarea completa"""
        tasks = [
            "Creando documento en Word",
            "Enviando email con adjuntos",
            "Navegando a sitio web específico",
            "Organizando archivos en carpetas",
            "Ejecutando análisis de datos",
            "Configurando preferencias del sistema",
            "Descargando e instalando software"
        ]

        task = random.choice(tasks)
        print(f"\n{'='*60}")
        print(f"🎯 INICIANDO TAREA: {task}")
        print(f"{'='*60}\n")

        # Simular secuencia de acciones para completar la tarea
        for i in range(random.randint(5, 12)):
            # Tomar screenshot
            self.simulate_screenshot()

            # Razonamiento
            self.simulate_reasoning()

            # Acción aleatoria
            action_type = random.choice([
                "move", "click", "type", "screenshot"
            ])

            if action_type == "move":
                self.simulate_mouse_move()
            elif action_type == "click":
                self.simulate_click()
            elif action_type == "type":
                self.simulate_typing()
            else:
                self.simulate_screenshot()

            # Pausa entre acciones
            time.sleep(random.uniform(0.5, 2.0))

        print(f"✅ TAREA COMPLETADA: {task}")
        print(f"📊 Total de acciones ejecutadas: {i + 1}")
        print(f"⏱️  Tiempo estimado: {(i + 1) * 1.5:.1f} segundos\n")

    def run_demo(self, num_tasks=3):
        """Ejecuta demo completa para presentación"""
        print("🚀 AGENT.EXE - SIMULADOR PARA PRESENTACIÓN")
        print("=" * 60)
        print("Simulando comportamiento de agente AI autónomo")
        print("Perfecto para demos y presentaciones")
        print("=" * 60 + "\n")

        for task_num in range(1, num_tasks + 1):
            print(f"\n📋 EJECUTANDO TAREA {task_num}/{num_tasks}")
            self.simulate_task_completion()

            if task_num < num_tasks:
                print("⏸️  Esperando próxima tarea...\n")
                time.sleep(3)

        print("\n" + "="*60)
        print("🎉 DEMO COMPLETADA - TODAS LAS TAREAS EJECUTADAS")
        print("💡 El agente demostró capacidades de:")
        print("   • Análisis visual de pantalla")
        print("   • Navegación precisa del mouse")
        print("   • Interacción con aplicaciones")
        print("   • Escritura de texto inteligente")
        print("   • Razonamiento paso a paso")
        print("="*60)

def main():
    """Función principal para ejecutar la simulación"""
    try:
        simulator = AgentSimulator()

        print("Presiona Enter para iniciar la demo...")
        input()

        # Limpiar pantalla
        os.system('cls' if os.name == 'nt' else 'clear')

        # Ejecutar demo
        simulator.run_demo(num_tasks=3)

        print("\n🎬 ¿Quieres ejecutar otra demo? (y/n): ", end="")
        if input().lower() == 'y':
            main()

    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error en la simulación: {e}")

if __name__ == "__main__":
    main()
