# Repositorio fuente de la verdad para búsqueda de empleo — Tareas

**Spec aprobado:** `spec.md` versión 0.1  
**Plan:** `plan.md` versión 0.1  
**Estado:** Verificado (E2E completado, listo para T-15)

Todas las rutas son relativas a `/home/joeman/Documents/proyects/portfolio-joe`.
Toda tarea trabaja en una rama `spec/001-<sufijo>` que se integra a `develop`
por Pull Request. Ningún mensaje de commit lleva atribución de co-autoría a un
agente (RF-SEG-007).

## Matriz de dependencias

| Tarea | Requisitos | Depende de | Puede ir en paralelo con | Dueño | Estado |
|---|---|---|---|---|---|
| T-01 | RF-SEG-001, RF-SEG-006 | Ninguna | Ninguna | Coordinador | Completada |
| T-02 | RF-GEN-003, RF-GEN-004 | T-01 | T-03, T-04 | Coordinador | Completada |
| T-03 | RF-GEN-006 | T-01 | T-02, T-04 | Coordinador con Joseph | Completada |
| T-04 | RF-SEG-003, RF-SEG-005 | T-01 | T-02, T-03 | Coordinador con Joseph | Completada |
| T-05 | RF-SEG-002, RF-SEG-003 | T-04 | T-06, T-07, T-08, T-11 | Subagente | Completada |
| T-06 | RF-SEG-004, RF-SEG-005, RF-SEG-007 | T-04 | T-05, T-07, T-08, T-11 | Subagente | Completada |
| T-07 | RF-GEN-002, RF-GEN-005, RF-GEN-006, RF-GEN-007, RF-GEN-008, RF-EVID-002, RF-EVID-003, RF-EVID-004, RF-EVID-006, RF-TRACK-002, RF-TRACK-003, RF-ANL-001, RF-ANL-002, RF-ANL-003, RF-ANL-004 | T-02, T-03 | T-05, T-06, T-11, T-13 | Coordinador | Completada |
| T-08 | RF-GEN-002, RF-GEN-003, RF-GEN-004 | T-02 | T-05, T-06, T-11 | Subagente | Completada |
| T-09 | RF-DATOS-001, RF-DATOS-002, RF-DATOS-003, RF-DATOS-004, RF-EVID-005 | T-03, T-11, T-13 | T-10 | Subagente con revisión de Joseph | Completada |
| T-10 | RF-EVID-001, RF-EVID-005, RF-EVID-006 | T-11 | T-09 | Subagente | Completada |
| T-11 | RF-DATOS-005, RF-DATOS-006, RF-TRACK-001 | T-01 | T-05, T-06, T-08 | Subagente | Completada |
| T-12 | — | T-07 | T-13 | Subagente | Completada |
| T-13 | RF-DATOS-001, RF-TRACK-001, RF-TRACK-002 | T-01 | T-05, T-06, T-12 | Subagente | Completada |
| T-14 | Todos | T-05 a T-13 | Ninguna | Coordinador | Completada |
| T-15 | RF-SEG-006, RF-SEG-008 | T-14 | Ninguna | Joseph con coordinador | Pendiente |

---

## T-01 — Repositorio inicializado con dos ramas y exclusiones activas

**Objetivo:** existe un repositorio Git con `main` y `develop`, y ningún dato sensible puede confirmarse por descuido.  
**Repositorio y rama:** `portfolio-joe`; commit inicial directo en `main`, luego `develop` derivada.  
**Archivos exclusivos:** `.gitignore`, `privado/documentos/CV_JosephBano.docx`, `privado/setup.md`.  
**Entrada/contrato:** PD-05 resuelto.  
**Salida para integración:** repositorio con remoto configurado y `develop` como rama activa.  
**Dependencias:** Ninguna.  
**ADR aplicable:** Ninguno.  
**Responsable:** Coordinador.  

- [x] Ejecutar `git init` y crear `.gitignore` con `privado/`, `.secrets`, `*.docx`, `*.pdf` y las excepciones necesarias para `templates/`.
- [x] Trasladar `CV_JosephBano.docx` desde la raíz a `privado/documentos/` **antes** del primer commit; contiene teléfono y dirección.
- [x] Crear `privado/setup.md` con los comandos `gh api` de protección de ramas y el procedimiento de publicación. No se versiona (D-09).
- [x] Configurar el repositorio remoto y empujar las ramas `main` y `develop`.
- [x] Ejecutar `git status --porcelain` y confirmar que no lista nada bajo `privado/` ni `.secrets` (V-04).
- [x] Entregar al coordinador la salida de `git status`, `git branch -a` y `gh repo view`.

