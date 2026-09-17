# Repositorio fuente de la verdad para búsqueda de empleo — Spec

**ID:** SPEC-001
**Versión:** 0.1
**Estado:** Aprobado
**Responsable funcional:** Joseph Andrés Baño Naranjo
**Fecha:** 2026-09-17
**Repositorios afectados:** `portfolio-joe` (repositorio único, aún sin inicializar)

## Problema y resultado esperado

Hoy la hoja de vida de Joseph existe como un único archivo binario,
`CV_JosephBano.docx`, en la raíz de esta carpeta. Ese archivo tiene tres
defectos comprobados:

1. **Está desactualizado.** Declara cuatro proyectos (SIBA, AMMI Online,
   SIPLECE, VITA), mientras que en el equipo local existen **doce
   repositorios de trabajo** bajo `/home/joeman/Documents/istpet-dev/`. El
   documento no refleja lo que Joseph sabe hacer actualmente.
2. **No es adaptable.** Enviar el mismo documento a toda oferta obliga a
   editarlo a mano, y cada edición manual produce una versión distinta que
   nadie vuelve a encontrar.
3. **No deja rastro.** No existe registro de a qué ofertas se postuló, con
   qué versión del documento, ni qué respuesta se obtuvo. No hay forma de
   saber qué funciona.

El resultado esperado es un repositorio público en GitHub que actúe como
**fuente única de la verdad** sobre la trayectoria profesional de Joseph, del
que se derive —sin editar nada a mano— una hoja de vida optimizada para
sistemas de filtrado de personal (ATS) y adaptada a cada oferta concreta, y
que registre el resultado de cada postulación para poder medirlo.

Quien usa el sistema es Joseph. La decisión que necesita tomar en cada ciclo
es: *qué versión de su perfil enviar a una oferta determinada*, y más
adelante, *qué está funcionando y qué habilidad le está costando entrevistas*.

## Fuentes y decisiones vigentes

| Fuente | Ruta o enlace exacto | Regla o dato que aporta |
|---|---|---|
| Hoja de vida actual | `CV_JosephBano.docx` | Carga inicial de datos: perfil, un puesto, cuatro proyectos, educación, seis certificados, stack e idiomas. Confirmado: el texto fue extraído y leído. |
| Repositorios de trabajo | `/home/joeman/Documents/istpet-dev/` | Doce repositorios Git locales. Confirmado por inspección: `gestion_mecanica_ISTPET`, `generador-docs-istpet`, `leccionario_inspeccion`, `Istpet_Vehiculos`, `titulacion_istpet`, `gestion_academica_istpet`, `gestion_recursos_humanos_istpet`, `gestion_administrativa_istpet`, `Mi_ISTPET`, `Bienestar_Institucional`, `fake_reports`, `biometric_sistem_reports`. |
| Flujo Spec Kit | `specs/README.md`, `specs/plantillas/` | Formato y flujo de aprobación de este mismo documento. Copiado desde `istpet-dev/gitlab/departamento-medico/specs`. |
| Decisiones de diseño de Joseph | Sesión de diseño del 2026-09-17 | Ver tabla siguiente. |
| Herramientas del equipo | Verificado por comando el 2026-09-17 | Disponibles: LibreOffice 26.8, `gh` 2.100, Git 2.55, Python 3.14.7. **No disponibles:** `pandoc`, `gitleaks`, `weasyprint`, `wkhtmltopdf`. |
| ADR vigente | `docs/adr/` | **Ninguno encontrado.** El repositorio no existe todavía; no hay decisiones de arquitectura previas que respetar. |

Decisiones ya tomadas por Joseph durante el diseño, que este spec trata como
restricciones y no como opciones abiertas:

