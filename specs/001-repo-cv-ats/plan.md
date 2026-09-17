# Repositorio fuente de la verdad para búsqueda de empleo — Plan de implementación

**Spec aprobado:** `spec.md` versión 0.1 — aprobado por Joseph el 2026-09-17
**Objetivo:** Un repositorio en GitHub del que se derive, sin edición manual, una hoja de vida ATS adaptada a cada oferta, cuya información esté respaldada por los repositorios de trabajo reales y cuyo resultado quede medido.
**Repositorios:** `portfolio-joe` (único, aún sin inicializar). Rutas relativas a `/home/joeman/Documents/proyects/portfolio-joe`.
**Tecnologías:** Git 2.55 · GitHub Actions · Python 3.14.7 con `python-docx` · LibreOffice 26.8 en modo headless · YAML · Markdown. Verificadas en el equipo el 2026-09-17.

## Frontera de código

D-01 excluye código de aplicación. El plan mantiene esa frontera y admite
exactamente dos excepciones, ambas ya implícitas en los requisitos aprobados:

1. **Guardas de seguridad** (`.githooks/pre-commit`, flujos de Actions). RF-SEG-002
   exige un hook que aborte; un hook es por definición un ejecutable.
2. **Derivador de documentos** (`tools/render_docx.py`). RF-GEN-007 exige que dos
   generaciones idénticas produzcan el mismo resultado. Un script escrito de nuevo
   en cada ejecución no puede garantizarlo.

Ninguna de las dos genera contenido: no seleccionan viñetas, no redactan, no
deciden. La selección y la redacción siguen siendo del agente leyendo `AGENTS.md`.
Esta frontera se registra en ADR-001 y se declara en `README.md`.

## Correspondencia con el spec

