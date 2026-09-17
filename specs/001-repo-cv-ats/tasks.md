# Repositorio fuente de la verdad para búsqueda de empleo — Tareas

**Spec aprobado:** `spec.md` versión 0.1
**Plan:** `plan.md` versión 0.1
**Estado:** Preparado para implementación

Todas las rutas son relativas a `/home/joeman/Documents/proyects/portfolio-joe`.
Toda tarea trabaja en una rama `spec/001-<sufijo>` que se integra a `develop`
por Pull Request. Ningún mensaje de commit lleva atribución de co-autoría a un
agente (RF-SEG-007).

## Matriz de dependencias

| Tarea | Requisitos | Depende de | Puede ir en paralelo con | Dueño |
|---|---|---|---|---|
| T-01 | RF-SEG-001, RF-SEG-006 | Ninguna | Ninguna | Coordinador |
| T-02 | RF-GEN-003, RF-GEN-004 | T-01 | T-03, T-04 | Coordinador |
| T-03 | RF-GEN-006 | T-01 | T-02, T-04 | Coordinador con Joseph |
| T-04 | RF-SEG-003, RF-SEG-005 | T-01 | T-02, T-03 | Coordinador con Joseph |
| T-05 | RF-SEG-002, RF-SEG-003 | T-04 | T-06, T-07, T-08, T-11 | Subagente |
| T-06 | RF-SEG-004, RF-SEG-005, RF-SEG-007 | T-04 | T-05, T-07, T-08, T-11 | Subagente |
| T-07 | RF-GEN-002, RF-GEN-005, RF-GEN-006, RF-GEN-007, RF-GEN-008, RF-EVID-002, RF-EVID-003, RF-EVID-004, RF-EVID-006, RF-TRACK-002, RF-TRACK-003, RF-ANL-001, RF-ANL-002, RF-ANL-003, RF-ANL-004 | T-02, T-03 | T-05, T-06, T-11, T-13 | Coordinador |
| T-08 | RF-GEN-002, RF-GEN-003, RF-GEN-004 | T-02 | T-05, T-06, T-11 | Subagente |
| T-09 | RF-DATOS-001, RF-DATOS-002, RF-DATOS-003, RF-DATOS-004, RF-EVID-005 | T-03, T-11, T-13 | T-10 | Subagente con revisión de Joseph |
| T-10 | RF-EVID-001, RF-EVID-005, RF-EVID-006 | T-11 | T-09 | Subagente |
| T-11 | RF-DATOS-005, RF-DATOS-006, RF-TRACK-001 | T-01 | T-05, T-06, T-08 | Subagente |
| T-12 | — | T-07 | T-13 | Subagente |
| T-13 | RF-DATOS-001, RF-TRACK-001, RF-TRACK-002 | T-01 | T-05, T-06, T-12 | Subagente |
| T-14 | Todos | T-05 a T-13 | Ninguna | Coordinador |
| T-15 | RF-SEG-006, RF-SEG-008 | T-14 | Ninguna | Joseph con coordinador |

T-02, T-03 y T-04 redactan ADR-001, ADR-002 y ADR-003 respectivamente. Toda
tarea que los cite está **bloqueada por ADR** hasta que el archivo exista y
Joseph lo haya revisado.

---

## T-01 — Repositorio inicializado con dos ramas y exclusiones activas

**Objetivo:** existe un repositorio Git privado con `main` y `develop`, y ningún dato sensible puede confirmarse por descuido.
**Repositorio y rama:** `portfolio-joe`; commit inicial directo en `main`, luego `develop` derivada.
**Archivos exclusivos:** `.gitignore`, `privado/documentos/CV_JosephBano.docx`, `privado/setup.md`.
**Entrada/contrato:** PD-05 resuelto — el repositorio nace privado.
**Salida para integración:** repositorio con remoto configurado y `develop` como rama por defecto.
**Dependencias:** Ninguna.
**ADR aplicable:** Ninguno.
**Responsable:** Coordinador.

- [ ] Ejecutar `git init` y crear `.gitignore` con `privado/`, `.secrets`, `*.docx`, `*.pdf` y las excepciones necesarias para `templates/`.
- [ ] Trasladar `CV_JosephBano.docx` desde la raíz a `privado/documentos/` **antes** del primer commit; contiene teléfono y dirección.
- [ ] Crear `privado/setup.md` con los comandos `gh api` de protección de ramas y el procedimiento de publicación. No se versiona (D-09).
- [ ] Crear el repositorio remoto **privado** con `gh repo create` y establecer `develop` como rama por defecto.
- [ ] Ejecutar `git status --porcelain` y confirmar que no lista nada bajo `privado/` ni `.secrets` (V-04).
- [ ] Entregar al coordinador la salida de `git status`, `git branch -a` y `gh repo view --json visibility`.

