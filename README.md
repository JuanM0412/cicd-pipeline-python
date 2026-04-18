# Respuestas a Preguntas de CI/CD

### 1. ¿Qué ventajas le proporciona a un proyecto el uso de un pipeline de CI?
Un pipeline de Integración Continua (CI) aporta ventajas fundamentales como:
*   **Detección temprana de errores:** Al compilar y ejecutar pruebas de forma automática con cada `push` o `Pull Request` (PR), el equipo puede detectar fallos inmediatamente (un linter fallando, un unit test roto) antes de mezclar el código con la rama principal.
*   **Calidad de código constante e inquebrantable:** El sistema automatizado verifica la legibilidad y la deuda técnica (por medio de `Black`, `Flake8`, `Pylint` y el escaneo de `SonarCloud`). Esto garantiza que nadie integre código que no cumpla con los estándares acordados sin ser avisado.
*   **Automatización sin intervención humana:** Reduce enormemente el error humano a la hora de preparar entregables. No hay necesidad de empaquetar, hacer pruebas locales a mano, ni construir la imagen de Docker paso por paso; todo se desencadena de forma fiable.

### 2. Diferencia principal entre una prueba unitaria y una de aceptación (con ejemplo)
*   **Diferencia:** La prueba unitaria aísla una pequeña pieza de código (como una función) para probar que lógicamente funciona bajo ciertas entradas, desligada del sistema real. La prueba de aceptación (o End-to-End) revisa el sistema interactuando con él como lo haría el usuario real con un sistema completo y en funcionamiento (incluyendo la UI, base de datos y red).
*   **Ejemplo (Aplicación de tu Calculadora):**
    *   **Prueba Unitaria:** Tomar el archivo `calculadora.py` y probar simplemente que `dividir(10, 2)` devuelva `5.0`. No hay interfaz web ni conexión a un puerto, solo se ejecuta la orden nativa del lenguaje.
    *   **Prueba de Aceptación:** Desplegar el servidor web de Flask en `localhost:8000`, usar una librería (como Selenium, Playwright o requests) para simular que un usuario abre el navegador, ingresa '10' en el primer campo, '2' en el segundo y da clic al botón "Dividir". El test pasa si en el HTML devuelto por la página web aparece un mensaje visible diciendo `Resultado: 5.0`.

### 3. Explicación de los steps principales del workflow de GitHub Actions
*   **checkout:** Clona y descarga el código fuente de tu repositorio en la máquina virtual (runner) de GitHub Actions para poder acceder a los archivos.
*   **Set up Python:** Configura el entorno virtual instalando la versión exacta de Python que va a necesitar el proyecto.
*   **Install dependencies:** Ejecuta `pip install -r requirements.txt` para descargar librerías como Flask o Pytest.
*   **Run Black / Flake8 / Pylint:** Tres pasos diferentes dedicados a revisar el código. Black comprueba que esté formateado correctamente, y Flake8/Pylint revisan malas prácticas de sintaxis (análisis estático). Todo esto uniformiza el estilo del código en el equipo.
*   **Run Unit Tests:** Corre los tests unitarios (`pytest`) para certificar que el código local funciona, y emite un reporte de cobertura.
*   **Run Acceptance Tests:** Levanta el servidor con Gunicorn en fondo y luego lanza pruebas contra la aplicación en vivo (`test_acceptance_app.py`). Ayuda a confirmar que lo que el usuario va a ver realmente sirve.
*   **SonarCloud Scan:** Envía los reportes de cobertura de código generados por Pytest y analiza la "deuda técnica" del proyecto en la nube (bugs, code smells y vulnerabilidades de SonarQube).
*   **Set up QEMU & Docker Buildx:**  Prepara los motores de construcción de Docker que posibilitan un empaquetado más rápido e incluso en arquitecturas diferentes a la que estás usando (como ARM o x86).
*   **Login to Docker Hub & Build/Push:** Autentica a tu GitHub Actions frente a Docker Hub usando las variables configuradas como credenciales. Inmediatamente después, empaqueta el contenido utilizando el `Dockerfile`, crea la imagen final unificada y la publica en línea, dejándola lista para ser usada en casi cualquier servidor web de producción.

### 4. Problemas o dificultades encontradas
*   **Errores de Precisión Flotante:** Al diseñar `test_calculadora.py`, el uso del operador estricto `==` falló al manejar flotantes. Esto requirió investigar y reemplazar el chequeo lógico para que utilizara `math.isclose()` (o `pytest.approx`) y así asegurar que las aproximaciones decimales, por ejemplo al testear la división, no dispararan fallos falsos en la suite de pruebas.
*   **Conflicto de Análisis de SonarCloud:** Durante la configuración del pipeline, SonarCloud rechazaba la conexión del CI de GitHub Actions abortando el workflow. La dificultad radicaba en que el servicio alojaba el Análisis Automático por default mientras externamente se le solicitaba un Análisis tipo CI, por lo cual fue necesario dirigirse al portal de SonarCloud y desactivar la opción "Automatic Analysis" explícitamente para ceder todo el control al archivo del Workflow en GitHub.
*   **Estilo del linter (líneas largas):** Configurar Pylint/Flake8 fue muy estricto al inicio arrojando el error `line too long (213 > 79 characters)`. La solución consistió en romper manualmente el bloque en fragmentos cortos y agregar un correcto `Module Docstring`.

### 5. ¿Qué ventajas ofrece empaquetar la aplicación en una imagen Docker al final?
Principalmente ofrece la tranquilidad del principio **"se construye una vez, se despliega en cualquier lado"**. En lugar de sólo validar que el código es correcto, empaquetas la aplicación junto con su versión exacta del sistema operativo base, variables de entorno, Flask y Python, solucionando el mítico síndrome de "en mi máquina sí funciona".  
Al tener la imagen final de Docker de tu calculadora alojada (y testeada) en el registro, el sistema en Producción ya no necesita instalar programas extraños o dependencias por `pip`; únicamente necesita descargar la imagen (`docker pull`) e iniciar el contenedor (`docker run`). Esto hace el proceso de despliegue y reversión de versiones (Rollback) inmensamente más fácil, predecible y seguro.