| # | Decisión | Consecuencia |
|---|---|---|
| D-01 | **Sin código de aplicación.** El repositorio contiene datos, plantillas y convenciones; la generación la ejecuta un agente de IA leyendo esos archivos. | No hay CLI, no hay dependencias que instalar, no hay pruebas unitarias de aplicación. El contrato operativo (`AGENTS.md`) cumple el papel del programa. |
| D-02 | **El origen del CV es Markdown**, y de él se derivan `.docx` y `.pdf`. | El documento enviado es binario, pero su fuente es texto diffeable y versionado. |
| D-03 | **Repositorio público.** Todo lo generado y todo dato sensible vive en `privado/`, excluido de Git. Las variables personales se cargan desde `.secrets`. | `profile/` (experiencia, habilidades) es público; contacto, documentos, ofertas, postulaciones y feedback no lo son. |
| D-04 | **Experiencia almacenada como biblioteca de viñetas etiquetadas**, no como párrafos fijos. | La adaptación por oferta es una selección y reordenación determinista, no una reescritura. |
| D-05 | **Bilingüe desde el inicio:** cada viñeta lleva campos `es` y `en`. | Un solo origen produce hoja de vida en español o en inglés. |
| D-06 | **El contrato para agentes se llama `AGENTS.md`**, no `CLAUDE.md`. | Estándar abierto, válido para cualquier agente. |
| D-07 | **Dos ramas protegidas:** `main` y `develop`. Todo cambio entra por `develop` mediante Pull Request. | Ningún push directo, ningún force-push, checks obligatorios en verde. |
| D-08 | **Los repositorios de trabajo se leen en local**, nunca se suben ni se clonan a un remoto ajeno. | De ellos solo salen hechos derivados y genéricos. |
| D-09 | **`setup.md` no se publica**; vive en `privado/`. | Las instrucciones de configuración de GitHub quedan fuera del repositorio público. |
| D-10 | **Prohibida la co-autoría de IA en los commits.** | Ningún mensaje de commit ni descripción de PR lleva líneas de atribución a un agente. |
| D-11 | **Solo los repositorios públicos pueden presentarse como obra propia.** Los internos sustentan experiencia, nunca autoría ni propiedad. | Las viñetas derivadas de fuentes internas se atribuyen al puesto en el ISTPET, sin nombrar el repositorio ni enlazarlo. Los tres repositorios públicos sí se enlazan como prueba verificable. |

## Alcance

**Incluye:**

- Estructura del repositorio y su documentación de uso (`README.md`).
- Contrato operativo para agentes (`AGENTS.md`): reglas de selección de
  viñetas, cálculo de coincidencia, reglas ATS inviolables, reglas de
  sanitización y reglas de higiene de commits.
- Modelo de datos del perfil en YAML: identidad, experiencia, proyectos,
  habilidades, educación, certificaciones, idiomas y fuentes de evidencia.
- Carga inicial de datos a partir de `CV_JosephBano.docx`.
- Plantillas de hoja de vida optimizadas para ATS y de carta de presentación.
- Mecanismo de variables personales (`.secrets` + `.secrets.example`).
- Tres capas de defensa contra fuga de datos: `.gitignore`, hook local
  `pre-commit` y flujo de GitHub Actions bloqueante en cada PR.
- Configuración de ramas `main` y `develop` con protección.
- Proceso de auditoría de repositorios locales para derivar viñetas y
  habilidades, con regla de sanitización.
- Registro de postulaciones y su ciclo de estados.
- Informe de analítica derivado de ese registro.

**Excluye:**

- Cualquier código de aplicación ejecutable: CLI, servicio web, interfaz
  gráfica (deriva de D-01).
- Envío automático de postulaciones a portales de empleo.
- Raspado o descarga automatizada de ofertas desde sitios de terceros. La
  oferta la aporta Joseph como texto o enlace.
- Publicación de un portafolio web, hoja de vida con diseño gráfico
  elaborado, o perfil de GitHub. Son extensiones posteriores.
- Sincronización con LinkedIn en cualquier dirección.
- Migración del contenido de los doce repositorios de trabajo. Solo se leen.

**Límites del proceso:**

El ciclo empieza cuando Joseph aporta una oferta de empleo y termina cuando
el resultado de esa postulación queda registrado en `privado/aplicaciones.yml`.
El envío del documento al portal de la empresa es manual y queda fuera del
sistema. No hay integración con sistemas externos en esta versión.

## Requisitos verificables

### Datos y estructura