**Resultado registrado:** pendiente
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

- [ ] Redactar el ADR con contexto, las tres opciones evaluadas (pandoc, `python-docx`, HTML intermedio), la decisión y sus consecuencias.
- [ ] Declarar el límite duro de R-01: un solo archivo, una sola dependencia, dos argumentos de ruta, sin configuración. Superarlo obliga a volver a revisión funcional.
- [ ] Declarar el comportamiento ante ausencia o fallo de LibreOffice: se conserva el `.docx` y se informa; no se sustituye el método en silencio.
- [ ] Obtener la revisión de Joseph y registrar fecha y decisión en el ADR.
- [ ] Entregar al coordinador el diff y la confirmación de revisión.

**Resultado registrado:** pendiente
**Bloqueos:** Ninguno

---

## T-03 — ADR-002 y vocabulario canónico de etiquetas

**Objetivo:** dos viñetas que hablan de lo mismo llevan la misma etiqueta, y el porcentaje de coincidencia deja de ser errático.
**Repositorio y rama:** `portfolio-joe`; `spec/001-taxonomia`.
**Archivos exclusivos:** `docs/adr/ADR-002-taxonomia-etiquetas.md`, `profile/taxonomy.yml`.
**Entrada/contrato:** PD-07, abierto. El stack real de Joseph según `CV_JosephBano.docx` y los diez repositorios clasificados.
**Salida para integración:** `taxonomy.yml` con etiquetas canónicas y alias; desbloquea T-07 y T-09.
**Dependencias:** T-01.
**ADR aplicable:** este. **Bloquea T-07 y T-09 hasta estar revisado.**
**Responsable:** Coordinador, con decisión de Joseph.

- [ ] Derivar el conjunto inicial de etiquetas del stack declarado y de los diez repositorios de `sources.yml`.
- [ ] Definir cada etiqueta canónica con su lista de alias, cubriendo al menos las variantes `k8s`/`kubernetes`, `csharp`/`c#`/`dotnet`, `postgres`/`postgresql`.
- [ ] Declarar la regla: una etiqueta usada en `profile/` que no exista en `taxonomy.yml` es un error de validación, no una etiqueta nueva.
- [ ] Redactar ADR-002 con la decisión y el procedimiento para añadir etiquetas.
- [ ] Obtener la revisión de Joseph y registrarla.
- [ ] Entregar al coordinador `taxonomy.yml`, el ADR y la confirmación de revisión.

**Resultado registrado:** pendiente
**Bloqueos:** PD-07 abierto hasta completar esta tarea.

---

## T-04 — ADR-003 y patrones de detección compartidos

**Objetivo:** el hook local y el CI aplican exactamente el mismo criterio, para que ningún Pull Request sorprenda con un fallo que el equipo no reprodujo.
**Repositorio y rama:** `portfolio-joe`; `spec/001-patrones-seguridad`.
**Archivos exclusivos:** `docs/adr/ADR-003-deteccion-secretos.md`, `.security/patterns.txt`, `.security/README.md`.
**Entrada/contrato:** PD-06, abierto. Propuesta del plan: archivo único de expresiones regulares consumido por ambos lados, con `gitleaks` como capa adicional solo en CI.
**Salida para integración:** `patterns.txt`; desbloquea T-05 y T-06.
**Dependencias:** T-01.
**ADR aplicable:** este. **Bloquea T-05 y T-06 hasta estar revisado.**
**Responsable:** Coordinador, con decisión de Joseph.

- [ ] Crear una prueba que falle: un archivo de ejemplo con un teléfono, un correo y una cadena de conexión ficticios que los patrones deben detectar, y un archivo limpio que no deben marcar.
- [ ] Escribir `.security/patterns.txt` con una expresión regular por línea: teléfono ecuatoriano, correo electrónico, dirección, cédula, tokens y claves privadas.
- [ ] Verificar que `grep -E -f .security/patterns.txt` marca el archivo sucio y no marca el limpio.
- [ ] Declarar en ADR-003 que CI es un superconjunto y nunca un criterio distinto, y cómo se ajusta un falso positivo: por Pull Request sobre `patterns.txt`, jamás desactivando el check.
- [ ] Obtener la revisión de Joseph y registrarla.
- [ ] Entregar al coordinador el diff, la salida de `grep` sobre ambos archivos y la confirmación de revisión.