| Requisito o escenario | Decisión de diseño | Componente o archivo | Tarea | Verificación |
|---|---|---|---|---|
| RF-DATOS-001 | Ocho archivos YAML de esquema fijo, documentado en `docs/schemas.md`. | `profile/*.yml` | T-09 | V-01 |
| RF-DATOS-002 | Trazabilidad dato a dato contra el texto extraído del `.docx`, revisada por Joseph. | `profile/*.yml` | T-09 | V-02 |
| RF-DATOS-003 | Esquema de viñeta con `id`, `tags`, `weight`, `es`, `en`, `evidence`. | `profile/experience.yml`, `profile/projects.yml` | T-09 | V-01 |
| RF-DATOS-004 | Vocabulario cerrado de nivel y lista `aliases`. | `profile/skills.yml` | T-09 | V-01 |
| RF-DATOS-005 | Referencias `{{secrets.<clave>}}` en lugar de literales. | `profile/identity.yml` | T-11 | V-03 |
| RF-DATOS-006 | `.secrets.example` es la lista canónica de claves. | `.secrets.example` | T-11 | V-03 |
| RF-GEN-001 | Directorio por postulación con cinco artefactos. | `AGENTS.md` §Generación, `privado/generados/` | T-07, T-14 | E2E-01 |
| RF-GEN-002 | Sustitución de marcadores como paso obligatorio previo al render; falla si queda alguno. | `AGENTS.md` §Variables, `tools/render_docx.py` | T-07, T-08 | E2E-04 |
| RF-GEN-003 | `python-docx` construye el documento con estilos explícitos; sin tablas ni cajas. | `tools/render_docx.py`, `templates/STYLE.md` | T-08 | E2E-02 |
| RF-GEN-004 | LibreOffice headless convierte el `.docx` ya conforme. | `tools/render_docx.py` | T-08 | E2E-02 |
| RF-GEN-005 | Un único campo de idioma seleccionado en toda la composición. | `AGENTS.md` §Idioma, `templates/ats-standard.md` | T-07, T-08 | E2E-03 |
| RF-GEN-006 | Cruce de palabras clave contra `name` y `aliases`, normalizado por la taxonomía. | `AGENTS.md` §Coincidencia, `profile/taxonomy.yml` | T-03, T-07 | E2E-01 |
| RF-GEN-007 | Orden de selección totalmente determinista: relevancia, luego `weight`, luego `id` alfabético como desempate. | `AGENTS.md` §Selección | T-07 | E2E-05 |
| RF-GEN-008 | Prohibición explícita de afirmar lo que no está en `profile/`, con el hueco reportado en su lugar. | `AGENTS.md` §Prohibiciones | T-07 | E2E-06 |
| RF-SEG-001 | `.gitignore` con `privado/` y `.secrets`. | `.gitignore` | T-01 | V-04 |
| RF-SEG-002 | Hook que inspecciona el índice antes de crear el commit. | `.githooks/pre-commit` | T-05 | E2E-07 |
| RF-SEG-003 | Patrones compartidos aplicados al contenido añadido. | `.security/patterns.txt`, `.githooks/pre-commit` | T-04, T-05 | E2E-08 |
| RF-SEG-004 | Job `path-guard` sobre los archivos del PR. | `.github/workflows/secret-guard.yml` | T-06 | E2E-09 |
| RF-SEG-005 | Jobs `pii-scan` y `gitleaks` sobre diff e historial. | `.github/workflows/secret-guard.yml` | T-04, T-06 | E2E-09 |
| RF-SEG-006 | Reglas de protección aplicadas con `gh api`, documentadas fuera del repositorio público. | `privado/setup.md` | T-01, T-15 | V-05 |
| RF-SEG-007 | Regla de higiene en el contrato y comprobación en CI sobre los mensajes del PR. | `AGENTS.md` §Commits, `.github/workflows/secret-guard.yml` | T-06, T-07 | E2E-10 |
| RF-SEG-008 | Revisión del historial completo como puerta previa a publicar. | Procedimiento en `privado/setup.md` | T-15 | V-06 |
| RF-EVID-001 | Esquema de fuente con `id`, `ruta_local`, `confidencialidad`, `permite_extraer`. | `profile/sources.yml` | T-10 | V-01 |
| RF-EVID-002 | Regla de sanitización enunciada como lista de prohibiciones concretas. | `AGENTS.md` §Sanitización | T-07 | E2E-11 |
| RF-EVID-003 | Auditoría que produce informe y propuestas, nunca escritura directa. | `AGENTS.md` §Auditoría | T-07 | E2E-11 |
| RF-EVID-004 | Aprobación viñeta por viñeta como paso obligatorio. | `AGENTS.md` §Auditoría | T-07 | E2E-11 |
| RF-EVID-005 | Los valores de `evidence` referencian `id` de `sources.yml`. | `profile/sources.yml`, `profile/experience.yml` | T-09, T-10 | V-01 |
| RF-EVID-006 | Regla de atribución: `interno` sustenta experiencia bajo el puesto; solo `publico` se enlaza y se presenta como obra propia. | `AGENTS.md` §Atribución, `profile/sources.yml` | T-07, T-10 | E2E-14 |
| RF-TRACK-001 | Esquema de postulación con `id` igual al nombre del directorio generado. | `privado/aplicaciones.yml`, `docs/schemas.md` | T-11, T-13 | E2E-12 |
| RF-TRACK-002 | Vocabulario cerrado de diez estados. | `docs/schemas.md`, `AGENTS.md` §Seguimiento | T-07, T-13 | E2E-12 |
| RF-TRACK-003 | `timeline` de solo anexión; prohibido editar entradas previas. | `AGENTS.md` §Seguimiento | T-07 | E2E-12 |
| RF-ANL-001 | Embudo por estado con conversión entre etapas consecutivas. | `AGENTS.md` §Analítica | T-07 | E2E-13 |
| RF-ANL-002 | Desglose por `fuente`, `idioma`, `plantilla` y rango de `match_score`. | `AGENTS.md` §Analítica | T-07 | E2E-13 |
| RF-ANL-003 | Palabras clave de ofertas ausentes de `skills.yml`, por frecuencia. | `AGENTS.md` §Analítica | T-07 | E2E-13 |
| RF-ANL-004 | Toda tasa se escribe como `n/N`; por debajo de diez postulaciones solo conteos. | `AGENTS.md` §Analítica | T-07 | E2E-13 |
| Escenario 1 | Flujo completo de generación. | `AGENTS.md`, `templates/`, `tools/` | T-14 | E2E-01 a E2E-06 |
| Escenario 2 | Flujo de auditoría con aprobación. | `AGENTS.md`, `profile/sources.yml` | T-10, T-14 | E2E-11 |
| Escenario 3 | Bloqueo en las tres capas. | `.gitignore`, `.githooks/`, `.github/workflows/` | T-05, T-06 | E2E-07 a E2E-10 |
| Escenario 4 | Registro y analítica. | `AGENTS.md`, `privado/aplicaciones.yml` | T-11, T-14 | E2E-12, E2E-13 |