| ID único | Condición y comportamiento observable | Prioridad de la fuente | Fuente |
|---|---|---|---|
| RF-DATOS-001 | Dado el repositorio inicializado, cuando se inspecciona `profile/`, existen y validan como YAML los archivos `identity.yml`, `experience.yml`, `projects.yml`, `skills.yml`, `education.yml`, `certifications.yml`, `languages.yml` y `sources.yml`. | Alta | D-01, D-03 |
| RF-DATOS-002 | Dado `CV_JosephBano.docx`, cuando se completa la carga inicial, cada dato del documento (perfil, puesto, cuatro proyectos, educación, seis certificados, stack, dos idiomas) aparece exactamente una vez en `profile/`, sin duplicados entre archivos. | Alta | `CV_JosephBano.docx` |
| RF-DATOS-003 | Dada cualquier viñeta de `experience.yml` o `projects.yml`, tiene `id` único en todo el repositorio, lista `tags` no vacía, `weight` entero de 1 a 5, y textos en `es` y `en`. | Alta | D-04, D-05 |
| RF-DATOS-004 | Dada cualquier habilidad de `skills.yml`, tiene `name`, `level` de un vocabulario cerrado (`basico`, `intermedio`, `avanzado`) y una lista `aliases` que puede estar vacía. | Alta | D-04 |
| RF-DATOS-005 | Dado `profile/identity.yml`, ningún dato de contacto aparece literal: teléfono, correo, dirección y ciudad se expresan como referencias `{{secrets.<clave>}}`. | Alta | D-03 |
| RF-DATOS-006 | Dado `.secrets.example`, contiene toda clave referenciada desde `profile/`, con valores de ejemplo ficticios y ningún dato real de Joseph. | Alta | D-03 |

### Generación de documentos

| ID único | Condición y comportamiento observable | Prioridad de la fuente | Fuente |
|---|---|---|---|
| RF-GEN-001 | Dada una oferta aportada por Joseph, cuando se ejecuta la generación, se crea el directorio `privado/generados/<AAAA-MM-DD>-<empresa>-<rol>/` con `oferta.yml`, `match.md`, `cv.md`, `cv.docx` y `cv.pdf`. | Alta | D-02, D-03 |
| RF-GEN-002 | Dado un `cv.md` generado, todo marcador `{{secrets.<clave>}}` fue sustituido por su valor de `.secrets`; no queda ningún marcador sin resolver. | Alta | D-03 |
| RF-GEN-003 | Dado un `cv.docx` generado, cumple las reglas ATS declaradas en `templates/STYLE.md`: una sola columna, sin tablas, sin cuadros de texto, sin imágenes, sin encabezado ni pie de página, fuente estándar, y encabezados de sección con nombres convencionales. | Alta | Reglas ATS, `docs/ats-rules.md` |
| RF-GEN-004 | Dado un `cv.pdf` generado, su texto es extraíble como texto real; no es una imagen rasterizada. | Alta | Reglas ATS |
| RF-GEN-005 | Dado el parámetro de idioma `es` o `en`, el documento generado usa exclusivamente el campo de ese idioma en todas las viñetas, encabezados de sección y nombre del puesto. | Alta | D-05 |
| RF-GEN-006 | Dada una oferta, `match.md` declara un porcentaje de coincidencia entero de 0 a 100, la lista de palabras clave de la oferta halladas en `profile/`, y la lista de las no halladas. | Alta | D-04 |
| RF-GEN-007 | Dadas dos generaciones consecutivas con la misma oferta, el mismo `profile/` y el mismo idioma, los `cv.md` resultantes son idénticos byte a byte. | Alta | D-01, D-04 |
| RF-GEN-008 | Dada una selección de viñetas, el documento resultante no contiene ninguna afirmación que no derive de un campo de `profile/`. | Alta | D-01 |

### Seguridad y control de cambios

