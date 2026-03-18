import flet as ft
from core.theme import DesignTokens

class GlassContainer(ft.Container):
    def __init__(self, content=None, padding=None, margin=None, protocol="alpha", **kwargs):
        tokens = DesignTokens
        
        # Merge default glass styles with kwargs
        style = {
            "blur": ft.Blur(tokens.GLASS_STYLE["blur"], tokens.GLASS_STYLE["blur"]),
            "animate_opacity": 300,
            "border_radius": tokens.GLASS_STYLE["border_radius"],
            "border": ft.border.all(1.5, tokens.get_glass_border(protocol)),
            "bgcolor": tokens.get_glass_bg(protocol),
            "shadow": ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            "gradient": ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[
                    ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                    ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                ],
            ),
            "padding": padding or tokens.get_spacing(1),
            "margin": margin or 0,
        }
        
        # Update style with any explicit kwargs
        style.update(kwargs)
        
        super().__init__(content=content, **style)
