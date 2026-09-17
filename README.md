# portfolio-joe — Repositorio fuente de la verdad para búsqueda de empleo

Este repositorio es la **fuente única de la verdad** sobre la trayectoria profesional de **Joseph Andrés Baño Naranjo**. A partir de datos estructurados en YAML y plantillas en Markdown, un agente de Inteligencia Artificial deriva hojas de vida optimizadas para sistemas de filtrado de personal (ATS) en formatos `.docx` y `.pdf`, adaptadas de forma determinista a cada oferta de empleo, midiendo el resultado de cada postulación.

No es una carpeta de currículos en Word ni un sitio web estático: es un sistema de ingeniería para gestionar una carrera profesional como código.

---

## 1. Instalación inicial (Paso obligatorio)

Para garantizar que ningún dato personal ni secreto se confirme en el repositorio público, configure los hooks de Git locales inmediatamente después de clonar:

```bash
git config core.hooksPath .githooks
```

Esta configuración activa el hook `.githooks/pre-commit`, que inspecciona el índice y aborta cualquier commit que intente incluir archivos protegidos (`privado/`, `.secrets`) o patrones de información de contacto literal (teléfonos, correos, contraseñas, etc.).

---

## 2. Arquitectura de privacidad y separación de datos

El repositorio divide estrictamente la información en dos dominios:

| Dominio | Directorios | Control de versiones | Descripción |
|---|---|---|---|
| **Público** | `profile/`, `templates/`, `docs/`, `specs/`, `AGENTS.md` | Sí (Git público) | Experiencia profesional, habilidades, educación, certificaciones, taxonomía y reglas ATS. No contiene datos de contacto. |
| **Privado** | `privado/`, `.secrets` | **No** (excluido por `.gitignore` y protegido por hooks) | Teléfono, correo personal, dirección, ofertas laborales, CVs generados, registro de postulaciones, notas y contratos. |

Para habilitar la generación local:
1. Copie `.secrets.example` a `privado/.secrets`.
2. Configure sus datos personales en `privado/.secrets`.
3. Al generar un currículum, los marcadores `{{secrets.*}}` se sustituyen en memoria sin exponerlos en Git.

---

## 3. Frontera de código (D-01, R-01)

El repositorio respeta la decisión arquitectónica de **no contener código de aplicación** (sin microservicios, sin frontend, sin APIs). El contrato operativo [AGENTS.md](file:///home/joeman/Documents/proyects/portfolio-joe/AGENTS.md) actúa como la especificación que rige la ejecución del agente.

Se admiten exactamente dos excepciones técnicas acotadas:
1. **Guardas de seguridad:** `.githooks/pre-commit` y los flujos de GitHub Actions (`.github/workflows/`), necesarias para prevenir fugas de datos.
2. **Derivador de documentos:** `tools/render_docx.py`, un único script con una sola dependencia (`python-docx`), sin configuración, limitado a transformar Markdown básico a un documento Word de una columna conforme a las reglas ATS (ADR-001).

---

## 4. Ciclo de uso en los cuatro escenarios

### Escenario 1 — Generar una hoja de vida adaptada a una oferta
Joseph entrega el texto o enlace de una oferta de trabajo al agente indicando idioma (`es` | `en`) y plantilla (`ats-standard` | `ats-compact`).

El agente:
1. Extrae y normaliza la oferta en `privado/generados/<id>/oferta.yml`.
2. Cruza las palabras clave contra `profile/taxonomy.yml` y `profile/skills.yml`.
3. Calcula el porcentaje de coincidencia en `match.md`.
4. Selecciona deterministamente las viñetas más relevantes de `profile/experience.yml` y `profile/projects.yml`.
5. Compone `cv.md` sustituyendo variables de `privado/.secrets`.
6. Deriva `cv.docx` y `cv.pdf` (con LibreOffice headless).
7. Registra la postulación en `privado/aplicaciones.yml` con estado `borrador`.

### Escenario 2 — Auditar un repositorio local y actualizar el perfil
Joseph solicita auditar una fuente declarada en `profile/sources.yml`.

El agente:
1. Inspecciona el código local, dependencias, patrones arquitectónicos y commits de Joseph.
2. Aplica la regla de sanitización (RF-EVID-002): no extrae código propietario, ni endpoints, ni esquemas de bases de datos de repositorios institucionales.
3. Propone viñetas y habilidades atómicas en la consola.
4. Joseph aprueba viñeta por viñeta antes de que se integren a `profile/` mediante Pull Request.

### Escenario 3 — Bloqueo de datos sensibles en tres capas
El sistema cuenta con tres líneas de defensa:
1. **Capa 1:** `.gitignore` ignora `privado/`, `.secrets`, `.docx` y `.pdf`.
2. **Capa 2:** Hook local `.githooks/pre-commit` aborta commits que añadan rutas protegidas o datos sensibles según `.security/patterns.txt`.
3. **Capa 3:** GitHub Actions (`secret-guard.yml` y `profile-lint.yml`) ejecuta jobs bloqueantes en cada Pull Request (`path-guard`, `pii-scan`, `commit-hygiene`, `gitleaks`).

### Escenario 4 — Seguimiento y analítica de resultados
Cuando Joseph recibe respuesta de una empresa:
1. Actualiza el estado en `privado/aplicaciones.yml` (`postulado`, `tecnica`, `oferta`, etc.) anexando un evento inmutable al `timeline`.
2. Tras 21 días de inactividad, pasa a `sin_respuesta` (PD-01).
3. Solicita regenerar `privado/analitica.md` para visualizar el embudo de conversión, efectividad por fuente y palabras clave ausentes en el perfil.

---

## 5. Documentación de referencia

- [AGENTS.md](file:///home/joeman/Documents/proyects/portfolio-joe/AGENTS.md): Contrato operativo para agentes de IA.
- [docs/schemas.md](file:///home/joeman/Documents/proyects/portfolio-joe/docs/schemas.md): Especificación de esquemas YAML.
- [docs/ats-rules.md](file:///home/joeman/Documents/proyects/portfolio-joe/docs/ats-rules.md): Reglas de optimización para ATS y justificación técnica.
- [docs/workflow.md](file:///home/joeman/Documents/proyects/portfolio-joe/docs/workflow.md): Diagrama y detalle del flujo de 6 fases.
- [docs/adr/](file:///home/joeman/Documents/proyects/portfolio-joe/docs/adr/): Registros de Decisiones de Arquitectura (ADR-001, ADR-002, ADR-003).
