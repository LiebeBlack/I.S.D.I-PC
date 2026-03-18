import flet as ft

class DesignTokens:
    @staticmethod
    def get_spacing(n: int) -> float:
        """S=8*1.618^n (Golden Ratio Spacing)"""
        return 8 * (1.618 ** n)

    COLORS = {
        "primary": "#00C853",   # Vibrant Green (Alpha)
        "secondary": "#00B0FF",  # Electric Blue (Delta)
        "critical": "#FF3D00",   # Deep Orange/Red (Omega)
        "tertiary": "#6200EA",   # Deep Purple
        "warning": "#FFD600",    # Vivid Yellow
        "bg_dark": "#F0F4F0",    # Soft Grey-Green
        "bg_panel": "#FFFFFF",
        "accent": "#2E7D32",     
        "glass": "rgba(255, 255, 255, 0.7)",
        "vibrant_pink": "#FF4081",
        "vibrant_cyan": "#00E5FF",
    }

    @classmethod
    def get_text_main(cls, protocol: str):
        # High contrast for light mode - Casi negro para máxima nitidez
        return "#0A0D0A"

    @classmethod
    def get_text_dim(cls, protocol: str):
        # Contraste medio para información secundaria
        return "#37474F"

    @classmethod
    def get_glass_bg(cls, protocol: str):
        color = cls.get_protocol_color(protocol)
        return ft.Colors.with_opacity(0.06, color)

    @classmethod
    def get_glass_border(cls, protocol: str):
        color = cls.get_protocol_color(protocol)
        return ft.Colors.with_opacity(0.15, color)

    @classmethod
    def get_protocol_color(cls, protocol: str):
        if protocol == "alpha": return cls.COLORS["primary"]
        if protocol == "delta": return cls.COLORS["secondary"]
        if protocol == "omega": return cls.COLORS["critical"]
        return cls.COLORS["primary"]

    @classmethod
    def get_premium_gradient(cls, protocol: str):
        color = cls.get_protocol_color(protocol)
        return ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[
                ft.Colors.with_opacity(0.15, color),
                ft.Colors.with_opacity(0.05, color),
            ]
        )

    # Fuentes registradas para Flet Desktop
    FONTS = {
        "JetBrains Mono": "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf",
        "Inter": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.otf",
        "Lexend": "https://github.com/googlefonts/lexend/raw/main/fonts/lexend/ttf/Lexend-Regular.ttf",
    }

    GLASS_STYLE = {
        "blur": 30,
        "opacity": 0.1,
        "border_radius": 20,
    }

