import flet as ft
import asyncio
import random
import time
from base.module import BaseModule
from core.theme import DesignTokens
from core.content import ContentEngine
from components.glass_container import GlassContainer


class Dashboard(BaseModule):
    def __init__(self, navigation_manager=None, protocol="alpha"):
        super().__init__(navigation_manager, protocol)
        self.protocol_data = ContentEngine.PROTOCOLS.get(self.protocol, ContentEngine.PROTOCOLS["alpha"])
        self.protocol_color = DesignTokens.get_protocol_color(self.protocol)
        
        # Escenarios adaptados por protocolo (Edad)
        data = ContentEngine.DASHBOARD.get(self.protocol, ContentEngine.DASHBOARD["alpha"])
        self.title_text = data["title"]
        self.status_labels = data["labels"]
        self.mission_desc = data["mission"]
            
        self.metric_controls = {}
        self._telemetry_active = True
        self._telemetry_task_started = False
        self.initialize()

    def build(self):
        # Header
        header = ft.Row([
            ft.Column([
                ft.Text(self.title_text, 
                        size=28, 
                        font_family="JetBrains Mono",
                        weight=ft.FontWeight.BOLD,
                        color=self.protocol_color),
                ft.Row([
                    ft.Container(width=10, height=10, bgcolor=DesignTokens.COLORS["accent"], border_radius=5),
                    ft.Text(f"ACCESO AUTORIZADO // NIVEL_{self.protocol.upper()}", size=11, color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono"),
                ], spacing=8),
            ], spacing=2),
            ft.Container(expand=True),
            GlassContainer(
                content=ft.Row([
                    ft.Icon(ft.Icons.SHIELD, color=DesignTokens.COLORS["accent"], size=16),
                    ft.Text("CIFRADO ACTIVO: AES-256", size=10, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
                ], spacing=8),
                padding=ft.padding.symmetric(horizontal=15, vertical=8),
                protocol=self.protocol
            )
        ])

        # Tarjeta de Bienvenida
        welcome_card = GlassContainer(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.AUTO_AWESOME, size=40, color=self.protocol_color),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.1, self.protocol_color),
                    border_radius=15,
                ),
                ft.VerticalDivider(width=20, color="transparent"),
                ft.Column([
                    ft.Text(f"BIENVENIDO A LA {self.protocol_data['name']}", size=22, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
                    ft.Text(self.mission_desc, size=14, color=DesignTokens.get_text_dim(self.protocol)),
                    ft.Container(height=5),
                    ft.Row([
                        ft.ElevatedButton(
                            "Comenzar Misión", 
                            icon=ft.Icons.PLAY_ARROW,
                            style=ft.ButtonStyle(
                                bgcolor=self.protocol_color,
                                color=ft.Colors.WHITE,
                            ),
                            on_click=lambda _: self.nav.navigate_to("zones")
                        ),
                        ft.TextButton(
                            "Manual de Protocolo", 
                            icon=ft.Icons.BOOK_OUTLINED,
                            style=ft.ButtonStyle(
                                color=DesignTokens.get_text_dim(self.protocol)
                            )
                        )
                    ], spacing=15)
                ], expand=True, spacing=5)
            ]),
            padding=30,
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.3, self.protocol_color)),
            protocol=self.protocol
        )

        # Sección de Telemetría
        telemetry_grid = ft.Row(
            spacing=20,
            wrap=True,
            controls=[self._create_telemetry_card(label) for label in self.status_labels]
        )

        # Barra de información inferior
        info_bar = ft.Container(
            content=ft.Row([
                ft.Text("SISTEMA_OPERATIVO: ISDI_OS_4.0", size=10, color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono"),
                ft.Container(expand=True),
                ft.Text(f"REGISTRO: {time.strftime('%d/%m/%Y %H:%M')}", size=10, color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono"),
            ]),
            padding=10,
            border=ft.border.only(top=ft.BorderSide(1, DesignTokens.get_glass_border(self.protocol)))
        )

        return ft.Column(
            controls=[
                header,
                ft.Divider(height=40, color=DesignTokens.get_glass_border(self.protocol)),
                welcome_card,
                ft.Container(height=30),
                ft.Row([
                    ft.Icon(ft.Icons.MONITOR_HEART, color=self.protocol_color, size=18),
                    ft.Text("DIAGNÓSTICO DE SISTEMAS EN TIEMPO REAL", size=14, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
                ], spacing=10),
                ft.Container(height=15),
                telemetry_grid,
                ft.Container(expand=True),
                info_bar
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0
        )

    def _create_telemetry_card(self, label):
        val_control = ft.Text("0%", size=32, font_family="JetBrains Mono", weight="bold", color=DesignTokens.get_text_main(self.protocol))
        self.metric_controls[label] = val_control
        
        progress_bar = ft.ProgressBar(value=0, color=self.protocol_color, bgcolor=ft.Colors.with_opacity(0.1, self.protocol_color), height=6, border_radius=3)
        # Store ref to progress bar for easier update
        val_control.data = progress_bar 
        
        return GlassContainer(
            content=ft.Column([
                ft.Row([
                    ft.Text(label.upper(), size=11, color=self.protocol_color, weight="bold", font_family="JetBrains Mono"),
                    ft.Container(expand=True),
                    ft.Icon(ft.Icons.SIGNAL_CELLULAR_ALT, size=12, color=self.protocol_color),
                ]),
                ft.Divider(height=10, color="transparent"),
                val_control,
                ft.Container(height=5),
                progress_bar,
            ], spacing=2),
            width=230,
            height=140,
            padding=20,
            protocol=self.protocol
        )

    def did_mount(self):
        """Se llama cuando el control se monta en la página. Inicia la telemetría."""
        if not self._telemetry_task_started:
            self._telemetry_task_started = True
            self.page.run_task(self._update_telemetry_async)

    def cleanup(self):
        self._telemetry_active = False

    async def _update_telemetry_async(self):
        """Actualización de telemetría async-safe (compatible con Pyodide)."""
        await asyncio.sleep(1.0)
        while self._telemetry_active:
            try:
                # Check if still attached to a session
                if not self.page or self.page.session_id is None:
                    break
                    
                for label, control in self.metric_controls.items():
                    val = random.randint(88, 100)
                    control.value = f"{val}%"
                    # Using stored ref in .data for performance and safety
                    if hasattr(control, "data") and control.data:
                        control.data.value = val / 100
                
                try:
                    self.update()
                except Exception:
                    pass
                await asyncio.sleep(2.5)
            except Exception:
                break
