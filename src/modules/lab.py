import flet as ft
import time
import random
from base.module import BaseModule
from core.theme import DesignTokens
from components.glass_container import GlassContainer

class Lab(BaseModule):
    def __init__(self, navigation_manager=None, protocol="alpha"):
        super().__init__(navigation_manager, protocol)
        self.protocol_color = DesignTokens.get_protocol_color(self.protocol)
        self.active_activity = None
        self.immersive_mode = False
        
        # Estado para el dibujo (Alpha)
        self.canvas = ft.canvas.Canvas(
            allow_interaction=True,
            on_resize=self._on_canvas_resize,
            expand=True,
        )
        self.current_stroke = []
        self.drawing_color = self.protocol_color
        
        # Estado para el reto de teclado (Delta/Omega)
        self.target_text = "print('SISTEMA_SECURO')"
        self.typed_text = ""
        self.start_time: float = 0.0
        self.wpm = 0
        
        self.initialize()

    def _on_canvas_resize(self, e):
        pass

    def build(self):
        if not self.active_activity:
            return self._build_selector()
        
        if self.active_activity == "drawing":
            return self._build_drawing_lab()
        elif self.active_activity == "keyboard":
            return self._build_keyboard_lab()
        elif self.active_activity == "logic":
            return self._build_logic_lab()
        
        return self._build_selector()

    def _build_selector(self):
        activities = [
            {
                "id": "drawing",
                "title": "TALLER DE DISEÑO",
                "icon": ft.Icons.BRUSH_ROUNDED,
                "desc": "Dibuja tus ideas para la ciudad digital.",
                "protocols": ["alpha"]
            },
            {
                "id": "keyboard",
                "title": "CÓDIGO RÁPIDO",
                "icon": ft.Icons.KEYBOARD_ROUNDED,
                "desc": "Mejora tu velocidad de escritura técnica.",
                "protocols": ["delta", "omega"]
            },
            {
                "id": "logic",
                "title": "RETO DE LÓGICA",
                "icon": ft.Icons.EXTENSION_ROUNDED,
                "desc": "Ordena las piezas para activar el núcleo.",
                "protocols": ["alpha", "delta", "omega"]
            }
        ]

        cards = []
        for act in activities:
            if self.protocol in act["protocols"]:
                cards.append(
                    GlassContainer(
                        content=ft.Column([
                            ft.Icon(act["icon"], size=40, color=self.protocol_color),
                            ft.Text(act["title"], weight="bold", size=18, color=DesignTokens.get_text_main(self.protocol)),
                            ft.Text(act["desc"], size=12, color=DesignTokens.get_text_dim(self.protocol), text_align="center"),
                            ft.Container(height=10),
                            ft.ElevatedButton(
                                "INICIAR", 
                                on_click=lambda _, a=act["id"]: self._start_activity(a),
                                style=ft.ButtonStyle(bgcolor=self.protocol_color, color=ft.Colors.WHITE)
                            )
                        ], horizontal_alignment="center", spacing=10),
                        width=250, height=250, padding=20, protocol=self.protocol
                    )
                )

        return ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("LABORATORIO INTERACTIVO", size=32, weight="bold", color=self.protocol_color, font_family="Lexend"),
                    ft.Text("Entrena tus habilidades en el simulador avanzado.", size=14, color=DesignTokens.get_text_dim(self.protocol)),
                ]),
                ft.Container(expand=True),
                ft.Switch(label="MODO INMERSIVO", on_change=self._toggle_immersive, active_color=self.protocol_color)
            ]),
            ft.Container(height=40),
            ft.Row(cards, alignment="center", spacing=30)
        ], alignment="center", horizontal_alignment="center", expand=True)

    def _toggle_immersive(self, e):
        self.immersive_mode = e.control.value
        if self.nav and self.nav.sidebar:
            self.nav.sidebar.visible = not self.immersive_mode
            self.nav.app_page.update()
        self.update()

    def _start_activity(self, activity_id):
        self.active_activity = activity_id
        self.content = self.build()
        self.update()

    # --- LABORATORIO DE DIBUJO (ALPHA) ---
    def _build_drawing_lab(self):
        cp = ft.GestureDetector(
            content=self.canvas,
            on_pan_start=self._pan_start,
            on_pan_update=self._pan_update,
            expand=True,
        )

        return ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._reset_lab()),
                ft.Text("DISEÑA TU CIUDAD DIGITAL", size=20, weight="bold", color=self.protocol_color),
                ft.Container(expand=True),
                ft.IconButton(ft.Icons.DELETE, on_click=self._clear_canvas),
            ]),
            ft.Container(
                content=cp,
                border=ft.border.all(2, self.protocol_color),
                border_radius=15,
                bgcolor=ft.Colors.WHITE,
                expand=True,
            ),
            ft.Row([
                self._color_picker(ft.Colors.RED),
                self._color_picker(ft.Colors.BLUE),
                self._color_picker(ft.Colors.GREEN),
                self._color_picker(ft.Colors.ORANGE),
                self._color_picker(ft.Colors.PURPLE),
                self._color_picker(ft.Colors.BLACK),
            ], alignment="center", spacing=20)
        ], expand=True, spacing=20)

    def _color_picker(self, color):
        return ft.Container(
            width=30, height=30, bgcolor=color, border_radius=15,
            on_click=lambda _: self._set_drawing_color(color),
            border=ft.border.all(2, ft.Colors.BLACK if self.drawing_color == color else ft.Colors.TRANSPARENT)
        )

    def _set_drawing_color(self, color):
        self.drawing_color = color
        self.content = self.build()
        self.update()

    def _pan_start(self, e: ft.DragStartEvent):
        self.current_stroke = []
        self.canvas.shapes.append(
            ft.canvas.Path(
                elements=[],
                paint=ft.Paint(color=self.drawing_color, stroke_width=4, style=ft.PaintingStyle.STROKE, stroke_join=ft.StrokeJoin.ROUND, stroke_cap=ft.StrokeCap.ROUND),
            )
        )
        self.update()

    def _pan_update(self, e: ft.DragUpdateEvent):
        # En Flet, para actualizar el path eficientemente
        shape = self.canvas.shapes[-1]
        if not shape.elements:
            shape.elements.append(ft.canvas.Path.MoveTo(e.local_x, e.local_y))
        else:
            shape.elements.append(ft.canvas.Path.LineTo(e.local_x, e.local_y))
        self.canvas.update()

    def _clear_canvas(self, _):
        self.canvas.shapes.clear()
        self.canvas.update()

    # --- LABORATORIO DE TECLADO (DELTA/OMEGA) ---
    def _build_keyboard_lab(self):
        codes = [
            "print('ISDI_V4_ONLINE')",
            "for i in range(10): sync()",
            "if security.is_active(): access_granted()",
            "def firewall_scan(host): return True",
            "import crypto_core as cc",
            "kernel.load_module('SECURITY_GATE')"
        ]
        
        if self.typed_text == "" and self.start_time == 0:
            self.target_text = random.choice(codes)

        def on_change(e):
            if self.start_time == 0:
                self.start_time = time.time()
            
            self.typed_text = e.data
            if self.typed_text == self.target_text:
                end_time = time.time()
                total_time = end_time - self.start_time
                self.wpm = int((len(self.target_text) / 5) / (total_time / 60))
                self.typed_text = ""
                self.start_time = 0
                self.target_text = random.choice(codes)
                t_field.value = ""
                results_text.value = f"¡Excelente! Velocidad: {self.wpm} PPM"
            self.update()

        t_field = ft.TextField(
            label="ESCRIBE EL CÓDIGO",
            on_change=on_change,
            focused_border_color=self.protocol_color,
            text_size=20,
            text_style=ft.TextStyle(font_family="JetBrains Mono"),
            autofocus=True
        )
        
        results_text = ft.Text(f"Velocidad previa: {self.wpm} PPM", size=16, italic=True)

        return ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._reset_lab()),
                ft.Text("ENTRENAMIENTO DE CÓDIGO", size=20, weight="bold", color=self.protocol_color),
            ]),
            ft.Container(height=40),
            GlassContainer(
                content=ft.Column([
                    ft.Text("RETO ACTUAL:", size=12, color=DesignTokens.get_text_dim(self.protocol)),
                    ft.Text(self.target_text, size=32, weight="bold", font_family="JetBrains Mono", color=self.protocol_color),
                ], horizontal_alignment="center", spacing=10),
                padding=40, protocol=self.protocol
            ),
            ft.Container(height=20),
            t_field,
            results_text
        ], alignment="center", horizontal_alignment="center", expand=True)

    # --- LABORATORIO DE LÓGICA (SECUENCIA DE ARRANQUE) ---
    def _build_logic_lab(self):
        if not hasattr(self, "logic_sequence"):
            icons = [ft.Icons.POWER, ft.Icons.MEMORY, ft.Icons.DNS, ft.Icons.TERMINAL, ft.Icons.SECURITY]
            self.logic_sequence = random.sample(icons, 4)
            self.user_sequence = []
            self.logic_status = "ORDENA LA SECUENCIA DE ARRANQUE"

        def add_to_seq(icon):
            if icon not in self.user_sequence:
                self.user_sequence.append(icon)
                if len(self.user_sequence) == len(self.logic_sequence):
                    if self.user_sequence == self.logic_sequence:
                        self.logic_status = "¡SISTEMA INICIALIZADO CON ÉXITO!"
                    else:
                        self.logic_status = "ERROR EN LA SECUENCIA. REINICIANDO..."
                        self.user_sequence = []
                self.content = self.build()
                self.update()

        items = []
        for icon in [ft.Icons.POWER, ft.Icons.MEMORY, ft.Icons.DNS, ft.Icons.TERMINAL, ft.Icons.SECURITY]:
            items.append(
                ft.Container(
                    content=ft.Icon(icon, size=40, color=self.protocol_color),
                    on_click=lambda _, i=icon: add_to_seq(i),
                    padding=20, border_radius=15,
                    bgcolor=ft.Colors.with_opacity(0.1, self.protocol_color),
                    animate_scale=300
                )
            )

        user_view = []
        for icon in self.user_sequence:
            user_view.append(ft.Icon(icon, size=30, color=DesignTokens.COLORS["accent"]))

        return ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._reset_lab_logic()),
                ft.Text("CONEXIÓN DE COMPONENTES", size=24, weight="bold", color=self.protocol_color, font_family="Lexend"),
            ]),
            ft.Container(height=40),
            ft.Text(self.logic_status, size=16, weight="bold", color=DesignTokens.get_text_dim(self.protocol), font_family="JetBrains Mono"),
            ft.Container(height=20),
            ft.Row(items, alignment="center", spacing=20),
            ft.Container(height=30),
            ft.Text("TU SECUENCIA:", size=12, color=DesignTokens.get_text_dim(self.protocol)),
            ft.Row(user_view, alignment="center", spacing=15),
            ft.Container(height=40),
            ft.ElevatedButton("REINICIAR", on_click=lambda _: self._reset_lab_logic(), bgcolor=DesignTokens.COLORS["critical"], color=ft.Colors.WHITE)
        ], alignment="center", horizontal_alignment="center", expand=True)

    def _reset_lab_logic(self):
        if hasattr(self, "logic_sequence"):
            delattr(self, "logic_sequence")
        self._reset_lab()

    def _reset_lab(self):
        self.active_activity = None
        self.typed_text = ""
        self.start_time: float = 0.0
        self.content = self.build()
        self.update()