| ID único | Condición y comportamiento observable | Prioridad de la fuente | Fuente |
|---|---|---|---|
| RF-SEG-001 | Dado `.gitignore`, `git status` no lista como no rastreado ningún archivo bajo `privado/` ni `.secrets`. | Alta | D-03 |
| RF-SEG-002 | Dado un intento de `git commit` con cualquier ruta bajo `privado/` o con `.secrets` en el índice, el hook `pre-commit` aborta con código distinto de cero y un mensaje que nombra la ruta ofensora. | Alta | D-03 |
| RF-SEG-003 | Dado un intento de `git commit` cuyo contenido añadido contiene el teléfono, el correo o la dirección de Joseph, el hook `pre-commit` aborta con código distinto de cero. | Alta | D-03 |
| RF-SEG-004 | Dado un Pull Request hacia `develop` o `main` que modifica rutas bajo `privado/` o `.secrets`, el flujo `secret-guard` falla y el PR no es mezclable. | Alta | D-03, D-07 |
| RF-SEG-005 | Dado un Pull Request que introduce un secreto detectable (token, clave privada, cadena de conexión) o datos personales en cualquier ruta, el flujo `secret-guard` falla. | Alta | D-03 |
| RF-SEG-006 | Dado el repositorio publicado, `main` y `develop` rechazan push directo y force-push, y exigen Pull Request con el check `secret-guard` en verde. | Alta | D-07 |
| RF-SEG-007 | Dado cualquier commit creado por un agente en este repositorio, su mensaje no contiene líneas de atribución o co-autoría a un agente de IA. | Alta | D-10 |
| RF-SEG-008 | Dado el historial completo del repositorio en el momento de publicarlo, no contiene ningún dato de contacto de Joseph ni ningún archivo de `privado/`. | Alta | D-03 |

### Evidencia desde repositorios de trabajo

| ID único | Condición y comportamiento observable | Prioridad de la fuente | Fuente |
|---|---|---|---|
| RF-EVID-001 | Dado `profile/sources.yml`, cada fuente declara `id`, `ruta_local`, `confidencialidad` de un vocabulario cerrado (`publico`, `interno`, `confidencial`) y `permite_extraer`. | Alta | D-08 |
| RF-EVID-002 | Dada una fuente con confidencialidad `interno` o `confidencial`, ningún artefacto público del repositorio contiene fragmentos de su código, nombres de sus tablas, rutas de sus endpoints, nombres de clientes ni capturas de pantalla. | Alta | D-08 |
| RF-EVID-003 | Dada una auditoría de una fuente, produce un informe con lenguajes y marcos detectados, patrones de arquitectura, escala observable y participación de Joseph en el historial, y **propone** viñetas y habilidades sin escribirlas en `profile/`. | Alta | D-08 |
| RF-EVID-004 | Ninguna viñeta o habilidad entra en `profile/` sin aprobación explícita de Joseph sobre la propuesta concreta. | Alta | D-08 |
| RF-EVID-005 | Dada una viñeta con campo `evidence`, cada valor de esa lista corresponde a un `id` existente en `sources.yml`. | Media | D-08 |
| RF-EVID-006 | Dada una fuente de confidencialidad `interno`, ningún documento generado la nombra, la enlaza ni la presenta como obra propia de Joseph; sus viñetas se atribuyen al puesto desempeñado, no a un proyecto personal. Solo las fuentes `publico` pueden enlazarse y presentarse como obra propia. | Alta | D-11 |

### Seguimiento y analítica

| ID único | Condición y comportamiento observable | Prioridad de la fuente | Fuente |
|---|---|---|---|
| RF-TRACK-001 | Dada una postulación registrada en `privado/aplicaciones.yml`, tiene `id` coincidente con el nombre de su directorio en `privado/generados/`, y campos `empresa`, `rol`, `fuente`, `url`, `cv`, `match_score`, `plantilla`, `idioma`, `estado` y `timeline`. | Alta | D-03 |
| RF-TRACK-002 | Dado el campo `estado`, su valor pertenece al vocabulario cerrado: `borrador`, `postulado`, `screening`, `tecnica`, `final`, `oferta`, `aceptada`, `rechazada`, `sin_respuesta`, `retirada`. | Alta | D-03 |
| RF-TRACK-003 | Dado un cambio de estado, se añade una entrada al `timeline` con fecha y evento; las entradas anteriores no se modifican ni se eliminan. | Alta | D-03 |
| RF-ANL-001 | Dado `privado/aplicaciones.yml` con al menos una postulación, el informe `privado/analitica.md` presenta el embudo por estado con tasa de conversión entre etapas consecutivas. | Media | D-03 |
| RF-ANL-002 | Dado el mismo registro, el informe presenta tasa de respuesta desglosada por `fuente`, por `idioma`, por `plantilla` y por rango de `match_score`. | Media | D-03 |
| RF-ANL-003 | Dado el mismo registro, el informe lista las palabras clave que aparecen en ofertas registradas y no existen en `profile/skills.yml`, ordenadas por frecuencia. | Media | D-04 |
| RF-ANL-004 | Dado un informe generado, cada cifra declara sobre cuántas postulaciones se calcula; ninguna tasa se presenta sin su denominador. | Media | Precisión estadística |