Verificaciones que no son recorridos de punta a punta:

| ID | Comprobación | Cómo se ejecuta |
|---|---|---|
| V-01 | Todo YAML de `profile/` carga sin error y cumple su esquema. | Job `profile-lint` en CI y comprobación local con Python. |
| V-02 | Cada dato de `CV_JosephBano.docx` aparece una vez en `profile/`. | Revisión de Joseph contra el texto extraído, en el PR de T-09. |
| V-03 | Toda clave `{{secrets.*}}` referenciada existe en `.secrets.example`. | Job `profile-lint`. |
| V-04 | `git status --porcelain` no lista nada bajo `privado/` ni `.secrets`. | Comando en la revisión de T-01. |
| V-05 | `gh api repos/:owner/:repo/branches/main/protection` devuelve las reglas esperadas. | Comando en T-15. |
| V-06 | `git log -p --all` revisado y `git grep` del historial sin coincidencias de patrones. | Procedimiento de T-15, previo a publicar. |

## Diseño y contratos

### Flujo de generación

El actor es Joseph; no hay frontend, API ni servicio. El agente es el ejecutor
y `AGENTS.md` su contrato. La secuencia del Escenario 1 se fija así:

1. **Entrada:** texto o enlace de la oferta, más `idioma` (`es` o `en`) y
   `plantilla` (`ats-standard` o `ats-compact`).
2. **Normalización:** el agente escribe `oferta.yml` con `empresa`, `rol`,
   `seniority`, `modalidad`, `ubicacion`, `salario_publicado`, `requisitos_obligatorios`,
   `requisitos_deseables` y `keywords`. Las `keywords` se extraen literales del
   texto de la oferta y se normalizan contra `profile/taxonomy.yml`.
3. **Coincidencia:** cada keyword normalizada se busca en `skills.yml` por `name`
   y por `aliases`. `match_score = round(halladas / total_keywords * 100)`. Se
   escribe `match.md` con el porcentaje, la lista hallada y la lista ausente.
4. **Selección:** de cada puesto y proyecto se toman las viñetas cuyos `tags`
   intersecten las keywords normalizadas. Orden: número de coincidencias
   descendente, luego `weight` descendente, luego `id` ascendente. El desempate
   por `id` es lo que hace la salida reproducible (RF-GEN-007).
5. **Composición:** se aplica la plantilla, se sustituyen los `{{secrets.*}}` y,
   cuando una keyword de la oferta coincide con un `alias`, se escribe la variante
   textual de la oferta en lugar del `name` canónico.
6. **Derivación:** `tools/render_docx.py` produce `cv.docx` desde `cv.md`;
   LibreOffice headless produce `cv.pdf` desde `cv.docx`.
7. **Registro:** entrada nueva en `privado/aplicaciones.yml` con estado `borrador`.

**Errores y su tratamiento.** Falta de `.secrets` o de una clave: se detiene y
nombra la clave; no se emite documento con marcadores (RF-GEN-002). Coincidencia
baja: se informa con los huecos y se pregunta; nunca se inventa experiencia
(RF-GEN-008). Empresa o rol irreconocibles: se pregunta antes de crear el
directorio. LibreOffice ausente o fallido: `cv.docx` se conserva y se informa que
el PDF no se generó; no se sustituye por otro método en silencio.

### Contrato de `tools/render_docx.py`

- **Entrada:** ruta de `cv.md`, ruta de salida `.docx`.
- **Salida:** un `.docx` de una columna, sin tablas, sin cuadros de texto, sin
  imágenes, sin encabezado ni pie, fuente Calibri 11 y encabezados con los
  estilos nativos `Heading 1` y `Heading 2`.
- **Markdown admitido:** encabezados `#` y `##`, párrafos, listas con `-`,
  negrita `**texto**`, cursiva `*texto*` e hipervínculos `[texto](url)`.
  Cualquier otra construcción, incluido un marcador de énfasis sin cerrar,
  provoca error explícito con el número de línea; no se degrada en silencio.
