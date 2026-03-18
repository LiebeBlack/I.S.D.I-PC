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
            "title": "CENTRO DE EXPLORACIÓN ALPHA",
            "labels": ["Oxígeno", "Energía", "Escudo"],
            "mission": "¡Hola explorador! Tu nave está lista para descubrir nuevos mundos digitales. ¿Estás listo?"
        },
        "delta": {
            "title": "CONTROL DE OPERACIONES DELTA",
            "labels": ["Sinc_CPU", "Enlace_Red", "Seguridad"],
            "mission": "Agente Delta, el sistema está bajo tu supervisión. Vigila que todo funcione correctamente."
        },
        "omega": {
            "title": "INTERFAZ DE ARQUITECTURA OMEGA",
            "labels": ["Carga_Kernel", "Nodos_Activos", "Nivel_Amenaza"],
            "mission": "Arquitecto Omega, la integridad del núcleo depende de tu análisis técnico avanzado."
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
                "title": "La Gran Máquina: Los Motores de la Nave",
                "intro": "Imagina que la computadora es una nave espacial. Para viajar entre las estrellas, necesita motores que piensen, memorias que recuerden el camino y un armazón que proteja todo.",
                "architecture": "Dentro, el 'Cerebro Central' (CPU) da todas las órdenes. Los cables son como venas por donde corre la energía y la información, permitiendo que cada parte trabaje en armonía.",
                "security": "Una nave debe estar limpia y cuidada. No permitimos que entre polvo ni elementos extraños que puedan dañar los motores. El cuidado físico es nuestra primera defensa.",
                "challenge": "¿Si tu computadora fuera una ciudad, qué edificio sería el Procesador y por qué?",
                "fact": "¡Dato mágico! Las computadoras usan luces invisibles para enviarse mensajes, ¡como hadas de datos!"
            },
            "delta": {
                "title": "Arquitectura de Sistemas: El Ciclo de Datos",
                "intro": "El hardware no es solo metal y silicio; es una estructura lógica diseñada para procesar información a velocidades increíbles mediante impulsos eléctricos.",
                "architecture": "La placa base actúa como el sistema nervioso, conectando el CPU, la RAM y el almacenamiento. La RAM es el espacio de trabajo inmediato, mientras que el disco duro es el archivo a largo plazo.",
                "security": "La integridad del hardware depende de un entorno controlado. El sobrecalentamiento y las fluctuaciones de energía son riesgos que deben ser gestionados mediante sistemas de enfriamiento y protección eléctrica.",
                "challenge": "Dibuja un diagrama donde expliques el viaje de un dato desde que presionas una tecla hasta que aparece en pantalla.",
                "fact": "Dato Técnico: Un bit es la unidad mínima de información, ¡un simple Sí o No!"
            },
            "omega": {
                "title": "Ingeniería de Sistemas y Microarquitectura",
                "intro": "La computación moderna se basa en la abstracción de niveles, desde puertas lógicas hasta complejos sistemas operativos. Entender el hardware es entender la base de la computación cuántica y tradicional.",
                "architecture": "Analizaremos la arquitectura de Von Neumann: la separación entre la unidad de procesamiento y la memoria. Exploraremos cómo los ciclos de reloj y el ancho de banda definen el rendimiento de un sistema escalable.",
                "security": "A nivel de arquitectura, existen vulnerabilidades críticas como ataques de ejecución especulativa (Spectre/Meltdown). La seguridad comienza en el diseño del chip y la gestión de privilegios del kernel.",
                "challenge": "Investiga y explica cómo una vulnerabilidad a nivel de hardware puede comprometer todo el cifrado de un sistema operativo.",
                "fact": "Protocolo de Seguridad: Una contraseña fuerte tarda siglos en ser descifrada por una computadora normal.",
                "quiz": [
                    {"q": "¿Qué arquitectura separa la memoria del procesador?", "a": ["Von Neumann", "Harvard", "RISC"], "c": 0}
                ]
            }
        },
        "logic": {
            "icon": "TERMINAL",
            "alpha": {
                "title": "El Idioma Secreto de las Luces",
                "intro": "Las computadoras solo hablan un idioma de dos letras: Encendido y Apagado. Es como un código de espejos que permite contar historias complejas usando solo ceros y unos.",
                "architecture": "Cuando agrupamos estas luces, formamos instrucciones. Como una receta de cocina, la computadora sigue cada paso sin saltarse ninguno para crear algo maravilloso.",
                "security": "Decir la verdad es importante. En el mundo digital, nos aseguramos de que las instrucciones sean claras y honestas para que la nave no se confunda de camino.",
                "challenge": "Intenta explicarle a un robot cómo hacer un sándwich, pero usando solo pasos de 'Sí' o 'No'.",
                "fact": "¡Sabías que...? La primera programadora fue una mujer llamada Ada Lovelace.",
                "quiz": [
                    {"q": "¿Cómo se llama el idioma de las computadoras?", "a": ["Binario", "Español", "Robótico"], "c": 0}
                ]
            },
            "delta": {
                "title": "Lógica Procedimental y Algoritmos",
                "intro": "Un algoritmo es una secuencia finita de instrucciones definidas y no ambiguas que representan un modelo de solución para un problema determinado.",
                "architecture": "Exploraremos las estructuras de control: bucles, condicionales y funciones. Estas herramientas permiten que el software tome decisiones basadas en variables de entrada y estados del sistema.",
                "security": "Los algoritmos deben ser auditables. Un código mal estructurado puede ocultar errores lógicos que comprometen la estabilidad del sistema o permiten fugas de información no deseadas.",
                "challenge": "Escribe el pseudocódigo para un sistema que verifique si una contraseña cumple con los requisitos mínimos de seguridad.",
                "fact": "La palabra 'Algoritmo' viene del nombre de un matemático persa llamado Al-Juarismi.",
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
                "title": "Hilos Invisibles entre Estrellas",
                "intro": "El internet es como una red de pesca gigante que envuelve al mundo, conectando cada nave y cada planeta para que podamos enviarnos mensajes y dibujos al instante.",
                "architecture": "La información viaja en pequeños paquetes, como cartas en naves mensajeras rápidas. Cada casa tiene una dirección única para que los mensajes nunca se pierdan en el espacio.",
                "security": "En esta red, viajamos acompañados de guardianes. Nunca abrimos la puerta a naves desconocidas y siempre usamos un lenguaje secreto que solo nosotros y nuestros amigos entendemos.",
                "challenge": "¿Cómo crees que viaja una foto desde tu casa hasta la de un amigo que vive muy lejos?",
                "fact": "Existen cables gigantes debajo del mar que conectan todos los continentes."
            },
            "delta": {
                "title": "Conectividad y Protocolos de Red",
                "intro": "Las redes de computadoras permiten el intercambio de recursos e información mediante protocolos estandarizados como el TCP/IP, que aseguran que los datos lleguen íntegros a su destino.",
                "architecture": "Estudiaremos el modelo cliente-servidor. Cuando navegas por la web, tu dispositivo solicita información a un servidor remoto, el cual responde enviando los datos organizados en paquetes numerados.",
                "security": "El uso de redes públicas conlleva riesgos de interceptación. Es vital utilizar protocolos cifrados (HTTPS) y firewalls que filtren el tráfico malicioso antes de que alcance nuestra red local.",
                "challenge": "Explica la diferencia entre una dirección IP privada y una dirección IP pública.",
                "fact": "¡El primer mensaje enviado por Arpanet (el abuelo del Internet) fue 'LO'!"
            },
            "omega": {
                "title": "Topología de Redes y Seguridad Perimetral",
                "intro": "La infraestructura global de red es un sistema complejo de sistemas autónomos interconectados. El entendimiento de las capas del modelo OSI es fundamental para cualquier analista de sistemas.",
                "architecture": "Analizaremos el enrutamiento dinámico, el DNS y cómo la latencia afecta a las aplicaciones distribuidas. La transición de IPv4 a IPv6 es un reto crítico para la escalabilidad de la red global.",
                "security": "La implementación de una estrategia de Defensa en Profundidad incluye VPNs, Sistemas de Detección de Intrusos (IDS) y la segmentación de redes para mitigar el movimiento lateral de atacantes.",
                "challenge": "Investiga qué es un ataque de 'Man-in-the-Middle' y cómo el protocolo TLS previene este tipo de interceptación.",
                "fact": "El protocolo TCP/IP fue diseñado para ser tan robusto que pudiera sobrevivir a un ataque nuclear."
            }
        },
        "cybersecurity": {
            "icon": "SECURITY",
            "alpha": {
                "title": "El Escudo de Cristal",
                "intro": "En nuestro viaje digital, llevamos un escudo de cristal que brilla cuando somos cuidadosos. Proteger nuestra información es tan importante como llevar casco en el espacio.",
                "architecture": "Este escudo se fortalece con llaves secretas y puertas cerradas. No compartimos nuestras llaves con nadie, porque son las que mantienen nuestra nave segura y privada.",
                "security": "La amabilidad es nuestra mejor regla. Si algo en el espacio digital nos hace sentir incómodos, avisamos de inmediato a los comandantes de nuestra base (padres o maestros).",
                "challenge": "¿Qué harías si una nave desconocida te pide la llave de tu casa digital?",
                "fact": "¡Captcha significa: Prueba de Turing pública y automática para diferenciar a computadoras de humanos!"
            },
            "delta": {
                "title": "Ciberseguridad Activa y Privacidad",
                "intro": "La ciberseguridad es la práctica de proteger sistemas, redes y programas de ataques digitales. Estos ataques suelen apuntar a acceder, cambiar o destruir información sensible.",
                "architecture": "La autenticación multifactor (MFA) añade una capa extra de protección más allá de la contraseña. La criptografía convierte tus mensajes en códigos que solo el destinatario puede descifrar.",
                "security": "La ingeniería social es una técnica de manipulación que busca obtener datos confidenciales. Desconfiar de correos sospechosos (Phishing) es fundamental para mantener la integridad de tus cuentas.",
                "challenge": "Crea una lista de 5 reglas de oro para mantener tus perfiles en línea protegidos de intrusos.",
                "fact": "La mayoría de los ataques exitosos no son por fallas técnicas, sino por engañar a las personas (Ingeniería Social)."
            },
            "omega": {
                "title": "Criptografía Avanzada y Gestión de Amenazas",
                "intro": "En un entorno hostil, la seguridad no es un producto, sino un proceso continuo de monitoreo y respuesta. El principio de 'Confianza Cero' (Zero Trust) debe regir toda arquitectura moderna.",
                "architecture": "Exploraremos el cifrado asimétrico (claves públicas y privadas) y el hashing. Entender cómo se firman digitalmente los certificados permite validar la autenticidad de cualquier servicio en línea.",
                "security": "El análisis de malware y la respuesta ante incidentes son pilares de la ciberdefensa. Las organizaciones deben poseer planes de continuidad de negocio y recuperación ante desastres para enfrentar amenazas como el Ransomware.",
                "challenge": "Debate sobre las implicaciones éticas y técnicas de la encriptación de extremo a extremo frente a las solicitudes de acceso por parte de autoridades gubernamentales.",
                "fact": "La computación cuántica podría romper la mayoría de los cifrados actuales en el futuro cercano."
            }
        },
        "os": {
            "icon": "SETTINGS_SYSTEM_DAYDREAM",
            "alpha": {
                "title": "El Director de Orquesta Digital",
                "intro": "El Sistema Operativo es como el director de una orquesta, asegurándose de que cada músico (el hardware) toque en el momento justo para crear una canción perfecta.",
                "architecture": "Su trabajo es repartir el tiempo y el espacio. Decide quién puede hablar y quién debe esperar, manteniendo el orden para que tú puedas jugar y aprender sin problemas.",
                "security": "Un buen director cuida que nadie interrumpa la función. El sistema operativo pone vallas invisibles entre los programas para que si uno falla, los demás sigan funcionando.",
                "challenge": "¿Si tu computadora fuera una casa, qué tareas haría el Sistema Operativo para mantenerla en orden?",
                "fact": "El primer sistema operativo fue creado por General Motors en 1956 para una computadora IBM."
            },
            "delta": {
                "title": "Gestión de Recursos y Kernel",
                "intro": "El Sistema Operativo (SO) es el software que gestiona el hardware y actúa como intermediario entre el usuario y la máquina, administrando memoria, procesos y archivos.",
                "architecture": "El núcleo o 'Kernel' es la parte más interna. Se encarga de la planificación de procesos (Scheduling) y la gestión de la memoria RAM, asegurando que los recursos se utilicen de forma eficiente.",
                "security": "La gestión de permisos es vital. El SO utiliza listas de control de acceso (ACL) para decidir qué usuarios o aplicaciones pueden leer, escribir o ejecutar archivos específicos.",
                "challenge": "Investiga qué sucede cuando dos programas intentan usar el mismo recurso al mismo tiempo. ¿Cómo lo resuelve el SO?",
                "fact": "¡Linux está en todas partes! Desde tu teléfono Android hasta la Estación Espacial Internacional."
            },
            "omega": {
                "title": "Microkernels, Virtualización y Abstracción",
                "intro": "Los sistemas operativos modernos implementan capas de abstracción complejas para permitir la ejecución de múltiples entornos sobre un mismo hardware físico.",
                "architecture": "Exploraremos el espacio de usuario frente al espacio de kernel. Estudiaremos cómo las llamadas al sistema (syscalls) permiten una comunicación segura y controlada entre las aplicaciones y el hardware.",
                "security": "El aislamiento mediante 'Sandboxing' y contenedores es esencial. Analizaremos cómo las vulnerabilidades de escalada de privilegios intentan romper estas barreras para obtener control total del sistema.",
                "challenge": "Explica la diferencia técnica entre un proceso y un hilo (thread), y por qué el aislamiento de procesos es una medida de seguridad crítica.",
                "fact": "Windows originalmente se iba a llamar 'Interface Manager', pero el equipo de marketing prefirió 'Windows'."
            }
        },
        "ai": {
            "icon": "PSYCHOLOGY",
            "alpha": {
                "title": "Máquinas que Aprenden a Mirar",
                "intro": "La Inteligencia Artificial es como un robot que estudia millones de fotos y cuentos para aprender a reconocer cosas, tal como tú aprendes en la escuela.",
                "architecture": "No es magia, son matemáticas. La IA busca patrones: si ve muchas fotos de gatos, aprende que las orejas puntiagudas y los bigotes significan 'Gato'.",
                "security": "Debemos enseñar a la IA a ser justa y buena. Ella aprende de lo que nosotros le damos, así que debemos darle solo la mejor y más honesta información.",
                "challenge": "¿Cómo le explicarías a una IA qué es la felicidad usando solo imágenes?",
                "fact": "¡Una IA ya ha logrado ganarle a los mejores jugadores del mundo en juegos como el Ajedrez y Go!"
            },
            "delta": {
                "title": "Redes Neuronales y Aprendizaje Automático",
                "intro": "La IA se basa en algoritmos inspirados en el cerebro humano para procesar datos y tomar decisiones o predicciones basadas en la experiencia previa.",
                "architecture": "El Machine Learning utiliza datos para 'entrenar' modelos. Mediante redes neuronales artificiales, la IA puede identificar tendencias complejas que serían imposibles de detectar manualmente.",
                "security": "El sesgo algorítmico es un riesgo ético. Si los datos de entrenamiento están sesgados, la IA tomará decisiones injustas. La transparencia en los algoritmos es fundamental para la confianza digital.",
                "challenge": "Piensa en una IA que uses a diario (como un recomendador de videos). ¿Cómo crees que decidió qué mostrarte hoy?",
                "fact": "El término 'Inteligencia Artificial' se acuñó en una conferencia en la universidad de Dartmouth en 1956."
            },
            "omega": {
                "title": "Ética del Algoritmo y Deep Learning",
                "intro": "La Inteligencia Artificial generativa y los grandes modelos de lenguaje (LLM) están transformando la sociedad. Entender su arquitectura es entender el futuro del trabajo y la verdad.",
                "architecture": "Analizaremos el concept de 'Caja Negra' en modelos de aprendizaje profundo y la importancia de la 'IA Explicable'. Veremos cómo los transformadores permiten procesar contextos masivos de información.",
                "security": "Los ataques de envenenamiento de datos (Data Poisoning) y los Deepfakes son amenazas críticas. La integridad de la información depende de nuestra capacidad para verificar la procedencia de los contenidos generados.",
                "challenge": "Debate: ¿Quién es responsable si una IA toma una decisión errónea en un sistema crítico de salud o defensa?",
                "fact": "Las redes neuronales artificiales no son nuevas; ¡la idea básica existe desde los años 40!"
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
                "fact": "¡El primer lenguaje de programación se llamó Plankalkül!"
            },
            "delta": {
                "title": "Variables, Tipos y Control de Flujo",
                "intro": "Las variables son cajas donde guardamos información. Pueden guardar números, nombres o incluso si una puerta está abierta o cerrada.",
                "architecture": "El flujo de ejecución decide qué camino toma el programa. Si hay energía, enciende la luz; si no, espera a que cargue.",
                "security": "Validar los datos es vital. No permitas que un usuario escriba letras donde el sistema espera números, o podrías causar un error crítico.",
                "challenge": "Escribe un pequeño programa que pregunte la edad y decida si alguien puede entrar a la zona de juegos.",
                "fact": "Python es uno de los lenguajes más populares porque se lee casi como el inglés."
            },
            "omega": {
                "title": "Paradigmas de Programación y Escalabilidad",
                "intro": "La programación orientada a objetos (POO) permite modelar el mundo real en el código, creando sistemas modulares y fáciles de mantener.",
                "architecture": "Analizaremos clases, herencia y polimorfismo. Estas herramientas permiten que miles de programadores trabajen en el mismo núcleo sin chocar entre sí.",
                "security": "El encapsulamiento protege los datos sensibles. Las variables privadas aseguran que solo las funciones autorizadas puedan modificar el estado crítico del sistema.",
                "challenge": "Diseña la estructura de clases para un sistema bancario digital, asegurando que el saldo no pueda ser modificado directamente.",
                "fact": "C++ es el lenguaje que corre la mayoría de los motores de videojuegos modernos."
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
                "fact": "La netiqueta es el conjunto de reglas para ser educado en internet."
            },
            "delta": {
                "title": "Propiedad Intelectual y Huella Digital",
                "intro": "Todo lo que haces en internet deja un rastro, como las huellas en la arena. Es importante que tus huellas sean de cosas de las que estés orgulloso.",
                "architecture": "Respetar el trabajo de los demás es fundamental. No copies dibujos o textos sin permiso del autor original.",
                "security": "Configura tu privacidad para que solo tus amigos vean lo que compartes. Tu información es un tesoro valioso.",
                "challenge": "Busca un ejemplo de una noticia falsa (Fake News) y explica cómo podrías darte cuenta de que no es verdad.",
                "fact": "Lo que publicas hoy puede ser visto por alguien en el futuro distante."
            },
            "omega": {
                "title": "Algoritmos, Sesgo y Sociedad Tecnológica",
                "intro": "La tecnología no es neutral; refleja los valores de quienes la crean. Entender esto es vital para construir un futuro más justo.",
                "architecture": "Los sistemas de recomendación pueden crear 'Burbujas de Filtro' que nos muestran solo lo que queremos ver, aislándonos de otras realidades.",
                "security": "La ética en la IA implica transparencia. Debemos poder explicar por qué un algoritmo tomó una decisión que afecta la vida de una persona.",
                "challenge": "Debate: ¿Deberían las redes sociales censurar información falsa o dejar que los usuarios decidan qué creer?",
                "fact": "El sesgo de confirmación nos hace creer más fácilmente aquello que ya encaja con nuestras ideas."
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
            units.append(cls.get_unit(unit_id, protocol))
        return units