## Escenarios del proceso

### Escenario 1 — Generar una hoja de vida para una oferta concreta

- **Actor y precondición:** Joseph, con el repositorio clonado, `.secrets`
  completo y `profile/` cargado.
- **Disparador:** Joseph aporta el texto o el enlace de una oferta de empleo
  y el idioma deseado.
- **Secuencia:**
  1. El agente normaliza la oferta a `oferta.yml`: empresa, rol, seniority,
     modalidad, ubicación, salario publicado si existe, requisitos obligatorios,
     requisitos deseables y palabras clave extraídas literalmente del texto.
  2. El agente cruza las palabras clave con `profile/skills.yml` usando `name`
     y `aliases`, y escribe `match.md` con el porcentaje, las coincidencias y
     los huecos.
  3. El agente selecciona las viñetas cuyos `tags` intersectan las palabras
     clave, las ordena por relevancia frente a la oferta y, a igualdad, por
     `weight` descendente.
  4. El agente compone `cv.md` aplicando `templates/ats-standard.md`, sustituye
     los marcadores `{{secrets.*}}` y emplea la variante de alias que coincide
     literalmente con el texto de la oferta.
  5. El agente deriva `cv.docx` y `cv.pdf`.
  6. El agente registra la postulación en `privado/aplicaciones.yml` con
     estado `borrador`.
- **Resultado:** el directorio `privado/generados/<id>/` completo y una
  entrada nueva en el registro. Nada de esto queda bajo control de Git.
- **Variantes y errores:**
  - Si el porcentaje de coincidencia es bajo, el agente lo informa junto con
    los huecos concretos y pregunta si se continúa. No inventa experiencia
    para cerrar el hueco (RF-GEN-008).
  - Si falta `.secrets` o una clave referenciada, la generación se detiene y
    nombra la clave faltante; no se emite un documento con marcadores.
  - Si la oferta no aporta empresa o rol reconocibles, se solicita a Joseph
    antes de crear el directorio.

### Escenario 2 — Auditar un repositorio de trabajo y actualizar el perfil

- **Actor y precondición:** Joseph, con el repositorio de trabajo clonado en
  local y declarado en `profile/sources.yml`.
- **Disparador:** Joseph indica qué fuente auditar.
- **Secuencia:**
  1. El agente lee la fuente en su ruta local: manifiestos de dependencias,
     estructura de directorios, migraciones, configuración de despliegue y el
     historial de commits atribuibles a Joseph.
  2. El agente redacta un informe de hallazgos con escala observable y rol
     desempeñado, y propone viñetas y habilidades nuevas o corregidas.
  3. Joseph aprueba, rechaza o corrige cada propuesta una por una.
  4. Solo lo aprobado se escribe en `profile/`, en una rama de trabajo, y
     entra por Pull Request a `develop`.
  5. La trazabilidad viñeta → fuente queda en `privado/evidencia/`.
- **Resultado:** `profile/` refleja la capacidad real y verificable de Joseph,
  y cada afirmación puede sustentarse en una entrevista.
- **Variantes y errores:**
  - Si la fuente es `interno` o `confidencial`, el informe solo enuncia hechos
    derivados y genéricos (RF-EVID-002). Ante la duda sobre si un dato es
    propietario, el agente lo omite y lo señala como pregunta a Joseph.
  - Si la ruta local declarada no existe, la auditoría se detiene sin escribir
    nada.
  - Si una propuesta contradice una viñeta existente, se presenta la
    contradicción; no se sobrescribe en silencio.

### Escenario 3 — Un intento de publicar datos sensibles es bloqueado

- **Actor y precondición:** Joseph o un agente, con cambios en el árbol de
  trabajo.
- **Disparador:** un `git commit` o un Pull Request que incluye un archivo de
  `privado/`, el archivo `.secrets`, o datos personales o credenciales en
  cualquier ruta.
- **Secuencia:**
  1. El hook `pre-commit` inspecciona el índice y el contenido añadido.
  2. Si halla una infracción, aborta con código distinto de cero e informa la
     ruta y el motivo. El commit no llega a existir.
  3. Si el commit igualmente alcanza el remoto —hook desinstalado u omitido
     con `--no-verify`—, el flujo `secret-guard` del Pull Request ejecuta las
     mismas comprobaciones más la exploración del historial.
  4. Un fallo del check impide la mezcla, porque `develop` y `main` lo exigen
     en verde.