- **Dependencias:** `python-docx`. Nada más.
- **Errores:** código distinto de cero y mensaje que nombre la línea ofensora.

### Contrato de las guardas de seguridad

Un único origen de verdad para los patrones: `.security/patterns.txt`, una
expresión regular por línea, con comentarios `#`. Lo consumen el hook local
(`grep -E -f`) y el job `pii-scan` de CI, de modo que ambos aplican el mismo
criterio. CI añade `gitleaks` como capa adicional: es un superconjunto, nunca
un criterio distinto. Esta es la resolución propuesta para PD-06.

El hook comprueba, en este orden: rutas bajo `privado/`, presencia de `.secrets`
en el índice, y patrones sobre el contenido añadido. Aborta al primer hallazgo.

## ADR aplicables y por redactar

| Decisión | Repositorio y ADR | Estado | Tareas condicionadas |
|---|---|---|---|
| Mecanismo de derivación `.md` → `.docx` → `.pdf` y frontera de código admisible | `docs/adr/ADR-001-derivacion-documentos.md` | Propuesto — decidido por Joseph el 2026-09-17, pendiente de redacción | T-08, T-14 |
| Vocabulario canónico de etiquetas (PD-07) | `docs/adr/ADR-002-taxonomia-etiquetas.md` | Pendiente | T-03, T-09 |
| Criterio único de detección de secretos en local y CI (PD-06) | `docs/adr/ADR-003-deteccion-secretos.md` | Pendiente | T-04, T-05, T-06 |

Ninguna tarea condicionada se ejecuta antes de que su ADR esté redactado y
revisado. T-02 redacta ADR-001; T-03 redacta ADR-002; T-04 redacta ADR-003.

## Mapa de archivos

| Repositorio | Crear o modificar | Responsabilidad | Depende de |
|---|---|---|---|
| `portfolio-joe` | `.gitignore` | Excluir `privado/` y `.secrets` del control de versiones. | — |
| `portfolio-joe` | `.secrets.example` | Lista canónica de claves personales, con valores ficticios. | — |
| `portfolio-joe` | `README.md` | Qué es el repositorio, cómo se instala el hook, cómo se usa el ciclo. | T-07 |
| `portfolio-joe` | `AGENTS.md` | Contrato operativo: generación, selección, coincidencia, idioma, sanitización, auditoría, seguimiento, analítica, prohibiciones, higiene de commits. | ADR-001, ADR-002 |
| `portfolio-joe` | `.security/patterns.txt` | Origen único de patrones de detección. | ADR-003 |
| `portfolio-joe` | `.githooks/pre-commit` | Capa 2: aborta el commit ofensor. | `.security/patterns.txt` |
| `portfolio-joe` | `.github/workflows/secret-guard.yml` | Capa 3: `path-guard`, `pii-scan`, `gitleaks`, `commit-hygiene`. Check requerido. | `.security/patterns.txt` |
| `portfolio-joe` | `.github/workflows/profile-lint.yml` | Validar esquemas de `profile/`, taxonomía y claves de `.secrets.example`. | `docs/schemas.md` |
| `portfolio-joe` | `profile/identity.yml` | Identidad y titulares por rol; contacto solo por referencia. | `.secrets.example` |
| `portfolio-joe` | `profile/experience.yml` | Puestos y biblioteca de viñetas etiquetadas. | `profile/taxonomy.yml` |
| `portfolio-joe` | `profile/projects.yml` | Proyectos y sus viñetas. | `profile/taxonomy.yml` |
| `portfolio-joe` | `profile/skills.yml` | Habilidades con nivel y alias ATS. | `profile/taxonomy.yml` |
| `portfolio-joe` | `profile/education.yml` | Formación. Salesiana como estudios cursados sin titulación (PD-04). | — |
| `portfolio-joe` | `profile/certifications.yml` | Certificados, con ruta al PDF en `privado/documentos/`. | — |
| `portfolio-joe` | `profile/languages.yml` | Idiomas y nivel. | — |
| `portfolio-joe` | `profile/taxonomy.yml` | Vocabulario canónico de etiquetas y sus alias. | ADR-002 |
| `portfolio-joe` | `profile/sources.yml` | Las diez fuentes de evidencia con su confidencialidad. | Tabla de PD-03 |
| `portfolio-joe` | `templates/ats-standard.md` | Plantilla principal de una columna. | ADR-001 |
| `portfolio-joe` | `templates/ats-compact.md` | Variante de una página. | `templates/ats-standard.md` |
| `portfolio-joe` | `templates/cover-letter.md` | Carta de presentación. | `templates/ats-standard.md` |
| `portfolio-joe` | `templates/STYLE.md` | Reglas de render inviolables. | ADR-001 |
| `portfolio-joe` | `tools/render_docx.py` | Derivar `.docx` conforme desde `cv.md`. | ADR-001, `templates/STYLE.md` |
| `portfolio-joe` | `docs/ats-rules.md` | Las reglas ATS y el motivo de cada una. | — |
| `portfolio-joe` | `docs/workflow.md` | El ciclo completo paso a paso. | `AGENTS.md` |
| `portfolio-joe` | `docs/schemas.md` | Campos y vocabularios cerrados de cada YAML. | — |
| `portfolio-joe` | `docs/adr/ADR-001..003` | Decisiones de arquitectura. | — |
| Fuera de Git | `privado/.secrets` | Valores reales de contacto. | `.secrets.example` |
| Fuera de Git | `privado/setup.md` | Comandos `gh api` de protección de ramas y procedimiento de publicación. | — |
| Fuera de Git | `privado/aplicaciones.yml` | Registro de postulaciones. | `docs/schemas.md` |
| Fuera de Git | `privado/generados/`, `privado/documentos/`, `privado/notas/`, `privado/evidencia/` | Artefactos y material sensible. | — |