**Resultado registrado:** pendiente
**Bloqueos:** PD-06 abierto hasta completar esta tarea.

---

## T-05 — Hook `pre-commit` que aborta el commit ofensor

**Objetivo:** un commit con datos sensibles no llega a existir.
**Repositorio y rama:** `portfolio-joe`; `spec/001-hook-precommit`.
**Archivos exclusivos:** `.githooks/pre-commit`.
**Entrada/contrato:** `.security/patterns.txt` de T-04.
**Salida para integración:** hook ejecutable, instalable con `git config core.hooksPath .githooks`.
**Dependencias:** T-04.
**ADR aplicable:** ADR-003.
**Responsable:** Subagente.

- [ ] Crear una prueba que falle: preparar un índice con `.secrets` y otro con un archivo bajo `privado/`, y comprobar que el hook aún inexistente no los detiene.
- [ ] Implementar el hook: comprobar rutas bajo `privado/`, presencia de `.secrets` en el índice, y patrones sobre el contenido añadido, abortando al primer hallazgo.
- [ ] Hacer que el mensaje de error nombre la ruta ofensora y el motivo (RF-SEG-002).
- [ ] Ejecutar `git commit` en los tres escenarios de prueba y registrar el código de salida de cada uno.
- [ ] Revisar que un commit legítimo sobre `profile/` no es bloqueado.
- [ ] Entregar al coordinador el diff, los códigos de salida y los mensajes emitidos.

**Resultado registrado:** pendiente
**Bloqueos:** Bloqueada por ADR-003 hasta que T-04 esté revisada.

---

## T-06 — Flujos de GitHub Actions bloqueantes

**Objetivo:** aunque el hook se omita con `--no-verify`, el Pull Request no es mezclable.
**Repositorio y rama:** `portfolio-joe`; `spec/001-actions-secret-guard`.
**Archivos exclusivos:** `.github/workflows/secret-guard.yml`, `.github/workflows/profile-lint.yml`, `.gitleaksignore`.
**Entrada/contrato:** `.security/patterns.txt` de T-04; esquemas de `docs/schemas.md`.
**Salida para integración:** dos checks que se pueden exigir en la protección de ramas.
**Dependencias:** T-04.
**ADR aplicable:** ADR-003.
**Responsable:** Subagente.

- [ ] Crear una rama de prueba con una infracción deliberada y comprobar que sin los flujos el Pull Request sería mezclable.
- [ ] Implementar `secret-guard.yml` con los jobs `path-guard`, `pii-scan`, `gitleaks` y `commit-hygiene`, disparados en Pull Request hacia `develop` y `main`.
- [ ] Hacer que `pii-scan` consuma `.security/patterns.txt` y no una copia de los patrones.
- [ ] Hacer que `commit-hygiene` falle si algún mensaje de commit del Pull Request contiene atribución de co-autoría a un agente (RF-SEG-007).
- [ ] Implementar `profile-lint.yml`: carga de todo YAML de `profile/`, validación contra `docs/schemas.md`, comprobación de que toda etiqueta existe en `taxonomy.yml`, que todo `evidence` existe en `sources.yml` y que toda clave `{{secrets.*}}` existe en `.secrets.example` (V-01, V-03).
- [ ] Acotar `.gitleaksignore` exclusivamente a `.secrets.example` y justificarlo en el archivo (R-03).
- [ ] Ejecutar ambos flujos sobre la rama de prueba y registrar el resultado de cada job.
- [ ] Entregar al coordinador el diff y el enlace a las ejecuciones fallidas y exitosas.

**Resultado registrado:** pendiente
**Bloqueos:** Bloqueada por ADR-003 hasta que T-04 esté revisada. `profile-lint` requiere `docs/schemas.md` de T-13.

---

## T-07 — `AGENTS.md`, el contrato operativo