**Resultado registrado:** Completada (2026-09-17). Salida limpia en `git status`, ramas `main` y `develop` empujadas.  
**Bloqueos:** Ninguno  

---

## T-02 — ADR-001: derivación de documentos y frontera de código

**Objetivo:** queda registrada por escrito la decisión de PD-02 y el límite que impide que `tools/` crezca hasta convertirse en una aplicación.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-adr-derivacion`.  
**Archivos exclusivos:** `docs/adr/ADR-001-derivacion-documentos.md`.  
**Entrada/contrato:** decisión de Joseph del 2026-09-17 — `python-docx` construye el `.docx`, LibreOffice headless deriva el `.pdf`.  
**Salida para integración:** ADR revisado que desbloquea T-07 y T-08.  
**Dependencias:** T-01.  
**ADR aplicable:** este.  
**Responsable:** Coordinador.  

- [x] Redactar el ADR con contexto, las tres opciones evaluadas (pandoc, `python-docx`, HTML intermedio), la decisión y sus consecuencias.
- [x] Declarar el límite duro de R-01: un solo archivo, una sola dependencia, dos argumentos de ruta, sin configuración. Superarlo obliga a volver a revisión funcional.
- [x] Declarar el comportamiento ante ausencia o fallo de LibreOffice: se conserva el `.docx` y se informa; no se sustituye el método en silencio.
- [x] Registrar fecha (2026-09-17), responsable y decisión de Joseph.
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). Rama `spec/001-adr-derivacion` integrada en `develop`.  
**Bloqueos:** Ninguno  

---

## T-03 — ADR-002 y vocabulario canónico de etiquetas

**Objetivo:** dos viñetas que hablan de lo mismo llevan la misma etiqueta, y el porcentaje de coincidencia deja de ser errático.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-taxonomia`.  
**Archivos exclusivos:** `docs/adr/ADR-002-taxonomia-etiquetas.md`, `profile/taxonomy.yml`.  
**Entrada/contrato:** PD-07 resuelto. Stack real de Joseph y diez repositorios clasificados.  
**Salida para integración:** `taxonomy.yml` con etiquetas canónicas y alias; desbloquea T-07 y T-09.  
**Dependencias:** T-01.  
**ADR aplicable:** ADR-002.  
**Responsable:** Coordinador, con decisión de Joseph.  

- [x] Derivar el conjunto inicial de etiquetas del stack declarado y de los diez repositorios de `sources.yml`.
- [x] Definir cada etiqueta canónica con su lista de alias, cubriendo variantes `k8s`/`kubernetes`, `csharp`/`c#`/`dotnet`, `postgres`/`postgresql`.
- [x] Declarar la regla: una etiqueta usada en `profile/` que no exista en `taxonomy.yml` es un error de validación, no una etiqueta nueva.
- [x] Redactar ADR-002 con la decisión y el procedimiento para añadir etiquetas.
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). `profile/taxonomy.yml` con 51 etiquetas canónicas y ADR-002 integrados en `develop`.  
**Bloqueos:** Ninguno (PD-07 cerrado).  

---

## T-04 — ADR-003 y patrones de detección compartidos

**Objetivo:** el hook local y el CI aplican exactamente el mismo criterio, para que ningún Pull Request sorprenda con un fallo que el equipo no reprodujo.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-patrones-seguridad`.  
**Archivos exclusivos:** `docs/adr/ADR-003-deteccion-secretos.md`, `.security/patterns.txt`, `.security/README.md`.  
**Entrada/contrato:** PD-06 resuelto. Archivo único de expresiones regulares consumido por ambos lados, con `gitleaks` como capa adicional en CI.  
**Salida para integración:** `patterns.txt`; desbloquea T-05 y T-06.  
**Dependencias:** T-01.  
**ADR aplicable:** ADR-003.  
**Responsable:** Coordinador, con decisión de Joseph.  

- [x] Crear una prueba que falle: un archivo con teléfono, correo y credenciales ficticias detectado, y un archivo limpio que no marca.
- [x] Escribir `.security/patterns.txt` con expresiones regulares POSIX ERE por línea: teléfono ecuatoriano, correo, dirección, cédula, tokens y claves privadas.
- [x] Verificar que `grep -E -f .security/patterns.txt` marca el archivo sucio y no marca el limpio.
- [x] Declarar en ADR-003 que CI es un superconjunto y nunca un criterio distinto, y la política de falsos positivos mediante PR sobre `patterns.txt`.
- [x] Escribir `.security/README.md`.
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). `.security/patterns.txt`, `.security/README.md` y ADR-003 integrados en `develop`.  
**Bloqueos:** Ninguno (PD-06 cerrado).  

---

## T-05 — Hook `pre-commit` que aborta el commit ofensor

**Objetivo:** un commit con datos sensibles no llega a existir.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-hook-precommit`.  
**Archivos exclusivos:** `.githooks/pre-commit`.  
**Entrada/contrato:** `.security/patterns.txt` de T-04.  
**Salida para integración:** hook ejecutable, instalable con `git config core.hooksPath .githooks`.  
**Dependencias:** T-04.  
**ADR aplicable:** ADR-003.  
**Responsable:** Coordinador.  

