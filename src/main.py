import flet as ft
import asyncio
from core.event_bus import bus
from core.theme import DesignTokens
from components.sidebar import Sidebar
from modules.dashboard import Dashboard
from modules.zones import Zones
from modules.security import Security
from modules.lab import Lab





class App(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.app_page = page
        self.expand = True
        self.age_protocol = None  # alpha (3-7), delta (8-12), or omega (13-16)
        self.current_module_container = ft.Container(
            expand=True,
            animate_opacity=300,
            opacity=1
        )
        self.active_module_instance = None
        self.sidebar = None
        
        self._setup_page()
        self.show_initialization()

    def _setup_page(self):
        self.app_page.title = "I.S.D.I // TERMINAL_INTERACTIVA"
        self.app_page.padding = 0
        self.app_page.spacing = 0
        self.app_page.theme_mode = ft.ThemeMode.LIGHT
        self.app_page.bgcolor = DesignTokens.COLORS["bg_dark"]
        
        self.app_page.fonts = DesignTokens.FONTS
        self.app_page.theme = ft.Theme(
            font_family="Inter",
            visual_density=ft.VisualDensity.COMPACT,
            color_scheme=ft.ColorScheme(
                primary=DesignTokens.COLORS["primary"],
                secondary=DesignTokens.COLORS["secondary"],
                surface=DesignTokens.COLORS["bg_dark"],
                on_surface="#1B1F1B",
                error=DesignTokens.COLORS["critical"],
            )
        )

    def show_initialization(self):
        """Pantalla de inicialización pedagógica (Narrativa I.S.D.I)"""
        terminal_text = ft.Text("", font_family="JetBrains Mono", color=DesignTokens.COLORS["primary"], size=12)
        
        self.content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.SMART_TOY_OUTLINED, size=50, color=DesignTokens.COLORS["primary"]),
                ft.Text("I.S.D.I // SECUENCIA DE ARRANQUE", size=20, weight="bold", font_family="JetBrains Mono"),
                ft.Divider(color=DesignTokens.COLORS["primary"], height=2, thickness=2),
                terminal_text,
            ], alignment="center", horizontal_alignment="center", spacing=20),
            alignment=ft.Alignment(0, 0),
            padding=50
        )
        
        self.app_page.update()
        
        # Ejecutar la secuencia de arranque de forma async-safe
        self.app_page.run_task(self._run_boot_sequence, terminal_text)

    async def _run_boot_sequence(self, terminal_text):
        """Secuencia de arranque async (~3.5s total)."""
        BOOT_LOGS = [
            "> [SISTEMA] Iniciando Núcleo I.S.D.I v4.0.2... LISTO",
            "> [RECORRIDO] Sincronizando protocolos pedagógicos... LISTO",
            "> [SEGURIDAD] Estableciendo perímetro digital seguro... LISTO",
            "> [DATOS] Indexando biblioteca de conocimientos... LISTO",
            "> [OK] SISTEMA PREPARADO. ESPERANDO SELECCIÓN DE NIVEL..."
        ]
        
        for log in BOOT_LOGS:
            terminal_text.value += f"\n{log}"
            try:
                self.app_page.update()
            except Exception:
                pass
            await asyncio.sleep(0.6)  # 0.6s × 5 = 3.0s
        
        # Pausa de estabilización para renderizado final
        await asyncio.sleep(0.5)  # Total: ~3.5s
            
        self.show_protocol_selection()

    def show_protocol_selection(self):
        """Selección de Protocolo por edad (Diseño Visual Premium)"""
        
        def select_protocol(protocol):
            self.age_protocol = protocol
            # Actualizar color primario según protocolo
            p_color = DesignTokens.get_protocol_color(protocol)
            self.app_page.theme.color_scheme.primary = p_color
            self.build_main_layout()
            self.navigate_to("dashboard")

        protocol_cards = [
            {
                "id": "alpha",
                "icon": ft.Icons.ROCKET_LAUNCH,
                "title": "PROTOCOLO ALPHA",
                "age": "3 - 7 AÑOS",
                "desc": "¡Exploradores del Espacio!",
                "color": DesignTokens.COLORS["primary"]
            },
            {
                "id": "delta",
                "icon": ft.Icons.TERMINAL,
                "title": "PROTOCOLO DELTA",
                "age": "8 - 12 AÑOS",
                "desc": "Lógica y Seguridad Activa",
                "color": DesignTokens.COLORS["secondary"]
            },
            {
                "id": "omega",
                "icon": ft.Icons.SHIELD_MOON,
                "title": "PROTOCOLO OMEGA",
                "age": "13 - 16 AÑOS",
                "desc": "Arquitectura y Ciberdefensa",
                "color": DesignTokens.COLORS["critical"]
            }
        ]

        cards_controls = []
        for card in protocol_cards:
            cards_controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(card["icon"], size=50, color=card["color"]),
                        ft.Text(card["title"], weight="bold", size=18, color=DesignTokens.get_text_main("alpha")),
                        ft.Text(card["age"], size=16, weight="bold", color=card["color"]),
                        ft.Text(card["desc"], size=10, italic=True, color=DesignTokens.get_text_dim("alpha"), text_align="center")
                    ], horizontal_alignment="center", spacing=8),
                    on_click=lambda _, p=card["id"]: select_protocol(p),
                    width=230, height=250,
                    padding=30,
                    border=ft.border.all(1, DesignTokens.get_glass_border(card["id"])),
                    border_radius=20,
                    bgcolor=ft.Colors.with_opacity(0.05, card["color"]),
                    ink=True,
                    animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE),
                    on_hover=lambda e: self._on_card_hover(e)
                )
            )

        self.content = ft.Container(
            content=ft.Column([
                ft.Text("INSTITUTO DE SEGURIDAD DIGITAL Y ARQUITECTURA", size=14, color=DesignTokens.get_text_dim("alpha"), font_family="JetBrains Mono", weight="bold"),
                ft.Text("SELECCIÓN DE NIVEL DE ACCESO", size=32, weight="bold", color=DesignTokens.get_text_main("alpha")),
                ft.Container(height=30),
                ft.Row(cards_controls, alignment="center", spacing=30, wrap=True)
            ], alignment="center", horizontal_alignment="center"),
            alignment=ft.Alignment(0, 0)
        )
        self.app_page.update()

    def _on_card_hover(self, e):
        e.control.scale = 1.05 if e.data == "true" else 1.0
        e.control.update()

    def build_main_layout(self):
        self.sidebar = Sidebar(on_nav_change=self.navigate_to, protocol=self.age_protocol)
        self.content = ft.Row(
            controls=[
                self.sidebar,
                ft.Container(
                    content=self.current_module_container,
                    expand=True,
                    padding=DesignTokens.get_spacing(2)
                )
            ],
            expand=True,
            spacing=0
        )
        self.app_page.update()

    def navigate_to(self, module_name: str):
        """Navegación centralizada y adaptativa."""
        if module_name == "dashboard":
            module = Dashboard(navigation_manager=self, protocol=self.age_protocol)
        elif module_name == "zones":
            module = Zones(navigation_manager=self, protocol=self.age_protocol)
        elif module_name == "security":
            module = Security(navigation_manager=self, protocol=self.age_protocol)
        elif module_name == "lab":
            module = Lab(navigation_manager=self, protocol=self.age_protocol)
        else:
            module = ft.Container(
                content=ft.Text(f"EN_DESARROLLO // MÓDULO_{module_name.upper()}", 
                               font_family="JetBrains Mono", color=DesignTokens.get_text_dim(self.age_protocol)),
                alignment=ft.Alignment(0, 0)
            )

        if self.active_module_instance and hasattr(self.active_module_instance, "cleanup"):
            self.active_module_instance.cleanup()

        # Animación de transición sin bloquear
        self.current_module_container.opacity = 0
        self.app_page.update()

        self.active_module_instance = module
        self.current_module_container.content = self.active_module_instance
        
        # Animación de entrada
        self.current_module_container.opacity = 1
        
        if self.sidebar:
            self.sidebar.set_active(module_name)
        
        bus.emit("nav_change", module_name)
        self.app_page.update()

def main(page: ft.Page):
    app = App(page)
    page.add(app)

import sys

if __name__ == "__main__":
    ft.app(target=main)
