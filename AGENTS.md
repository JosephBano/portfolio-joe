# AGENTS.md — Contrato operativo para agentes de IA

Este documento rige la actuación de cualquier agente de Inteligencia Artificial que interactúe con el repositorio `portfolio-joe`. Define las reglas inviolables para la generación determinista de documentos, auditoría de evidencia local, seguimiento de postulaciones y seguridad.

---

## 1. Propósito y rol del agente

El repositorio `portfolio-joe` es la **fuente única de la verdad** sobre la trayectoria profesional de Joseph Andrés Baño Naranjo. En cumplimiento de la decisión **D-01**, el repositorio no contiene código de aplicación para la lógica de negocio; el agente de IA actúa como el motor de ejecución leyendo los datos en `profile/`, las plantillas en `templates/` y ejecutando los procedimientos estandarizados en este contrato.

---

## 2. Generación de documentos (Escenario 1)

Dado un requerimiento de Joseph con el texto o enlace de una oferta de empleo, el idioma objetivo (`es` | `en`) y la plantilla (`ats-standard` | `ats-compact`):

### Pasos obligatorios de generación:
1. **Identificar y crear directorio de salida:**
   - Formato de identificador: `<AAAA-MM-DD>-<empresa>-<rol>` en minúsculas sin espacios (ej. `2026-09-17-northwind-senior-backend`).
   - Ruta: `privado/generados/<id>/`. Si empresa o rol son irreconocibles, consultar a Joseph antes de proceder.
2. **Normalizar la vacante en `oferta.yml`:**
   - Escribir `privado/generados/<id>/oferta.yml` con: `empresa`, `rol`, `seniority`, `modalidad`, `ubicacion`, `salario_publicado`, `requisitos_obligatorios`, `requisitos_deseables` y `keywords`.
   - Las `keywords` deben extraerse literalmente del texto de la vacante.
3. **Calcular coincidencia en `match.md`:**
   - Cruzar las palabras clave con `profile/taxonomy.yml` y `profile/skills.yml`.
   - Aplicar la fórmula de coincidencia (§3) y registrar el porcentaje, las palabras clave halladas y las ausentes.
4. **Seleccionar y ordenar viñetas deterministamente:**
   - Aplicar el algoritmo determinista (§4) para seleccionar los logros más relevantes de `profile/experience.yml` y `profile/projects.yml`.
5. **Componer el documento Markdown (`cv.md`):**
   - Cargar la plantilla especificada (`templates/ats-standard.md` o `templates/ats-compact.md`).
   - Aplicar el idioma seleccionado (§5).
   - Sustituir los marcadores de variables privadas (§6).
   - Si una keyword de la oferta coincide con un alias textual de una habilidad o viñeta, utilizar la variante textual de la vacante para maximizar la concordancia ATS.
   - Escribir el archivo en `privado/generados/<id>/cv.md`.
6. **Derivar formatos binarios (`cv.docx` y `cv.pdf`):**
   - Ejecutar `python3 tools/render_docx.py privado/generados/<id>/cv.md privado/generados/<id>/cv.docx`.
   - Ejecutar `soffice --headless --convert-to pdf privado/generados/<id>/cv.docx --outdir privado/generados/<id>/`.
   - Si LibreOffice falla o no está disponible, conservar el `.docx`, advertir explícitamente en la consola y no sustituir por métodos no autorizados.
7. **Registrar postulación preliminar:**
   - Añadir una nueva entrada en `privado/aplicaciones.yml` con estado inicial `borrador` y el evento en su `timeline`.

### Artefactos exactos producidos en `privado/generados/<id>/`:
1. `oferta.yml`
2. `match.md`
3. `cv.md`
4. `cv.docx`
5. `cv.pdf`

---

## 3. Cálculo de coincidencia (§Coincidencia, RF-GEN-006)

1. **Normalización:** Cada palabra clave extraída de la vacante se busca en `profile/taxonomy.yml` por su clave canónica o dentro de sus `aliases`.
   - Si coincide con un alias, se mapea a su etiqueta canónica.
   - Si no existe en `profile/taxonomy.yml`, se conserva la palabra clave original para el análisis de brechas.
