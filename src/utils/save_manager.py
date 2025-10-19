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
        self._ensure_save_dir_exists()

    def _ensure_save_dir_exists(self):
        """Crea el directorio de guardados si no existe"""
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True, exist_ok=True)

    def _migrate_legacy_save(self) -> Optional[Dict[str, Any]]:
        """
        Migra el archivo legacy campaign_progress.json al formato nuevo

        Returns:
            Datos del guardado migrado o None si falla
        """
        legacy_file = self.save_dir / "campaign_progress.json"
        if not legacy_file.exists():
            return None

        try:
            # Leer archivo legacy
            with open(legacy_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Determinar tipo de campaña
            tipo = save_data.get('tipo_campania', 'tutorial')

            # Normalizar tipo
            if tipo == 'cesar_galia':
                tipo = 'galia'
                save_data['tipo_campania'] = 'galia'  # Actualizar en los datos

            # Obtener archivo destino
            try:
                new_file = self._get_save_file(tipo)
            except ValueError:
                print(f"[SAVE] Tipo de campaña inválido en archivo legacy: {tipo}")
                return None

            # Guardar en nuevo archivo
            with open(new_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            print(f"[SAVE] Archivo legacy migrado exitosamente a {new_file.name}")

            # Eliminar archivo legacy
            legacy_file.unlink()
            print("[SAVE] Archivo legacy eliminado")

            return save_data

        except Exception as e:
            print(f"[ERROR] No se pudo migrar archivo legacy: {e}")
            return None

    def _get_save_file(self, tipo_campania: str = None) -> Path:
        """
        ARREGLO: Obtiene el archivo de guardado para una campaña específica

        Args:
            tipo_campania: 'tutorial', 'galia', 'cesar_galia'

        Returns:
            Path al archivo de guardado

        Raises:
            ValueError: Si no se especifica tipo_campania
        """
        if tipo_campania in ['galia', 'cesar_galia']:
            return self.save_dir / "campaign_galia.json"
        elif tipo_campania == 'tutorial':
            return self.save_dir / "campaign_tutorial.json"
        else:
            # ARREGLO: No usar archivo legacy - forzar especificar tipo
            raise ValueError(f"Tipo de campaña inválido o no especificado: {tipo_campania}. Use 'tutorial' o 'galia'")

    def save_campaign(self, campaign_data: Dict[str, Any]) -> bool:
        """
        ARREGLO: Guarda el progreso de la campaña en el archivo apropiado

        Args:
            campaign_data: Diccionario con datos de la campaña (debe incluir 'tipo_campania')

        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        try:
            # Detectar tipo de campaña
            tipo_campania = campaign_data.get('tipo_campania', 'tutorial')
            save_file = self._get_save_file(tipo_campania)

            # Añadir metadata de guardado
            save_data = {
                "version": "1.0",
                "last_save": datetime.now().isoformat(),
                **campaign_data
            }

            # Guardar a archivo JSON
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            print(f"[SAVE] Progreso de '{tipo_campania}' guardado en {save_file}")
            return True

        except Exception as e:
            print(f"[ERROR] No se pudo guardar el progreso: {e}")
            return False

    def load_campaign(self, tipo_campania: str = None) -> Optional[Dict[str, Any]]:
        """
        ARREGLO: Carga el progreso guardado de una campaña específica

        Args:
            tipo_campania: 'tutorial', 'galia', o None para intentar migración legacy

        Returns:
            Diccionario con datos de la campaña, o None si no existe guardado
        """
        if tipo_campania:
            # Normalizar tipo_campania
            if tipo_campania == 'cesar_galia':
                tipo_campania = 'galia'

            # Cargar campaña específica
            try:
                save_file = self._get_save_file(tipo_campania)
            except ValueError:
                print(f"[SAVE] Tipo de campaña inválido: {tipo_campania}")
                return None

            if not save_file.exists():
                print(f"[SAVE] No se encontró guardado para '{tipo_campania}'")
                return None
        else:
            # Intento de migración legacy
            legacy_file = self.save_dir / "campaign_progress.json"
            if legacy_file.exists():
                print("[SAVE] Migrando archivo legacy campaign_progress.json")
                return self._migrate_legacy_save()
            else:
                print("[SAVE] No se encontró archivo de guardado")
                return None

        try:
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            print(f"[SAVE] Progreso cargado desde {save_file}")
            print(f"[SAVE] Última partida: {save_data.get('last_save', 'Desconocido')}")

            return save_data

        except Exception as e:
            print(f"[ERROR] No se pudo cargar el progreso: {e}")
            return None

    def delete_save(self, tipo_campania: str = None) -> bool:
        """
        ARREGLO: Elimina el archivo de guardado de una campaña específica

        Args:
            tipo_campania: 'tutorial', 'galia', o None para eliminar todas

        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        try:
            if tipo_campania:
                save_file = self._get_save_file(tipo_campania)
                if save_file.exists():
                    save_file.unlink()
                    print(f"[SAVE] Guardado de '{tipo_campania}' eliminado")
                    return True
            else:
                # Eliminar todos los guardados
                deleted = False
                for file in self.save_dir.glob("campaign_*.json"):
                    file.unlink()
                    deleted = True
                if deleted:
                    print("[SAVE] Todos los guardados eliminados")
                    return True
            return False
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar el guardado: {e}")
            return False

    def save_exists(self, tipo_campania: str = None) -> bool:
        """
        ARREGLO: Verifica si existe un archivo de guardado

        Args:
            tipo_campania: 'tutorial', 'galia', o None para verificar cualquiera

        Returns:
            True si existe guardado, False en caso contrario
        """
        if tipo_campania:
            return self._get_save_file(tipo_campania).exists()
        else:
            # Verificar si existe algún guardado
            return any(self.save_dir.glob("campaign_*.json"))

    def get_save_info(self, tipo_campania: str = None) -> Optional[Dict[str, Any]]:
        """
        ARREGLO: Obtiene información del guardado sin cargarlo completamente

        Args:
            tipo_campania: 'tutorial', 'galia', o None para archivo por defecto

        Returns:
            Diccionario con info básica del guardado
        """
        save_file = self._get_save_file(tipo_campania)
        if not save_file.exists():
            return None

        try:
            with open(save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return {
                "tipo_campania": data.get("tipo_campania", "tutorial"),
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