**Objetivo:** existe un documento que hace la generación repetible sin código, y que un agente distinto puede seguir obteniendo el mismo resultado.
**Repositorio y rama:** `portfolio-joe`; `spec/001-agents-md`.
**Archivos exclusivos:** `AGENTS.md`.
**Entrada/contrato:** ADR-001 y ADR-002 revisados; escenarios 1, 2 y 4 del spec.
**Salida para integración:** contrato que T-12 y T-14 consumen.
**Dependencias:** T-02, T-03.
**ADR aplicable:** ADR-001, ADR-002.
**Responsable:** Coordinador. **Archivo de edición exclusiva: ninguna otra tarea lo toca.**

- [ ] Redactar §Generación con los siete pasos del Escenario 1 y los artefactos exactos que produce.
- [ ] Redactar §Coincidencia con la fórmula `round(halladas / total * 100)` y el uso de `taxonomy.yml` para normalizar (RF-GEN-006).
- [ ] Redactar §Selección con el orden determinista: coincidencias, luego `weight`, luego `id` ascendente (RF-GEN-007).
- [ ] Redactar §Idioma: un único campo de idioma en toda la composición, incluidos encabezados y nombre del puesto (RF-GEN-005).
- [ ] Redactar §Variables: la sustitución de `{{secrets.*}}` es obligatoria y su fallo detiene la generación (RF-GEN-002).
- [ ] Redactar §Sanitización con prohibiciones concretas para fuentes `interno` y `confidencial`, y la regla de que ante la duda se omite y se pregunta (RF-EVID-002).
- [ ] Redactar §Auditoría: produce informe y propuestas, nunca escritura directa; aprobación viñeta por viñeta (RF-EVID-003, RF-EVID-004).
- [ ] Redactar §Atribución: una viñeta cuya `evidence` sea de confidencialidad `interno` se atribuye al puesto en el ISTPET y nunca nombra ni enlaza el repositorio; solo las fuentes `publico` se enlazan y se presentan como obra propia (RF-EVID-006).
- [ ] Redactar §Seguimiento con los diez estados, el umbral de 21 días para `sin_respuesta` y la regla de `timeline` de solo anexión (RF-TRACK-002, RF-TRACK-003).
- [ ] Redactar §Analítica con el embudo por estado (RF-ANL-001), el desglose por fuente, idioma, plantilla y rango de coincidencia (RF-ANL-002), las keywords de mercado ausentes de `skills.yml` (RF-ANL-003) y la regla de que toda tasa se escribe `n/N`, con solo conteos por debajo de diez postulaciones (RF-ANL-004).
- [ ] Redactar §Prohibiciones: nunca afirmar lo que no está en `profile/` (RF-GEN-008); nunca escribir atribución de co-autoría en un commit (RF-SEG-007); nunca editar `privado/aplicaciones.yml` salvo por anexión.
- [ ] Revisar que cada requisito asignado a T-07 en `plan.md` tiene su sección correspondiente.
- [ ] Entregar al coordinador el diff y la tabla requisito → sección.

**Resultado registrado:** pendiente
**Bloqueos:** Bloqueada por ADR-001 y ADR-002.

---

## T-08 — Plantillas y derivador de documentos

**Objetivo:** un `cv.md` se convierte en un `.docx` y un `.pdf` que un ATS parsea sin perder información.
**Repositorio y rama:** `portfolio-joe`; `spec/001-plantillas-render`.
**Archivos exclusivos:** `templates/ats-standard.md`, `templates/ats-compact.md`, `templates/cover-letter.md`, `templates/STYLE.md`, `tools/render_docx.py`.
**Entrada/contrato:** ADR-001; el contrato de `render_docx.py` fijado en `plan.md`.
**Salida para integración:** plantillas y derivador que T-14 ejecuta.
**Dependencias:** T-02.
**ADR aplicable:** ADR-001.
**Responsable:** Subagente.

- [ ] Crear una prueba que falle: un `cv.md` de ejemplo con datos ficticios y la comprobación, aún sin implementación, de que no existe `.docx` conforme.
- [ ] Escribir `templates/STYLE.md` con las reglas inviolables: una columna, sin tablas, sin cuadros de texto, sin imágenes, sin encabezado ni pie, fuente estándar, encabezados de sección con nombres convencionales.
- [ ] Escribir `templates/ats-standard.md` con el orden de secciones y los marcadores de sustitución.
- [ ] Escribir `templates/ats-compact.md` y `templates/cover-letter.md` derivadas de la anterior.
- [ ] Implementar `tools/render_docx.py` limitado al contrato de `plan.md`: una dependencia, dos rutas, error explícito ante Markdown no admitido.
- [ ] Ejecutar el derivador sobre el `cv.md` de ejemplo y convertir a PDF con LibreOffice headless.
- [ ] Verificar sobre el `.docx` resultante: cero tablas, cero cuadros de texto, cero imágenes, sin encabezado ni pie (RF-GEN-003).
- [ ] Verificar que el texto del PDF es extraíble y coincide con el del `.docx` (RF-GEN-004).
- [ ] Entregar al coordinador el diff, los artefactos de ejemplo y la salida de ambas verificaciones.

