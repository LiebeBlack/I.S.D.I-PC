import flet as ft
from abc import ABC, abstractmethod
from core.theme import DesignTokens

class BaseModule(ft.Container, ABC):
    def __init__(self, navigation_manager=None, protocol="alpha", **kwargs):
        super().__init__(**kwargs)
        self.nav = navigation_manager
        self.protocol = protocol
        self.expand = True
        
        # Estilos técnicos I.S.D.I
        self.glass_config = {
            "blur": DesignTokens.GLASS_STYLE["blur"],
            "opacity": DesignTokens.GLASS_STYLE["opacity"],
            "border_radius": DesignTokens.GLASS_STYLE["border_radius"],
            "border": ft.border.all(1, DesignTokens.get_glass_border(self.protocol)),
            "bgcolor": DesignTokens.get_glass_bg(self.protocol),
        }

    @abstractmethod
    def build(self) -> ft.Control:
        """Debe retornar el control principal del módulo."""
        pass

    def initialize(self):
        """Metodo para inicializar el contenido después de que el niño haya configurado sus datos."""
        self.content = self.build()

    def cleanup(self):
        """Metodo para liberar recursos antes de destruir el módulo."""
        pass