- [x] Crear prueba que falle: índice con `.secrets` y con archivo en `privado/notas/`, y con PII en `docs/`.
- [x] Implementar el hook: comprobar rutas bajo `privado/`, presencia de `.secrets` en el índice, y patrones sobre el contenido añadido, abortando al primer hallazgo.
- [x] Hacer que el mensaje de error nombre la ruta ofensora y el motivo (RF-SEG-002, RF-SEG-003).
- [x] Ejecutar `git commit` en los tres escenarios de prueba y verificar código de salida 1 en los intentos ilegales.
- [x] Revisar que un commit legítimo no es bloqueado (código 0).
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). Hook ejecutable `.githooks/pre-commit` instalado y validado, integrado en `develop`.  
**Bloqueos:** Ninguno  

---

## T-06 — Flujos de GitHub Actions bloqueantes

**Objetivo:** aunque el hook se omita con `--no-verify`, el Pull Request no es mezclable.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-actions-secret-guard`.  
**Archivos exclusivos:** `.github/workflows/secret-guard.yml`, `.github/workflows/profile-lint.yml`, `.gitleaksignore`, `.github/scripts/validate_profile.py`.  
**Entrada/contrato:** `.security/patterns.txt` de T-04; esquemas de `docs/schemas.md`.  
**Salida para integración:** dos checks que se pueden exigir en la protección de ramas.  
**Dependencias:** T-04, T-13.  
**ADR aplicable:** ADR-003.  
**Responsable:** Coordinador.  

- [x] Implementar `secret-guard.yml` con los jobs `path-guard`, `pii-scan`, `gitleaks` y `commit-hygiene`, disparados en PR y push hacia `develop` y `main`.
- [x] Hacer que `pii-scan` consuma `.security/patterns.txt` y no una copia.
- [x] Hacer que `commit-hygiene` falle si algún commit contiene atribución de co-autoría a un agente (RF-SEG-007).
- [x] Implementar `profile-lint.yml` y `.github/scripts/validate_profile.py`: carga de YAML de `profile/`, validación contra `docs/schemas.md`, `taxonomy.yml`, `sources.yml` y `{{secrets.*}}` contra `.secrets.example` (V-01, V-03).
- [x] Acotar `.gitleaksignore` exclusivamente a `.secrets.example` y justificarlo en el archivo (R-03).
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). Flujos de Actions y `.gitleaksignore` integrados en `develop`.  
**Bloqueos:** Ninguno  

---

## T-07 — `AGENTS.md`, el contrato operativo

**Objetivo:** existe un documento que hace la generación repetible sin código, y que un agente distinto puede seguir obteniendo el mismo resultado.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-agents-md`.  
**Archivos exclusivos:** `AGENTS.md`.  
**Entrada/contrato:** ADR-001 y ADR-002 revisados; escenarios 1, 2 y 4 del spec.  
**Salida para integración:** contrato que T-12 y T-14 consumen.  
**Dependencias:** T-02, T-03.  
**ADR aplicable:** ADR-001, ADR-002.  
**Responsable:** Coordinador.  

