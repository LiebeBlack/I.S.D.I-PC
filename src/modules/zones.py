import flet as ft
from base.module import BaseModule
from core.theme import DesignTokens
from core.content import ContentEngine
from core.database import db
from components.glass_container import GlassContainer
from components.technical_diagram import TechnicalDiagram

class Zones(BaseModule):
    def __init__(self, navigation_manager=None, protocol="alpha"):
        super().__init__(navigation_manager, protocol)
        self.protocol_data = ContentEngine.PROTOCOLS.get(self.protocol, ContentEngine.PROTOCOLS["alpha"])
        self.units = ContentEngine.get_all_units(self.protocol)
        self.current_view = "list" # "list" or "detail"
        self.selected_unit = None
        self.immersive_mode = False
        self.challenge_input = ft.TextField(
            label="TU RESPUESTA O REFLEXIÓN",
            multiline=True,
            min_lines=3,
            border_color=DesignTokens.get_glass_border(self.protocol),
            focused_border_color=DesignTokens.COLORS["accent"],
            cursor_color=DesignTokens.get_protocol_color(self.protocol),
            label_style=ft.TextStyle(color=DesignTokens.get_text_dim(self.protocol), weight="bold"),
            text_style=ft.TextStyle(color=DesignTokens.get_text_main(self.protocol)),
            bgcolor=ft.Colors.with_opacity(0.05, DesignTokens.get_protocol_color(self.protocol)),
        )
        self.initialize()

    def build(self):
        if self.current_view == "list":
            return self._build_list_view()
        else:
            return self._build_detail_view()

    def _build_list_view(self):
        title_color = DesignTokens.get_protocol_color(self.protocol)
        completed_units = db.get_progress(self.protocol)
        
        # Titulo adaptado por protocolo
        if self.protocol == "alpha":
            title_main = "MAPA DE AVENTURAS"
            subtitle = f"> EXPLORANDO EL NIVEL {self.protocol_data['age_range']}"
        elif self.protocol == "delta":
            title_main = "SECTORES DE APRENDIZAJE"
            subtitle = f"> BASE DE DATOS OPERACIONAL // NIVEL_{self.protocol_data['age_range']}"
        else: # omega
            title_main = "TOPOLOGÍA DEL CONOCIMIENTO"
            subtitle = f"> INFRAESTRUCTURA CRÍTICA // NIVEL_{self.protocol_data['age_range']}"

        header = ft.Row([
            ft.Column([
                ft.Text(title_main, 
                        size=22, 
                        font_family="JetBrains Mono",
                        weight=ft.FontWeight.BOLD,
                        color=title_color),
                ft.Text(subtitle, size=10, color=DesignTokens.get_text_dim(self.protocol)),
            ], spacing=0),
            ft.Container(expand=True),
            ft.Text(f"PROGRESO: {len(completed_units)}/{len(self.units)}", size=11, weight="bold", color=DesignTokens.get_text_dim(self.protocol))
        ])

        # Fichas de Estadísticas
        stats = ft.Row([
            self._create_stat_chip(ft.Icons.AUTO_AWESOME, f"{len(completed_units)} Completados", DesignTokens.COLORS["accent"]),
            self._create_stat_chip(ft.Icons.LOCK_OPEN, f"{len(self.units) - len(completed_units)} Pendientes", DesignTokens.COLORS["warning"]),
        ], spacing=10)

        units_list = ft.Column(
            spacing=20,
            controls=[self._create_unit_card(unit, unit["id"] in completed_units) for unit in self.units],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        return ft.Column(
            controls=[
                header,
                ft.Divider(height=10, color="transparent"),
                stats,
                ft.Divider(height=20, color=DesignTokens.get_glass_border(self.protocol)),
                ft.Row([
                    ft.Icon(ft.Icons.SEARCH, size=14, color=DesignTokens.get_text_dim(self.protocol)),
                    ft.Text("CARGANDO SECTORES DISPONIBLES...", size=11, color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono"),
                ], spacing=8),
                ft.Container(height=10),
                units_list,
            ],
            expand=True
        )

    def _create_stat_chip(self, icon, label, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=14, color=color),
                ft.Text(label, size=11, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
            ], spacing=5),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            bgcolor=ft.Colors.with_opacity(0.1, color),
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, color))
        )

    def _create_unit_card(self, unit, completed):
        protocol_color = DesignTokens.get_protocol_color(self.protocol)
        
        return GlassContainer(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.CHECK_CIRCLE if completed else getattr(ft.Icons, unit["icon"], ft.Icons.BOOK), 
                        color=DesignTokens.COLORS["accent"] if completed else protocol_color, 
                        size=30
                    ),
                    padding=15,
                    bgcolor=ft.Colors.with_opacity(0.1, DesignTokens.COLORS["accent"] if completed else protocol_color),
                    border_radius=12,
                ),
                ft.VerticalDivider(width=20, color="transparent"),
                ft.Column([
                    ft.Text(unit["title"].upper(), size=16, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
                    ft.Text(unit["intro"], size=12, color=DesignTokens.get_text_dim(self.protocol), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                ], expand=True, spacing=2),
                ft.IconButton(
                    icon=ft.Icons.ARROW_FORWARD_IOS,
                    icon_color=protocol_color,
                    icon_size=16,
                    on_click=lambda _, u=unit: self._open_unit_detail(u)
                )
            ]),
            padding=15,
            border=ft.border.all(1, DesignTokens.COLORS["accent"] if completed else DesignTokens.get_glass_border(self.protocol)),
            on_click=lambda _, u=unit: self._open_unit_detail(u),
            protocol=self.protocol
        )

    def _build_detail_view(self):
        protocol_color = DesignTokens.get_protocol_color(self.protocol)
        unit = self.selected_unit
        
        return ft.Column([
            # Cabecera de Módulo
            ft.Row([
                ft.IconButton(
                    ft.Icons.ARROW_BACK_ROUNDED, 
                    icon_color=protocol_color, 
                    on_click=lambda _: self._back_to_list(),
                    tooltip="Volver al Mapa"
                ),
                ft.Column([
                    ft.Text(unit["title"].upper(), size=24, weight="bold", color=DesignTokens.get_text_main(self.protocol), font_family="Lexend"),
                    ft.ProgressBar(value=0.4, color=protocol_color, bgcolor=ft.Colors.with_opacity(0.1, protocol_color), height=4, width=300),
                ], spacing=2, expand=True),
                ft.Switch(label="ENFOQUE", on_change=self._toggle_immersive, active_color=protocol_color)
            ]),
            ft.Divider(height=10, color="transparent"),
            
            # Contenido Desplazable
            ft.Column([
                # 1. Introducción
                self._create_section("01 // MISIÓN", unit["intro"], ft.Icons.LIGHTBULB_ROUNDED),
                
                # 2. Análisis (Con Diagrama)
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.ACCOUNT_TREE_ROUNDED, color=protocol_color, size=18),
                            ft.Text("02 // ESTRUCTURA", size=14, weight="bold", color=protocol_color, font_family="JetBrains Mono"),
                        ], spacing=10),
                        ft.Divider(height=10, color="transparent"),
                        ft.Text(unit["architecture"], size=14, color=DesignTokens.get_text_main(self.protocol), text_align=ft.TextAlign.JUSTIFY),
                        ft.Container(height=15),
                        TechnicalDiagram(unit_id=unit["id"], protocol=self.protocol),
                    ]),
                    padding=25,
                    border=ft.border.all(1, DesignTokens.get_glass_border(self.protocol)),
                    border_radius=15,
                    bgcolor=ft.Colors.with_opacity(0.08, protocol_color)
                ),

                # 3. Dato Curioso
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, color=DesignTokens.COLORS["warning"], size=20),
                        ft.VerticalDivider(width=10, color="transparent"),
                        ft.Column([
                            ft.Text("¿SABÍAS QUE...?", size=10, weight="bold", color=DesignTokens.COLORS["warning"]),
                            ft.Text(unit.get("fact", ""), size=13, color=DesignTokens.get_text_main(self.protocol), italic=True),
                        ], expand=True)
                    ]),
                    padding=15,
                    bgcolor=ft.Colors.with_opacity(0.05, DesignTokens.COLORS["warning"]),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, DesignTokens.COLORS["warning"])),
                    border_radius=10
                ),
                
                # 4. Seguridad
                self._create_section("03 // BUENAS PRÁCTICAS", unit["security"], ft.Icons.GPP_GOOD_ROUNDED),
                
                # 5. Desafío
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, color=DesignTokens.COLORS["accent"], size=24),
                            ft.Text("DESAFÍO FIN DE SECTOR", size=18, weight="bold", color=DesignTokens.COLORS["accent"], font_family="Lexend"),
                        ], spacing=12),
                        ft.Divider(height=10, color="transparent"),
                        ft.Text(unit["challenge"], size=15, color=DesignTokens.get_text_main(self.protocol)),
                        ft.Container(height=15),
                        self.challenge_input,
                        ft.Container(height=15),
                        ft.Row([
                            ft.ElevatedButton(
                                content=ft.Text("COMPLETAR Y GUARDAR", weight="bold"),
                                icon=ft.Icons.CLOUD_DONE_ROUNDED,
                                on_click=lambda _: self._save_challenge(unit),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=DesignTokens.COLORS["accent"],
                                    padding=20,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                )
                            ),
                            ft.TextButton(
                                "Ayuda del Maestro", 
                                icon=ft.Icons.HELP_OUTLINE_ROUNDED, 
                                style=ft.ButtonStyle(
                                    color=DesignTokens.get_text_dim(self.protocol)
                                )
                            )
                        ], spacing=15)
                    ]),
                    padding=30,
                    border=ft.border.all(2, DesignTokens.COLORS["accent"]),
                    border_radius=15,
                    bgcolor=ft.Colors.with_opacity(0.1, DesignTokens.COLORS["accent"])
                ),

                # 6. Mini Quiz Interactivo
                self._build_quiz(unit)
            ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=25)
        ], expand=True)

    def _build_quiz(self, unit):
        if "quiz" not in unit:
            return ft.Container()
            
        questions = unit["quiz"]
        protocol_color = DesignTokens.get_protocol_color(self.protocol)
        
        quiz_controls = []
        for q_data in questions:
            options = []
            for i, opt in enumerate(q_data["a"]):
                options.append(
                    ft.ElevatedButton(
                        opt,
                        on_click=lambda e, idx=i, correct=q_data["c"]: self._check_answer(e, idx, correct),
                        style=ft.ButtonStyle(
                            color=DesignTokens.get_text_main(self.protocol),
                            bgcolor=ft.Colors.with_opacity(0.05, protocol_color),
                            padding=15,
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    )
                )
            
            quiz_controls.append(
                ft.Column([
                    ft.Text(q_data["q"], size=16, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
                    ft.Container(height=10),
                    ft.Row(options, wrap=True, spacing=10)
                ])
            )

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.QUIZ_ROUNDED, color=DesignTokens.COLORS["tertiary"], size=24),
                    ft.Text("AUTO-EVALUACIÓN RÁPIDA", size=18, weight="bold", color=DesignTokens.COLORS["tertiary"], font_family="Lexend"),
                ], spacing=12),
                ft.Divider(height=10, color="transparent"),
                *quiz_controls
            ]),
            padding=30,
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.3, DesignTokens.COLORS["tertiary"])),
            border_radius=15,
            bgcolor=ft.Colors.with_opacity(0.05, DesignTokens.COLORS["tertiary"])
        )

    def _check_answer(self, e, selected, correct):
        if selected == correct:
            e.control.bgcolor = DesignTokens.COLORS["accent"]
            e.control.color = ft.Colors.WHITE
            e.control.text = "¡CORRECTO!"
        else:
            e.control.bgcolor = DesignTokens.COLORS["critical"]
            e.control.color = ft.Colors.WHITE
            e.control.text = "INTENTA OTRA VEZ"
        e.control.update()

    def _create_section(self, title, text, icon):
        protocol_color = DesignTokens.get_protocol_color(self.protocol)
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, color=protocol_color, size=18),
                    ft.Text(title, size=14, weight="bold", color=protocol_color, font_family="JetBrains Mono"),
                ], spacing=10),
                ft.Divider(height=10, color="transparent"),
                ft.Text(text, size=14, color=DesignTokens.get_text_main(self.protocol), text_align=ft.TextAlign.JUSTIFY),
            ]),
            padding=25,
            border=ft.border.all(1, DesignTokens.get_glass_border(self.protocol)),
            border_radius=15,
            bgcolor=ft.Colors.with_opacity(0.08, protocol_color)
        )

    def _toggle_immersive(self, e):
        self.immersive_mode = e.control.value
        if self.nav and self.nav.sidebar:
            self.nav.sidebar.visible = not self.immersive_mode
            self.nav.app_page.update()
        self.update()

    def _open_unit_detail(self, unit):
        self.selected_unit = unit
        self.current_view = "detail"
        self.challenge_input.value = ""
        self.initialize()
        self.update()

    def _back_to_list(self):
        self.current_view = "list"
        self.selected_unit = None
        self.initialize()
        self.update()

    def _save_challenge(self, unit):
        if not self.challenge_input.value:
            return
            
        db.save_response(self.protocol, unit["id"], self.challenge_input.value)
        db.update_progress(self.protocol, unit["id"])
        self._back_to_list()
