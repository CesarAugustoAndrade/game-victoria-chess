"""
Sistema de guardado de progreso para la campaña de Legio Romana
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class SaveManager:
    """Gestiona el guardado y carga del progreso de la campaña"""

    def __init__(self, save_dir: str = "saves"):
        self.save_dir = Path(save_dir)
        self.save_file = self.save_dir / "campaign_progress.json"
        self._ensure_save_dir_exists()

    def _ensure_save_dir_exists(self):
        """Crea el directorio de guardados si no existe"""
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True, exist_ok=True)

    def save_campaign(self, campaign_data: Dict[str, Any]) -> bool:
        """
        Guarda el progreso de la campaña

        Args:
            campaign_data: Diccionario con datos de la campaña

        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        try:
            # Añadir metadata de guardado
            save_data = {
                "version": "1.0",
                "last_save": datetime.now().isoformat(),
                **campaign_data
            }

            # Guardar a archivo JSON
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            print(f"[SAVE] Progreso guardado exitosamente en {self.save_file}")
            return True

        except Exception as e:
            print(f"[ERROR] No se pudo guardar el progreso: {e}")
            return False

    def load_campaign(self) -> Optional[Dict[str, Any]]:
        """
        Carga el progreso guardado de la campaña

        Returns:
            Diccionario con datos de la campaña, o None si no existe guardado
        """
        if not self.save_exists():
            print("[SAVE] No se encontró archivo de guardado")
            return None

        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            print(f"[SAVE] Progreso cargado desde {self.save_file}")
            print(f"[SAVE] Última partida: {save_data.get('last_save', 'Desconocido')}")

            return save_data

        except Exception as e:
            print(f"[ERROR] No se pudo cargar el progreso: {e}")
            return None

    def delete_save(self) -> bool:
        """
        Elimina el archivo de guardado

        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        try:
            if self.save_file.exists():
                self.save_file.unlink()
                print("[SAVE] Guardado eliminado exitosamente")
                return True
            return False
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar el guardado: {e}")
            return False

    def save_exists(self) -> bool:
        """
        Verifica si existe un archivo de guardado

        Returns:
            True si existe guardado, False en caso contrario
        """
        return self.save_file.exists()

    def get_save_info(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene información del guardado sin cargarlo completamente

        Returns:
            Diccionario con info básica del guardado
        """
        if not self.save_exists():
            return None

        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return {
                "last_save": data.get("last_save", "Desconocido"),
                "nivel_actual": data.get("nivel_actual", 0),
                "progreso": data.get("progreso", 0),
                "niveles_completados_count": len(data.get("niveles_completados", []))
            }

        except Exception as e:
            print(f"[ERROR] No se pudo leer info del guardado: {e}")
            return None


# Instancia global del gestor de guardado
save_manager = SaveManager()