- **Resultado:** ningún dato sensible alcanza el repositorio público, y el
  motivo del bloqueo queda escrito.
- **Variantes y errores:**
  - Un falso positivo se resuelve ajustando el patrón de detección mediante
    Pull Request, nunca desactivando el check.
  - El hook local se instala con `git config core.hooksPath .githooks`; el
    `README.md` lo indica como primer paso y `secret-guard` no depende de él.

### Escenario 4 — Registrar el resultado y leer la analítica

- **Actor y precondición:** Joseph, con postulaciones ya registradas.
- **Disparador:** llega una respuesta de una empresa, o Joseph pide el informe.
- **Secuencia:**
  1. Joseph informa el hecho: invitación a entrevista, rechazo con o sin
     motivo, oferta, o silencio pasado el umbral acordado.
  2. El agente actualiza `estado`, añade la entrada al `timeline` y registra
     el `feedback` textual y el `motivo_rechazo` cuando existan.
  3. A petición, el agente regenera `privado/analitica.md`.
- **Resultado:** el informe describe el embudo, las tasas por segmento con su
  denominador, los motivos de rechazo agrupados y las palabras clave del
  mercado ausentes del perfil.
- **Variantes y errores:**
  - Con menos de diez postulaciones, el informe advierte que las tasas no son
    concluyentes y muestra solo conteos absolutos.
  - Una postulación sin respuesta pasa a `sin_respuesta` únicamente al superar
    el umbral de días definido en PD-01.

## Datos, seguridad e integraciones

**Datos capturados y su ubicación.** El repositorio separa tres clases:

| Clase | Ubicación | Bajo control de Git | Contenido |
|---|---|---|---|
| Perfil profesional | `profile/` | Sí, público | Experiencia, proyectos, habilidades, educación, certificaciones, idiomas, alias ATS. Información equivalente a la ya publicada en LinkedIn. |
| Plantillas y reglas | `templates/`, `docs/`, `AGENTS.md`, `README.md` | Sí, público | Ningún dato personal. |
| Datos sensibles y derivados | `privado/` y `.secrets` | No | Contacto, documentos escaneados, ofertas, documentos generados, registro de postulaciones, feedback, notas de entrevista, evidencia, `setup.md`. |

**Quién puede verlos.** El contenido público es legible por cualquiera, y eso
es intencional: es material de portafolio. El contenido de `privado/` no sale
del equipo de Joseph por ningún mecanismo del sistema.

**Cuándo se persisten.** El punto de confirmación es la escritura en disco de
cada archivo; no hay base de datos ni transacciones. La escritura en `profile/`
solo ocurre tras aprobación explícita de Joseph (RF-EVID-004). La escritura en
`privado/` ocurre durante la generación y el registro, sin aprobación previa,
porque nunca abandona el equipo.

**Cómo se auditan.** El historial de Git audita `profile/` y las plantillas.
`privado/evidencia/` audita el origen de cada afirmación del perfil. El
`timeline` de cada postulación es de solo anexión (RF-TRACK-003).

**Datos de terceros.** Los doce repositorios de `istpet-dev` pertenecen a la
institución empleadora. La regla de sanitización (RF-EVID-002) es la frontera:
salen capacidades demostradas, no propiedad intelectual. Los ejemplos que se
incluyan en documentación pública usarán valores ficticios.

**Integraciones.** Ninguna en esta versión. GitHub actúa como alojamiento y
motor de las comprobaciones, no como integración de datos. Se declara como
punto abierto (PD-02) el mecanismo exacto de derivación `.md` → `.docx` → `.pdf`,
porque `pandoc` no está instalado en el equipo.

## Criterios de aceptación

- [ ] El repositorio está inicializado con ramas `main` y `develop`, ambas
      protegidas conforme a RF-SEG-006, y el primer contenido entró por Pull
      Request.
- [ ] `profile/` contiene la totalidad de los datos de `CV_JosephBano.docx`,
      sin pérdidas ni duplicados, validado contra el texto extraído
      (RF-DATOS-002).