2. **Cruce:** Se compara el conjunto de etiquetas canónicas requeridas frente a las habilidades declaradas en `profile/skills.yml` (y sus etiquetas asociadas).
3. **Fórmula matemática:**
   $$\text{match\_score} = \text{round}\left(\frac{\text{keywords\_halladas}}{\text{total\_keywords\_requeridas}} \times 100\right)$$
4. **Control de brechas:** Si el resultado es inferior al 60%, el agente debe reportar los vacíos técnicos detectados a Joseph y solicitar confirmación antes de continuar la generación. **Prohibición (RF-GEN-008):** Jamás inventar habilidades o experiencia para inflar el porcentaje.

---

## 4. Selección y ordenación determinista (§Selección, RF-GEN-007)

Para garantizar que dos generaciones consecutivas con la misma entrada produzcan archivos idénticos byte a byte (RF-GEN-007):
1. **Puntaje de relevancia por viñeta:**
   - Intersección entre los `tags` de la viñeta y las palabras clave canónicas de la vacante.
   - `relevancia = len(tags_viñeta \cap keywords_vacante)`.
2. **Criterio de ordenación estricto:**
   - 1.º Relevancia (`relevancia` descendente).
   - 2.º Peso asignado (`weight` descendente, 5 a 1).
   - 3.º Desempate lexicográfico por identificador (`id` ascendente alfabético).
3. **Cupos por sección:**
   - En plantilla `ats-standard`: seleccionar entre 4 y 6 viñetas para puestos principales, y entre 2 y 3 viñetas por proyecto relevante.
   - En plantilla `ats-compact`: seleccionar máximo 3 viñetas por puesto y 2 por proyecto.

---

## 5. Idioma unificado (§Idioma, RF-GEN-005)

- El parámetro de idioma (`es` | `en`) determina la totalidad de la composición.
- **Prohibición de mezcla:** No se permite mezclar idiomas. Si el idioma es `en`, todos los encabezados de sección ("Professional Experience", "Technical Skills", "Education", etc.), el nombre de los cargos y las viñetas deben tomarse exclusivamente del campo `en`.
- Si una viñeta carece de texto en el idioma solicitado, la generación se detiene con error reportando el ID de la viñeta incompleta.

---

## 6. Variables personales (§Variables, RF-GEN-002)

- Todos los datos de contacto y residencia residen exclusivamente en `privado/.secrets`.
- Al componer `cv.md`, el agente debe reemplazar cada marcador `{{secrets.<clave>}}` por su valor exacto cargado desde `privado/.secrets`.
- **Condición de detención:** Si el archivo `privado/.secrets` no existe, o si una clave referenciada (ej. `{{secrets.telefono}}`) no está definida en él, la generación se **detiene inmediatamente** reportando la clave faltante.
- **Prohibición:** Jamás emitir o renderizar un documento con marcadores `{{secrets.*}}` sin resolver.

---

## 7. Sanitización de fuentes (§Sanitización, RF-EVID-002)

Al auditar o hacer referencia a repositorios con confidencialidad `interno` o `confidencial` (declarados en `profile/sources.yml`):
1. **Prohibiciones absolutas:**
   - Cero fragmentos de código fuente o lógica interna propietaria.
   - Cero nombres de tablas, columnas o esquemas de base de datos internos.
   - Cero rutas de endpoints o URLs de servidores institucionales/privados.
   - Cero nombres de clientes, estudiantes, docentes o directivos.
   - Cero capturas de pantalla o volcados de datos.
2. **Abstracción de logros:** Expresar los resultados en términos de arquitectura general, patrones técnicos (ej. "Arquitectura multi-tenant con aislamiento por esquema"), métricas de concurrencia, rendimiento o tecnologías utilizadas.
3. **Regla de duda:** Ante cualquier duda sobre si un dato es confidencial o de dominio institucional, **se omite y se formula la pregunta a Joseph**.

---

## 8. Proceso de auditoría (§Auditoría, RF-EVID-003, RF-EVID-004)

