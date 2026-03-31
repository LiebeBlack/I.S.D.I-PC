class ContentEngine:
    """
    Motor central de contenido educativo para Isla Digital.
    Organizado por Protocolo (Edad) y Unidades Pedagógicas.
    """
    
    PROTOCOLS = {
        "alpha": {
            "name": "PROTOCOLO ALPHA",
            "age_range": "3-7 años",
            "description": "Exploración Estelar y Fundamentos Físicos",
            "theme_color": "#00FF41"
        },
        "delta": {
            "name": "PROTOCOLO DELTA",
            "age_range": "8-12 años",
            "description": "Lógica Operacional y Seguridad Activa",
            "theme_color": "#00E5FF"
        },
        "omega": {
            "name": "PROTOCOLO OMEGA",
            "age_range": "13-16 años",
            "description": "Arquitectura de Sistemas y Ciberdefensa",
            "theme_color": "#FF3D00"
        }
    }

    DASHBOARD = {
        "alpha": {
            "title": "Centro de Exploración Alpha",
            "labels": ["Oxígeno", "Energía", "Escudo"],
            "mission": "¡Hola, explorador! Tu nave está lista para descubrir nuevos mundos digitales."
        },
        "delta": {
            "title": "Sala de Control Delta",
            "labels": ["CPU", "Red", "Seguridad"],
            "mission": "Agente Delta, todo el sistema está bajo tu supervisión. ¿Listo para la operación?"
        },
        "omega": {
            "title": "Interfaz de Arquitectura Omega",
            "labels": ["Kernel", "Nodos", "Amenazas"],
            "mission": "Arquitecto Omega, la integridad del núcleo depende de tu análisis técnico."
        }
    }

    SECURITY_PRACTICES = {
        "alpha": [
            ("Nunca compartas tus 'Llaves Estelares' (contraseñas) con desconocidos.", "PASSWORD_ROUNDED"),
            ("Si ves algo extraño en el espacio, avisa a un adulto de confianza.", "REPORT_PROBLEM_ROUNDED"),
            ("Sé amable y respetuoso con todos los viajeros digitales.", "FAVORITE_ROUNDED"),
        ],
        "delta": [
            ("Usa siempre la 'Doble Cerradura' (verificación en dos pasos).", "PHONELINK_LOCK_ROUNDED"),
            ("No caigas en trampas de mensajes sospechosos (Phishing).", "ATTACH_EMAIL_ROUNDED"),
            ("Navega solo por sitios seguros con el candado verde (HTTPS).", "HTTPS_ROUNDED"),
        ],
        "omega": [
            ("Aplica el 'Principio de Mínimo Privilegio' en tus sistemas.", "MANAGE_ACCOUNTS_ROUNDED"),
            ("Audita regularmente quién tiene acceso a tu información.", "FACT_CHECK_ROUNDED"),
            ("Tus acciones digitales definen tu reputación técnica y ética.", "GAVEL_ROUNDED"),
        ]
    }

    SECURITY_METRICS = {
        "alpha": {
            "title": "ESCUDO LUNAR // PROTECCIÓN",
            "metrics": [
                {"label": "Escudo de Cristal", "value": "ACTIVO", "icon_name": "SHIELD_ROUNDED", "color_key": "accent"},
                {"label": "Llaves Secretas", "value": "SEGURAS", "icon_name": "KEY_ROUNDED", "color_key": "warning"},
                {"label": "Guardianes", "value": "EN ALERTA", "icon_name": "GPP_GOOD_ROUNDED", "color_key": "primary"},
            ]
        },
        "delta": {
            "title": "CENTRO DE CIFRADO // MONITOREO",
            "metrics": [
                {"label": "Integridad_Muro", "value": "100%", "icon_name": "SECURITY_ROUNDED", "color_key": "accent"},
                {"label": "Cifrado_Datos", "value": "256-BIT", "icon_name": "LOCK_ROUNDED", "color_key": "primary"},
                {"label": "Filtro_Mensajes", "value": "ACTIVO", "icon_name": "VERIFIED_USER_ROUNDED", "color_key": "warning"},
            ]
        },
        "omega": {
            "title": "CENTRO DE COMANDO CIBERDEFENSA",
            "metrics": [
                {"label": "Kernel_Reforzado", "value": "MÁXIMO", "icon_name": "MEMORY_ROUNDED", "color_key": "accent"},
                {"label": "Autenticación_ZTA", "value": "ESTRICTA", "icon_name": "ADMIN_PANEL_SETTINGS_ROUNDED", "color_key": "primary"},
                {"label": "Análisis_Amenazas", "value": "SINCRO", "icon_name": "HUB_ROUNDED", "color_key": "warning"},
            ]
        }
    }

    UNITS = {
        "hardware": {
            "icon": "MEMORY",
            "alpha": {
                "title": "La Nave Espacial",
                "intro": "🚀 Imagina que tu computadora es una nave mágica. Necesita motores fuertes para volar por las estrellas.",
                "architecture": "🧠 El cerebro (CPU) da las órdenes, y los cables son carreteras donde viajan rápidamente tus dibujos y juegos.",
                "security": "🛡️ Siempre mantén tu nave limpia y no dejes entrar virus malvados del espacio exterior.",
                "challenge": "Dibuja tu computadora como si fuera una nave que viaja al espacio.",
                "fact": "⚡ ¡Tu computadora piensa miles de veces más rápido que un cohete despuntando al cielo!",
                "quiz": [
                    {"q": "¿Qué parte de la computadora piensa y da las órdenes?", "a": ["El Teclado", "El Cerebro (CPU)", "El Ratón"], "c": 1},
                    {"q": "¿Cómo debemos cuidar nuestra nave digital?", "a": ["Dejándola sucia", "Con un Escudo Seguro y sin virus 🛡️", "Golpeándola"], "c": 1}
                ]
            },
            "delta": {
                "title": "Arquitectura de Sistemas: El Ciclo de Datos",
                "intro": "El hardware no es solo metal y silicio; es una estructura lógica diseñada para procesar información a velocidades increíbles mediante impulsos eléctricos.",
                "architecture": "La placa base actúa como el sistema nervioso, conectando el CPU, la RAM y el almacenamiento. La RAM es el espacio de trabajo inmediato, mientras que el disco duro es el archivo a largo plazo.",
                "security": "La integridad del hardware depende de un entorno controlado. El sobrecalentamiento y las fluctuaciones de energía son riesgos que deben ser gestionados mediante sistemas de enfriamiento y protección eléctrica.",
                "challenge": "Dibuja un diagrama donde expliques el viaje de un dato desde que presionas una tecla hasta que aparece en pantalla.",
                "fact": "Un bit es la unidad mínima de información: solo puede ser 0 o 1, como un interruptor apagado o encendido.",
                "quiz": [
                    {"q": "¿Qué componente actúa como la memoria a corto plazo?", "a": ["Disco Duro", "Memoria RAM", "Tarjeta Gráfica", "Placa Base"], "c": 1},
                    {"q": "¿Qué riesgo físico amenaza severamente el rendimiento del procesador?", "a": ["Exceso de Luz solar", "Poco espacio en SSD", "Sobrecalentamiento extremo", "Ondas de radio"], "c": 2},
                    {"q": "¿Qué significa que una computadora opere de forma binaria?", "a": ["Usa dos procesadores", "Trabaja empleando únicamente unos (1) y ceros (0)", "Tiene dos monitores", "Requiere doble autenticación"], "c": 1}
                ]
            },
            "omega": {
                "title": "Ingeniería de Sistemas y Microarquitectura",
                "intro": "La computación moderna se basa en la abstracción de niveles, desde puertas lógicas hasta complejos sistemas operativos. Entender el hardware es entender la base de la computación cuántica y tradicional.",
                "architecture": "Analizaremos la arquitectura de Von Neumann: la separación entre la unidad de procesamiento y la memoria. Exploraremos cómo los ciclos de reloj y el ancho de banda definen el rendimiento de un sistema escalable.",
                "security": "A nivel de arquitectura, existen vulnerabilidades críticas como ataques de ejecución especulativa (Spectre/Meltdown). La seguridad comienza en el diseño del chip y la gestión de privilegios del kernel.",
                "challenge": "Investiga y explica cómo una vulnerabilidad a nivel de hardware puede comprometer todo el cifrado de un sistema operativo.",
                "fact": "Una vulnerabilidad a nivel de hardware como Spectre o Meltdown puede comprometer el cifrado completo de un sistema.",
                "quiz": [
                    {"q": "¿Qué arquitectura separa la memoria del procesador?", "a": ["Von Neumann", "Harvard", "RISC"], "c": 0}
                ]
            }
        },
        "logic": {
            "icon": "TERMINAL",
            "alpha": {
                "title": "El Idioma de las Luces",
                "intro": "💡 Las computadoras solo saben dos palabras: Encendido (1) y Apagado (0). ¡Como un interruptor de luz!",
                "architecture": "🤖 Juntando miles de estas luces, la computadora entiende cómo pintar colores, sumar números y jugar contigo.",
                "security": "🚦 Para no perdernos, siempre seguimos las instrucciones paso a paso, igual que una receta para hornear galletas.",
                "challenge": "Juego: Explícale a tu amigo cómo dibujar un cuadrado diciendo solo SÍ o NO.",
                "fact": "✨ La primera programadora del mundo inventó este idioma de luces mágicas hace más de 100 años.",
                "quiz": [
                    {"q": "¿Cuántas palabras entiende en el fondo la computadora?", "a": ["Mil palabras", "Solo dos: Encendido y Apagado (1 y 0)", "Todo el diccionario"], "c": 1}
                ]
            },
            "delta": {
                "title": "Lógica Procedimental y Algoritmos",
                "intro": "Un algoritmo es una secuencia finita de instrucciones definidas y no ambiguas que representan un modelo de solución para un problema determinado.",
                "architecture": "Exploraremos las estructuras de control: bucles, condicionales y funciones. Estas herramientas permiten que el software tome decisiones basadas en variables de entrada y estados del sistema.",
                "security": "Los algoritmos deben ser auditables. Un código mal estructurado puede ocultar errores lógicos que comprometen la estabilidad del sistema o permiten fugas de información no deseadas.",
                "challenge": "Escribe el pseudocódigo para un sistema que verifique si una contraseña cumple con los requisitos mínimos de seguridad.",
                "fact": "La palabra 'Algoritmo' viene del nombre del matemático persa Al-Juarismi, del siglo IX.",
                "quiz": [
                    {"q": "¿Qué es un bucle?", "a": ["Una instrucción que se repite", "Un error del sistema", "Un tipo de cable"], "c": 0}
                ]
            },
            "omega": {
                "title": "Pensamiento Computacional y Estructuras Complejas",
                "intro": "El software moderno se construye sobre paradigmas de programación que optimizan la eficiencia y la mantenibilidad. La lógica es el tejido que sostiene la inteligencia artificial.",
                "architecture": "Profundizaremos en la complejidad algorítmica (Notación Big O) y cómo la elección de una estructura de datos adecuada puede transformar el rendimiento de una aplicación a gran escala.",
                "security": "La seguridad por diseño implica validar cada entrada y prever comportamientos inesperados (Buffer Overflow). El análisis estático y dinámico de código es esencial para identificar debilidades estructurales.",
                "challenge": "Analiza cómo un bucle infinito en un proceso crítico de sistema puede ser utilizado para realizar un ataque de Denegación de Servicio (DoS).",
                "fact": "El término 'Bug' se popularizó cuando encontraron una polilla real dentro de una computadora en 1947.",
                "quiz": [
                    {"q": "¿Qué mide la Notación Big O?", "a": ["Eficiencia de un algoritmo", "Tamaño de la pantalla", "Velocidad de internet"], "c": 0}
                ]
            }
        },
        "network": {
            "icon": "LANGUAGE",
            "alpha": {
                "title": "Hilos y Telarañas Invisibles",
                "intro": "🌐 ¡El internet es una tela de araña gigante! Conecta las computadoras de todas las casas del mundo.",
                "architecture": "📨 Cuando mandas un dibujo a tu abuela, viaja súper rápido por cables escondidos o por el aire.",
                "security": "🕵️‍♂️ Solo hablamos con amigos que conocemos. Nunca abrimos mensajes de monstruos desconocidos.",
                "challenge": "Pregúntale a alguien mayor por dónde entra el Internet a tu casa (¡busca el módem!).",
                "fact": "🌊 ¡Hay cables gigantes de internet que viven debajo del agua con los peces!",
                "quiz": [
                    {"q": "¿Internet conecta...?", "a": ["A los extraterrestres", "Las computadoras de todo el mundo 🌍", "Las televisiones rotas"], "c": 1}
                ]
            },
            "delta": {
                "title": "Conectividad y Protocolos de Red",
                "intro": "Las redes de computadoras permiten el intercambio de recursos e información mediante protocolos estandarizados como el TCP/IP, que aseguran que los datos lleguen íntegros a su destino.",
                "architecture": "Estudiaremos el modelo cliente-servidor. Cuando navegas por la web, tu dispositivo solicita información a un servidor remoto, el cual responde enviando los datos organizados en paquetes numerados.",
                "security": "El uso de redes públicas conlleva riesgos de interceptación. Es vital utilizar protocolos cifrados (HTTPS) y firewalls que filtren el tráfico malicioso antes de que alcance nuestra red local.",
                "challenge": "Explica la diferencia entre una dirección IP privada y una dirección IP pública.",
                "fact": "El primer mensaje enviado por ARPANET, el abuelo del internet, fue simplemente 'LO': el sistema falló antes de terminar de escribir 'LOGIN'.",
                "quiz": [
                    {"q": "¿Qué protocolo garantiza que las páginas web sean enviadas cifradas?", "a": ["HTTP", "FTP", "HTTPS", "SMTP"], "c": 2},
                    {"q": "¿En el modelo cliente-servidor, tu navegador actuaría como...?", "a": ["El enrutador", "El servidor remoto", "El DNS central", "El cliente"], "c": 3},
                    {"q": "¿Para qué sirve exactamente un Firewall perimetral?", "a": ["Aumentar la velocidad del internet", "Bloquear paquetes no autorizados", "Compartir archivos más rápido", "Crear copias de seguridad"], "c": 1}
                ]
            },
            "omega": {
                "title": "Topología de Redes y Seguridad Perimetral",
                "intro": "La infraestructura global de red es un sistema complejo de sistemas autónomos interconectados. El entendimiento de las capas del modelo OSI es fundamental para cualquier analista de sistemas.",
                "architecture": "Analizaremos el enrutamiento dinámico, el DNS y cómo la latencia afecta a las aplicaciones distribuidas. La transición de IPv4 a IPv6 es un reto crítico para la escalabilidad de la red global.",
                "security": "La implementación de una estrategia de Defensa en Profundidad incluye VPNs, Sistemas de Detección de Intrusos (IDS) y la segmentación de redes para mitigar el movimiento lateral de atacantes.",
                "challenge": "Investiga qué es un ataque de 'Man-in-the-Middle' y cómo el protocolo TLS previene este tipo de interceptación.",
                "fact": "El protocolo TCP/IP fue diseñado para ser tan robusto que pudiera sobrevivir a un ataque nuclear.",
                "quiz": [
                    {"q": "¿Qué rol cumple el Sistema de Nombres de Dominio (DNS)?", "a": ["Cifrar datos de internet", "Traducir dominios a direcciones IP", "Acelerar conexiones de fibra"], "c": 1},
                    {"q": "¿En qué capa OSI opera principalmente un Enrutador (Router)?", "a": ["Capa 2: Enlace", "Capa 3: Red", "Capa 7: Aplicación"], "c": 1},
                    {"q": "¿Qué técnica frena a un atacante escalando privilegios a otros servidores internos?", "a": ["Segmentación de Red (VLANs)", "Instalación de antivirus ligeros", "Mejorar la latencia (Ping)"], "c": 0}
                ]
            }
        },
        "cybersecurity": {
            "icon": "SECURITY",
            "alpha": {
                "title": "El Escudo de Cristal",
                "intro": "🦸‍♀️ En nuestro viaje, llevamos un escudo mágico. Proteger nuestra información es como llevar casco en la bicicleta.",
                "architecture": "🔑 Tu escudo funciona con contraseñas. ¡Son súper secretas! No se las digas a nadie.",
                "security": "💖 Si algo en internet te asusta, ¡avísale rápido a tus papás o profes!",
                "challenge": "Dibuja un escudo de superhéroe que proteja tu tablet o computadora.",
                "fact": "🤖 A veces, las páginas te piden buscar semáforos en fotos para saber que eres un niño y no un robot.",
                "quiz": [
                    {"q": "¿Qué debes hacer con tus contraseñas?", "a": ["Gritarlas fuerte", "Guardarlas en secreto 🤫", "Escribirlas en la pared"], "c": 1}
                ]
            },
            "delta": {
                "title": "Ciberseguridad Activa y Privacidad",
                "intro": "La ciberseguridad es la práctica de proteger sistemas, redes y programas de ataques digitales. Estos ataques suelen apuntar a acceder, cambiar o destruir información sensible.",
                "architecture": "La autenticación multifactor (MFA) añade una capa extra de protección más allá de la contraseña. La criptografía convierte tus mensajes en códigos que solo el destinatario puede descifrar.",
                "security": "La ingeniería social es una técnica de manipulación que busca obtener datos confidenciales. Desconfiar de correos sospechosos (Phishing) es fundamental para mantener la integridad de tus cuentas.",
                "challenge": "Crea una lista de 5 reglas de oro para mantener tus perfiles en línea protegidos de intrusos.",
                "fact": "La mayor parte de los ataques exitosos no se deben a fallas técnicas, sino a engaños a personas (Ingeniería Social).",
                "quiz": [
                    {"q": "¿Qué añade la Autenticación Multifactor (MFA)?", "a": ["Más velocidad de red", "Una capa extra de seguridad (ej. código SMS)", "Gráficos más bonitos"], "c": 1},
                    {"q": "¿Qué es el Phishing?", "a": ["Pulsar muchas teclas rápido", "Un engaño para robar tus contraseñas haciéndose pasar por alguien de confianza", "Un tipo de memoria moderna"], "c": 1}
                ]
            },
            "omega": {
                "title": "Criptografía Avanzada, Gestión de Amenazas y Arquitectura Zero-Trust",
                "intro": "En un entorno hostil donde las amenazas evolucionan mediante IA y automatización, la seguridad estática ya no es funcional. El principio arquitectónico moderno exige 'Confianza Cero' (Zero Trust), implicando que nadie, ni dentro ni fuera de la red perimetral, es confiable por defecto. Todo acceso debe ser verificado continuamente mediante múltiples factores de autenticación (2FA/MFA) y análisis contextual de comportamiento. Además, los SOC (Security Operations Centers) monitorean en tiempo real patrones de tráfico anómalos buscando indicadores de compromiso (IoC) antes de que el malware logre establecer persistencia.",
                "architecture": "Exploraremos a fondo la estructura matemática de la criptografía asimétrica como RSA y Curvas Elípticas (ECC). Diferenciamos claramente el cifrado (bidireccional) del hashing (unidireccional como SHA-256). Entender cómo se firman digitalmente los certificados SSL/TLS permite validar la autenticidad de cualquier servicio y establece la capa fundamental de la web segura. También analizaremos las Infraestructuras de Clave Pública (PKI) y el rol crítico que juegan las Autoridades de Certificación (CA).",
                "security": "El análisis dinámico de malware en sandboxes y la respuesta automatizada ante incidentes (SOAR) son pilares de la ciberdefensa. Investigaremos cómo operan las tácticas de las Amenazas Persistentes Avanzadas (APT), el funcionamiento interno de campañas de Ransomware (LockBit, Conti) y cómo las organizaciones modelan sus defensas usando frameworks reconocidos como MITRE ATT&CK. Comprenderás la diferencia letal entre un ataque de día cero (0-day) y una vulnerabilidad N-day no parcheada.",
                "challenge": "Redacta un reporte técnico ejecutivo evaluando las implicaciones éticas y los riesgos de privacidad frente a la propuesta gubernamental de incluir 'Puertas Traseras' (Backdoors) obligatorias en el cifrado de extremo a extremo de plataformas de mensajería.",
                "fact": "La computación cuántica, utilizando el algoritmo de Shor, teóricamente podría factorizar en segundos las claves RSA que a una supercomputadora clásica le tomaría millones de años romper. Esto empuja al mundo hacia la Criptografía Post-Cuántica (PQC).",
                "quiz": [
                    {"q": "¿Qué principio fundamenta la arquitectura Zero Trust?", "a": ["Confiar solo en la red interna", "Verificar siempre y nunca confiar", "Usar antivirus avanzados"], "c": 1},
                    {"q": "¿Cuál es la función principal de un algoritmo de HASH (ej. SHA-256)?", "a": ["Ocultar datos bidireccionalmente", "Comprimir archivos grandes", "Generar una firma única irreversible"], "c": 2},
                    {"q": "¿Qué diferencia a un ataque 0-day de otros?", "a": ["Ocurre a medianoche", "El fabricante aún no conoce la vulnerabilidad", "Usa fuerza bruta extrema"], "c": 1}
                ]
            }
        },
        "os": {
            "icon": "SETTINGS_SYSTEM_DAYDREAM",
            "alpha": {
                "title": "El Director de Orquesta",
                "intro": "🎶 El Sistema Operativo (como Windows o Android) es como un director de banda. Hace que todo funcione bonito y sin pelear.",
                "architecture": "🚦 Dice cuándo suena el tambor (tus juegos) y cuándo suena la flauta (tus videos).",
                "security": "👮 También es el policía que vigila que un juego no cierre a los demás por accidente.",
                "challenge": "Imagina que eres un director de orquesta. ¿A quién le darías permiso primero: a un juego o a una tarea?",
                "fact": "📱 Lo que usas para tocar la pantalla de la tablet también es un Sistema Operativo.",
                "quiz": [
                    {"q": "¿Qué hace el Sistema Operativo?", "a": ["Cocina pizza", "Organiza todo para que juegues y veas videos 🎮", "Borra todo"], "c": 1}
                ]
            },
            "delta": {
                "title": "Gestión de Recursos y Kernel",
                "intro": "El Sistema Operativo (SO) es el software que gestiona el hardware y actúa como intermediario entre el usuario y la máquina, administrando memoria, procesos y archivos.",
                "architecture": "El núcleo o 'Kernel' es la parte más interna. Se encarga de la planificación de procesos (Scheduling) y la gestión de la memoria RAM, asegurando que los recursos se utilicen de forma eficiente.",
                "security": "La gestión de permisos es vital. El SO utiliza listas de control de acceso (ACL) para decidir qué usuarios o aplicaciones pueden leer, escribir o ejecutar archivos específicos.",
                "challenge": "Investiga qué sucede cuando dos programas intentan usar el mismo recurso al mismo tiempo. ¿Cómo lo resuelve el SO?",
                "fact": "Linux está en todas partes: en tu teléfono Android, en los servidores de internet y en la Estación Espacial Internacional.",
                "quiz": [
                    {"q": "¿Qué componente del sistema operativo distribuye activamente la memoria RAM?", "a": ["El Explorador de Archivos", "El Kernel (Núcleo)", "El Antivirus"], "c": 1},
                    {"q": "¿Qué significa ACL en la seguridad del sistema?", "a": ["Accesorio de Cálculo Local", "Listas de Control de Acceso", "Aplicación de Código Libre"], "c": 1}
                ]
            },
            "omega": {
                "title": "Microkernels, Virtualización y Abstracción",
                "intro": "Los sistemas operativos modernos implementan capas de abstracción complejas para permitir la ejecución de múltiples entornos sobre un mismo hardware físico.",
                "architecture": "Exploraremos el espacio de usuario frente al espacio de kernel. Estudiaremos cómo las llamadas al sistema (syscalls) permiten una comunicación segura y controlada entre las aplicaciones y el hardware.",
                "security": "El aislamiento mediante 'Sandboxing' y contenedores (Docker, Kubernetes) es esencial. Analizaremos cómo las vulnerabilidades de escalada de privilegios (Privilege Escalation) rompen barreras lógicas.",
                "challenge": "Explica la diferencia técnica entre un proceso y un hilo (thread), y por qué el aislamiento de procesos es una medida de seguridad crítica para los navegadores modernos.",
                "fact": "Windows originalmente se iba a llamar 'Interface Manager', pero el equipo de marketing prefirió 'Windows'.",
                "quiz": [
                    {"q": "¿El área donde los programas con máximos permisos del hardware se ejecutan se denomina...?", "a": ["Kernel Space", "User Space", "Virtual Space"], "c": 0},
                    {"q": "¿Qué tecnología empaqueta aplicaciones junto con sus librerías para portabilidad?", "a": ["Antivirus Avanzados", "Contenedores (Ej. Docker)", "Hilos Multitarea (Threads)"], "c": 1},
                    {"q": "¿Por qué Chrome consume tanta RAM en el sistema operativo?", "a": ["Es un virus", "Cada pestaña ejecuta un proceso aislado por seguridad", "Está minando criptomonedas"], "c": 1}
                ]
            }
        },
        "ai": {
            "icon": "PSYCHOLOGY",
            "alpha": {
                "title": "Máquinas que Aprenden",
                "intro": "🐶 La Inteligencia Artificial es como un robot bebé. Aprende mirando muchas cosas nuevas.",
                "architecture": "🎨 Si le enseñas 100 dibujos de perritos, ¡aprende súper rápido cómo se ve un perro!",
                "security": "🌟 Debemos enseñarle cosas buenas para que no sea grosera ni mala.",
                "challenge": "Juego: Intenta actuar como un robot que está aprendiendo a caminar.",
                "fact": "♟️ ¡Una IA ya le ganó a los mejores jugadores de ajedrez del mundo!",
                "quiz": [
                    {"q": "¿Cómo aprende la Inteligencia Artificial?", "a": ["Durmiendo mucho", "Viendo miles de ejemplos y fotos 📚", "Comiendo vegetales"], "c": 1}
                ]
            },
            "delta": {
                "title": "Redes Neuronales y Aprendizaje Automático",
                "intro": "La IA se basa en algoritmos inspirados en el cerebro humano para procesar datos y tomar decisiones o predicciones basadas en la experiencia previa.",
                "architecture": "El Machine Learning utiliza datos para 'entrenar' modelos. Mediante redes neuronales artificiales, la IA puede identificar tendencias complejas que serían imposibles de detectar manualmente.",
                "security": "El sesgo algorítmico es un riesgo ético. Si los datos de entrenamiento están sesgados, la IA tomará decisiones injustas. La transparencia en los algoritmos es fundamental para la confianza digital.",
                "challenge": "Piensa en una IA que uses a diario (como un recomendador de videos). ¿Cómo crees que decidió qué mostrarte hoy?",
                "fact": "El término 'Inteligencia Artificial' se acuñó en una conferencia en la universidad de Dartmouth en 1956.",
                "quiz": [
                    {"q": "¿Qué técnica de IA se inspira en el cerebro humano?", "a": ["Hojas de cálculo", "Redes Neuronales Artificiales", "Bases de datos SQL"], "c": 1},
                    {"q": "¿Qué problema ético puede tener una IA mal entrenada?", "a": ["Ser muy rápida", "Sesgo algorítmico (decisiones injustas)", "Consumir poca energía"], "c": 1}
                ]
            },
            "omega": {
                "title": "Ética del Algoritmo y Deep Learning",
                "intro": "La Inteligencia Artificial generativa y los grandes modelos de lenguaje (LLM) están transformando la sociedad. Entender su arquitectura es entender el futuro del trabajo y la verdad.",
                "architecture": "Analizaremos el concepto de 'Caja Negra' en modelos de aprendizaje profundo y la importancia de la 'IA Explicable'. Veremos cómo los transformadores permiten procesar contextos masivos de información.",
                "security": "Los ataques de envenenamiento de datos (Data Poisoning) y los Deepfakes son amenazas críticas. La integridad de la información depende de nuestra capacidad para verificar la procedencia de los contenidos generados.",
                "challenge": "Debate: ¿Quién es responsable si una IA toma una decisión errónea en un sistema crítico de salud o defensa?",
                "fact": "Las redes neuronales artificiales existen como concepto desde los años 40, mucho antes de que las computadoras fueran accesibles al público.",
                "quiz": [
                    {"q": "¿Qué es un modelo de 'Caja Negra' en IA?", "a": ["Un modelo cuyo proceso de decisión no es transparente", "Un modelo que solo funciona de noche", "Un modelo pintado de negro"], "c": 0},
                    {"q": "¿Qué amenaza usa IA para crear videos falsos realistas?", "a": ["Phishing", "Deepfakes", "Ransomware"], "c": 1}
                ]
            }
        },
        "programming": {
            "icon": "CODE",
            "alpha": {
                "title": "Dibujando con Instrucciones",
                "intro": "Programar es como darle un mapa del tesoro a un robot. Si le dices 'Tres pasos al frente y dos giros', ¡encontrará el cofre!",
                "architecture": "Usamos flechas y colores para hablar con las máquinas. Cada bloque es una acción que el robot entiende perfectamente.",
                "security": "Las instrucciones deben ser seguras. Nunca le pidas a un robot que haga algo que pueda romper la nave o lastimar a alguien.",
                "challenge": "Dibuja el camino que debe seguir un robot para llegar a su cargador evitando los obstáculos.",
                "fact": "El primer lenguaje de programación se llamó Plankalkül, diseñado por Konrad Zuse en 1943.",
                "quiz": [
                    {"q": "¿Qué es programar?", "a": ["Cantar una canción", "Darle instrucciones paso a paso a una máquina", "Pintar un cuadro"], "c": 1}
                ]
            },
            "delta": {
                "title": "Variables, Tipos y Control de Flujo",
                "intro": "Las variables son cajas donde guardamos información. Pueden guardar números, nombres o incluso si una puerta está abierta o cerrada.",
                "architecture": "El flujo de ejecución decide qué camino toma el programa. Si hay energía, enciende la luz; si no, espera a que cargue.",
                "security": "Validar los datos es vital. No permitas que un usuario escriba letras donde el sistema espera números, o podrías causar un error crítico.",
                "challenge": "Escribe un pequeño programa que pregunte la edad y decida si alguien puede entrar a la zona de juegos.",
                "fact": "Python es uno de los lenguajes más populares del mundo porque su sintaxis se parece mucho al inglés cotidiano.",
                "quiz": [
                    {"q": "¿Qué es una variable en programación?", "a": ["Un tipo de computadora", "Una caja donde se guarda información", "Un cable de red"], "c": 1},
                    {"q": "¿Por qué es importante validar datos de entrada?", "a": ["Para que la pantalla brille más", "Para evitar errores y vulnerabilidades", "Para acelerar internet"], "c": 1}
                ]
            },
            "omega": {
                "title": "Paradigmas de Programación y Escalabilidad",
                "intro": "La programación orientada a objetos (POO) permite modelar el mundo real en el código, creando sistemas modulares y fáciles de mantener.",
                "architecture": "Analizaremos clases, herencia y polimorfismo. Estas herramientas permiten que miles de programadores trabajen en el mismo núcleo sin chocar entre sí.",
                "security": "El encapsulamiento protege los datos sensibles. Las variables privadas aseguran que solo las funciones autorizadas puedan modificar el estado crítico del sistema.",
                "challenge": "Diseña la estructura de clases para un sistema bancario digital, asegurando que el saldo no pueda ser modificado directamente.",
                "fact": "C++ es el lenguaje que corre la mayoría de los motores de videojuegos modernos.",
                "quiz": [
                    {"q": "¿Qué paradigma modela el mundo real usando clases y objetos?", "a": ["Programación funcional", "Programación Orientada a Objetos (POO)", "Programación lineal"], "c": 1},
                    {"q": "¿Qué protege el encapsulamiento?", "a": ["Los cables del hardware", "Los datos sensibles de acceso no autorizado", "La velocidad del procesador"], "c": 1}
                ]
            }
        },
        "ethics": {
            "icon": "GAVEL",
            "alpha": {
                "title": "Ciudadanos del Espacio Digital",
                "intro": "En la Isla Digital, todos somos vecinos. Ser amable y ayudar a los demás es lo que hace que nuestra ciudad brille.",
                "architecture": "Las reglas son como puentes: nos permiten cruzar a nuevos lugares de forma segura y sin caernos.",
                "security": "Si alguien es rudo o te pide tus secretos, ¡pulsa el botón de ayuda! Los guardianes siempre están para protegerte.",
                "challenge": "¿Cómo ayudarías a un nuevo explorador que se siente perdido en el mapa estelar?",
                "fact": "La netiqueta es el conjunto de reglas para ser educado en internet.",
                "quiz": [
                    {"q": "¿Qué debemos hacer si alguien nos pide nuestros secretos en internet?", "a": ["Dárselos rápidamente", "Pedir ayuda a un adulto de confianza", "Apagar la computadora para siempre"], "c": 1}
                ]
            },
            "delta": {
                "title": "Propiedad Intelectual y Huella Digital",
                "intro": "Todo lo que haces en internet deja un rastro, como las huellas en la arena. Es importante que tus huellas sean de cosas de las que estés orgulloso.",
                "architecture": "Respetar el trabajo de los demás es fundamental. No copies dibujos o textos sin permiso del autor original.",
                "security": "Configura tu privacidad para que solo tus amigos vean lo que compartes. Tu información es un tesoro valioso.",
                "challenge": "Busca un ejemplo de una noticia falsa (Fake News) y explica cómo podrías darte cuenta de que no es verdad.",
                "fact": "Todo lo que publicas en internet puede estar visible para alguien en el futuro, incluso años después de que lo borres.",
                "quiz": [
                    {"q": "¿Qué es la huella digital?", "a": ["La marca de tu dedo en la pantalla", "El rastro que dejan tus acciones en internet", "Un tipo de virus"], "c": 1},
                    {"q": "¿Por qué es peligroso compartir información personal en redes sociales públicas?", "a": ["Porque internet se hace lento", "Porque desconocidos pueden usarla en tu contra", "Porque la pantalla se rompe"], "c": 1}
                ]
            },
            "omega": {
                "title": "Algoritmos, Sesgo y Sociedad Tecnológica",
                "intro": "La tecnología no es neutral; refleja los valores de quienes la crean. Entender esto es vital para construir un futuro más justo.",
                "architecture": "Los sistemas de recomendación pueden crear 'Burbujas de Filtro' que nos muestran solo lo que queremos ver, aislándonos de otras realidades.",
                "security": "La ética en la IA implica transparencia. Debemos poder explicar por qué un algoritmo tomó una decisión que afecta la vida de una persona.",
                "challenge": "Debate: ¿Deberían las redes sociales censurar información falsa o dejar que los usuarios decidan qué creer?",
                "fact": "El sesgo de confirmación nos hace creer más fácilmente aquello que ya encaja con nuestras ideas.",
                "quiz": [
                    {"q": "¿Qué son las 'Burbujas de Filtro' en redes sociales?", "a": ["Publicidades de jabón", "Algoritmos que solo muestran contenido afín a tus ideas", "Errores de conexión"], "c": 1},
                    {"q": "¿Qué implica la transparencia en la IA?", "a": ["Que la IA sea invisible", "Poder explicar por qué la IA tomó una decisión", "Que la IA trabaje más rápido"], "c": 1}
                ]
            }
        }
    }

    @classmethod
    def get_unit(cls, unit_id: str, protocol: str):
        unit = cls.UNITS.get(unit_id)
        if not unit:
            return None
        
        content = unit.get(protocol)
        if not content:
            return None
            
        return {
            "id": unit_id,
            "icon": unit["icon"],
            **content
        }

    @classmethod
    def get_all_units(cls, protocol: str):
        units = []
        for unit_id in cls.UNITS:
            unit = cls.get_unit(unit_id, protocol)
            if unit is not None:
                units.append(unit)
        return units
