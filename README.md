# 🏝️ I.S.D.I — ISla DIgital

[![Platform: Windows | Mobile](https://img.shields.io/badge/Platform-Windows%20%7C%20Mobile-00C853?style=flat-square)](#)
[![Flet Version](https://img.shields.io/badge/Flet-0.27.3-00B0FF?style=flat-square)](https://flet.dev)

**Isla Digital** no es solo una aplicación; es un ecosistema pedagógico diseñado para transformar la educación en ciberseguridad. Basado en el modelo **CPA (Concreto-Pictórico-Abstracto)** y los principios de gamificación interactiva, el sistema traduce conceptos tecnológicos de alta complejidad en metáforas visuales que niños y adolescentes de 3 a 16 años pueden navegar intuitivamente.


## 🏗️ Arquitectura del Sistema

La aplicación está construida sobre una arquitectura modular y limpia, utilizando el framework **Flet (Flutter/Python)** para garantizar una experiencia fluida y multiplataforma.

### Componentes Core:
- **`ContentEngine`**: El cerebro de contenido. Gestiona 8 unidades temáticas cruzadas por 3 protocolos adaptativos (Alpha, Delta, Omega).
- **`DatabaseManager`**: Persistencia local mediante SQLite3 para el seguimiento de progreso y respuestas de desafíos.
- **`EventBus`**: Sistema de comunicación desacoplada entre módulos.
- **`DesignTokens`**: Sistema de diseño unificado basado en el Golden Ratio para espaciado y tipografía premium (Inter, JetBrains Mono).

### Módulos Pedagógicos:
1. **Hardware**: Fundamentos físicos y microarquitectura.
2. **Lógica**: Pensamiento computacional y algoritmos.
3. **Redes**: Conectividad global y protocolos.
4. **Ciberseguridad**: Protección de datos y ciberdefensa.
5. **Sistemas Operativos**: Gestión de recursos y el kernel.
6. **Inteligencia Artificial**: Redes neuronales y ética del algoritmo.
7. **Programación**: Paradigmas y código limpio.
8. **Ética Digital**: Ciudadanía en el ciberespacio.

---

## 🛠️ Tecnologías Utilizadas

- **Backend Logic**: Python 3.12
- **Frontend Framework**: [Flet](https://flet.dev) (v0.27.3)
- **Deployment**: Local Execution

---

## 🚀 Despliegue y Desarrollo

### Ejecución Local
Para correr el proyecto en tu máquina local:

```powershell
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python src/main.py
```

---

## 📜 Licencia

Este proyecto está bajo la Licencia Apache 2.0. Ver el archivo [LICENSE](LICENSE) para más detalles.