- [ ] Ninguna referencia de contacto aparece literal en el árbol público, y
      `.secrets.example` cubre toda clave referenciada (RF-DATOS-005,
      RF-DATOS-006).
- [ ] Una generación de prueba con una oferta ficticia produce los cinco
      artefactos del Escenario 1, y el `.docx` resultante cumple las reglas de
      `templates/STYLE.md` (RF-GEN-001, RF-GEN-003).
- [ ] Repetir esa generación produce un `cv.md` idéntico (RF-GEN-007).
- [ ] Un commit de prueba que incluye `.secrets` es abortado por el hook
      (RF-SEG-002), y un Pull Request de prueba equivalente es rechazado por
      `secret-guard` (RF-SEG-004).
- [ ] El historial completo, revisado antes de publicar, no contiene datos de
      contacto ni archivos de `privado/` (RF-SEG-008).
- [ ] Ningún commit del repositorio contiene atribución de co-autoría a un
      agente (RF-SEG-007).
- [ ] Una auditoría de prueba sobre un repositorio `interno` produce
      propuestas que Joseph aprueba una a una, y el informe no contiene código,
      nombres de tablas ni endpoints (RF-EVID-002, RF-EVID-004).
- [ ] Un documento generado a partir de viñetas con `evidence` de fuentes internas no nombra ni enlaza ningún repositorio institucional, y atribuye esos logros al puesto (RF-EVID-006).
- [ ] `privado/analitica.md` se genera a partir de al menos una postulación
      registrada y declara el denominador de cada cifra (RF-ANL-004).

## Puntos que requieren decisión

| ID | Contradicción o dato faltante | Impacto | Quién decide | Estado y decisión |
|---|---|---|---|---|
| PD-01 | No estaba definido cuántos días sin respuesta hacen que una postulación pase a `sin_respuesta`. | RF-TRACK-002 y el embudo de RF-ANL-001 no pueden calcularse de forma consistente. | Joseph | **Resuelto 2026-09-17: 21 días** desde la fecha del último evento del `timeline`. |
| PD-02 | `pandoc` no está instalado y sí lo están LibreOffice 26.8 y Python 3.14.7. La ruta `.md` → `.docx` → `.pdf` no estaba decidida. | RF-GEN-001, RF-GEN-003 y RF-GEN-004 no pueden implementarse ni probarse. Afecta la fidelidad ATS del resultado. | Joseph, con ADR en `docs/adr/` | **Resuelto 2026-09-17: `.docx` construido con biblioteca de Python, `.pdf` derivado con LibreOffice en modo headless.** Sin instalaciones nuevas. Requiere ADR-001, que el plan identifica y una tarea redacta antes de implementar la generación. |
| PD-03 | De los doce repositorios locales hallados no se sabía cuáles son de Joseph, cuáles corresponden a los cuatro proyectos ya declarados, y qué confidencialidad tiene cada uno. | `profile/sources.yml` no puede poblarse y el Escenario 2 no puede ejecutarse. | Joseph | **Resuelto 2026-09-17.** Ver la tabla «Fuentes de evidencia clasificadas» más abajo. |
| PD-04 | El estado de la carrera en la Universidad Politécnica Salesiana no constaba. | `education.yml` quedaría incompleto, y el dato es material para filtros ATS que exigen título. | Joseph | **Resuelto 2026-09-17: estudios cursados sin titulación, actualmente en pausa.** Se declara como estudios cursados, sin afirmar título ni fecha de graduación. |
| PD-05 | No estaba decidido si el repositorio se publica desde el primer commit. | Determina cuándo empieza a correr el riesgo de RF-SEG-008. | Joseph | **Resuelto 2026-09-17: nace privado.** Se publica solo tras completar la carga inicial y revisar el historial completo contra RF-SEG-008. |
| PD-06 | `gitleaks` no está instalado en local y sí existe como acción oficial en GitHub Actions. | RF-SEG-003 y RF-SEG-005 podrían aplicar criterios distintos en local y en CI. | Joseph | **Abierto.** El plan debe proponer un mecanismo que garantice un único criterio en ambos lados sin exigir instalaciones. |
| PD-07 | No está definido el vocabulario canónico de `tags`. | RF-GEN-006 produciría porcentajes de coincidencia erráticos. | Joseph, decidible durante el plan | **Abierto.** Se resuelve en `plan.md` y se versiona como archivo del repositorio. |
| PD-08 | `biometric_sistem_reports` está hoy bajo la cuenta personal de Joseph, pero su propiedad debe cederse al ISTPET. | Si se enlaza como prueba pública y luego cambia de dueño, el enlace del CV se rompe o apunta a un repositorio institucional. | Joseph | **Resuelto 2026-09-17: se clasifica como `interno` desde ahora**, pese a su ubicación actual. No se enlaza desde ningún documento. |
| PD-09 | No estaba delimitado hasta dónde puede atribuirse a Joseph el trabajo de las fuentes internas. | RF-EVID-002 no distinguía entre «no revelar el material» y «no reclamar la autoría», que son cosas distintas. | Joseph | **Resuelto 2026-09-17: los internos sustentan experiencia, no autoría.** Ver D-11 y RF-EVID-006. |