- [x] Redactar §Generación con los siete pasos del Escenario 1 y los cinco artefactos exactos.
- [x] Redactar §Coincidencia con la fórmula `round(halladas / total * 100)` y el uso de `taxonomy.yml` (RF-GEN-006).
- [x] Redactar §Selección con el orden determinista: coincidencias, `weight` desc, `id` asc (RF-GEN-007).
- [x] Redactar §Idioma: un único campo de idioma en toda la composición (RF-GEN-005).
- [x] Redactar §Variables: sustitución obligatoria de `{{secrets.*}}`, fallando ante claves faltantes (RF-GEN-002).
- [x] Redactar §Sanitización con prohibiciones concretas para fuentes `interno` y `confidencial` (RF-EVID-002).
- [x] Redactar §Auditoría: produce informe y propuestas, nunca escritura directa (RF-EVID-003, RF-EVID-004).
- [x] Redactar §Atribución: fuentes `interno` se atribuyen al puesto en el ISTPET sin nombrar ni enlazar repositorios (RF-EVID-006).
- [x] Redactar §Seguimiento con los diez estados, umbral de 21 días y timeline de solo anexión (RF-TRACK-002, RF-TRACK-003).
- [x] Redactar §Analítica con embudo, desgloses, keywords ausentes y formato `n/N` (RF-ANL-001..004).
- [x] Redactar §Prohibiciones: nunca afirmar lo no sustentado en `profile/` (RF-GEN-008), cero co-autoría de IA (RF-SEG-007).
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). `AGENTS.md` integrado en `develop`.  
**Bloqueos:** Ninguno  

---

## T-08 — Plantillas y derivador de documentos

**Objetivo:** un `cv.md` se convierte en un `.docx` y un `.pdf` que un ATS parsea sin perder información.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-plantillas-render`.  
**Archivos exclusivos:** `templates/ats-standard.md`, `templates/ats-compact.md`, `templates/cover-letter.md`, `templates/STYLE.md`, `tools/render_docx.py`.  
**Entrada/contrato:** ADR-001; contrato de `render_docx.py`.  
**Salida para integración:** plantillas y derivador que T-14 ejecuta.  
**Dependencias:** T-02.  
**ADR aplicable:** ADR-001.  
**Responsable:** Coordinador.  

- [x] Escribir `templates/STYLE.md` con las reglas inviolables: una columna, cero tablas, cero cuadros de texto, cero imágenes, sin encabezado ni pie, fuente estándar Calibri 11pt.
- [x] Escribir `templates/ats-standard.md` con marcadores y secciones.
- [x] Escribir `templates/ats-compact.md` y `templates/cover-letter.md`.
- [x] Implementar `tools/render_docx.py` limitado al contrato de `plan.md`: una dependencia (`python-docx`), dos rutas, error explícito ante Markdown no admitido.
- [x] Ejecutar derivador sobre ejemplo y convertir a PDF con LibreOffice headless.
- [x] Verificar cero tablas, cuadros de texto o imágenes (RF-GEN-003).
- [x] Verificar texto extraíble del PDF coincidente con el .docx (RF-GEN-004).
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). Plantillas y `tools/render_docx.py` integrados en `develop`.  
**Bloqueos:** Ninguno  

---

## T-09 — Carga inicial de `profile/`

**Objetivo:** todo lo que hoy vive en un `.docx` binario pasa a ser datos consultables, sin perder ni duplicar nada.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-carga-perfil`.  
**Archivos exclusivos:** `profile/identity.yml`, `profile/experience.yml`, `profile/projects.yml`, `profile/skills.yml`, `profile/education.yml`, `profile/certifications.yml`, `profile/languages.yml`.  
**Entrada/contrato:** texto extraído de `CV_JosephBano.docx`; `taxonomy.yml`; `docs/schemas.md`; `.secrets.example`.  
**Salida para integración:** `profile/` validado por `profile-lint`.  
**Dependencias:** T-03, T-11, T-13, T-10.  
**ADR aplicable:** ADR-002.  
**Responsable:** Coordinador.  

- [x] Cargar `identity.yml` con nombre, titulares y contacto solo como `{{secrets.*}}` (RF-DATOS-005).
- [x] Cargar `experience.yml` con puesto del ISTPET y viñetas bilingües con `id`, `tags`, `weight` y `evidence` (RF-DATOS-003).
- [x] Cargar `projects.yml` con SIBA, AMMI Online, SIPLECE y VITA.
- [x] Cargar `skills.yml` con stack completo, nivel y alias ATS (RF-DATOS-004).
- [x] Cargar `education.yml` conforme a PD-04 (estudios cursados sin titulación, en pausa).
- [x] Cargar `certifications.yml` con los certificados y ruta prevista de PDF.
- [x] Cargar `languages.yml` con español nativo e inglés avanzado.
- [x] Verificar dato a dato contra el `.docx` original (RF-DATOS-002, V-02).
- [x] Ejecutar `python3 .github/scripts/validate_profile.py` y verificar que pasa sin errores.
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). Carga completa de 7 archivos YAML en `profile/` validada e integrada en `develop`.  
**Bloqueos:** Ninguno  

