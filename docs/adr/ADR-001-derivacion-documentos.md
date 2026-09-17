# ADR-001: Mecanismo de derivación de documentos y frontera de código

- **ID:** ADR-001
- **Fecha:** 2026-09-17
- **Estado:** Aprobado
- **Decisor:** Joseph Andrés Baño Naranjo
- **Requisitos vinculados:** RF-GEN-003, RF-GEN-004, D-01, D-02, R-01, PD-02

---

## Contexto

El diseño del portafolio (SPEC-001) define que el origen de la verdad para una hoja de vida adaptada es Markdown (`cv.md`), permitiendo versionado, diffs limpios y selección determinista de viñetas mediante un agente de IA. No obstante, los reclutadores y las plataformas ATS (Applicant Tracking Systems) exigen documentos binarios en formato Word (`.docx`) y PDF (`.pdf`).

La decisión D-01 del spec prohíbe código de aplicación ejecutable (sin CLI, sin servicios web, sin dependencias pesadas que transformarían el portafolio en una aplicación). Adicionalmente, se verificó el entorno técnico local (PD-02):
- `pandoc` no está instalado en el equipo.
- `weasyprint` y `wkhtmltopdf` no están instalados.
- Sí están disponibles Python 3.14.7 con la biblioteca `python-docx` (v1.2.0) y LibreOffice 26.8 en modo headless (`soffice`).

Se requería definir el mecanismo determinista para pasar de `cv.md` a `.docx` y a `.pdf`, garantizando el cumplimiento estricto de las reglas ATS sin violar la frontera de código fijada por D-01.

---

## Opciones evaluadas

1. **Pandoc (`pandoc cv.md -o cv.docx`):**
   - *Ventajas:* Estándar en la conversión de documentos técnicos.
   - *Desventajas:* Requiere instalar software adicional no presente en el entorno; control limitado sobre las restricciones ATS finas sin plantillas complejas.
   - *Descarte:* Descartado por no estar instalado y para evitar dependencias del sistema operativo adicionales.

2. **HTML intermedio + convertidor headless (`weasyprint` o `wkhtmltopdf`):**
   - *Ventajas:* Soporte CSS para estilos de página.
   - *Desventajas:* Requiere herramientas externas no presentes; genera PDFs orientados a diseño gráfico que con frecuencia fragmentan texto o introducen artefactos no óptimos para motores de parseo ATS. No genera `.docx` nativo.
   - *Descarte:* Descartado por requerir herramientas no disponibles y no generar formato Word directo.

3. **Constructor Python con `python-docx` + LibreOffice headless (`soffice`):**
   - *Ventajas:* Utiliza herramientas ya instaladas y verificadas. `python-docx` construye el archivo `.docx` aplicando de forma programática las restricciones ATS (fuente Calibri 11, títulos nativos `Heading 1` y `Heading 2`, párrafos, viñetas nativas; cero tablas, cero cuadros de texto, cero imágenes, sin encabezados ni pies de página). Luego LibreOffice convierte `cv.docx` a `cv.pdf` de forma fiel con texto extraíble.
   - *Desventajas:* Requiere un script ejecutable auxiliar (`tools/render_docx.py`), lo que roza la frontera de D-01.

---

## Decisión

Se adopta la opción 3:
1. Se implementa `tools/render_docx.py` utilizando la biblioteca `python-docx` para procesar el Markdown básico (`cv.md`) y construir el archivo binario `cv.docx` conforme a las reglas ATS.
2. Se utiliza LibreOffice headless (`soffice --headless --convert-to pdf cv.docx`) para derivar el archivo `cv.pdf` a partir del `.docx` generado.

### Límite duro de la frontera de código (R-01)
Para preservar la decisión D-01 e impedir que `tools/` crezca hasta convertirse en una aplicación, se establece un límite duro inviolable:
- **Un solo archivo:** `tools/render_docx.py`.
- **Una sola dependencia externa:** `python-docx`.
- **Exactamente dos argumentos posicionales de ruta:** archivo Markdown de entrada y archivo `.docx` de salida.
- **Cero configuración:** sin archivos de configuración, flags complejas ni interfaz interactiva.
- **Sin lógica de negocio ni redacción:** el script no decide viñetas, no traduce, no calcula coincidencias ni genera contenido; solo renderiza la estructura de texto recibida.
- **Markdown admitido:** encabezados `#` y `##` (que se emiten con los estilos nativos `Heading 1` y `Heading 2`), párrafos, listas con `-`, negrita `**texto**`, cursiva `*texto*` e hipervínculos `[texto](url)`.
- **Error explícito:** ante cualquier elemento de Markdown no admitido (tablas, imágenes, bloques de código, citas) **o ante un marcador de énfasis sin cerrar**, el script aborta con código distinto de cero y un mensaje que indica la línea ofensora; jamás se degrada en silencio. Un asterisco que llegue al documento tal cual es un defecto, no una salida aceptable.

Cualquier necesidad de ampliar este script o superar estos límites obliga a volver a revisión funcional del spec con Joseph.

### Comportamiento ante ausencia o fallo de LibreOffice
Si LibreOffice no está instalado o la ejecución de `soffice` falla durante la conversión a PDF:
- Se **conserva** el archivo `cv.docx` ya generado.
- Se emite un mensaje explícito indicando que el PDF no pudo ser derivado y el motivo.
- **Prohibición:** Está terminantemente prohibido sustituir el método en silencio o recurrir a servicios en línea o bibliotecas no aprobadas.

---

## Consecuencias

### Positivas
- Se garantiza la reproducibilidad exacta de los documentos `.docx` y `.pdf` (RF-GEN-007).
- Se asegura el cumplimiento total de los requisitos ATS: documento de una sola columna, texto plano estructurado, sin tablas ni elementos gráficos que confundan a los analizadores automáticos (RF-GEN-003, RF-GEN-004).
- No se requieren nuevas instalaciones en el entorno local.

### Negativas / Restricciones
- Requiere mantener `tools/render_docx.py` bajo el límite estricto de R-01.
- La generación de PDF depende de la presencia local de LibreOffice.
