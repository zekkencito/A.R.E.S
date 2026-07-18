# Sistema A.R.E.S. (Audit Resource & Environment System)
### Mars Challenge 2026 - Elemento Tierra

A.R.E.S. es un avanzado sistema de auditoría de recursos y simulación ambiental basado en web, diseñado específicamente para el Mars Challenge 2026. Su propósito principal es garantizar la supervivencia de las tripulaciones de exploración marciana mediante el cálculo riguroso de los recursos hídricos necesarios para lavar los percloratos tóxicos del suelo marciano, un proceso crítico para la construcción de bases, la agricultura y la filtración de agua.

## Arquitectura

El sistema utiliza una arquitectura Cliente-Servidor robusta y asíncrona:

- **Frontend (React + Three.js + TailwindCSS)**: Proporciona una simulación 3D inmersiva en tiempo real del terreno marciano utilizando un dron de escaneo. Visualiza dinámicamente los sectores de tierra asignados a los equipos de exploración y ofrece un panel de control interactivo para ajustar la telemetría ambiental (Temperatura, Humedad, Presión y Área del terreno).
- **Backend (Python + FastAPI)**: Actúa como el núcleo de procesamiento determinista. Calcula los requerimientos exactos de agua basándose en leyes físicas simuladas (evaporación y sublimación) y se comunica con un LLM externo (Groq) para generar reportes tácticos de voz mediante Edge TTS.

## Características Principales

- **Visualización 3D Interactiva**: Control de un dron de escaneo mediante teclado (WASD/QE) para sobrevolar e inspeccionar el paisaje marciano simulado.
- **Cálculo Determinista de Recursos**: Modelado matemático preciso para calcular la evaporación, la sublimación y la retención del suelo según variables ambientales dinámicas.
- **Sistema de Alertas Críticas**: Evalúa las reservas actuales de agua contra el agua requerida. Dispara alertas de seguridad si las reservas son insuficientes o si existe un exceso hídrico que podría causar erosión del suelo y deslaves irreparables.
- **Enlace de Tripulación con IA**: Incluye una interfaz de comunicación de texto directo con "DaLiA", la inteligencia artificial a bordo. La IA retiene el contexto estricto de la misión, la telemetría en tiempo real y el análisis de recursos para asistir a la tripulación frente a peligros inminentes.

## Instalación y Despliegue

### 🚀 Despliegue en Servidor Casero con Docker & Cloudflare Tunnels (Recomendado)

El sistema está preconfigurado en una arquitectura multi-contenedor aislada (`ares_frontend` + `ares_backend`) y ruteada a través de Nginx en el puerto **`3001`**. Esta configuración evita problemas de CORS y prepara el proyecto al 100% para ser expuesto con **Cloudflare Tunnels**.

1. **Clonar el repositorio y configurar entorno**:
   ```bash
   git clone https://github.com/zekkencito/A.R.E.S.git
   cd A.R.E.S
   cp .env.example .env
   ```
2. **Añadir API Key de Groq**:
   Edita el archivo `.env` y coloca tu API Key de Groq:
   ```env
   VITE_GROQ_API_KEY=tu_api_key_aqui
   ```
3. **Iniciar con Docker Compose**:
   ```bash
   docker compose up -d --build
   ```
4. **Acceso local o por túnel**:
   - **En tu red local:** Abre tu navegador en `http://IP-DE-TU-SERVIDOR:3001` (por ejemplo, `http://192.168.1.50:3001`).
   - **Con Cloudflare Tunnels (`cloudflared`):** Configura el túnel apuntando tu dominio hacia `http://localhost:3001`. El proxy inverso de Nginx gestionará automáticamente las peticiones y el tráfico HTTPS sin requerir ningún cambio en el código o configuración.

---

### Despliegue Manual para Desarrollo Local

#### Requisitos Previos
- Node.js v18+
- Python 3.10+

#### Configuración del Backend
1. Abre una terminal en la raíz del repositorio.
2. Crea y activa un entorno virtual de Python (`python -m venv venv && source venv/bin/activate`).
3. Instala las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```
4. Define la variable de entorno `VITE_GROQ_API_KEY` en tu sistema o archivo `.env`.
5. Inicia el servidor FastAPI:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

#### Configuración del Frontend
1. Abre una nueva terminal en el repositorio e instala las dependencias:
   ```bash
   npm install
   ```
2. Crea un archivo `.env` en el directorio raíz indicando la URL de tu backend en desarrollo:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
3. Inicia el entorno de desarrollo de Vite:
   ```bash
   npm run dev
   ```

## Licencia
Desarrollado en exclusiva para el Mars Challenge 2026. Todos los derechos reservados.