1. El agente lee la fuente local declarada en `profile/sources.yml` (archivos de configuración, dependencias, patrones arquitectónicos y commits de Joseph).
2. El agente elabora un informe de hallazgos en la consola o en `privado/evidencia/`.
3. El agente formula **propuestas** de viñetas y habilidades técnicas con sus respectivos campos (`id`, `tags`, `weight`, `es`, `en`, `evidence`).
4. **Aprobación paso a paso:** Joseph debe aprobar, rechazar o ajustar cada propuesta individualmente.
5. **Prohibición:** El agente tiene prohibido escribir o modificar directamente `profile/` sin la confirmación explícita de Joseph sobre cada elemento.

---

## 9. Regla de atribución de proyectos (§Atribución, RF-EVID-006, D-11)

- **Fuentes clasificadas como `interno`:**
  - Sustentan experiencia laboral adquirida.
  - Sus viñetas deben asignarse al puesto desempeñado en la institución empleadora (ej. Instituto Tecnológico Superior Mayor Pedro Traversari - ISTPET).
  - **Queda estrictamente prohibido:** nombrar el repositorio interno, enlazar su URL o presentarlo como proyecto de autoría personal.
- **Fuentes clasificadas como `publico`:**
  - Son las únicas que pueden presentarse como proyectos de autoría propia y enlazarse directamente en la sección de Proyectos del currículum.

---

## 10. Seguimiento de postulaciones (§Seguimiento, RF-TRACK-002, RF-TRACK-003)

- Archivo de registro: `privado/aplicaciones.yml`.
- **Vocabulario cerrado de estados:**
  `borrador`, `postulado`, `screening`, `tecnica`, `final`, `oferta`, `aceptada`, `rechazada`, `sin_respuesta`, `retirada`.
- **Regla de inmutabilidad del `timeline`:** Las transiciones de estado solo se registran anexando un nuevo objeto `{ fecha: "AAAA-MM-DD", evento: "..." }`. Queda prohibido modificar, sobrescribir o eliminar eventos anteriores.
- **Umbral de inactividad (PD-01):** Toda postulación en estado `postulado`, `screening` o `tecnica` que supere **21 días calendario** sin comunicación ni eventos nuevos debe transicionar automáticamente al estado `sin_respuesta`.

---

## 11. Analítica de conversión (§Analítica, RF-ANL-001..004)

Al solicitar la generación del reporte `privado/analitica.md`:
1. **Embudo de conversión (RF-ANL-001):** Cantidad de postulaciones en cada etapa y tasa de paso entre etapas consecutivas.
2. **Segmentación (RF-ANL-002):** Tasa de respuesta desglosada por fuente (LinkedIn, portal directo, etc.), por idioma, por plantilla utilizada y por rango de `match_score` (ej. 80-100%, 60-79%, <60%).
3. **Brechas de mercado (RF-ANL-003):** Lista de keywords presentes en ofertas registradas que no existen en `profile/skills.yml`, ordenadas por frecuencia descendente.
4. **Rigor de muestra (RF-ANL-004):**
   - Toda tasa o porcentaje debe escribirse con su denominador explícito en formato `n/N` (ej. `3/5 (60%)`).
   - Si el total de aplicaciones registradas es **menor a 10**, el informe debe incluir una advertencia destacada indicando que el tamaño de muestra es insuficiente para conclusiones estadísticas, presentando únicamente recuentos absolutos.

---

## 12. Prohibiciones e higiene del repositorio

1. **RF-GEN-008:** Prohibido inventar o afirmar cualquier experiencia, cargo o habilidad que no esté respaldada documentalmente en `profile/`.
2. **RF-SEG-007:** **Prohibida la co-autoría de IA.** Ningún commit, mensaje de control de versiones ni descripción de Pull Request debe incluir líneas `Co-authored-by:` atribuidas a un agente, modelo o bot de IA.
3. **RF-SEG-001:** Prohibido agregar o confirmar archivos en `privado/` o archivos `.secrets` en el árbol de Git.
4. **RF-TRACK-003:** Prohibido alterar el historial de `privado/aplicaciones.yml` salvo por adición de nuevas aplicaciones o anexión de eventos en el timeline.
