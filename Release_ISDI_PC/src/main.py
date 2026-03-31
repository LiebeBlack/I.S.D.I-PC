"""
Módulo: main.py
Propósito: Punto de entrada y controlador principal de la aplicación I.S.D.I.
Archivo desarrollado por Yoangel Gómez
"""

import sys
import flet as ft
import asyncio
import time
import random

from core.event_bus import bus
from core.theme import DesignTokens
from components.sidebar import Sidebar
from modules.dashboard import Dashboard
from modules.zones import Zones
from modules.security import Security
from modules.lab import Lab


class App(ft.Container):
    """
    Controlador principal de la aplicación I.S.D.I.

    Responsabilidades:
        1. Configurar la página (tema, fuentes, fondo).
        2. Mostrar la secuencia de arranque pedagógica.
        3. Gestionar la selección de protocolo por edad.
        4. Construir el layout principal (Sidebar + área de contenido).
        5. Centralizar la navegación entre módulos con limpieza de recursos.
    """

    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.app_page              = page
        self.expand                = True
        self.age_protocol: str | None = None
        self.sidebar: Sidebar | None  = None
        self.active_module_instance   = None
        self.current_module_container = ft.Container(
            expand=True,
            animate_opacity=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            opacity=1,
        )

        # Configuración Maestro y Estado del Sistema (Persistente)
        self.master_volume: float = 0.8
        self.sfx_volume: float    = 0.5
        self.anim_intensity: str  = "Media"
        self.version: str         = "v4.2.0-STABLE"
        self.is_admin: bool       = False

        # Estado de telemetría y navegación
        self._current_module = None
        self._nav_history    = []

        # Referencia al fondo dinámico (se asigna en build_main_layout)
        self._bg_container: ft.Container | None = None
        self._blob_running = False

        self._setup_page()
        self.show_initialization()

    # ──────────────────────────────────────────────────────────────────────────
    # CONFIGURACIÓN DE PÁGINA
    # ──────────────────────────────────────────────────────────────────────────

    def _setup_page(self) -> None:
        """Aplica el tema global, fuentes y colores base a la página."""
        p = self.app_page
        p.title      = "I.S.D.I — Plataforma Educativa Digital"
        p.padding    = 0
        p.spacing    = 0
        p.theme_mode = ft.ThemeMode.LIGHT
        p.bgcolor    = None
        p.fonts      = DesignTokens.FONTS

        # Elementos para el Fondo Líquido Dinámico (Premium 2026)
        self.blobs = [
            ft.Container(width=600, height=600, border_radius=300, bgcolor=ft.Colors.with_opacity(0.20, DesignTokens.COLORS["primary"]), blur=ft.Blur(120, 120), left=-150, top=-150, animate_offset=ft.Animation(14000, "easeInOutSine")),
            ft.Container(width=700, height=700, border_radius=350, bgcolor=ft.Colors.with_opacity(0.15, DesignTokens.COLORS["secondary"]), blur=ft.Blur(140, 140), right=-200, bottom=-200, animate_offset=ft.Animation(18000, "easeInOutSine")),
            ft.Container(width=500, height=500, border_radius=250, bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.PURPLE_400), blur=ft.Blur(100, 100), left=200, bottom=50, animate_offset=ft.Animation(22000, "easeInOutSine")),
            ft.Container(width=450, height=450, border_radius=225, bgcolor=ft.Colors.with_opacity(0.10, ft.Colors.CYAN_400), blur=ft.Blur(90, 90), right=100, top=100, animate_offset=ft.Animation(20000, "easeInOutSine")),
        ]

        p.theme = ft.Theme(
            font_family="Inter",
            visual_density=ft.VisualDensity.COMPACT,
            color_scheme=ft.ColorScheme(
                primary=DesignTokens.COLORS["primary"],
                secondary=DesignTokens.COLORS["secondary"],
            ),
        )

    # ──────────────────────────────────────────────────────────────────────────
    # PANTALLA DE ARRANQUE
    # ──────────────────────────────────────────────────────────────────────────

    def show_initialization(self) -> None:
        """Muestra la pantalla de arranque con la secuencia de logs de terminal."""
        terminal_text = ft.Text(
            "",
            font_family="JetBrains Mono",
            color=DesignTokens.COLORS["primary"],
            size=12,
        )

        self.content = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.SMART_TOY_OUTLINED, size=56, color=DesignTokens.COLORS["primary"]),
                    ft.Text("I.S.D.I — Iniciando Sistema", size=22, weight="bold", font_family="JetBrains Mono", color=DesignTokens.get_text_main("alpha")),
                    ft.Divider(color=DesignTokens.COLORS["primary"], height=2, thickness=2),
                    terminal_text,
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20,
            ),
            alignment=ft.Alignment(0, 0),
            padding=50,
        )

        self.app_page.update()
        self.app_page.run_task(self._run_boot_sequence, terminal_text)

    async def _run_boot_sequence(self, terminal_text: ft.Text) -> None:
        """Secuencia de arranque asíncrona (~3.5 s total)."""
        boot_logs = [
            f"> Iniciando sistema I.S.D.I {self.version}...",
            "> Cargando protocolos de aprendizaje...",
            "> Estableciendo entorno seguro...",
            "> Indexando contenido educativo...",
            "> Todo listo. Selecciona tu nivel para comenzar.",
        ]

        for log in boot_logs:
            terminal_text.value += f"\n{log}"
            try:
                self.app_page.update()
            except Exception:
                pass
            await asyncio.sleep(0.55)

        await asyncio.sleep(0.45)
        self.show_protocol_selection()

    # ──────────────────────────────────────────────────────────────────────────
    # SELECCIÓN DE PROTOCOLO
    # ──────────────────────────────────────────────────────────────────────────

    def show_protocol_selection(self) -> None:
        """Muestra las tarjetas de selección de Protocolo (Alpha / Delta / Omega)."""

        def select_protocol(protocol: str) -> None:
            self.age_protocol = protocol
            p_color = DesignTokens.get_protocol_color(protocol)
            self.app_page.theme = ft.Theme(
                font_family="Inter",
                color_scheme=ft.ColorScheme(primary=p_color)
            )
            self.build_main_layout()
            self.navigate_to("zones")

        protocol_cards_data = [
            {"id": "alpha", "icon": ft.Icons.ROCKET_LAUNCH, "title": "Nivel Alpha", "age": "3 a 7 años", "desc": "Explora el mundo digital con juegos y colores.", "color": DesignTokens.COLORS["primary"]},
            {"id": "delta", "icon": ft.Icons.TERMINAL, "title": "Nivel Delta", "age": "8 a 12 años", "desc": "Aprende lógica, redes y seguridad básica.", "color": DesignTokens.COLORS["secondary"]},
            {"id": "omega", "icon": ft.Icons.SHIELD_MOON, "title": "Nivel Omega", "age": "13 a 16 años", "desc": "Diseña sistemas y domina la ciberdefensa.", "color": DesignTokens.COLORS["critical"]},
        ]

        cards = []
        for card in protocol_cards_data:
            cards.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(card["icon"], size=52, color=card["color"]),
                            ft.Text(card["title"], weight="bold", size=18, color=DesignTokens.get_text_main("alpha")),
                            ft.Text(card["age"], size=16, weight="bold", color=card["color"]),
                            ft.Text(card["desc"], size=11, italic=True, color=DesignTokens.get_text_dim("alpha"), text_align="center"),
                        ],
                        horizontal_alignment="center",
                        spacing=8,
                    ),
                    on_click=lambda _, p=card["id"]: select_protocol(p),
                    width=230, height=260, padding=30,
                    border=ft.border.all(1, DesignTokens.get_glass_border(card["id"])),
                    border_radius=20,
                    bgcolor=ft.Colors.with_opacity(0.05, card["color"]),
                    ink=True,
                    animate_scale=ft.Animation(250, ft.AnimationCurve.DECELERATE),
                    on_hover=lambda e: self._on_card_hover(e),
                )
            )

        self.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Instituto de Seguridad Digital e Interactiva", size=13, color=DesignTokens.get_text_dim("alpha"), font_family="JetBrains Mono", weight="bold"),
                    ft.Text("¿Cuántos años tienes?", size=32, weight="bold", color=DesignTokens.get_text_main("alpha")),
                    ft.Container(height=30),
                    ft.Row(cards, alignment="center", spacing=30, wrap=True),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            alignment=ft.Alignment(0, 0),
        )
        self.app_page.update()

    def _on_card_hover(self, e: ft.HoverEvent) -> None:
        """Efecto de escala al hacer hover sobre las tarjetas de protocolo."""
        e.control.scale = 1.06 if e.data == "true" else 1.0
        e.control.update()

    # ──────────────────────────────────────────────────────────────────────────
    # CONSOLA DE CONTROL (SETTINGS)
    # ──────────────────────────────────────────────────────────────────────────

    def show_settings(self, e) -> None:
        """Consola de Control de Sistema — Panel completo con Modo Admin."""
        protocol_color = DesignTokens.get_protocol_color(self.age_protocol)
        text_main = DesignTokens.get_text_main(self.age_protocol)
        text_dim  = DesignTokens.get_text_dim(self.age_protocol)

        def launch_link(url: str):
            self.app_page.launch_url(url)

        # ── FUNCIÓN: CAMBIAR TEMA ──
        def change_theme(mode: str) -> None:
            new_theme = ft.Theme(font_family="Inter")
            if mode == "sunrise":
                self.app_page.theme_mode = ft.ThemeMode.LIGHT
                bg_color = "#FFFFFF"
                self.blobs[0].bgcolor = ft.Colors.with_opacity(0.18, DesignTokens.COLORS["primary"])
                self.blobs[1].bgcolor = ft.Colors.with_opacity(0.12, DesignTokens.COLORS["secondary"])
                self.blobs[2].bgcolor = ft.Colors.with_opacity(0.10, ft.Colors.PURPLE_200)
                self.blobs[3].bgcolor = ft.Colors.with_opacity(0.08, ft.Colors.CYAN_200)
                new_theme.color_scheme = ft.ColorScheme(primary=protocol_color, surface="#FFFFFF", on_surface="#000000", on_surface_variant="#455A64")
            elif mode == "rest":
                self.app_page.theme_mode = ft.ThemeMode.LIGHT
                bg_color = "#FFF9E6"
                self.blobs[0].bgcolor = ft.Colors.with_opacity(0.28, ft.Colors.AMBER_400)
                self.blobs[1].bgcolor = ft.Colors.with_opacity(0.18, ft.Colors.ORANGE_400)
                self.blobs[2].bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.DEEP_ORANGE_200)
                self.blobs[3].bgcolor = ft.Colors.with_opacity(0.12, ft.Colors.YELLOW_500)
                new_theme.color_scheme = ft.ColorScheme(primary=protocol_color, surface="#FFF9E6", on_surface="#2D1B18", on_surface_variant="#5D4037")
            elif mode == "sleep":
                self.app_page.theme_mode = ft.ThemeMode.DARK
                bg_color = "#0A0A12"
                self.blobs[0].bgcolor = ft.Colors.with_opacity(0.25, ft.Colors.BLUE_ACCENT_700)
                self.blobs[1].bgcolor = ft.Colors.with_opacity(0.18, ft.Colors.PURPLE_ACCENT_400)
                self.blobs[2].bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.CYAN_500)
                self.blobs[3].bgcolor = ft.Colors.with_opacity(0.12, ft.Colors.PINK_400)
                new_theme.color_scheme = ft.ColorScheme(primary=protocol_color, surface="#0A0A12", on_surface="#FFFFFF", on_surface_variant="#B0BEC5")
            else:
                bg_color = "#FFFFFF"
            if self._bg_container:
                self._bg_container.bgcolor = bg_color
            self.app_page.theme = new_theme
            try:
                self.app_page.update()
            except Exception:
                pass

        # ── SECCIÓN: ILUMINACIÓN ──
        theme_section = ft.Container(
            content=ft.Column([
                ft.Text("AMBIENTE DE ILUMINACIÓN", size=10, weight="bold", color=protocol_color, font_family="JetBrains Mono"),
                ft.Container(height=8),
                ft.Row([
                    ft.Container(content=ft.Column([
                        ft.IconButton(icon=ft.Icons.WB_SUNNY_ROUNDED, icon_color=ft.Colors.AMBER_600, icon_size=28, on_click=lambda _: change_theme("sunrise"), tooltip="Modo claro",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.AMBER_600))),
                        ft.Text("Sunrise", size=10, weight="bold", color=text_dim),
                    ], horizontal_alignment="center", spacing=4)),
                    ft.Container(content=ft.Column([
                        ft.IconButton(icon=ft.Icons.COFFEE_ROUNDED, icon_color=ft.Colors.ORANGE_400, icon_size=28, on_click=lambda _: change_theme("rest"), tooltip="Modo descanso",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.ORANGE_400))),
                        ft.Text("Rest", size=10, weight="bold", color=text_dim),
                    ], horizontal_alignment="center", spacing=4)),
                    ft.Container(content=ft.Column([
                        ft.IconButton(icon=ft.Icons.NIGHTS_STAY_ROUNDED, icon_color=ft.Colors.INDIGO_300, icon_size=28, on_click=lambda _: change_theme("sleep"), tooltip="Modo oscuro",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.INDIGO_300))),
                        ft.Text("Sleep", size=10, weight="bold", color=text_dim),
                    ], horizontal_alignment="center", spacing=4)),
                ], alignment="center", spacing=30),
            ]),
            padding=16, bgcolor=ft.Colors.with_opacity(0.03, protocol_color), border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, protocol_color)),
        )

        # ── SECCIÓN: AUDIO ──
        audio_panel = ft.Container(
            content=ft.Column([
                ft.Text("CONTROL DE FRECUENCIAS (AUDIO)", size=10, weight="bold", color=protocol_color, font_family="JetBrains Mono"),
                ft.Container(height=8),
                ft.Row([
                    ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, size=16, color=protocol_color),
                    ft.Text("Volumen Maestro", size=12, expand=True, color=text_main),
                    ft.Slider(min=0, max=1, value=self.master_volume, active_color=protocol_color, width=180,
                              on_change=lambda ev: setattr(self, 'master_volume', ev.control.value))
                ]),
                ft.Row([
                    ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, size=16, color=DesignTokens.COLORS["secondary"]),
                    ft.Text("Efectos SFX", size=12, expand=True, color=text_main),
                    ft.Slider(min=0, max=1, value=self.sfx_volume, active_color=DesignTokens.COLORS["secondary"], width=180,
                              on_change=lambda ev: setattr(self, 'sfx_volume', ev.control.value))
                ])
            ], spacing=8),
            padding=16, bgcolor=ft.Colors.with_opacity(0.03, protocol_color), border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, protocol_color)),
        )

        # ── SECCIÓN: ANIMACIONES (FIX: usar e.control.selected) ──
        def _on_anim_change(ev):
            sel = ev.control.selected
            if sel:
                self.anim_intensity = next(iter(sel))

        anim_panel = ft.Container(
            content=ft.Column([
                ft.Text("DINÁMICA DE INTERFAZ", size=10, weight="bold", color=protocol_color, font_family="JetBrains Mono"),
                ft.Container(height=8),
                ft.SegmentedButton(
                    selected={self.anim_intensity},
                    on_change=_on_anim_change,
                    segments=[
                        ft.Segment(value="Baja", label=ft.Text("Baja")),
                        ft.Segment(value="Media", label=ft.Text("Media")),
                        ft.Segment(value="Alta", label=ft.Text("Alta")),
                    ],
                )
            ]),
            padding=16, bgcolor=ft.Colors.with_opacity(0.03, protocol_color), border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, protocol_color)),
        )

        # ── NODO DESARROLLADOR ──
        dev_node = ft.Container(
            content=ft.Column([
                ft.Text("NODO DE DESARROLLO CORE", size=10, weight="bold", color=protocol_color, font_family="JetBrains Mono"),
                ft.Container(height=8),
                ft.Row([
                    ft.Icon(ft.Icons.VERIFIED_USER_ROUNDED, color=DesignTokens.COLORS["accent"], size=18),
                    ft.Text("Yoangel Gómez (Liebe Black)", weight="bold", size=15, color=text_main),
                ], spacing=10),
                ft.Container(height=4),
                ft.Row([
                    ft.TextButton("GitHub", icon=ft.Icons.CODE_ROUNDED, on_click=lambda _: launch_link("https://github.com/LiebeBlack/I.S.D.I-PC")),
                    ft.TextButton("Contacto", icon=ft.Icons.EMAIL_ROUNDED, on_click=lambda _: launch_link("mailto:Liebeblack01@gmail.com")),
                ], spacing=5)
            ], spacing=2),
            padding=16, bgcolor=ft.Colors.with_opacity(0.04, protocol_color), border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, protocol_color)),
        )

        # ══════════════════════════════════════════════════════════════════════
        # CONSTRUIR CONTENIDO SEGÚN MODO
        # ══════════════════════════════════════════════════════════════════════

        if self.is_admin:
            dialog_content = self._build_admin_dialog_content(
                protocol_color, text_main, text_dim,
                theme_section, audio_panel, anim_panel, dev_node,
            )
            dialog_title_color = "#FFD600"
            dialog_title_text  = "CONSOLA ADMIN I.S.D.I"
            dialog_title_icon  = ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED
        else:
            dialog_content = self._build_visitor_dialog_content(
                protocol_color, text_main, text_dim,
                theme_section, audio_panel, anim_panel, dev_node,
            )
            dialog_title_color = protocol_color
            dialog_title_text  = "CONSOLA DE CONTROL I.S.D.I"
            dialog_title_icon  = ft.Icons.SETTINGS_OUTLINED

        # ═══ DIÁLOGO PRINCIPAL ═══
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(dialog_title_icon, color=dialog_title_color, size=24),
                ft.Text(dialog_title_text, size=16, weight="bold"),
                ft.Container(expand=True),
                ft.IconButton(ft.Icons.CLOSE_ROUNDED, icon_color=text_dim, icon_size=20,
                    on_click=lambda _: self.app_page.close(dialog), tooltip="Cerrar"),
            ], alignment="center", spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            content=dialog_content,
            shape=ft.RoundedRectangleBorder(radius=20),
        )

        self.app_page.open(dialog)

    # ──────────────────────────────────────────────────────────────────────────
    # MODO VISITANTE (NORMAL)
    # ──────────────────────────────────────────────────────────────────────────

    def _build_visitor_dialog_content(self, protocol_color, text_main, text_dim,
                                       theme_section, audio_panel, anim_panel, dev_node):
        """Construye el contenido del diálogo para modo visitante (no admin)."""

        admin_input = ft.TextField(
            label="Clave de Desarrollador", password=True, can_reveal_password=True,
            text_size=12, border_radius=10, width=280,
            text_style=ft.TextStyle(font_family="JetBrains Mono")
        )
        status_text = ft.Text("⬤ MODO VISITANTE", size=10, weight="bold", italic=True, color=text_dim)

        def validate_admin(_):
            pin = admin_input.value or ""
            if pin == "aidmind":
                self.is_admin = True
                self.version = "v4.2.0-ADMIN-UNLOCKED"
                # Cerrar y reabrir con panel admin
                try:
                    # Cerrar todos los overlays abiertos
                    for overlay in list(self.app_page.overlay):
                        try:
                            self.app_page.close(overlay)
                        except Exception:
                            pass
                except Exception:
                    pass
                self.show_settings(None)
                return
            else:
                status_text.value = "⬤ CLAVE INCORRECTA"
                status_text.color = DesignTokens.COLORS["critical"]
            try:
                self.app_page.update()
            except Exception:
                pass

        submit_btn = ft.ElevatedButton(
            "Verificar", icon=ft.Icons.LOCK_OPEN_ROUNDED, on_click=validate_admin,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=12),
        )
        admin_input.on_submit = validate_admin

        admin_panel = ft.Container(
            content=ft.Column([
                ft.Text("SEGURIDAD DE NÚCLEO", size=10, weight="bold", color=protocol_color, font_family="JetBrains Mono"),
                ft.Container(height=8),
                ft.Row([ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, size=14, color=text_dim), status_text]),
                ft.Row([admin_input, submit_btn], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ], spacing=10),
            padding=16, bgcolor=ft.Colors.with_opacity(0.03, protocol_color), border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, protocol_color)),
        )

        return ft.Column([
            theme_section, audio_panel, anim_panel, admin_panel, dev_node,
            ft.Container(height=8),
            ft.Row([
                ft.Text(f"V {self.version}", size=9, weight="bold", color=text_dim, font_family="JetBrains Mono"),
                ft.Container(expand=True),
                ft.Text("I.S.D.I — Isla Digital", size=10, italic=True, color=protocol_color),
            ])
        ], spacing=16, width=480, height=650, scroll=ft.ScrollMode.HIDDEN)

    # ──────────────────────────────────────────────────────────────────────────
    # MODO ADMINISTRADOR (COMPLETO)
    # ──────────────────────────────────────────────────────────────────────────

    def _build_admin_dialog_content(self, protocol_color, text_main, text_dim,
                                     theme_section, audio_panel, anim_panel, dev_node):
        """Construye el panel de administrador con herramientas de desarrollo completas."""
        from core.database import db
        from core.content import ContentEngine
        import platform

        GOLD = "#FFD600"  # Acento dorado admin

        # ── BADGE DE ADMIN ──
        def logout_admin(_):
            self.is_admin = False
            self.version = "v4.2.0-STABLE"
            for overlay in list(self.app_page.overlay):
                try:
                    self.app_page.close(overlay)
                except Exception:
                    pass
            self.show_settings(None)

        admin_badge = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, color=GOLD, size=18),
                ft.Text("MODO ADMINISTRADOR", size=12, weight="bold", color=GOLD, font_family="JetBrains Mono"),
                ft.Container(expand=True),
                ft.TextButton("Cerrar Sesión", icon=ft.Icons.LOGOUT_ROUNDED, on_click=logout_admin,
                    style=ft.ButtonStyle(color=DesignTokens.COLORS["critical"])),
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            bgcolor=ft.Colors.with_opacity(0.1, GOLD), border_radius=12,
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.3, GOLD)),
        )

        # ── HERRAMIENTA 1: INSPECTOR DEL SISTEMA ──
        flet_ver = "N/A"
        try:
            flet_ver = ft.version.version
        except Exception:
            pass

        sys_info = [
            ("Python",          f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"),
            ("Flet",            flet_ver),
            ("OS",              f"{platform.system()} {platform.release()}"),
            ("Protocolo",       (self.age_protocol or "N/A").upper()),
            ("Módulo Activo",   type(self.active_module_instance).__name__ if self.active_module_instance else "None"),
            ("Tema",            str(self.app_page.theme_mode).split(".")[-1]),
            ("Animaciones",     self.anim_intensity),
            ("Vol. Maestro",    f"{int(self.master_volume * 100)}%"),
            ("Vol. SFX",        f"{int(self.sfx_volume * 100)}%"),
            ("Admin",           "✓ ACTIVO"),
            ("DB Path",         db.db_path),
            ("Navegación",      f"{len(self._nav_history)} items en historial"),
        ]
        sys_rows = [
            ft.Row([
                ft.Text(lbl, size=10, weight="bold", color=GOLD, width=110, font_family="JetBrains Mono"),
                ft.Text(val, size=10, color=text_main, font_family="JetBrains Mono"),
            ], spacing=8)
            for lbl, val in sys_info
        ]

        sys_inspector = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.DEVELOPER_BOARD_ROUNDED, color=GOLD, size=16),
                        ft.Text("INSPECTOR DEL SISTEMA", size=10, weight="bold", color=GOLD, font_family="JetBrains Mono")], spacing=8),
                ft.Container(height=6),
                *sys_rows,
            ], spacing=3),
            padding=14, bgcolor=ft.Colors.with_opacity(0.06, GOLD), border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, GOLD)),
        )

        # ── HERRAMIENTA 2: VISOR DE BASE DE DATOS ──
        db_output = ft.Text("", font_family="JetBrains Mono", size=10, color=text_main, selectable=True)

        def show_db_progress(_):
            lines = []
            for proto in ["alpha", "delta", "omega"]:
                progress = db.get_progress(proto)
                lines.append(f"[{proto.upper()}] Completadas: {len(progress)}")
                for uid in progress:
                    lines.append(f"  ✓ {uid}")
            db_output.value = "\n".join(lines) if lines else "Sin progreso registrado."
            try: self.app_page.update()
            except: pass

        def show_db_responses(_):
            responses = db.get_responses()
            lines = []
            for row in responses[:20]:
                lines.append(f"[{row[0]}] {str(row[1])[:60]}{'...' if len(str(row[1])) > 60 else ''}")
                if len(row) > 2:
                    lines.append(f"  📅 {row[2]}")
            db_output.value = "\n".join(lines) if lines else "Sin respuestas guardadas."
            try: self.app_page.update()
            except: pass

        def show_db_stats(_):
            lines = ["=== ESTADÍSTICAS DB ==="]
            total_progress = 0
            total_responses = 0
            for proto in ["alpha", "delta", "omega"]:
                prog = db.get_progress(proto)
                total_progress += len(prog)
                lines.append(f"  [{proto.upper()}] {len(prog)} unidades completadas")
            responses = db.get_responses()
            total_responses = len(responses)
            lines.append(f"\n  Total progreso: {total_progress}")
            lines.append(f"  Total respuestas: {total_responses}")
            lines.append(f"  DB: {db.db_path}")
            db_output.value = "\n".join(lines)
            try: self.app_page.update()
            except: pass

        def clear_db_output(_):
            db_output.value = ""
            try: self.app_page.update()
            except: pass

        db_viewer = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.STORAGE_ROUNDED, color=GOLD, size=16),
                        ft.Text("VISOR DE BASE DE DATOS", size=10, weight="bold", color=GOLD, font_family="JetBrains Mono")], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    ft.ElevatedButton("Progreso", icon=ft.Icons.CHECKLIST_ROUNDED, on_click=show_db_progress,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8, bgcolor=ft.Colors.with_opacity(0.1, GOLD))),
                    ft.ElevatedButton("Respuestas", icon=ft.Icons.QUESTION_ANSWER_ROUNDED, on_click=show_db_responses,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8, bgcolor=ft.Colors.with_opacity(0.1, GOLD))),
                    ft.ElevatedButton("Stats", icon=ft.Icons.ANALYTICS_ROUNDED, on_click=show_db_stats,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8, bgcolor=ft.Colors.with_opacity(0.1, GOLD))),
                    ft.IconButton(ft.Icons.CLEAR_ALL_ROUNDED, icon_color=text_dim, on_click=clear_db_output, tooltip="Limpiar"),
                ], spacing=6, wrap=True),
                ft.Container(
                    content=ft.Column([db_output], scroll=ft.ScrollMode.AUTO),
                    padding=10, bgcolor=ft.Colors.with_opacity(0.04, GOLD), border_radius=8,
                    height=120, border=ft.border.all(1, ft.Colors.with_opacity(0.1, GOLD)),
                ),
            ], spacing=4),
            padding=14, bgcolor=ft.Colors.with_opacity(0.06, GOLD), border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, GOLD)),
        )

        # ── HERRAMIENTA 3: GESTOR DE PROGRESO ──
        progress_status = ft.Text("", font_family="JetBrains Mono", size=10, color=GOLD)

        def unlock_all_units(_):
            proto = self.age_protocol
            units = ContentEngine.get_all_units(proto)
            for unit in units:
                db.update_progress(proto, unit["id"])
            progress_status.value = f"✓ {len(units)} unidades desbloqueadas para [{proto.upper()}]"
            try: self.app_page.update()
            except: pass

        def unlock_all_protocols(_):
            count = 0
            for proto in ["alpha", "delta", "omega"]:
                units = ContentEngine.get_all_units(proto)
                for unit in units:
                    db.update_progress(proto, unit["id"])
                count += len(units)
            progress_status.value = f"✓ {count} unidades desbloqueadas en TODOS los protocolos"
            try: self.app_page.update()
            except: pass

        def reset_current_progress(_):
            db.reset_progress(self.age_protocol)
            progress_status.value = f"✓ Progreso eliminado para [{self.age_protocol.upper()}]"
            try: self.app_page.update()
            except: pass

        def reset_all_progress(_):
            for proto in ["alpha", "delta", "omega"]:
                db.reset_progress(proto)
            progress_status.value = "✓ Progreso eliminado para TODOS los protocolos."
            try: self.app_page.update()
            except: pass

        progress_mgr = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.TUNE_ROUNDED, color=GOLD, size=16),
                        ft.Text("GESTOR DE PROGRESO", size=10, weight="bold", color=GOLD, font_family="JetBrains Mono")], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.LOCK_OPEN_ROUNDED, size=14), ft.Text("Desbloquear Actual", size=11)], spacing=4),
                        on_click=unlock_all_units,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=10, bgcolor=DesignTokens.COLORS["accent"], color="white")),
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.KEY_ROUNDED, size=14), ft.Text("Desbloquear Todo", size=11)], spacing=4),
                        on_click=unlock_all_protocols,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=10, bgcolor="#FFD600", color="black")),
                ], spacing=6, wrap=True),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.RESTART_ALT_ROUNDED, size=14), ft.Text("Reset Actual", size=11)], spacing=4),
                        on_click=reset_current_progress,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=10, bgcolor=ft.Colors.ORANGE_700, color="white")),
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.DELETE_FOREVER_ROUNDED, size=14), ft.Text("Reset Global", size=11)], spacing=4),
                        on_click=reset_all_progress,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=10, bgcolor=DesignTokens.COLORS["critical"], color="white")),
                ], spacing=6, wrap=True),
                progress_status,
            ], spacing=6),
            padding=14, bgcolor=ft.Colors.with_opacity(0.06, GOLD), border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, GOLD)),
        )

        # ── HERRAMIENTA 4: MAPA DE CONTENIDO ──
        content_lines = []
        for proto in ["alpha", "delta", "omega"]:
            units = ContentEngine.get_all_units(proto)
            content_lines.append(f"[{proto.upper()}] {len(units)} unidades:")
            for u in units:
                quiz_count = len(u.get("quiz", []))
                content_lines.append(f"  • {u['id']}: {u['title']} ({quiz_count}Q)")

        content_map = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.MAP_ROUNDED, color=GOLD, size=16),
                        ft.Text("MAPA DE CONTENIDO", size=10, weight="bold", color=GOLD, font_family="JetBrains Mono")], spacing=8),
                ft.Container(height=6),
                ft.Container(
                    content=ft.Column([
                        ft.Text("\n".join(content_lines), font_family="JetBrains Mono", size=9, color=text_main, selectable=True),
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=10, bgcolor=ft.Colors.with_opacity(0.04, GOLD), border_radius=8,
                    height=150, border=ft.border.all(1, ft.Colors.with_opacity(0.1, GOLD)),
                ),
            ], spacing=4),
            padding=14, bgcolor=ft.Colors.with_opacity(0.06, GOLD), border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, GOLD)),
        )

        # ── HERRAMIENTA 5: MONITOR EVENT BUS ──
        event_log_text = ft.Text("Esperando...", font_family="JetBrains Mono", size=10, color=text_main, selectable=True)

        def show_bus_state(_):
            from core.event_bus import bus as event_bus
            lines = ["=== EVENT BUS STATE ==="]
            if hasattr(event_bus, '_listeners') and event_bus._listeners:
                for event_type, listeners in event_bus._listeners.items():
                    lines.append(f"  [{event_type}] → {len(listeners)} listener(s)")
            else:
                lines.append("  (vacío — sin suscripciones activas)")
            event_log_text.value = "\n".join(lines)
            try: self.app_page.update()
            except: pass

        def emit_test_event(_):
            from core.event_bus import bus as event_bus
            event_bus.emit("admin_test", {"source": "admin_console", "time": time.time()})
            event_log_text.value = f"✓ Evento 'admin_test' emitido a las {time.strftime('%H:%M:%S')}"
            try: self.app_page.update()
            except: pass

        event_monitor = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.CABLE_ROUNDED, color=GOLD, size=16),
                        ft.Text("MONITOR EVENT BUS", size=10, weight="bold", color=GOLD, font_family="JetBrains Mono")], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    ft.ElevatedButton("Ver Estado", icon=ft.Icons.VISIBILITY_ROUNDED, on_click=show_bus_state,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8, bgcolor=ft.Colors.with_opacity(0.1, GOLD))),
                    ft.ElevatedButton("Emitir Test", icon=ft.Icons.SEND_ROUNDED, on_click=emit_test_event,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8, bgcolor=ft.Colors.with_opacity(0.1, GOLD))),
                ], spacing=6),
                ft.Container(
                    content=ft.Column([event_log_text], scroll=ft.ScrollMode.AUTO),
                    padding=10, bgcolor=ft.Colors.with_opacity(0.04, GOLD), border_radius=8,
                    height=80, border=ft.border.all(1, ft.Colors.with_opacity(0.1, GOLD)),
                ),
            ], spacing=4),
            padding=14, bgcolor=ft.Colors.with_opacity(0.06, GOLD), border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, GOLD)),
        )

        # ── HERRAMIENTA 6: NAVEGACIÓN RÁPIDA DEV ──
        def nav_to(module_name):
            for overlay in list(self.app_page.overlay):
                try: self.app_page.close(overlay)
                except: pass
            self.navigate_to(module_name)

        def switch_protocol(proto):
            for overlay in list(self.app_page.overlay):
                try: self.app_page.close(overlay)
                except: pass
            self.age_protocol = proto
            p_color = DesignTokens.get_protocol_color(proto)
            self.app_page.theme = ft.Theme(font_family="Inter", color_scheme=ft.ColorScheme(primary=p_color))
            self.build_main_layout()
            self.navigate_to("zones")

        quick_nav = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.SPEED_ROUNDED, color=GOLD, size=16),
                        ft.Text("NAVEGACIÓN RÁPIDA DEV", size=10, weight="bold", color=GOLD, font_family="JetBrains Mono")], spacing=8),
                ft.Container(height=6),
                ft.Text("Módulos:", size=9, color=text_dim, weight="bold"),
                ft.Row([
                    ft.ElevatedButton("Zones", on_click=lambda _: nav_to("zones"), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8)),
                    ft.ElevatedButton("Lab", on_click=lambda _: nav_to("lab"), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8)),
                    ft.ElevatedButton("Security", on_click=lambda _: nav_to("security"), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8)),
                    ft.ElevatedButton("Dashboard", on_click=lambda _: nav_to("dashboard"), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8)),
                ], spacing=6, wrap=True),
                ft.Container(height=4),
                ft.Text("Cambiar Protocolo:", size=9, color=text_dim, weight="bold"),
                ft.Row([
                    ft.ElevatedButton("Alpha", on_click=lambda _: switch_protocol("alpha"),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8, bgcolor=DesignTokens.COLORS["primary"], color="white")),
                    ft.ElevatedButton("Delta", on_click=lambda _: switch_protocol("delta"),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8, bgcolor=DesignTokens.COLORS["secondary"], color="white")),
                    ft.ElevatedButton("Omega", on_click=lambda _: switch_protocol("omega"),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=8, bgcolor=DesignTokens.COLORS["critical"], color="white")),
                ], spacing=6),
            ], spacing=4),
            padding=14, bgcolor=ft.Colors.with_opacity(0.06, GOLD), border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, GOLD)),
        )

        debug_output = ft.Text("", font_family="JetBrains Mono", size=10, color=text_main, selectable=True)
        debug_input  = ft.TextField(
            label="Ejecutar expresión Python (eval)", text_size=11, border_radius=8,
            width=380, text_style=ft.TextStyle(font_family="JetBrains Mono")
        )

        def run_debug_expr(_):
            expr = debug_input.value or ""
            if not expr.strip():
                return
            try:
                result = eval(expr, {"self": self, "ft": ft, "db": db, "bus": bus,
                                     "DesignTokens": DesignTokens, "ContentEngine": ContentEngine,
                                     "sys": sys, "os": __import__('os')})
                debug_output.value = f">>> {expr}\n{repr(result)}"
            except Exception as ex:
                debug_output.value = f">>> {expr}\n❌ {type(ex).__name__}: {ex}"
            try: self.app_page.update()
            except: pass

        debug_input.on_submit = run_debug_expr

        debug_console = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.TERMINAL_ROUNDED, color=GOLD, size=16),
                        ft.Text("CONSOLA DE DEBUG", size=10, weight="bold", color=GOLD, font_family="JetBrains Mono")], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    debug_input,
                    ft.IconButton(ft.Icons.PLAY_ARROW_ROUNDED, icon_color=GOLD, on_click=run_debug_expr, tooltip="Ejecutar"),
                ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Column([debug_output], scroll=ft.ScrollMode.AUTO),
                    padding=10, bgcolor=ft.Colors.with_opacity(0.04, GOLD), border_radius=8,
                    height=80, border=ft.border.all(1, ft.Colors.with_opacity(0.1, GOLD)),
                ),
            ], spacing=4),
            padding=14, bgcolor=ft.Colors.with_opacity(0.06, GOLD), border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, GOLD)),
        )

        # ── HERRAMIENTA 8: THEME LAB ──
        color_preview = ft.Container(width=40, height=40, border_radius=20, bgcolor=protocol_color)

        def apply_custom_color(ev):
            hex_val = ev.control.value or ""
            if len(hex_val) >= 4 and hex_val.startswith("#"):
                color_preview.bgcolor = hex_val
                self.app_page.theme = ft.Theme(
                    font_family="Inter",
                    color_scheme=ft.ColorScheme(primary=hex_val)
                )
                try: self.app_page.update()
                except: pass

        theme_lab = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.PALETTE_ROUNDED, color=GOLD, size=16),
                        ft.Text("THEME LAB", size=10, weight="bold", color=GOLD, font_family="JetBrains Mono")], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    ft.Text("Color hex:", size=11, color=text_main),
                    ft.TextField(value=protocol_color, width=120, text_size=11, border_radius=8,
                                 text_style=ft.TextStyle(font_family="JetBrains Mono"), on_submit=apply_custom_color),
                    color_preview,
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    ft.Text("Presets:", size=9, color=text_dim),
                    *[ft.Container(width=24, height=24, border_radius=12, bgcolor=c, on_click=lambda _, c=c: (
                        setattr(self.app_page, 'theme', ft.Theme(font_family="Inter", color_scheme=ft.ColorScheme(primary=c))),
                        setattr(color_preview, 'bgcolor', c),
                        self.app_page.update() if True else None,
                    )) for c in ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#FF8A5C", "#6C5CE7"]],
                ], spacing=6),
            ], spacing=6),
            padding=14, bgcolor=ft.Colors.with_opacity(0.06, GOLD), border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, GOLD)),
        )

        # ═══ ENSAMBLAR PANEL ADMIN ═══
        return ft.Column([
            admin_badge,
            theme_section,
            audio_panel,
            anim_panel,
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.15, GOLD)),
            ft.Text("⚡ HERRAMIENTAS DE DESARROLLADOR", size=11, weight="bold", color=GOLD, font_family="JetBrains Mono"),
            sys_inspector,
            quick_nav,
            db_viewer,
            progress_mgr,
            content_map,
            event_monitor,
            theme_lab,
            debug_console,
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.15, GOLD)),
            dev_node,
            ft.Container(height=8),
            ft.Row([
                ft.Text(f"V {self.version}", size=9, weight="bold", color=GOLD, font_family="JetBrains Mono"),
                ft.Container(expand=True),
                ft.Text("I.S.D.I — Admin Console", size=10, italic=True, color=GOLD),
            ])
        ], spacing=14, width=540, height=720, scroll=ft.ScrollMode.HIDDEN)

    # ──────────────────────────────────────────────────────────────────────────
    # LAYOUT PRINCIPAL
    # ──────────────────────────────────────────────────────────────────────────

    def build_main_layout(self) -> None:
        """Construye el layout Sidebar + área de contenido tras seleccionar protocolo."""
        self.sidebar = Sidebar(
            on_nav_change=self.navigate_to,
            on_home=self.show_protocol_selection,
            protocol=self.age_protocol,
        )

        settings_button = ft.Container(
            content=ft.Row(
                [
                    ft.Container(expand=True),
                    ft.IconButton(
                        ft.Icons.SETTINGS_ROUNDED,
                        icon_size=28,
                        icon_color=DesignTokens.get_protocol_color(self.age_protocol),
                        tooltip="Ajustes y Más Opciones",
                        on_click=self.show_settings,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            bgcolor=ft.Colors.with_opacity(0.06, DesignTokens.get_protocol_color(self.age_protocol)),
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            padding=ft.padding.only(top=10, right=20)
        )

        initial_bg = "#FFFFFF" if self.app_page.theme_mode == ft.ThemeMode.LIGHT else "#0A0A12"

        self._bg_container = ft.Container(
            content=ft.Stack(self.blobs),
            expand=True,
            bgcolor=initial_bg,
        )

        self.content = ft.Stack(
            [
                self._bg_container,
                ft.Row(
                    controls=[
                        self.sidebar,
                        ft.Column(
                            [
                                settings_button,
                                ft.Container(
                                    content=self.current_module_container,
                                    expand=True,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                )
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True,
                    spacing=0,
                )
            ],
            expand=True
        )
        self.app_page.update()

        if not self._blob_running:
            self._blob_running = True
            self.app_page.run_task(self._animate_blobs_async)

    async def _animate_blobs_async(self) -> None:
        """Animación asíncrona de blobs — usa asyncio en lugar de threading."""
        while self._blob_running:
            for blob in self.blobs:
                blob.offset = ft.Offset(
                    random.uniform(-0.15, 0.25),
                    random.uniform(-0.15, 0.25)
                )
            try:
                self.app_page.update()
            except Exception:
                break
            await asyncio.sleep(8)

    # ──────────────────────────────────────────────────────────────────────────
    # NAVEGACIÓN CENTRALIZADA
    # ──────────────────────────────────────────────────────────────────────────

    def navigate_to(self, module_name: str) -> None:
        """Navega al módulo indicado, limpiando el anterior."""
        module_map = {
            "dashboard": Dashboard,
            "zones":     Zones,
            "security":  Security,
            "lab":       Lab,
        }

        module_class = module_map.get(module_name)
        if module_class:
            module = module_class(navigation_manager=self, protocol=self.age_protocol)
        else:
            module = ft.Container(
                content=ft.Text(f"Módulo '{module_name}' en desarrollo.", font_family="JetBrains Mono", color=DesignTokens.get_text_dim(self.age_protocol)),
                alignment=ft.Alignment(0, 0),
            )

        if self.active_module_instance and hasattr(self.active_module_instance, "cleanup"):
            self.active_module_instance.cleanup()

        self.current_module_container.opacity = 0
        try:
            self.app_page.update()
        except Exception:
            pass

        self.active_module_instance            = module
        self.current_module_container.content = module
        self.current_module_container.opacity = 1

        # Registrar en historial de navegación
        self._nav_history.append(module_name)

        if self.sidebar:
            self.sidebar.set_active(module_name)

        bus.emit("nav_change", module_name)

        try:
            self.app_page.update()
        except Exception:
            pass


# ──────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ──────────────────────────────────────────────────────────────────────────────

def main(page: ft.Page) -> None:
    """Función de entrada principal requerida por Flet."""
    page.title = "I.S.D.I - 2026 Plataforma Educativa"
    page.theme_mode = ft.ThemeMode.LIGHT
    app = App(page)
    page.add(app)


if __name__ == "__main__":
    ft.app(target=main)