**Resultado registrado:** pendiente
**Bloqueos:** Bloqueada por ADR-001.

---

## T-09 — Carga inicial de `profile/`

**Objetivo:** todo lo que hoy vive en un `.docx` binario pasa a ser datos consultables, sin perder ni duplicar nada.
**Repositorio y rama:** `portfolio-joe`; `spec/001-carga-perfil`.
**Archivos exclusivos:** `profile/identity.yml`, `profile/experience.yml`, `profile/projects.yml`, `profile/skills.yml`, `profile/education.yml`, `profile/certifications.yml`, `profile/languages.yml`.
**Entrada/contrato:** texto extraído de `CV_JosephBano.docx`; `taxonomy.yml` de T-03; esquemas de `docs/schemas.md`; `.secrets.example` de T-11.
**Salida para integración:** `profile/` validado por `profile-lint`.
**Dependencias:** T-03, T-11, T-13.
**ADR aplicable:** ADR-002.
**Responsable:** Subagente, con revisión dato a dato de Joseph.

- [ ] Crear una prueba que falle: ejecutar `profile-lint` sobre el `profile/` vacío y registrar el fallo.
- [ ] Cargar `identity.yml` con nombre, titulares por rol y enlaces públicos; el contacto solo como `{{secrets.*}}` (RF-DATOS-005).
- [ ] Cargar `experience.yml` con el puesto del ISTPET y sus viñetas etiquetadas en `es` y `en`, cada una con `id`, `tags`, `weight` y `evidence` (RF-DATOS-003).
- [ ] Cargar `projects.yml` con SIBA, AMMI Online, SIPLECE y VITA, cada uno con sus viñetas.
- [ ] Cargar `skills.yml` con el stack completo, su nivel y sus alias ATS (RF-DATOS-004).
- [ ] Cargar `education.yml` declarando la Universidad Politécnica Salesiana como estudios cursados sin titulación, sin afirmar título ni fecha de graduación (PD-04).
- [ ] Cargar `certifications.yml` con los seis certificados y la ruta prevista de su PDF en `privado/documentos/`.
- [ ] Cargar `languages.yml` con español nativo e inglés avanzado.
- [ ] Verificar dato a dato contra el texto extraído del `.docx` que cada elemento aparece exactamente una vez, sin duplicados entre archivos (RF-DATOS-002, V-02).
- [ ] Ejecutar `profile-lint` y registrar que pasa.
- [ ] Entregar al coordinador el diff, la tabla de verificación dato a dato y la salida de `profile-lint`.

**Resultado registrado:** pendiente
**Bloqueos:** Bloqueada por ADR-002. No sustituye ni contradice lo declarado en el `.docx`; cualquier contradicción se reporta, no se corrige por cuenta propia.

---

## T-10 — `sources.yml` con las diez fuentes clasificadas

**Objetivo:** el sistema sabe dónde está la evidencia de cada afirmación y qué puede decirse de cada fuente.
**Repositorio y rama:** `portfolio-joe`; `spec/001-fuentes-evidencia`.
**Archivos exclusivos:** `profile/sources.yml`.
**Entrada/contrato:** tabla «Fuentes de evidencia clasificadas» de `spec.md`, resultado de PD-03 y PD-08.
**Salida para integración:** registro de fuentes que T-14 usa en la auditoría de prueba.
**Dependencias:** T-11.
**ADR aplicable:** Ninguno.
**Responsable:** Subagente.