### Fuentes de evidencia clasificadas

Resultado de PD-03 y PD-08. Verificado el 2026-09-17 contando commits cuyo
autor es el correo personal de Joseph o su alias `noreply` de GitHub;
esas cinco identidades de Git corresponden a la misma persona.

| Fuente | Confidencialidad | Commits de Joseph | Justificación |
|---|---|---|---|
| `fake_reports` | `publico` | 14 / 28 | Remoto en la cuenta personal, sin datos institucionales. Enlazable. |
| `leccionario_inspeccion` | `publico` | 88 / 88 | Remoto en la cuenta personal. Autoría exclusiva. Enlazable. |
| `titulacion_istpet` | `publico` | 21 / 47 | Remoto en la cuenta personal. Enlazable. |
| `biometric_sistem_reports` | `interno` | 156 / 158 | Propiedad pendiente de ceder al ISTPET (PD-08). No se enlaza. |
| `generador-docs-istpet` | `interno` | 20 / 20 | Sin remoto declarado; interno por precaución. |
| `gestion_mecanica_ISTPET` | `interno` | 46 / 57 | Organización institucional `ItspetDev`. |
| `gestion_administrativa_istpet` | `interno` | 56 / 90 | Organización institucional `ItspetDev`. |
| `gestion_academica_istpet` | `interno` | 167 / 291 | Organización institucional `ItspetDev`. |
| `Bienestar_Institucional` | `interno` | 224 / 398 | Organización institucional `ItspetDev`. |
| `Istpet_Vehiculos` | `interno` | 63 / 321 | Organización institucional `ItspetDev`. |
| `Mi_ISTPET` | Excluida | 1 / 306 | Participación marginal; no sustenta ninguna afirmación. |
| `gestion_recursos_humanos_istpet` | Excluida | 1 / 223 | Participación marginal; no sustenta ninguna afirmación. |

Las fuentes `publico` son las únicas enlazables y presentables como obra
propia (D-11, RF-EVID-006). Las `interno` sustentan viñetas atribuidas al
puesto en el ISTPET, sin nombrar ni enlazar el repositorio.

Cinco de estas fuentes con participación mayoritaria de Joseph no aparecen en
`CV_JosephBano.docx`: `leccionario_inspeccion`, `generador-docs-istpet`,
`Bienestar_Institucional`, `gestion_administrativa_istpet` y
`titulacion_istpet`. Es la evidencia directa del problema que este spec
resuelve.

## Revisión funcional

**Versión revisada:** 0.1
**Decisión:** Aprobado
**Aprobó:** Joseph Andrés Baño Naranjo, responsable funcional
**Fecha y evidencia de aprobación:** 2026-09-17 — aprobación explícita en la sesión de diseño: «ya leí y me parece correcto».
**Ajustes solicitados:** Ninguno.

Tras la aprobación se registraron las decisiones de PD-01 a PD-05 y PD-08 el
mismo 2026-09-17, sin cambio de alcance ni de requisitos. Se registró además PD-09 el mismo día, que
añade D-11 y RF-EVID-006 acotando la atribución de las fuentes internas; es
una restricción adicional, no una ampliación de alcance. PD-06 y PD-07 siguen
abiertos y se resuelven en `plan.md`; las tareas que dependan de ellos quedan
bloqueadas en `tasks.md` hasta que la decisión esté registrada.

Solo una aprobación explícita de esta versión habilita la creación de
`plan.md`, `tasks.md` y `test-e2e.md`.