`CV_JosephBano.docx` se traslada a `privado/documentos/` en T-01, antes del
primer commit. Contiene teléfono y dirección; no puede quedar en la raíz.

## Datos y migración

No hay base de datos ni migraciones. La persistencia son archivos.

**Migración inicial:** el contenido de `CV_JosephBano.docx` se traslada a
`profile/` una sola vez (T-09). El `.docx` original se conserva en
`privado/documentos/` como referencia histórica, no como fuente activa. Una vez
completada la carga, `profile/` es la única fuente; el `.docx` no vuelve a
consultarse para generar.

**Punto de confirmación:** la escritura en disco de cada archivo. En `profile/`
la escritura ocurre solo dentro de un PR aprobado por Joseph. En `privado/` la
escritura es directa, porque nunca abandona el equipo.

**Compatibilidad hacia adelante:** los vocabularios cerrados (`level`, `estado`,
`confidencialidad`, etiquetas) se amplían modificando `docs/schemas.md` y
`profile/taxonomy.yml` en el mismo PR que introduce el valor nuevo, para que
`profile-lint` nunca quede por detrás de los datos.

**Despliegue:** no aplica. El repositorio no se despliega; se publica.

## Orden de ejecución e integración

1. **Fundación, exclusiva del coordinador:** T-01 crea el repositorio privado,
   las ramas `main` y `develop`, `.gitignore`, y traslada el `.docx` a `privado/`.
   Nada puede ejecutarse antes.
2. **Decisiones de arquitectura, en paralelo entre sí:** T-02 (ADR-001),
   T-03 (ADR-002 y `taxonomy.yml`), T-04 (ADR-003 y `patterns.txt`). Archivos
   disjuntos, sin dependencias cruzadas.
3. **Construcción, en paralelo por grupos de archivos disjuntos:**
   - Guardas: T-05 y T-06, ambas dependen de T-04. T-05 toca `.githooks/`,
     T-06 toca `.github/workflows/`. Pueden ir en paralelo entre sí.
   - Contrato y plantillas: T-07 (`AGENTS.md`) y T-08 (`templates/`, `tools/`).
     T-08 depende de T-02; T-07 depende de T-02 y T-03.
   - Datos: T-11 (`.secrets.example` y estructura de `privado/`), luego T-09
     (`profile/` cargado) y T-10 (`sources.yml`). T-09 depende de T-03 y T-11.
   - Documentación: T-12 (`README.md`) y T-13 (`docs/`). T-12 depende de T-07.
4. **Integración y verificación:** T-14 ejecuta `test-e2e.md` completo sobre la
   rama `develop` integrada. Ninguna tarea se declara terminada por el mensaje
   de un subagente; el coordinador revisa cada diff.
