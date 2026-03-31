# E.E.D.A. PC (Ecosistema Educativo Digital Adaptable)

[![Platform: Windows | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-8E24AA?style=for-the-badge&logo=windows&logoColor=white)](#)
[![Flet Version](https://img.shields.io/badge/Flet-0.27.3-00B0FF?style=for-the-badge&logo=python&logoColor=white)](https://flet.dev)
[![License](https://img.shields.io/badge/License-Apache%202.0-D32F2F?style=for-the-badge)](#)

**E.E.D.A.** no es solo una aplicación; es un ecosistema pedagógico diseñado para transformar la educación en ciberseguridad. Basado en el modelo **CPA (Concreto-Pictórico-Abstracto)** y en principios de gamificación avanzada, el sistema traduce conceptos tecnológicos de alta complejidad en metáforas visuales que usuarios de **3 a 16 años** pueden navegar de forma intuitiva.

---

## Arquitectura del Sistema (Clean & Modular)

La versión para escritorio está construida sobre una arquitectura modular optimizada, utilizando el framework **Flet (Flutter/Python)** para garantizar una experiencia fluida, reactiva y multiplataforma con una estética de **Glassmorphism**.

### Componentes Core:
* **`ContentEngine`**: El motor lógico que gestiona 8 unidades temáticas mediante 3 protocolos adaptativos (**Alpha, Delta, Omega**).
* **`DatabaseManager`**: Persistencia local mediante **SQLite3** para el seguimiento preciso del progreso y analíticas de desafíos.
* **`EventBus`**: Sistema de comunicación desacoplada para mantener la integridad entre módulos y la UI.
* **`DesignTokens`**: Sistema de diseño unificado basado en la proporción áurea, utilizando tipografías premium como *Inter* y *JetBrains Mono*.

### Módulos Pedagógicos (Ejes de Aprendizaje):
1.  **Hardware**: Fundamentos físicos y microarquitectura.
2.  **Lógica**: Pensamiento computacional y algoritmia.
3.  **Redes**: Conectividad global y protocolos de comunicación.
4.  **Ciberseguridad**: Protección de identidad, criptografía y ciberdefensa.
5.  **Sistemas Operativos**: Gestión de recursos, kernel y sistemas de archivos.
6.  **Inteligencia Artificial**: Redes neuronales y ética algorítmica.
7.  **Programación**: Paradigmas de desarrollo y Clean Code.
8.  **Ética Digital**: Ciudadanía responsable en el ciberespacio.

---

## Stack Tecnológico

* **Backend Logic**: Python 3.12+
* **Frontend Framework**: [Flet](https://flet.dev) (v0.27.3+)
* **Arquitectura de UI**: Estética de contenedores translúcidos y diseño minimalista.
* **Deployment**: Ejecución local nativa y empaquetado multiplataforma.

---

##  Despliegue y Desarrollo

### Ejecución Local
Para inicializar el ecosistema en tu entorno de desarrollo:

```powershell
# 1. Instalar dependencias necesarias
pip install -r requirements.txt

# 2. Ejecutar la aplicación principal
python src/main.py
