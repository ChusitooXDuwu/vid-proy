# Time-Pilot-MISW4407

## Integrantes del grupo

| Nombre | Login |
| ------ | ----- |
| Nicolas Carvajal Chaves | n.carvajalc |
| Wyo Hann Chu Mendez | w.chu | 
| Sofia Velasquez Marin | s.velasquezm2 |
| Julian Padilla Molina | j.padilla |



## Enunciado

Aplicar todos los conocimientos aprendidos durante las primeras cuatro semanas del curso de Introducción a desarrollo de videojuegos. Todos estos conocimientos serán empleados en la creación de la reproducción exacta de un juego conocido.

## Objetivos

Los objetivos que este proyecto aplicará son:

- Aplicar la estructura básica del patrón gameloop en un proyecto de desarrollo de videojuego.

- Aplicar las bases de la estructura de la arquitectura ECS (Entidad-Componente-Sistema) en un proyecto de desarrollo de videojuego.

- Matemáticas en videojuegos

- Entender e implementar un sistema básico de colisión

- Reconocer y aplicar el patrón de diseño command, para el diseño de input de dispositivos y acciones.

- Identificar el concepto de "Game feel" y su aplicación en los videojuegos.

- Entender los conceptos básicos de texturas, sprites y animación 2D cuadro a cuadro, e implementar en un programa real.

- Aplicar el patrón "State" y utilizarlo en un programa real con el uso de IA de varias entidades en un juego.

- Entender los conceptos básicos de administración de recursos (assets) e implementar en un programa real, usando el patrón service locator.

- Conocer los métodos de despliegue de videojuegos para diferentes plataformas, y aplicar métodos específicos de despliegue en el lenguaje Python para escritorio y web.

Existen objetivos enseñados en la siguientes semanas que se considerarán un bono si se implementan:

- Reconocer el concepto de escena, y su manejo abstracto como patrón, y aplicar este conocimiento en un proyecto de juego real.

- Reconocer e identificar las diferencias entre motores de juegos y APIs o frameworks para juegos.

- Reconocer las diferentes formas de clasificación de herramientas en videojuegos y su aplicación en la creación de uno.

- Reconocer el concepto de IA de steering behaviours, su impacto en el concepto de emergencia, y aplicarlo en un juego.

## Producto o entregable (Clon de Time Pilot)

El proyecto consiste en realizar una reproducción de un juego clásico. El juego en cuestión es una versión del juego arcade Time Pilot, creado por Konami en 1982.

El proyecto tiene un fuerte énfasis en la exactitud: no es un proyecto “similar”, no es un proyecto “inspirado en”.

El producto final esperado debe ser lo más similar posible al juego original, replicando con las mismas dimensiones, sonidos y comportamientos.

Sin embargo, es posible extender el proyecto con los elementos que deseen, siempre y cuando se sienta como una extensión del juego actual, o una secuela.
Si desean jugarlo, pueden hacerlo aquí:
https://www.retrogames.me/arcade/time-pilot.html

Les recomiendo que modifiquen el juego con el botón de settings abajo a la derecha para que puedan modificarlo y "hacer trampa" colocando 256 vidas y reiniciando el emulador con el botón abajo a la izquierda. Así pueden apreciar todos los niveles y examinar con calma los comportamientos. Si usan "save states" pueden guardar estados en cada nivel para no tener que repetir todo para analizarlo bien.

