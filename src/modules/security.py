import flet as ft
from base.module import BaseModule
from core.theme import DesignTokens
from core.content import ContentEngine
from components.glass_container import GlassContainer

class Security(BaseModule):
    def __init__(self, navigation_manager=None, protocol="alpha"):
        super().__init__(navigation_manager, protocol)
        data = ContentEngine.SECURITY_METRICS.get(self.protocol, ContentEngine.SECURITY_METRICS["alpha"])
        self.title_text = data["title"]
        self.metrics_raw = data["metrics"]
        self.protocol_color = DesignTokens.get_protocol_color(self.protocol)
        
        self.initialize()

    def build(self):
        # Cabecera
        header = ft.Row([
            ft.Column([
                ft.Text(self.title_text, 
                        size=28, 
                        font_family="JetBrains Mono",
                        weight=ft.FontWeight.BOLD,
                        color=self.protocol_color),
                ft.Row([
                    ft.Icon(ft.Icons.LOCK_OUTLINE_ROUNDED, size=14, color=DesignTokens.get_text_dim(self.protocol)),
                    ft.Text(f"INFRAESTRUCTURA_ESTADO: SEGURO", size=11, color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono"),
                ], spacing=8),
            ], spacing=2),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SYNC, size=15, color=DesignTokens.COLORS["accent"]),
                    ft.Text("SINCRONIZANDO...", size=10, weight="bold", color=DesignTokens.COLORS["accent"]),
                ], spacing=5),
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border=ft.border.all(1, DesignTokens.COLORS["accent"]),
                border_radius=15,
            )
        ])

        # Cuadrícula de Métricas
        metrics_row = ft.Row(
            wrap=True,
            spacing=20,
            controls=[self._create_metric_card(m) for m in self.metrics_raw]
        )

        return ft.Column(
            controls=[
                header,
                ft.Divider(height=40, color=DesignTokens.get_glass_border(self.protocol)),
                ft.Row([
                    ft.Icon(ft.Icons.DASHBOARD_ROUNDED, color=self.protocol_color, size=18),
                    ft.Text("MÉTRICAS DE SEGURIDAD EN VIVO", size=14, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
                ], spacing=10),
                ft.Container(height=15),
                metrics_row,
                ft.Container(height=40),
                ft.Row([
                    ft.Icon(ft.Icons.GPP_MAYBE, color=DesignTokens.COLORS["warning"], size=18),
                    ft.Text("PROTOCOLOS DE ÉTICA Y BUENAS PRÁCTICAS", size=14, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
                ], spacing=10),
                ft.Container(height=15),
                ft.Row([
                    ft.Column([
                        self._get_best_practices(),
                    ], expand=True),
                    ft.VerticalDivider(width=30, color="transparent"),
                    ft.Column([
                        ft.Text("TERMINAL DE COMANDOS", size=14, weight="bold", color=self.protocol_color, font_family="JetBrains Mono"),
                        self._create_terminal_simulator(),
                    ], expand=True),
                ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

    def _create_terminal_simulator(self):
        self.term_output = ft.Text("Esperando comandos...", font_family="JetBrains Mono", size=11, color=DesignTokens.get_text_main(self.protocol))
        
        def run_cmd(cmd):
            logs = {
                "audit": ["> Iniciando auditoría de procesos...", "> Analizando privilegios...", "> [OK] No se detectaron anomalías."],
                "firewall": ["> Consultando estado del firewall...", "> Puertos detectados: 80, 443, 22...", "> [ESTADO] Perímetro activo y seguro."],
                "clear": ["Consola despejada."]
            }
            if cmd == "clear":
                self.term_output.value = ""
            else:
                lines = logs.get(cmd, [f"> Error: Comando '{cmd}' no reconocido."])
                self.term_output.value = "\n".join(lines)
            self.term_output.update()

        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=self.term_output,
                    padding=15,
                    bgcolor="#000000" if self.protocol == "omega" else ft.Colors.with_opacity(0.1, self.protocol_color),
                    border_radius=10,
                    height=150,
                ),
                ft.Row([
                    ft.ElevatedButton("AUDIT_KERN", on_click=lambda _: run_cmd("audit"), bgcolor=ft.Colors.with_opacity(0.1, self.protocol_color), color=self.protocol_color),
                    ft.ElevatedButton("FW_STATUS", on_click=lambda _: run_cmd("firewall"), bgcolor=ft.Colors.with_opacity(0.1, self.protocol_color), color=self.protocol_color),
                    ft.IconButton(ft.Icons.DELETE_SWEEP_ROUNDED, on_click=lambda _: run_cmd("clear"), icon_color=DesignTokens.get_text_dim(self.protocol))
                ], spacing=10)
            ]),
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.05, self.protocol_color),
            border_radius=15,
            border=ft.border.all(1, DesignTokens.get_glass_border(self.protocol))
        )

    def _create_metric_card(self, metric):
        icon = getattr(ft.Icons, metric["icon_name"], ft.Icons.SHIELD_ROUNDED)
        color = DesignTokens.COLORS.get(metric["color_key"], self.protocol_color)
        
        return GlassContainer(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon, color=color, size=30),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    border_radius=10,
                ),
                ft.Divider(height=10, color="transparent"),
                ft.Text(metric["label"].upper(), size=11, color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono", weight="bold"),
                ft.Text(metric["value"], size=22, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
            ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=230,
            height=160,
            protocol=self.protocol,
            padding=20,
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.2, color))
        )

    def _get_best_practices(self):
        practices = ContentEngine.SECURITY_PRACTICES.get(self.protocol, ContentEngine.SECURITY_PRACTICES["alpha"])
        
        controls = []
        for text, icon_name in practices:
            icon = getattr(ft.Icons, icon_name, ft.Icons.SHIELD_ROUNDED)
            controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(icon, color=self.protocol_color, size=24),
                        ft.Text(text, size=14, color=DesignTokens.get_text_main(self.protocol), weight="w500", expand=True)
                    ], spacing=15),
                    padding=15,
                    bgcolor=ft.Colors.with_opacity(0.04, self.protocol_color),
                    border_radius=12,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.15, self.protocol_color))
                )
            )

        return ft.Column(controls, spacing=10)
