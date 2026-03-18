import flet as ft
from core.theme import DesignTokens

class TechnicalDiagram(ft.Container):
    """Componente para renderizar diagramas técnicos interactivos."""
    
    def __init__(self, unit_id, protocol, **kwargs):
        super().__init__(**kwargs)
        self.unit_id = unit_id
        self.protocol = protocol
        self.protocol_color = DesignTokens.get_protocol_color(protocol)
        self.border_radius = 15
        self.padding = 25
        self.bgcolor = ft.Colors.with_opacity(0.04, self.protocol_color)
        self.border = ft.border.all(1.5, ft.Colors.with_opacity(0.15, self.protocol_color))
        self.content = self._build_diagram()
        self.animate_scale = ft.Animation(400, ft.AnimationCurve.DECELERATE)

    def _build_diagram(self):
        if self.unit_id == "hardware":
            return self._hardware_diagram()
        elif self.unit_id == "logic":
            return self._logic_diagram()
        elif self.unit_id == "network":
            return self._network_diagram()
        elif self.unit_id == "cybersecurity":
            return self._security_diagram()
        elif self.unit_id == "os":
            return self._os_diagram()
        elif self.unit_id == "ai":
            return self._ai_diagram()
        else:
            return ft.Text("DIAGRAMA EN PROCESO DE CARGA...", size=12, italic=True, color=DesignTokens.get_text_dim(self.protocol))

    def _os_diagram(self):
        # Diagrama de Capas de SO con más color
        return ft.Column([
            self._layer_box("USUARIO", ft.Colors.with_opacity(0.15, self.protocol_color)),
            ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN, size=15, color=self.protocol_color),
            self._layer_box("APLICACIONES", ft.Colors.with_opacity(0.25, self.protocol_color)),
            ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN, size=15, color=self.protocol_color),
            self._layer_box("KERNEL (CEREBRO)", ft.Colors.with_opacity(0.45, self.protocol_color), bold=True),
            ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN, size=15, color=self.protocol_color),
            self._layer_box("HARDWARE (PIEZAS)", ft.Colors.with_opacity(0.15, self.protocol_color)),
        ], horizontal_alignment="center", spacing=2)

    def _layer_box(self, text, bgcolor, bold=False):
        return ft.Container(
            content=ft.Text(text, weight="bold" if bold else "normal", size=11, color=DesignTokens.get_text_main(self.protocol)),
            bgcolor=bgcolor,
            padding=10,
            border_radius=8,
            alignment=ft.Alignment(0, 0),
            width=250,
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=lambda e: self._on_hover_box(e)
        )

    def _ai_diagram(self):
        # Diagrama de Red Neuronal más dinámico
        return ft.Row([
            ft.Column([ft.CircleAvatar(radius=6, bgcolor=self.protocol_color) for _ in range(3)], spacing=12),
            ft.Icon(ft.Icons.GRAIN, color=self.protocol_color, size=35),
            ft.Column([ft.CircleAvatar(radius=6, bgcolor=self.protocol_color) for _ in range(4)], spacing=12),
            ft.Icon(ft.Icons.GRAIN, color=self.protocol_color, size=35),
            ft.Column([ft.CircleAvatar(radius=6, bgcolor=self.protocol_color) for _ in range(2)], spacing=12),
        ], alignment="center", spacing=20)

    def _hardware_diagram(self):
        return ft.Row([
            self._box("CEREBRO (CPU)", ft.Icons.MEMORY, "Procesamiento"),
            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=self.protocol_color),
            self._box("MEMORIA (RAM)", ft.Icons.SD_CARD, "Donde trabaja"),
            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=self.protocol_color),
            self._box("BAÚL (DISK)", ft.Icons.STORAGE, "Donde guarda")
        ], alignment="center", spacing=20)

    def _logic_diagram(self):
        return ft.Row([
            self._box("ENTRADA", ft.Icons.INPUT, "Tus datos"),
            ft.Icon(ft.Icons.SETTINGS_SUGGEST, color=self.protocol_color),
            self._box("LÓGICA", ft.Icons.CODE, "Instrucciones"),
            ft.Icon(ft.Icons.OUTPUT, color=self.protocol_color),
            self._box("SALIDA", ft.Icons.AUTO_AWESOME, "Resultado")
        ], alignment="center", spacing=20)

    def _network_diagram(self):
        return ft.Column([
            ft.Row([
                self._box("TÚ (CLIENTE)", ft.Icons.LAPTOP, "Pides algo"),
                ft.Icon(ft.Icons.LANGUAGE, color=self.protocol_color, size=30),
                self._box("NUBE (SERVER)", ft.Icons.DNS, "Te responde")
            ], alignment="center"),
            ft.Container(height=10),
            ft.Text("CONEXIÓN SEGURA ACTIVA", size=10, font_family="JetBrains Mono", color=DesignTokens.COLORS["accent"], weight="bold")
        ], horizontal_alignment="center")

    def _security_diagram(self):
        return ft.Stack([
            ft.Container(width=180, height=180, border=ft.border.all(2, ft.Colors.with_opacity(0.1, self.protocol_color)), border_radius=100),
            ft.Container(width=130, height=130, border=ft.border.all(3, ft.Colors.with_opacity(0.3, self.protocol_color)), border_radius=80),
            ft.Container(width=80, height=80, bgcolor=ft.Colors.with_opacity(0.1, self.protocol_color), border_radius=50, content=ft.Icon(ft.Icons.LOCK, color=self.protocol_color, size=30)),
        ], alignment=ft.Alignment(0, 0))

    def _box(self, label, icon, subtitle):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=self.protocol_color, size=28),
                ft.Text(label, weight="bold", size=12, color=DesignTokens.get_text_main(self.protocol)),
                ft.Text(subtitle, size=9, color=DesignTokens.get_text_dim(self.protocol))
            ], horizontal_alignment="center", spacing=2),
            width=120,
            padding=15,
            bgcolor=ft.Colors.with_opacity(0.05, self.protocol_color),
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.2, self.protocol_color)),
            border_radius=12,
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=lambda e: self._on_hover_box(e)
        )

    def _on_hover_box(self, e):
        e.control.scale = 1.05 if e.data == "true" else 1.0
        e.control.bgcolor = ft.Colors.with_opacity(0.12, self.protocol_color) if e.data == "true" else ft.Colors.with_opacity(0.05, self.protocol_color)
        e.control.update()
