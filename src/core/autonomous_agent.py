# -*- coding: utf-8 -*-
"""
Inteligencia Autónoma de NEX-PULSE Agent.

Analiza las métricas en tiempo real, determina el estado de salud del sistema
y ejecuta acciones de optimización proactivas sin matar procesos de usuario.
"""
import time
import collections
import statistics
import os
import shutil
import ctypes
import psutil

from .logs_manager import setup_logger
from config import SAFE_FOLDERS_TO_CLEAN, TEMP_FILE_EXTENSIONS

logger = setup_logger("AutonomousAI")

class NexpulseAgent:
    def __init__(self, history_size=30):
        # Usamos deque para mantener un registro histórico (ventana móvil)
        self.cpu_history = collections.deque(maxlen=history_size)
        self.ram_history = collections.deque(maxlen=history_size)
        self.current_health = 100.0
        self.last_clean_time = 0
        # Enfoque conservador: Optimizar solo una vez cada 60 segundos
        self.cooldown_seconds = 60 

    def think_and_act(self, metrics, top_processes):
        """
        Ciclo principal de toma de decisiones.
        """
        cpu = metrics['cpu']['usage_percent']
        ram = metrics['memory']['percent']
        
        self.cpu_history.append(cpu)
        self.ram_history.append(ram)

        if len(self.cpu_history) < 10:
            return "Calibrando sensores de IA..."

        # Calcular medias móviles
        cpu_avg = statistics.mean(self.cpu_history)
        ram_avg = statistics.mean(self.ram_history)

        # Penalizaciones de salud más agresivas para reaccionar rápido
        cpu_penalty = max(0, cpu_avg - 50) * 0.8
        ram_penalty = max(0, ram_avg - 70) * 1.5
        self.current_health = max(0.0, min(100.0, 100.0 - (cpu_penalty + ram_penalty)))

        now = time.time()
        
        # Decidir acciones basadas en la salud (Menos de 85 = Estrés en RAM/CPU)
        if self.current_health < 85.0 and (now - self.last_clean_time) > self.cooldown_seconds:
            logger.warning(f"¡Estrés detectado! (Salud Sistema: {self.current_health:.1f}%). Iniciando Optimizador...")
            self._execute_optimization(top_processes)
            self.last_clean_time = now
            return "Optimización Ejecutada"
            
        return f"Sistema Estable ({self.current_health:.1f}%)"

    def _execute_optimization(self, top_processes):
        """Ejecuta los algoritmos de limpieza sin destruir procesos de usuario."""
        self._optimize_memory(top_processes)
        self._clean_temp_files()

    def _optimize_memory(self, top_processes):
        """
        Inteligencia: En lugar de matar el programa (Chrome, juegos), le ordenamos al SO
        que descargue la memoria inactiva (EmptyWorkingSet) del proceso.
        """
        logger.info("[NEX-AI] Ejecutando compresión de memoria profunda...")
        optimized_count = 0

        try:
            # Acceso a la API de Windows
            psapi = ctypes.WinDLL('psapi')
            kernel32 = ctypes.WinDLL('kernel32')
            PROCESS_SET_QUOTA = 0x0100
            
            for p in top_processes:
                pid = p['pid']
                name = str(p.get('name', 'unknown')).lower()
                
                # Ignoramos procesos críticos de Windows para no causar inestabilidad
                if name in ["system", "registry", "smss.exe", "csrss.exe", "wininit.exe", "services.exe", "lsass.exe", "svchost.exe"]:
                    continue
                
                try:
                    # Abrir proceso con permisos para modificar cuota de memoria
                    h_process = kernel32.OpenProcess(PROCESS_SET_QUOTA, False, pid)
                    if h_process:
                        # Forzar a Windows a recuperar las páginas de memoria no usadas de la app
                        result = psapi.EmptyWorkingSet(h_process)
                        kernel32.CloseHandle(h_process)
                        if result:
                            optimized_count += 1
                except Exception:
                    pass # Ignorar si está protegido por el sistema
                    
            logger.info(f"[NEX-AI] Memoria de {optimized_count} aplicaciones purgada y recuperada exitosamente.")
        except Exception as e:
            logger.error(f"[NEX-AI] Fallo al inyectar API de Windows: {e}")

    def _clean_temp_files(self):
        """
        Inteligencia: Borra basura del disco de forma dinámica. Ignora bloqueos de SO.
        """
        logger.info("[NEX-AI] Escaneando e incinerando caché y archivos residuales...")
        bytes_freed = 0
        deleted_files = 0

        for folder in SAFE_FOLDERS_TO_CLEAN:
            if not folder.exists() or not folder.is_dir():
                continue
                
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        os.remove(file_path) # Intento agresivo
                        bytes_freed += size
                        deleted_files += 1
                    except (PermissionError, FileNotFoundError, OSError):
                        # Inteligencia: Si falla, es porque la app activa lo está usando. Lo dejamos en paz.
                        pass
                        
        mb_freed = bytes_freed / (1024 * 1024)
        if deleted_files > 0:
            logger.info(f"[NEX-AI] Incineración de disco completada: {deleted_files} archivos ({mb_freed:.2f} MB liberados).")
        else:
            logger.info("[NEX-AI] Disco en estado óptimo. Sin basura residual.")