- [ ] Crear una prueba que falle: comprobar que `profile-lint` rechaza un `evidence` que no corresponde a ninguna fuente.
- [ ] Declarar las diez fuentes con `id`, `ruta_local`, `confidencialidad` y `permite_extraer` (RF-EVID-001).
- [ ] Clasificar `fake_reports`, `leccionario_inspeccion` y `titulacion_istpet` como `publico`.
- [ ] Clasificar `biometric_sistem_reports` como `interno` pese a estar bajo la cuenta personal, con nota de la cesión pendiente al ISTPET (PD-08).
- [ ] Clasificar las seis restantes como `interno`.
- [ ] Registrar por qué `Mi_ISTPET` y `gestion_recursos_humanos_istpet` quedan excluidas, para que nadie las añada después sin darse cuenta.
- [ ] Añadir a cada fuente el campo `enlazable`, verdadero solo para las tres `publico`, de modo que la regla de atribución sea un dato y no un criterio a recordar (RF-EVID-006).
- [ ] Verificar que ninguna ruta local declarada contiene datos que no deban versionarse y que todas existen en el equipo.
- [ ] Entregar al coordinador el diff y la comprobación de existencia de las diez rutas.

**Resultado registrado:** pendiente
**Bloqueos:** Ninguno

---

## T-11 — Variables personales y estructura de `privado/`

**Objetivo:** los datos de contacto existen en un solo lugar, fuera de Git, y el repositorio declara qué claves necesita sin revelar sus valores.
**Repositorio y rama:** `portfolio-joe`; `spec/001-variables-privado`.
**Archivos exclusivos:** `.secrets.example`, `privado/.secrets`, estructura de `privado/`.
**Entrada/contrato:** `.gitignore` de T-01.
**Salida para integración:** lista canónica de claves que T-09 consume.
**Dependencias:** T-01.
**ADR aplicable:** Ninguno.
**Responsable:** Subagente.

- [ ] Crear una prueba que falle: comprobar que `profile-lint` rechaza una referencia `{{secrets.*}}` sin clave correspondiente.
- [ ] Escribir `.secrets.example` con toda clave necesaria: teléfono, correo, dirección, ciudad, país (RF-DATOS-006).
- [ ] Usar valores de ejemplo deliberadamente no verosímiles, para no disparar falsos positivos de `gitleaks` (R-03).
- [ ] Crear `privado/.secrets` con los valores reales de Joseph, y confirmar que `git status` no lo lista.
- [ ] Crear los directorios `privado/generados/`, `privado/documentos/`, `privado/notas/`, `privado/evidencia/`.
- [ ] Crear `privado/aplicaciones.yml` vacío con el encabezado de esquema (RF-TRACK-001).
- [ ] Verificar con `git check-ignore -v` que cada ruta de `privado/` está excluida y por qué regla.
- [ ] Entregar al coordinador el diff de lo versionado y la salida de `git check-ignore`.

**Resultado registrado:** pendiente
**Bloqueos:** Ninguno

---

## T-12 — `README.md`

**Objetivo:** alguien que llega al repositorio entiende qué es y puede usarlo, y quien lo evalúa como portafolio ve criterio de ingeniería.
**Repositorio y rama:** `portfolio-joe`; `spec/001-readme`.
**Archivos exclusivos:** `README.md`.
**Entrada/contrato:** `AGENTS.md` de T-07.
**Salida para integración:** documentación de entrada del repositorio.
**Dependencias:** T-07.
**ADR aplicable:** Ninguno.
**Responsable:** Subagente.

- [ ] Explicar qué es el repositorio y por qué existe: una fuente única de la verdad de la que se derivan documentos, no una carpeta de currículos.
- [ ] Documentar la instalación del hook con `git config core.hooksPath .githooks` como primer paso obligatorio.
- [ ] Documentar el ciclo de uso en los cuatro escenarios del spec, con los comandos y peticiones concretas.
- [ ] Declarar la frontera de código de `plan.md` y por qué existen `.githooks/` y `tools/`.
- [ ] Declarar qué es público y qué nunca sale del equipo, y por qué.
- [ ] Verificar que ningún ejemplo del README contiene datos reales de contacto.
- [ ] Entregar al coordinador el diff y la comprobación de ausencia de datos reales.

**Resultado registrado:** pendiente
**Bloqueos:** Ninguno

---

## T-13 — Documentación de esquemas, reglas ATS y flujo

**Objetivo:** las reglas del sistema están escritas y justificadas, no solo implícitas en el contrato del agente.
**Repositorio y rama:** `portfolio-joe`; `spec/001-docs`.
**Archivos exclusivos:** `docs/schemas.md`, `docs/ats-rules.md`, `docs/workflow.md`.
**Entrada/contrato:** requisitos del spec.
**Salida para integración:** `docs/schemas.md`, que T-06 y T-09 consumen sin modificar.
**Dependencias:** T-01.
**ADR aplicable:** Ninguno.
**Responsable:** Subagente. **`docs/schemas.md` es de edición exclusiva de esta tarea.**

