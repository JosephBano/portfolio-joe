# Guía de estilo y restricciones ATS — templates/STYLE.md

Este documento establece las reglas visuales y estructurales inviolables para cualquier plantilla y documento derivado (`cv.docx` y `cv.pdf`) en el repositorio `portfolio-joe` (RF-GEN-003, RF-GEN-004, ADR-001).

---

## 1. Reglas estructurales inviolables

1. **Una sola columna:** Flujo de texto continuo de arriba a abajo. Prohibido usar columnas múltiples o diseños en cuadrícula.
2. **Cero tablas:** Ningún dato (ni habilidades, ni fechas, ni formación) puede maquetarse en tablas (`w:tbl`).
3. **Cero cuadros de texto o elementos flotantes:** Prohibido el uso de `text-boxes`, marcos, llamadas laterales o formas de dibujo (`w:drawing`, `w:txbx`).
4. **Cero imágenes:** Ninguna fotografía, logotipo, icono de habilidad o gráfico de barras.
5. **Cero encabezados y pies de página de documento:** La información de contacto debe residir en las primeras líneas del cuerpo principal (`w:body`), nunca en encabezados (`w:header`) ni pies de página (`w:footer`) de página Word.
6. **Márgenes de página uniformes:** 2.54 cm (1 pulgada) en los cuatro bordes (superior, inferior, izquierdo, derecho).

---

## 2. Tipografía y estilos

- **Tipografía universal:** Calibri en todo el documento.
- **Jerarquía de tamaños e interlineados:**
  - **Nombre del candidato (`#` / Título):** Calibri 18 pt, negrita, centrado o alineado a la izquierda.
  - **Línea de contacto y enlaces:** Calibri 10 pt, texto regular, separadores visuales claros (` | ` o ` · `).
  - **Encabezados de sección (`##` / Heading 1):** Calibri 12.5 pt a 13 pt, negrita, mayúsculas sostenidas, con línea de separación inferior sutil o espaciado anterior de 8-10 pt y posterior de 3 pt.
  - **Subtítulos de puesto / empresa (`Heading 2` o párrafo en negrita):** Calibri 11 pt, negrita.
  - **Cuerpo de texto y viñetas:** Calibri 11 pt, texto regular, interlineado sencillo (1.0 a 1.15), espaciado posterior de 2 a 3 pt entre viñetas.
- **Viñetas de lista:** Listas nativas de Word utilizando el glifo de viñeta circular estándar (`•`), con sangría regular a la izquierda de 0.63 cm (0.25 pulgadas).

---

## 3. Elementos Markdown admitidos en `cv.md`

`tools/render_docx.py` admite exclusivamente los siguientes elementos de Markdown:
- Encabezado de nivel 1 (`# Título`)
- Encabezado de nivel 2 (`## Sección`)
- Párrafos de texto
- Negrita (`**texto en negrita**`)
- Cursiva (`*texto en cursiva*`)
- Hipervínculos (`[texto visible](url)`)
- Listas no ordenadas (`- viñeta de logro`)

Cualquier otra construcción de Markdown (tablas con tuberías `|`, bloques de código ` ``` `, citas `> `, imágenes `![]()`) provocará un error de renderizado explícito.