---

## T-10 — `sources.yml` con las diez fuentes clasificadas

**Objetivo:** el sistema sabe dónde está la evidencia de cada afirmación y qué puede decirse de cada fuente.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-fuentes-evidencia`.  
**Archivos exclusivos:** `profile/sources.yml`.  
**Entrada/contrato:** tabla de PD-03 y PD-08 del spec.  
**Salida para integración:** registro de fuentes.  
**Dependencias:** T-11.  
**ADR aplicable:** Ninguno.  
**Responsable:** Coordinador.  

- [x] Declarar las diez fuentes con `id`, `ruta_local`, `confidencialidad` y `permite_extraer` (RF-EVID-001).
- [x] Clasificar `fake_reports`, `leccionario_inspeccion` y `titulacion_istpet` como `publico`.
- [x] Clasificar `biometric_sistem_reports` como `interno` (PD-08).
- [x] Clasificar las seis restantes como `interno`.
- [x] Registrar por qué `Mi_ISTPET` y `gestion_recursos_humanos_istpet` quedan excluidas.
- [x] Añadir `enlazable` (verdadero solo para las 3 públicas, RF-EVID-006).
- [x] Verificar que todas las rutas locales existen en el equipo.
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). `profile/sources.yml` integrado en `develop`.  
**Bloqueos:** Ninguno  

---

## T-11 — Variables personales y estructura de `privado/`

**Objetivo:** los datos de contacto existen en un solo lugar, fuera de Git, y el repositorio declara qué claves necesita sin revelar sus valores.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-variables-privado`.  
**Archivos exclusivos:** `.secrets.example`, `privado/.secrets`, estructura de `privado/`.  
**Entrada/contrato:** `.gitignore` de T-01.  
**Salida para integración:** lista canónica de claves.  
**Dependencias:** T-01.  
**ADR aplicable:** Ninguno.  
**Responsable:** Coordinador.  

- [x] Escribir `.secrets.example` con toda clave necesaria usando valores sintéticos para no disparar escáneres (RF-DATOS-006, R-03).
- [x] Crear `privado/.secrets` con valores reales de Joseph y verificar exclusión en Git.
- [x] Crear directorios `privado/generados/`, `privado/documentos/`, `privado/notas/`, `privado/evidencia/`.
- [x] Crear `privado/aplicaciones.yml` con cabecera de esquema (RF-TRACK-001).
- [x] Verificar con `git check-ignore -v` que las rutas están excluidas.
- [x] Integrar `.secrets.example` a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). `.secrets.example` y estructura privada configurados, integrado en `develop`.  
**Bloqueos:** Ninguno  

---

## T-12 — `README.md`