- [ ] Escribir `docs/schemas.md` con los campos y vocabularios cerrados de cada YAML de `profile/`, de `oferta.yml` y de `aplicaciones.yml` (RF-DATOS-001, RF-TRACK-001, RF-TRACK-002).
- [ ] Escribir `docs/ats-rules.md` con cada regla ATS y el motivo concreto por el que existe, no solo el enunciado.
- [ ] Escribir `docs/workflow.md` con el ciclo completo: auditar, actualizar, generar, postular, registrar, analizar.
- [ ] Verificar que todo vocabulario cerrado citado en el spec aparece completo y sin valores añadidos por cuenta propia.
- [ ] Entregar al coordinador el diff y la tabla vocabulario → sección del spec.

**Resultado registrado:** pendiente
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
**Responsable:** Coordinador.

- [ ] Ejecutar los catorce recorridos de `test-e2e.md` sobre la versión declarada de `develop`, cubriendo el ciclo completo de generación (RF-GEN-001), seguimiento y analítica.
- [ ] Registrar por recorrido el resultado obtenido, la evidencia y la fecha.
- [ ] Ejecutar E2E-05 dos veces y comparar los `cv.md` byte a byte (RF-GEN-007).
- [ ] Eliminar los artefactos de prueba de `privado/generados/` una vez registrada la evidencia, o marcarlos claramente como ficticios.
- [ ] Reportar como incidencia todo recorrido fallido o bloqueado; un recorrido bloqueado no cuenta como aprobado.
- [ ] Entregar al coordinador la tabla de resultado global.

**Resultado registrado:** pendiente
**Bloqueos:** Ninguno

---

## T-15 — Revisión del historial, protección de ramas y publicación

**Objetivo:** el repositorio se hace público solo cuando está demostrado que su historial completo está limpio.
**Repositorio y rama:** `portfolio-joe`; `main`.
**Archivos exclusivos:** `privado/setup.md` (registro de evidencia).
**Entrada/contrato:** T-14 con los catorce recorridos aprobados.
**Salida para integración:** repositorio público con ramas protegidas.
**Dependencias:** T-14.
**ADR aplicable:** Ninguno.
**Responsable:** Joseph, con el coordinador.

- [ ] Revisar el historial completo con `git log -p --all` y buscar coincidencias de `.security/patterns.txt` sobre todo el historial (V-06, RF-SEG-008).
- [ ] Si aparece cualquier hallazgo, reescribir el historial **antes** de publicar, mientras el repositorio sigue siendo privado (R-05).
- [ ] Confirmar que ningún commit contiene atribución de co-autoría a un agente (RF-SEG-007).
- [ ] Aplicar la protección de `main` y `develop` con `gh api`: sin push directo, sin force-push, Pull Request obligatorio, `secret-guard` y `profile-lint` como checks requeridos (RF-SEG-006).
- [ ] Verificar con `gh api repos/:owner/:repo/branches/{main,develop}/protection` y registrar la salida como evidencia (V-05, R-02).
- [ ] Intentar un push directo a `main` y confirmar que es rechazado.
- [ ] Cambiar la visibilidad del repositorio a pública solo tras completar todo lo anterior (PD-05).
- [ ] Entregar a Joseph la evidencia de cada paso.

**Resultado registrado:** pendiente
**Bloqueos:** Ninguno

---

## Integración y cierre

- [ ] El coordinador revisó cada diff y comprobó la evidencia de cada tarea. El mensaje «terminado» de un subagente no constituye evidencia.
- [ ] Se resolvieron dependencias y conflictos sin cambiar el spec aprobado. Toda contradicción hallada se registró y se llevó a decisión.
- [ ] ADR-001, ADR-002 y ADR-003 están redactados, revisados por Joseph y citados por las tareas que dependían de ellos.
- [ ] PD-06 y PD-07 quedaron cerrados con su decisión registrada en el spec.
- [ ] `profile-lint` pasa sobre `develop` integrada.
- [ ] Se ejecutó `test-e2e.md` y se registraron resultados por escenario.
- [ ] Cada tarea entró por Pull Request a `develop`, y `develop` entró a `main` por Pull Request.
- [ ] Ningún commit del repositorio contiene atribución de co-autoría a un agente.
- [ ] Solo los requisitos con evidencia integrada y prueba satisfactoria pasan a `Implementado`.