Pueden observar este video de gameplay como base para el proyecto final. (https://youtu.be/_TC_eH1E5Gw)

## Requisitos funcionales del proyecto

Para ser claros, del proyecto no se espera una realización 100% del juego presentado, pero sí se espera el mejor esfuerzo para reproducir el videojuego lo más fiel posible.

### Requerimientos obligatorios

El proyecto va a pedir exactitud en los siguientes elementos, los cuales servirán para obtener un 100% de la nota:

- Uso de la arquitectura ECS para el desarrollo del proyecto

  - Si el proyecto no utiliza arquitectura ECS en su mayoría, no será aceptado, así cumpla los demás requisitos.

-Una pantalla de menú principal con el titulo del juego e instrucciones para comenzar a jugar.

- Dibujado y movimiento de las nubes, junto con el color del fondo de acuerdo al nivel.

- Movimiento de la nave jugador con el ratón o con flechas

- Disparo de la nave del jugador con la tecla Z o el botón del ratón

- Generación progresiva de enemigos de acuerdo al nivel a una velocidad específica.

  - También hay un limite de seis (6) aeronaves en la pantalla a la vez

- Ataque de los enemigos en persecución contra el jugador que se acercan varias veces y luego se retiran (Steering behaviours)

- Disparo de balas por parte de los enemigos ocasionalmente en su movimiento básico.

  - También disparan a veces un misil pequeño. Es menos ocasional esta versión de proyectil.

- Colisión de balas enemigas con el jugador y balas del jugador con los enemigos.

- La posibilidad de pausar el juego con un botón de teclado de pausa y un texto que parpadee que diga PAUSED.

  - Las imágenes se siguen viendo excepto el jugador y los enemigos y el texto de PAUSED se ve en el centro de la pantalla.

- Texto de la fecha de acuerdo al nivel y sonido de introducción al comenzar el primer nivel.

- Al eliminar 40 enemigos, sale el "enemigo final" viaja horizontalmente en la pantalla. Si se sale de la pantalla vuelve a salir después de un rato.

  - Al eliminarlo se gana el nivel y los demás enemigos se destruyen (no cuentan como puntaje). Si no se implementan mas niveles se puede repetir e nivel o volver al menú principal.

- Despliegue del texto de puntaje en la parte superior con su texto 1-UP

- Un contador de enemigos eliminados en la parte de abajo a la izquierda (el juego original usa naves como UI de ese contador, pueden utilizar un número para cumplir el requisito básico, el UI completo se describe como un bono)

- Un mensaje de GAME OVER y reinicio del nivel cuando el personaje muera por una bala. Al perder todas las vidas (si se tiene varias) vuelve al menú principal.

- Sonidos implementados y animación de imágenes

- Distribución en a través del portal itch.io

  - Se recomienda que sea distribución web o distribución en windows

### Requerimientos opcionales de bonificación

Esto requerimientos a continuación se consideran requerimientos de bonificación y pueden ser usados para obtener una notar sobre el 100%

- Sistema de vidas del jugador (cuatro vidas definidas por un archivo de configuración)

    - EL jugador recupera vidas al adquirir 10 mil puntos y luego cada 50 mil (es decir la segunda vida es a los 60 mil puntos, y la tercera a los 110 mil puntos, etcétera).

- Implementación del contador de enemigos eliminados vía interfaz con aviones de UI (en vez de usar un numero).

- Sistema de puntaje máximo del juego (usando un archivo de configuración con el puntaje inicial máximo en 10000) con su texto HI-SCORE

- Pantalla de High Score final final con al posibilidad escribir el nombre si logra estar en la tabla.

- Crear más de un nivel y poder ir de un nivel a otro como lo muestra el juego al eliminar el enemigo final de ese nivel.

    - Los niveles tiene un contador arriba a la izquierda que se acumulan con cada nivel (hay imágenes para uno, cinco y diez niveles)

- Existe un objeto de bono en un paracaídas que desciende y da puntos extra. Implementarlo.

    - Existe otra nave de bono que viaja horizontalmente y da puntos al eliminarla. Implementarla.

- Algunos enemigos salen en escuadrón ocasionalmente diferente a los otros que salen regularmente.

- Los arcades antiguos tenía un modo "atracción" que simulaba el juego para que la gente se acercara. Esto se ve al principio del vídeo. Implementar un modo "atracción".

- Cualquier  vista de depurado que desarrollen sobre el juego para observar mejor elementos del nivel en modo depuración

- Cualquier herramienta de edición que desarrollen sobre el juego para editar y/o guardar niveles

- Cualquier efecto o elemento especial del jugador o enemigos que deseen implementar que no esté en el juego original. Esto puede ser:

    - Un arma secundaria especial

    - Enemigos especiales

    - Niveles diferentes o especiales de bono.

    - Efectos especiales en la pantalla o las entidades

    - Etcétera.

- Juego a dos jugadores

- Implementar input de juego con gamepads o controles de juego en adición a teclado/ratón.

A lo largo del proyecto también existen otros entregables, como documentos y código fuente. 

### Recursos para el proyecto

Para evitar problemas de copyright, se utilizarán imágenes y sonidos libres, que conservan las características originales del juego para representar los mismo restos.

Pueden descargar los recursos del proyecto en el sitio web:
(PROYECTO FINAL - RECURSOS DEL PROYECTO)

https://misw-4407-desarrollo-de-videojuegos.github.io/web-cohorte-2025-12/

En el enlace se encuentran los siguiente elementos:

- Imágenes: imágenes animadas y no animadas de todos los elementos del juego

- Sonidos: Los sonidos necesarios para el funcionamiento del juego

- Fuente: Una fuente de pixel que coincide con el estilo del juego

- No hay archivos de configuración. Se espera que ustedes creen su propia configuración. Pueden usar los formatos usados en los ejercicios individuales, pero es de esperar que tengan que crear los suyos para vairas cosas del juego.

### Proceso

El proyecto consistirá en una serie de entregables formativos a lo largo de las cuatro primeras semanas. Comenzado con un documento de propuesta de proyecto, seguido por un avance y al final con un entregable final y un post-mortem tanto grupal como individual.

Se ofrecerá asistencia continua en las sesiones asíncronas del curso y en el canal oficial de Slack del curso.

#### Trabajo en equipo
El desarrollo del proyecto debe ser en grupos. Los grupos son de al menos tres personas, máximo cuatro. No se permitirán proyectos individuales bajo ninguna circunstancia. Proyectos en parejas serán evaluados en caso por caso.

La asignación de equipos será responsabilidad de los estudiantes en la cuarta semana y antes de la primera entrega de avance, que deberá ser grupal.

Es importante hacer énfasis que este es un curso de programación de videojuegos. Aunque es posible que puedan hacer algún arte, o sonido o algo adicional para este proyecto, se espera que todos los integrantes del grupo programen. Se espera que cada miembro del equipo contribuya en programación y código, y esto se refleje dentro del proyecto. No hacerlo acarreará una penalización de la nota.

La documentación y proyectos a entregar en cada hito se harán de manera grupal. La excepción será la última entrega, que también tendrá un post-mortem individual en adición al post-mortem grupal.

## Entregas formativas (no calificables)

Las primeras tres entregas formativas del proyecto no son obligatorias, ni calificables. Pero si se considerarán como una invitación para los profesores y tutores que desean una revisión del estado del proyecto. Entonces consideren las entregas como una mentoría del proyecto.
Formato de entregas formativas (no calificable):

- Nombre y descripción del grupo. 

    - Integrantes, correos, sitio github público, y de documentos que tengan en el momento.

    - Propuesta técnica de proyecto 
    ¿desde un punto de vista técnico y arquitectónico, como piensan afrontar este trabajo?

- Documento de avance:

    - Una descripción inicial de la arquitectura propuesta para el proyecto. Debe seguir la estructura básica de ECS para ser válido

    - Descripción de los cambios ocurridos en la arquitectura hasta ahora.

    - Descripción de cada integrante en que ha hecho y en qué ha trabajado.

    - Planes para determinar el alcance para la entrega final.

- Código fuente elaborado hasta el momento.

## Entrega sumativa final (calificable)

La última semana será una entrega sumativa calificable de todo el proyecto. Los elementos a entregar serán:

- Proyecto finalizado con ejecutable compilado, ya sea para web o para descarga en un portal web (GameJolt o itch.io).

    - El juego se encuentra publicado en el estado que se encuentra en un portal web de juegos, ya sea itch.io, Gamejolt, Newgrounds o cualquier portal parecido.

    - Se publica una descripción del juego y pantallazo del mismo.

    - Bonificaciones aplicadas si el juego contiene elementos de bonificación.

- Código fuente del proyecto final. 

    - Enlace en github con un tag final asociado a una descripción

    - El código fuente refleja el funcionamiento de lo publicado.

    - Tiene un trabajo notorio y progresivo a lo largo de las semanas, según los registros en github.

- Documento de descripción de arquitectura y post-mortem grupal.

    - Describe un resumen del proceso de desarrollo del proyecto,  junto con una evolución del proceso de creación del juego pro semana

    - Contiene una análisis  arquitectónico del juego  (organización de clases, componentes y sistemas y por qué se tomaron esas decisiones) con diagramas  si es posible.

    - Análisis y opinión grupal de los patrones usados, en particular ECS, con la creación de juegos vs otras aplicaciones.

    - ¿Qué salió bien? ¿Qué salió mal? ¿Qué se puede cambiar futuro?

- Documento post-mortem individual (ENTREGA INDIVIDUAL)

    - Elaboración personal e individual de un documento post-mortem

    - Descripción individual de lo que trabajo de su rol en el proyecto de manera específica.

    - Qué salió bien, mal y que cambiarían para un nuevo proyecto a título personal.

    - Resumen de lo aprendido y análisis de lo aprendido en relación con la creación de videojuegos.

- **Presentación en vivo o preparada del proyecto final**: Un video explicando el resultado del proyecto. En esencia, un post-mortem en forma de presentación, que incluye:

    - Presentación del juego, equipo y roles

    - Explicación de la arquitectura ECS 

        - ¿Qué componentes, sistemas crearon y por qué?

        - ¿Qué archivos de configuración usaron?

        - ¿Que paradigmas, además de ECS, utilizaron?

    - Explicación del trabajo de cada persona

    - Pueden incluir un tráiler si lo desean, pero no es obligatorio

## Criterios de retroalimentación y evaluación

La evaluación de proyecto se dividirá entre cada ítem entregado.

- Entregables del proyecto final (50%) Compuesto de:

    - Juego publicado en WEB (20%)

    - Enlace al código fuente del proyecto (10%)

    - Documento de post-mortem en grupo (10%)

    - Documento post-mortem individual (10%)

- Video en vivo o preparado de presentación del proyecto (10%)

## Recomendaciones para un proyecto exitoso

Para poder terminar este proyecto de manera satisfactoria, se recomienda ampliamente hacer lo siguiente:

- Observar los videos y video tutoriales ofrecidos en cada semana. Estos van a hablar de temas fundamentales para aplicar en el proyecto, especialmente para las bonificaciones.

- Utilizar los programas creados en los ejercicios individuales y las demostraciones es altamente recomendado y alentado a que lo hagan para poder terminar el proyecto de manera satisfactoria.

- Se recomienda ampliamente implementar algún sistema de trampas o de acceso rápido a todas las características de su juego para que se pueda apreciar bien lo que hallan implementado. Ofrecer esto en el README o las instrucciones del proyecto al ser subido.

- Consulten sus problemas con los tutores, monitores o profesores, ellos estarán en mentoría con ustedes para una resolución satisfactoria del proyecto.