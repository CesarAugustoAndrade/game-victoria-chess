"""
Estado de selección de niveles
"""

import pygame
from src.core.state import State
from src.ui.button import Button
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src.domain.levels import CampaniaNiveles
from src.utils.save_manager import save_manager


class NivelSelectorState(State):
    """Estado para seleccionar niveles de la campaña"""

    def __init__(self, game, campania=None, tipo_campania='tutorial', cargar_guardado=False):
        super().__init__(game)

        # Determinar qué tipo de campaña usar
        self.tipo_campania = tipo_campania

        # Cargar campaña: desde parámetro, desde guardado, o nueva
        if campania:
            self.campania = campania
        elif cargar_guardado:
            # Intentar cargar progreso guardado
            save_data = save_manager.load_campaign()
            if save_data:
                # Detectar tipo de campaña desde guardado
                saved_tipo = save_data.get('tipo_campania', 'tutorial')
                self.tipo_campania = saved_tipo

                if saved_tipo == 'galia':
                    from src.domain.campania_galia import CampaniaCesarGalia
                    self.campania = CampaniaCesarGalia.from_dict(save_data)
                else:
                    self.campania = CampaniaNiveles.from_dict(save_data)
                print(f"[SELECTOR] Campaña {saved_tipo} cargada - Progreso: {int(self.campania.progreso_campania * 100)}%")
            else:
                # Sin guardado, crear nueva según tipo
                self.campania = self._crear_campania_nueva(tipo_campania)
                print("[SELECTOR] No se encontró guardado, iniciando campaña nueva")
        else:
            # Nueva campaña del tipo especificado
            self.campania = self._crear_campania_nueva(tipo_campania)

        self.buttons = []
        self.scroll_offset = 0

        # Fuentes
        self.title_font = pygame.font.Font(None, 56)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.desc_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 18)

        self.setup_buttons()

    def _crear_campania_nueva(self, tipo_campania):
        """Crea una nueva campaña del tipo especificado"""
        if tipo_campania == 'galia':
            from src.domain.campania_galia import CampaniaCesarGalia
            return CampaniaCesarGalia()
        else:
            return CampaniaNiveles()

    def on_enter(self):
        """Reconstruir botones cuando se vuelve a este estado"""
        self.setup_buttons()

    def setup_buttons(self):
        """Crea los botones de niveles"""
        self.buttons = []

        # Botón de volver
        self.back_button = Button(
            20, 20, 120, 40,
            "< Volver",
            self.volver_menu
        )

        # Botones de niveles en grid
        levels_per_row = 3
        button_width = 250
        button_height = 160
        padding = 20
        start_x = (WINDOW_WIDTH - (levels_per_row * button_width + (levels_per_row - 1) * padding)) // 2
        start_y = 120

        for i, nivel in enumerate(self.campania.niveles):
            row = i // levels_per_row
            col = i % levels_per_row

            x = start_x + col * (button_width + padding)
            y = start_y + row * (button_height + padding)

            # Verificar si el nivel está desbloqueado
            esta_desbloqueado = i == 0 or (i - 1) in self.campania.niveles_completados

            button = NivelButton(
                x, y, button_width, button_height,
                nivel, esta_desbloqueado,
                lambda n=nivel.numero: self.seleccionar_nivel(n),
                self.desc_font, self.small_font
            )
            self.buttons.append(button)

    def seleccionar_nivel(self, numero_nivel: int):
        """Inicia el nivel seleccionado"""
        if self.campania.seleccionar_nivel(numero_nivel):
            from src.states.batalla_state import BatallaState
            nivel = self.campania.obtener_nivel_actual()
            # Pasar la campaña para que pueda guardar el progreso
            self.game.change_state(BatallaState(self.game, nivel, self.campania))

    def volver_menu(self):
        """Vuelve al selector de campañas"""
        from src.states.selector_campania_state import SelectorCampaniaState
        self.game.change_state(SelectorCampaniaState(self.game, es_continuar=False))

    def handle_event(self, event):
        """Maneja eventos del selector de niveles"""
        self.back_button.handle_event(event)
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt):
        """Actualiza el selector de niveles"""
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)
        for button in self.buttons:
            button.update(mouse_pos)

    def render(self, screen):
        """Renderiza el selector de niveles"""
        # Fondo
        screen.fill((230, 210, 180))

        # Bordes decorativos
        pygame.draw.rect(screen, (150, 100, 50), (0, 0, WINDOW_WIDTH, 80))

        # Título según tipo de campaña
        if self.tipo_campania == 'galia':
            titulo = "CÉSAR EN LA GALIA"
            color_titulo = (70, 120, 70)  # Verde galo
        else:
            titulo = "CAMPAÑA TUTORIAL"
            color_titulo = (139, 69, 19)  # Marrón romano

        title_text = self.title_font.render(titulo, True, color_titulo)
        title_rect = title_text.get_rect(centerx=WINDOW_WIDTH // 2, y=20)
        screen.blit(title_text, title_rect)

        # Progreso
        progreso = int(self.campania.progreso_campania * 100)
        progreso_text = self.desc_font.render(
            f"Progreso: {progreso}% ({len(self.campania.niveles_completados)}/{len(self.campania.niveles)})",
            True, (80, 60, 40)
        )
        screen.blit(progreso_text, (WINDOW_WIDTH // 2 - progreso_text.get_width() // 2, 65))

        # Botón volver
        self.back_button.render(screen)

        # Botones de niveles
        for button in self.buttons:
            button.render(screen)


class NivelButton(Button):
    """Botón especializado para mostrar información de un nivel"""

    def __init__(self, x, y, width, height, nivel, desbloqueado, callback, desc_font, small_font):
        super().__init__(x, y, width, height, nivel.nombre, callback)
        self.nivel = nivel
        self.desbloqueado = desbloqueado
        self.desc_font = desc_font
        self.small_font = small_font

        # Colores según dificultad
        dificultad_colors = {
            "facil": (100, 200, 100),
            "medio": (255, 200, 50),
            "dificil": (255, 100, 100)
        }
        self.dificultad_color = dificultad_colors.get(nivel.dificultad, (200, 200, 200))

    def render(self, screen):
        """Renderiza el botón de nivel con información"""
        # Color de fondo según estado
        if not self.desbloqueado:
            bg_color = (100, 100, 100)
            border_color = (60, 60, 60)
            text_color = (150, 150, 150)
        elif self.is_hovered:
            bg_color = (220, 200, 160)
            border_color = (139, 69, 19)
            text_color = (60, 40, 20)
        else:
            bg_color = (200, 180, 150)
            border_color = (100, 60, 20)
            text_color = (60, 40, 20)

        # Fondo del botón
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 3)

        if not self.desbloqueado:
            # Candado para niveles bloqueados
            lock_text = self.desc_font.render("🔒 BLOQUEADO", True, text_color)
            lock_rect = lock_text.get_rect(center=self.rect.center)
            screen.blit(lock_text, lock_rect)

            # Número del nivel
            numero_text = self.small_font.render(f"Nivel {self.nivel.numero}", True, text_color)
            screen.blit(numero_text, (self.rect.x + 10, self.rect.y + 10))
        else:
            # Número del nivel
            numero_surface = self.desc_font.render(f"Nivel {self.nivel.numero}", True, (139, 69, 19))
            screen.blit(numero_surface, (self.rect.x + 10, self.rect.y + 10))

            # Nombre del nivel
            nombre_surface = self.desc_font.render(self.nivel.nombre, True, text_color)
            nombre_rect = nombre_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + 40)
            screen.blit(nombre_surface, nombre_rect)

            # Descripción (multilinea)
            desc_words = self.nivel.descripcion.split()
            lines = []
            current_line = []
            for word in desc_words:
                test_line = ' '.join(current_line + [word])
                if self.small_font.size(test_line)[0] < self.rect.width - 20:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))

            y_offset = self.rect.y + 70
            for line in lines[:2]:  # Máximo 2 líneas
                desc_surface = self.small_font.render(line, True, text_color)
                desc_rect = desc_surface.get_rect(centerx=self.rect.centerx, y=y_offset)
                screen.blit(desc_surface, desc_rect)
                y_offset += 20

            # Barra de dificultad
            difficulty_text = f"Dificultad: {self.nivel.dificultad.upper()}"
            diff_surface = self.small_font.render(difficulty_text, True, self.dificultad_color)
            screen.blit(diff_surface, (self.rect.x + 10, self.rect.y + self.rect.height - 30))

            # Icono de tutorial
            if self.nivel.es_tutorial:
                tutorial_surface = self.small_font.render("📖 Tutorial", True, (50, 150, 200))
                screen.blit(tutorial_surface, (self.rect.x + 10, self.rect.y + self.rect.height - 50))
