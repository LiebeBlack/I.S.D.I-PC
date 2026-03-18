import flet as ft
from core.theme import DesignTokens
from core.content import ContentEngine

class Sidebar(ft.Container):
    def __init__(self, on_nav_change, protocol="alpha"):
        super().__init__()
        self.on_nav_change = on_nav_change
        self.protocol = protocol
        self.active_module = "dashboard"
        
        self.protocol_data = ContentEngine.PROTOCOLS.get(self.protocol, ContentEngine.PROTOCOLS["alpha"])
        self.protocol_color = DesignTokens.get_protocol_color(self.protocol)
        
        self.width = 300
        self.bgcolor = ft.Colors.with_opacity(0.06, self.protocol_color)
        self.padding = DesignTokens.get_spacing(2)
        self.border = ft.border.only(right=ft.BorderSide(1.5, DesignTokens.get_glass_border(self.protocol)))
        
        self.nav_items_container = ft.Column(spacing=8)
        self._build_sidebar()

    def _build_sidebar(self):
        # Labels based on Protocol
        if self.protocol == "alpha":
            nav_labels = [
                (ft.Icons.ROCKET_LAUNCH_ROUNDED, "CENTRO ESPACIAL", "dashboard"),
                (ft.Icons.MAP_ROUNDED, "MAPA ESTELAR", "zones"),
                (ft.Icons.BRUSH_ROUNDED, "TALLER CREATIVO", "lab"),
                (ft.Icons.SHIELD_ROUNDED, "ESCUDO LUNAR", "security"),
            ]
        elif self.protocol == "delta":
            nav_labels = [
                (ft.Icons.TERMINAL_ROUNDED, "CONTROL LÓGICO", "dashboard"),
                (ft.Icons.AUTO_STORIES_ROUNDED, "SECTORES DATOS", "zones"),
                (ft.Icons.SCIENCE_ROUNDED, "LABORATORIO", "lab"),
                (ft.Icons.SECURITY_ROUNDED, "PROTOCOLO SEG.", "security"),
            ]
        else: # omega
            nav_labels = [
                (ft.Icons.MEMORY_ROUNDED, "DASHBOARD CENTRAL", "dashboard"),
                (ft.Icons.ACCOUNT_TREE_ROUNDED, "TOPOLOGÍA DE RED", "zones"),
                (ft.Icons.TERMINAL_ROUNDED, "SIMULADOR ARQ.", "lab"),
                (ft.Icons.GPP_GOOD_ROUNDED, "CIBERDEFENSA", "security"),
            ]

        self.nav_items = {}
        controls = []
        for icon, title, module_id in nav_labels:
            item = self._nav_item(icon, title, module_id)
            self.nav_items[module_id] = item
            controls.append(item)
            
        self.nav_items_container.controls = controls
        self.set_active(self.active_module) # Initialize active state

        self.content = ft.Column(
            controls=[
                # Header Section
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(width=4, height=25, bgcolor=self.protocol_color, border_radius=2),
                            ft.Text(f"I.S.D.I // {self.protocol.upper()}", size=20, weight="bold", color=DesignTokens.get_text_main(self.protocol)),
                        ], spacing=10),
                        ft.Text(f"NIVEL: {self.protocol_data['age_range']}", size=11, color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono"),
                    ], spacing=5),
                    margin=ft.margin.only(bottom=30, top=10)
                ),
                
                ft.Text("MÓDULOS DEL SISTEMA", size=10, weight="bold", color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono"),
                ft.Container(height=10),
                
                self.nav_items_container,
                
                ft.Container(expand=True),
                
                # Footer Section
                ft.Container(
                    content=ft.Column([
                        ft.Divider(color=DesignTokens.get_glass_border(self.protocol), height=1),
                        ft.Container(height=10),
                        ft.Text(f"LLAVE: {self.protocol.upper()}_SHA256", size=9, color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono"),
                        ft.Row([
                            ft.Container(width=10, height=10, bgcolor=DesignTokens.COLORS["accent"], border_radius=5),
                            ft.Text("ESTADO: SEGURO", size=9, color=DesignTokens.COLORS["accent"], weight="bold", font_family="JetBrains Mono")
                        ], spacing=8)
                    ], spacing=5),
                    padding=ft.padding.only(bottom=10)
                )
            ],
            expand=True
        )

    def set_active(self, module_id):
        self.active_module = module_id
        for m_id, item in self.nav_items.items():
            is_active = (m_id == module_id)
            
            # Efecto Premium: Gradiente y Borde para el activo
            if is_active:
                item.bgcolor = None # Usamos gradiente
                item.gradient = ft.LinearGradient(
                    begin=ft.Alignment(-1, 0),
                    end=ft.Alignment(1, 0),
                    colors=[
                        ft.Colors.with_opacity(0.15, self.protocol_color),
                        ft.Colors.with_opacity(0.02, self.protocol_color),
                    ]
                )
                item.border = ft.Border(left=ft.BorderSide(3, self.protocol_color))
            else:
                item.bgcolor = None
                item.gradient = None
                item.border = None

            # Icono y Texto
            item.content.controls[0].color = self.protocol_color if is_active else DesignTokens.get_text_dim(self.protocol)
            item.content.controls[1].color = DesignTokens.get_text_main(self.protocol) if is_active else DesignTokens.get_text_dim(self.protocol)
            
            try:
                item.update()
            except Exception:
                pass
        
        try:
            self.update()
        except Exception:
            pass

    def _nav_item(self, icon, title, module_id):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=DesignTokens.get_text_dim(self.protocol), size=22),
                ft.Text(title.upper(), color=DesignTokens.get_text_dim(self.protocol), size=14, weight="w600", font_family="JetBrains Mono"),
            ], spacing=15),
            padding=ft.padding.symmetric(horizontal=15, vertical=16),
            on_click=lambda _: self.on_nav_change(module_id),
            border_radius=12,
            ink=True,
            on_hover=lambda e: self._handle_hover(e, module_id),
        )

    def _handle_hover(self, e, module_id):
        if module_id == self.active_module:
            return
        e.control.bgcolor = ft.Colors.with_opacity(0.08, self.protocol_color) if e.data == "true" else None
        e.control.update()