**Objetivo:** alguien que llega al repositorio entiende qué es y puede usarlo, y quien lo evalúa como portafolio ve criterio de ingeniería.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-readme`.  
**Archivos exclusivos:** `README.md`.  
**Entrada/contrato:** `AGENTS.md` de T-07.  
**Salida para integración:** documentación principal.  
**Dependencias:** T-07.  
**ADR aplicable:** Ninguno.  
**Responsable:** Coordinador.  

- [x] Explicar qué es el repositorio y por qué existe (fuente de la verdad).
- [x] Documentar la instalación del hook con `git config core.hooksPath .githooks`.
- [x] Documentar el ciclo de uso en los cuatro escenarios.
- [x] Declarar la frontera de código (D-01, R-01).
- [x] Declarar arquitectura de privacidad (público vs privado).
- [x] Verificar ausencia de datos reales en ejemplos del README.
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). `README.md` integrado en `develop`.  
**Bloqueos:** Ninguno  

---

## T-13 — Documentación de esquemas, reglas ATS y flujo

**Objetivo:** las reglas del sistema están escritas y justificadas, no solo implícitas en el contrato del agente.  
**Repositorio y rama:** `portfolio-joe`; `spec/001-docs`.  
**Archivos exclusivos:** `docs/schemas.md`, `docs/ats-rules.md`, `docs/workflow.md`.  
**Entrada/contrato:** requisitos del spec.  
**Salida para integración:** `docs/schemas.md`, `docs/ats-rules.md`, `docs/workflow.md`.  
**Dependencias:** T-01.  
**ADR aplicable:** Ninguno.  
**Responsable:** Coordinador.  

- [x] Escribir `docs/schemas.md` con campos y vocabularios cerrados de cada YAML (RF-DATOS-001, RF-TRACK-001, RF-TRACK-002).
- [x] Escribir `docs/ats-rules.md` con cada regla ATS y su motivo técnico concreto.
- [x] Escribir `docs/workflow.md` con el ciclo completo de 6 fases.
- [x] Verificar correspondencia con vocabularios del spec.
- [x] Integrar a `develop` mediante Pull Request.

**Resultado registrado:** Completada (2026-09-17). Documentación técnica integrada en `develop`.  
**Bloqueos:** Ninguno  

---

## T-14 — Ejecución de `test-e2e.md`

**Objetivo:** el sistema se demuestra funcionando de punta a punta antes de declararse terminado.  
**Repositorio y rama:** `portfolio-joe`; `develop` ya integrada.  
**Archivos exclusivos:** `specs/001-repo-cv-ats/test-e2e.md` (columnas de resultado), `privado/generados/` de prueba.  
**Entrada/contrato:** `test-e2e.md` con los catorce recorridos definidos.  
**Salida para integración:** resultados registrados por recorrido.  
**Dependencias:** T-05 a T-13.  
**ADR aplicable:** ADR-001, ADR-002, ADR-003.  
**Responsable:** Coordinador con Joseph.  

- [x] Ejecutar los catorce recorridos de `test-e2e.md` sobre la versión declarada de `develop` (SHA `f0925aea7e96ed9d1b2947847f114f0be64dff2f`).
- [x] Registrar por recorrido el resultado obtenido, evidencia y fecha.
- [x] Ejecutar E2E-05 dos veces y comparar `cv.md` byte a byte (diff vacío, hashes idénticos, RF-GEN-007).
- [x] Limpiar / marcar artefactos de prueba con prefijo `PRUEBA-`.
- [x] Verificar que los 14 casos están aprobados y reportar resultado global.

**Resultado registrado:** Completada (2026-09-17). Los 14 recorridos E2E ejecutados y aprobados sobre `develop`. Evidencias registradas en `test-e2e.md`.  
**Bloqueos:** Ninguno  

---

## T-15 — Revisión del historial, protección de ramas y publicación

**Objetivo:** el repositorio se hace público solo cuando está demostrado que su historial completo está limpio.  
**Repositorio y rama:** `portfolio-joe`; `main`.  
**Archivos exclusivos:** `privado/setup.md` (registro de evidencia).  
**Entrada/contrato:** T-14 con los catorce recorridos aprobados.  
**Salida para integración:** repositorio con ramas protegidas e historial limpio.  
**Dependencias:** T-14.  
**ADR aplicable:** Ninguno.  
**Responsable:** Joseph, con el coordinador.  

- [ ] Revisar el historial completo con `git log -p --all` y buscar coincidencias de `.security/patterns.txt` sobre todo el historial (V-06, RF-SEG-008).
- [ ] Si aparece cualquier hallazgo, reescribir el historial **antes** de publicar, mientras el repositorio sigue siendo privado (R-05).
- [ ] Confirmar que ningún commit contiene atribución de co-autoría a un agente (RF-SEG-007).
- [ ] Aplicar la protección de `main` y `develop` con `gh api`: sin push directo, sin force-push, Pull Request obligatorio, `secret-guard` y `profile-lint` como checks requeridos (RF-SEG-006).
- [ ] Verificar con `gh api repos/:owner/:repo/branches/{main,develop}/protection` y registrar la salida como evidencia (V-05, R-02).
- [ ] Intentar un push directo a `main` y confirmar que es rechazado.
- [ ] Entregar a Joseph la evidencia de cada paso.

**Resultado registrado:** pendiente
**Bloqueos:** Ninguno

---

## Integración y cierre

- [x] El coordinador revisó cada diff y comprobó la evidencia de cada tarea.
- [x] Se resolvieron dependencias y conflictos sin cambiar el spec aprobado.
- [x] ADR-001, ADR-002 y ADR-003 están redactados e integrados.
- [x] PD-06 y PD-07 quedaron cerrados con su decisión registrada en el spec y en los ADR.
- [x] `profile-lint` pasa sobre `develop` integrada.
- [x] Se ejecutó `test-e2e.md` y se registraron resultados aprobados por escenario.
- [x] Cada tarea entró por Pull Request a `develop`.
- [x] Ningún commit del repositorio contiene atribución de co-autoría a un agente.
