# Especificación de esquemas de datos — portfolio-joe

Este documento fija la estructura, tipos de datos y vocabularios cerrados para todos los archivos YAML del repositorio (`profile/*.yml`), los artefactos de generación (`oferta.yml`) y el registro de postulaciones (`privado/aplicaciones.yml`).

Cualquier cambio a estos esquemas debe realizarse en un Pull Request dedicado antes de actualizar los archivos correspondientes.

---

## 1. Archivos de Perfil (`profile/*.yml`)

### 1.1 `profile/identity.yml`
Define la identidad profesional pública y referencias a datos privados de contacto.
- **`name`** *(string, obligatorio)*: Nombre completo de Joseph.
- **`titles`** *(map, obligatorio)*: Títulos profesionales según el enfoque del perfil:
  - `fullstack` *(string)*
  - `backend` *(string)*
  - `devops` *(string)*
- **`links`** *(list of objects, obligatorio)*:
  - `name` *(string)*: "GitHub", "LinkedIn", etc.
  - `url` *(string, URL válida)*
- **`contact`** *(map, obligatorio)*: **REGLA RF-DATOS-005: Ningún dato literal.** Todos los campos deben ser cadenas con el formato exacto `{{secrets.<clave>}}`:
  - `telefono`: `"{{secrets.telefono}}"`
  - `email`: `"{{secrets.email}}"`
  - `ciudad`: `"{{secrets.ciudad}}"`
  - `pais`: `"{{secrets.pais}}"`
  - `direccion`: `"{{secrets.direccion}}"`
- **`summary`** *(map, obligatorio)*: Resumen profesional bilingüe:
  - `es` *(string)*
  - `en` *(string)*

### 1.2 `profile/experience.yml`
Biblioteca de puestos desempeñados y viñetas atómicas de logros y responsabilidades.
- **Lista de puestos:**
  - `company` *(string, obligatorio)*
  - `role` *(map bilingüe: `es`, `en`, obligatorio)*
  - `start_date` *(string AAAA-MM, obligatorio)*
  - `end_date` *(string AAAA-MM o "present", obligatorio)*
  - `location` *(map bilingüe: `es`, `en`, obligatorio)*
  - `bullets` *(list of objects, obligatorio)*:
    - `id` *(string, único globalmente en el repositorio)*: Formato `exp-<empresa>-<num3>` (ej. `exp-istpet-001`).
    - `tags` *(list of strings, no vacía)*: Cada etiqueta DEBE existir en `profile/taxonomy.yml`.
    - `weight` *(integer de 1 a 5, obligatorio)*: Importancia relativa de la viñeta.
    - `es` *(string, obligatorio)*: Texto en español.
    - `en` *(string, obligatorio)*: Texto en inglés.
    - `evidence` *(list of strings, obligatorio)*: Cada valor DEBE existir como `id` en `profile/sources.yml`.

### 1.3 `profile/projects.yml`
Proyectos destacados y sus viñetas asociadas.
- **Lista de proyectos:**
  - `id` *(string, identificador del proyecto, ej. `siba`)*
  - `name` *(string, nombre comercial o del sistema)*
  - `description` *(map bilingüe: `es`, `en`, obligatorio)*
  - `url` *(string o null)*: Enlace público verificable (solo si la fuente es `publico`).
  - `bullets` *(list of objects, obligatorio)*:
    - `id` *(string, único globalmente)*: Formato `proj-<proyecto>-<num3>` (ej. `proj-siba-001`).
    - `tags` *(list of strings, no vacía)*: Cada etiqueta DEBE existir en `profile/taxonomy.yml`.
    - `weight` *(integer de 1 a 5, obligatorio)*
    - `es` *(string, obligatorio)*
    - `en` *(string, obligatorio)*
    - `evidence` *(list of strings, obligatorio)*: Cada valor DEBE existir como `id` en `profile/sources.yml`.

### 1.4 `profile/skills.yml`
Habilidades técnicas organizadas con su nivel y alias ATS.
- **Lista de habilidades:**
  - `name` *(string, obligatorio)*: Nombre de la habilidad (debe coincidir con clave canónica en `taxonomy.yml`).
  - `category` *(string, obligatorio)*: `backend`, `frontend`, `database`, `devops`, `security`, `architecture`, `methodology`, `data`, `tools`, `networking`.
  - `level` *(string, vocabulario cerrado)*:
    - `basico`
    - `intermedio`
    - `avanzado`
  - `aliases` *(list of strings, puede estar vacía)*: Variantes textuales de la habilidad.

### 1.5 `profile/education.yml`
Estudios cursados y formación académica.
- **Lista de instituciones:**
  - `institution` *(string, obligatorio)*
  - `degree` *(map bilingüe: `es`, `en`, obligatorio)*
  - `status` *(string, vocabulario cerrado)*:
    - `graduado`
    - `cursado_sin_titulacion` *(PD-04: estudios cursados sin titulación, en pausa)*
    - `en_curso`
  - `start_year` *(integer o string)*
  - `end_year` *(integer, string o null)*

