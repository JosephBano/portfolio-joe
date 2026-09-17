# Reglas de optimización ATS (Applicant Tracking Systems)

Este documento detalla cada regla de diseño y estructura aplicada a los documentos generados (`cv.docx` y `cv.pdf`), explicando el motivo técnico por el que existe.

---

## 1. Diseño estricto de una sola columna
- **Regla:** El documento se organiza en un flujo lineal vertical continuo de una sola columna.
- **Motivo técnico:** Los analizadores automáticos de currículums (ATS como Taleo, Workday, Greenhouse, Lever, etc.) procesan el flujo de texto de izquierda a derecha. Los diseños de dos o más columnas provocan que las líneas de texto de ambas columnas se lean de forma entrelazada en el mismo renglón, corrompiendo la coherencia de fechas, cargos y viñetas.

## 2. Prohibición total de tablas
- **Regla:** No se utilizan tablas para alinear texto, organizar habilidades ni mostrar datos cronológicos.
- **Motivo técnico:** Los motores de parseo interpretan las celdas de una tabla como bloques aislados de datos tabulares, perdiendo el flujo cronológico y contextual. Muchas plataformas ATS descartan el contenido de tablas o lo extraen al final del documento desarticulado de su puesto correspondiente.

## 3. Prohibición de cuadros de texto (Text Boxes) y elementos flotantes
- **Regla:** Todo el contenido debe formar parte del cuerpo principal del documento (`w:body` en OpenXML).
- **Motivo técnico:** En los archivos `.docx`, los cuadros de texto se almacenan en capas de dibujo separadas (`drawingML` o `VML`). La inmensa mayoría de los extractores ATS leen únicamente el cuerpo de texto principal e ignoran por completo las capas de dibujo. Colocar datos de contacto o habilidades en cuadros de texto equivale a ocultárselos al ATS.

## 4. Prohibición de imágenes, iconos y gráficos de nivel
- **Regla:** Cero imágenes, logos corporativos, fotografías de perfil o barras porcentuales de dominio.
- **Motivo técnico:** Los ATS no realizan OCR visual sobre logotipos de tecnologías. Las barras de progreso o iconos de habilidades ("5/5 estrellas") son ilegibles para el algoritmo y consumen espacio que debería contener texto descriptivo indexable.

## 5. Sin encabezados ni pies de página de documento (`header` / `footer`)
- **Regla:** Los datos de contacto, enlaces y nombre van en las primeras líneas del cuerpo principal, nunca en el encabezado (`header`) ni pie (`footer`) de Word.
- **Motivo técnico:** Para evitar repetir información entre páginas en documentos multipágina, muchos filtros ATS ignoran intencionalmente las secciones de encabezado y pie de página de Word. Si el correo o teléfono están en el encabezado, el ATS registrará al candidato sin información de contacto.

## 6. Tipografía estándar y jerarquía limpia
- **Regla:** Fuente Calibri (11 pt para cuerpo de texto, 13 pt para encabezados principales, interlineado regular).
- **Motivo técnico:** El uso de fuentes estándar universales (Calibri, Arial) evita problemas de codificación de glifos o ausencia de fuentes incrustadas en el servidor de destino que puedan rasterizar o corromper caracteres acentuados.

## 7. Nombres convencionales y estilos nativos para encabezados de sección
- **Regla:** Los títulos de sección usan estilos nativos (`Heading 1`, `Heading 2`) y nomenclaturas estándar: "Experiencia Profesional", "Habilidades Técnicas", "Educación", "Certificaciones", "Idiomas".
- **Motivo técnico:** Los ATS identifican los bloques de contenido mediante expresiones regulares y heurísticas sobre nombres estándar de sección. Si una sección se titula "Lo que me apasiona" en lugar de "Experiencia Profesional", el parser no puede clasificar los puestos ni calcular los años de experiencia.

## 8. Viñetas con caracteres estándar
- **Regla:** Uso de listas con viñetas nativas de Word con sangría regular.
- **Motivo técnico:** El uso de caracteres Unicode complejos o imágenes diminutas como viñetas se traduce frecuentemente en símbolos de interrogación `?` o caracteres no imprimibles que rompen el parseo de la oración.

## 9. Alineación literal de alias con las palabras clave de la vacante
- **Regla:** Cuando una vacante solicita textualmente un término específico (ej. "ASP.NET Core"), el currículum debe utilizar exactamente esa variante sintáctica en lugar de un término genérico (ej. ".NET").
- **Motivo técnico:** Muchos filtros ATS preliminares operan mediante coincidencias booleanas literales (`exact keyword matching`). Si el reclutador filtra por "ASP.NET Core", una hoja de vida que solo mencione "C#" puede ser descartada automáticamente con puntaje cero en ese criterio.
