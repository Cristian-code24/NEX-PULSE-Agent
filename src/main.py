# -*- coding: utf-8 -*-
"""
Punto de entrada principal para NEX-PULSE Agent.

Orquesta la configuración, logs, verificación de permisos y 
el bucle de monitoreo principal del sistema.

Autor: NEX-PULSE Team
Versión: 1.0.0
"""

import time
import sys
import os

from config import validate_config, MONITORING_INTERVAL
from core import logs_manager
from core import permissions
from core import system_monitor
from core.autonomous_agent import NexpulseAgent

def main():
    # 1. Configurar Logger Principal
    logger = logs_manager.setup_logger("Main")
    logger.info("Iniciando NEX-PULSE Agent...")

    # 2. Validar Configuración
    if not validate_config():
        logger.critical("Configuración inválida. Abortando inicio.")
        sys.exit(1)

    # 3. Verificar Privilegios
    if not permissions.is_admin():
        logger.warning("El agente no tiene privilegios de administrador.")
        logger.info("Intentando elevar privilegios...")
        permissions.relaunch_as_admin()
        logger.warning("Elevación declinada o fallida. Ejecutando en modo usuario (limpieza profunda restringida).")
    else:
        logger.info("Privilegios de Administrador verificados (OK).")

    logger.info("NEX-PULSE Core inicializado correctamente.")

    # 4. Loop de Monitoreo y Agente Autónomo
    ai_agent = NexpulseAgent()
    logger.info(f"Iniciando ciclo de monitoreo IA (Intervalo: {MONITORING_INTERVAL}s)...")
    try:
        while True:
            # Obtener snapshot del sistema
            metrics = system_monitor.get_system_summary()
            # Le damos a la IA los 15 procesos más pesados en RAM
            top_procs = system_monitor.get_top_processes(limit=15, sort_by='memory')
            
            cpu = metrics['cpu']['usage_percent']
            ram = metrics['memory']['percent']
            
            # La IA evalúa la salud y decide si actúa
            ai_status = ai_agent.think_and_act(metrics, top_procs)
            
            logger.info(f"[HEARTBEAT] CPU: {cpu}% | RAM: {ram}% | AI: {ai_status}")
            
            time.sleep(MONITORING_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("Señal de interrupción recibida (Ctrl+C). Apagando agente...")
    except Exception as e:
        logger.critical(f"Fallo crítico en el loop principal: {e}", exc_info=True)
    finally:
        logger.info("NEX-PULSE Agent detenido limpiamente.")

if __name__ == "__main__":
    main()
