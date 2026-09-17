# ADR-002: Taxonomía canónica de etiquetas y normalización de alias

- **ID:** ADR-002
- **Fecha:** 2026-09-17
- **Estado:** Aprobado
- **Decisor:** Joseph Andrés Baño Naranjo
- **Requisitos vinculados:** RF-GEN-006, RF-DATOS-003, RF-DATOS-004, PD-07

---

## Contexto

El sistema de generación de hojas de vida (SPEC-001) adapta el currículum a cada oferta seleccionando y ordenando viñetas de experiencia en función de las palabras clave requeridas.

En el mercado laboral y las ofertas de empleo existen múltiples variantes sintácticas para referirse a la misma tecnología o competencia (por ejemplo, `k8s` vs `kubernetes`, `c#` vs `csharp` vs `.net`, `postgres` vs `postgresql`). Si las viñetas de `profile/experience.yml` y `profile/projects.yml` utilizan etiquetas arbitrarias o no estandarizadas:
1. El cálculo del porcentaje de coincidencia (`match_score`) resulta errático e impredecible.
2. La intersección entre keywords de la oferta y etiquetas de viñetas falla, omitiendo viñetas relevantes o seleccionando viñetas irrelevantes.
3. El punto abierto PD-07 requería resolver este vocabulario de forma controlada y versionada.

---

## Opciones evaluadas

1. **Etiquetas libres sin control:**
   - Cada viñeta define etiquetas a criterio del redactor o agente.
   - *Descarte:* Genera dispersión inmediata (`c#`, `csharp`, `dotnet`, `.net`, `.NET`, `c-sharp`) haciendo imposible un cruce determinista.

2. **Sinonimia calculada por embeddings / LLM en tiempo de ejecución:**
   - El agente calcula similitud semántica en cada generación.
   - *Descarte:* Viola RF-GEN-007 (determinismo byte a byte), introduce variabilidad no controlada y costo innecesario.

3. **Catálogo canónico versionado en `profile/taxonomy.yml` con lista de alias:**
   - Se define una lista fija de etiquetas canónicas organizadas por categoría técnica, donde cada clave canónica mapea una lista de alias textuales conocidos.
   - Toda etiqueta utilizada en `profile/` debe existir en este archivo.
   - La normalización de keywords de ofertas mapea cualquier alias reconocido hacia su etiqueta canónica.

---

## Decisión

Se adopta la opción 3:
1. Se crea `profile/taxonomy.yml` como la única fuente de la verdad para etiquetas en el repositorio.
2. Cada entrada define una etiqueta canónica (`csharp`, `kubernetes`, `postgresql`, etc.) y una lista de alias que absorbe las variantes de mercado (`c#`, `.net`, `k8s`, `postgres`, etc.).
3. **Regla estricta de validación:** Toda etiqueta utilizada en los campos `tags` de `profile/experience.yml`, `profile/projects.yml` o en `profile/skills.yml` **DEBE** coincidir exactamente con una etiqueta canónica de `taxonomy.yml`. El uso de una etiqueta no registrada constituye un error de validación bloqueante en `profile-lint`, **no** una etiqueta nueva creada al vuelo.
4. **Procedimiento para añadir nuevas etiquetas:**
   - Si una nueva oferta o un proyecto auditado introduce una tecnología válida no contemplada, se debe enviar un Pull Request que añada la etiqueta canónica y sus alias a `profile/taxonomy.yml`.
   - Una vez integrado el cambio, las viñetas pueden referenciar la nueva etiqueta.

---

## Consecuencias

### Positivas
- Se garantiza consistencia total en el cálculo del porcentaje de coincidencia (`match_score`) (RF-GEN-006).
- La selección de viñetas se vuelve completamente determinista y reproducible (RF-GEN-007).
- Se cierra formalmente el punto de decisión PD-07.

### Negativas / Restricciones
- La adición de tecnologías al perfil requiere mantener actualizada la taxonomía.