5. **Publicación:** T-15 revisa el historial completo, aplica la protección de
   ramas y solo entonces cambia la visibilidad a pública.

**Edición exclusiva.** `AGENTS.md` lo escribe únicamente T-07; es el archivo con
más riesgo de conflicto porque casi todo requisito lo menciona. `docs/schemas.md`
lo escribe únicamente T-13, y T-09 lo consume sin modificarlo. Si T-09 detecta
que el esquema documentado no basta, no lo edita: reporta al coordinador.
`.security/patterns.txt` lo escribe únicamente T-04; T-05 y T-06 lo consumen.

## Riesgos y decisiones pendientes

| Riesgo o punto abierto | Efecto | Acción y responsable |
|---|---|---|
| R-01 | `tools/render_docx.py` es código de aplicación y roza la frontera de D-01. Si crece, el repositorio se convierte en el proyecto que Joseph decidió no construir. | Límite duro registrado en ADR-001: un solo archivo, una sola dependencia, sin interfaz de línea de comandos más allá de dos rutas, sin configuración. Si necesita más, se vuelve a revisión funcional. Responsable: coordinador en T-02. |
| R-02 | Las reglas de protección de ramas no son archivos del repositorio. Si se aplican mal o se revierten, RF-SEG-006 queda incumplido sin que nada falle visiblemente. | T-15 verifica con `gh api` y registra la salida como evidencia. Se repite la verificación tras cualquier cambio de configuración. Responsable: Joseph. |
| R-03 | `gitleaks` en CI puede producir falsos positivos sobre `.secrets.example`, que contiene valores con forma de dato real. | Valores de ejemplo deliberadamente no verosímiles y `.gitleaksignore` acotado a ese único archivo, revisado en T-06. Responsable: T-06. |
| R-04 | La sanitización (RF-EVID-002) y la atribución (RF-EVID-006) dependen del criterio del agente. Un juicio equivocado publica propiedad intelectual ajena y el daño no es reversible. | `AGENTS.md` enuncia prohibiciones concretas y la regla de que ante la duda se omite y se pregunta. Además, toda escritura en `profile/` pasa por PR revisado por Joseph. Responsable: T-07 y Joseph. |
| R-05 | El historial de Git puede contener datos sensibles ya confirmados antes de que las guardas existan. | El repositorio nace privado (PD-05) y T-15 revisa el historial completo antes de publicar. Si aparece algo, se reescribe el historial mientras aún es privado. Responsable: T-15. |
| R-06 | LibreOffice puede alterar el documento al convertir a PDF y romper la conformidad ATS verificada sobre el `.docx`. | E2E-02 verifica el PDF de forma independiente, extrayendo su texto, no solo el `.docx`. Responsable: T-14. |
| PD-06 | Criterio único de detección en local y CI. | Propuesta en este plan: `.security/patterns.txt` compartido, con `gitleaks` como capa adicional en CI. Requiere ADR-003 y aprobación de Joseph. Responsable: T-04. |
| PD-07 | Vocabulario canónico de etiquetas. | Se define en `profile/taxonomy.yml` con etiquetas canónicas y alias, validado por `profile-lint`. Requiere ADR-002. Responsable: T-03. |

## Comprobación del plan

- [x] Las rutas y tecnologías coinciden con el equipo real: LibreOffice 26.8,
      Python 3.14.7, Git 2.55 y `gh` 2.100 verificados el 2026-09-17; `pandoc`,
      `gitleaks`, `weasyprint` y `wkhtmltopdf` confirmados como ausentes y no
      requeridos en local.
- [x] Los ADR vigentes se respetan — no existe ninguno previo — y los tres
      nuevos tienen responsable y tareas condicionadas declaradas.
- [x] Los 35 requisitos del spec tienen ruta hasta una tarea y una verificación.
      No hay excepciones.
- [x] Las tareas tienen dependencias y límites de edición explícitos, y los tres
      archivos de conflicto probable tienen dueño único.
- [x] Las pruebas verifican comportamientos distintos: `profile-lint` valida
      estructura, los recorridos E2E validan comportamiento observable. Confirmado
      con los 14 recorridos de `test-e2e.md` aprobados el 2026-09-17.