### 1.6 `profile/certifications.yml`
Certificados obtenidos con trazabilidad a sus documentos fuente.
- **Lista de certificaciones:**
  - `id` *(string, único)*: Formato `cert-<emisor>-<nombre>`
  - `title` *(string, obligatorio)*
  - `issuer` *(string, obligatorio)*: Ej. "Cisco Networking Academy", "Udemy"
  - `year` *(integer, obligatorio)*
  - `pdf_path` *(string, obligatorio)*: Ruta esperada en `privado/documentos/`
  - `tags` *(list of strings)*: Etiquetas canónicas de `profile/taxonomy.yml`

### 1.7 `profile/languages.yml`
Idiomas y nivel de dominio.
- **Lista de idiomas:**
  - `language` *(map bilingüe: `es`, `en`, obligatorio)*
  - `level` *(map bilingüe: `es`, `en`, obligatorio)*

### 1.8 `profile/sources.yml`
Registro clasificado de fuentes de evidencia locales (PD-03, PD-08, RF-EVID-001).
- **Lista de fuentes:**
  - `id` *(string, obligatorio)*: Identificador del repositorio local o documento.
  - `ruta_local` *(string, obligatorio)*: Ruta absoluta local en el equipo.
  - `confidencialidad` *(string, vocabulario cerrado obligatorio)*:
    - `publico`
    - `interno`
    - `confidencial`
  - `permite_extraer` *(boolean, obligatorio)*
  - `enlazable` *(boolean, obligatorio)*: `true` ÚNICAMENTE si `confidencialidad` es `publico`; `false` en caso contrario (RF-EVID-006).
  - `descripcion` *(string)*

---

## 2. Artefacto de Oferta (`oferta.yml`)

Generado en `privado/generados/<id>/oferta.yml` durante el Escenario 1.
- **`empresa`** *(string, obligatorio)*
- **`rol`** *(string, obligatorio)*
- **`seniority`** *(string)*: "Junior", "Mid", "Senior", "Lead"
- **`modalidad`** *(string)*: "Remoto", "Hibrido", "Presencial"
- **`ubicacion`** *(string)*
- **`salario_publicado`** *(string o null)*
- **`requisitos_obligatorios`** *(list of strings)*
- **`requisitos_deseables`** *(list of strings)*
- **`keywords`** *(list of strings, obligatorio)*: Palabras clave extraídas literalmente del texto de la oferta.

---

## 3. Registro de Postulaciones (`privado/aplicaciones.yml`)

Registro cronológico y evolutivo de postulaciones (RF-TRACK-001, RF-TRACK-002, RF-TRACK-003).
- **Lista de aplicaciones (`aplicaciones`):**
  - `id` *(string, obligatorio)*: Coincide exactamente con el nombre de directorio `<AAAA-MM-DD>-<empresa>-<rol>`.
  - `empresa` *(string, obligatorio)*
  - `rol` *(string, obligatorio)*
  - `fuente` *(string, obligatorio)*: "LinkedIn", "Indeed", "Portal directo", etc.
  - `url` *(string)*: Enlace de la vacante.
  - `cv` *(string, obligatorio)*: Ruta relativa al PDF generado.
  - `match_score` *(integer de 0 a 100, obligatorio)*
  - `plantilla` *(string, vocabulario cerrado)*: `ats-standard`, `ats-compact`
  - `idioma` *(string, vocabulario cerrado)*: `es`, `en`
  - `estado` *(string, vocabulario cerrado obligatorio)*:
    1. `borrador`: CV generado, aún no enviado.
    2. `postulado`: Documento enviado a la vacante.
    3. `screening`: Contacto inicial con reclutador / RRHH.
    4. `tecnica`: En proceso de pruebas técnicas o entrevista técnica.
    5. `final`: Entrevista final con directivos o cliente.
    6. `oferta`: Oferta económica formal recibida.
    7. `aceptada`: Oferta aceptada por Joseph.
    8. `rechazada`: Postulación descartada por la empresa.
    9. `sin_respuesta`: Sin novedad tras 21 días del último evento (PD-01).
    10. `retirada`: Joseph retira su candidatura voluntariamente tras haber postulado.
    11. `descartada`: Joseph evalúa la oferta y decide no postular (PD-10). Terminal; nunca pasó por `postulado`. Excluida del embudo de conversión y analizada por separado.
  - `timeline` *(list of objects, solo anexión obligatorio)*:
    - `fecha` *(string AAAA-MM-DD)*
    - `evento` *(string)*
  - `feedback` *(string, opcional)*: Retroalimentación cualitativa recibida.
  - `motivo_rechazo` *(string, opcional)*: Causa reportada del descarte.

### `oferta.yml` — campo opcional `ubicacion_declarada`

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `ubicacion_declarada` | cadena | No | Ciudad y país que se escriben en la cabecera del documento en lugar de la residencia real, cuando la oferta es presencial o híbrida en otra ciudad donde Joseph puede residir. Solo se usa si la residencia es real y verificable. Ausente = se usa `{{secrets.ciudad}}, {{secrets.pais}}`. |
