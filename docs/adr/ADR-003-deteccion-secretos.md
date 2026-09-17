# ADR-003: Criterio único de detección de secretos en local y CI

- **ID:** ADR-003
- **Fecha:** 2026-09-17
- **Estado:** Aprobado
- **Decisor:** Joseph Andrés Baño Naranjo
- **Requisitos vinculados:** RF-SEG-003, RF-SEG-004, RF-SEG-005, PD-06

---

## Contexto

El repositorio `portfolio-joe` es de visibilidad pública, pero la gestión de búsqueda laboral involucra datos personales sensibles (teléfono móvil, dirección física, correo personal, número de cédula) y credenciales de acceso a entornos institucionales o personales (tokens, claves privadas, cadenas de conexión).

En la sesión de diseño se constató (PD-06):
- `gitleaks` no está instalado en el entorno local del desarrollador y no se desean herramientas pesadas adicionales.
- `gitleaks` sí existe como acción oficial estándar en GitHub Actions (`gitleaks/gitleaks-action`).
- Existía el riesgo de aplicar criterios discrepantes entre el entorno local y la integración continua (CI), donde un Pull Request falle sorpresivamente por una regla que el desarrollador nunca pudo verificar localmente.

---

## Opciones evaluadas

1. **Exclusividad en CI con `gitleaks`:**
   - No verificar secretos en local; confiar únicamente en GitHub Actions.
   - *Descarte:* Viola RF-SEG-002 y RF-SEG-003; permitiría que secretos queden registrados en el historial de commits locales antes de llegar al remoto, obligando a reescribir ramas.

2. **Forzar instalación de `gitleaks` en local:**
   - Exigir la instalación y configuración local de binarios externos.
   - *Descarte:* Añade fricción de dependencias de sistema innecesarias cuando las herramientas estándar POSIX (`grep -E`) ya están presentes.

3. **Patrones compartidos en `.security/patterns.txt` + CI como superconjunto:**
   - Un archivo único de expresiones regulares extendidas (`.security/patterns.txt`) consumido tanto por el hook `pre-commit` local como por el job `pii-scan` en GitHub Actions.
   - GitHub Actions ejecuta además `gitleaks` sobre el diff y el historial como capa adicional de defensa en profundidad.

---

## Decisión

Se adopta la opción 3:
1. Se define `.security/patterns.txt` como la única fuente de la verdad para patrones de detección de datos personales (PII) y credenciales comunes.
2. **Hook local (`.githooks/pre-commit`):** inspecciona los cambios preparados en el índice (`git diff --cached`) y ejecuta `grep -E -f .security/patterns.txt`. Aborta inmediatamente si encuentra cualquier coincidencia.
3. **Flujo de CI (`.github/workflows/secret-guard.yml`):**
   - El job `pii-scan` consume exactamente `.security/patterns.txt` (nunca una copia duplicada).
   - El job `gitleaks` actúa como capa complementaria sobre el commit range del Pull Request.
4. **Política de falsos positivos:** Si un patrón genera un falso positivo en código o documentación legítima, la solución obligatoria es refinar la expresión regular en `.security/patterns.txt` mediante un Pull Request. Está terminantemente prohibido usar `git commit --no-verify` o deshabilitar checks en CI.

---

## Consecuencias

### Positivas
- Criterio uniforme y reproducible entre el puesto de trabajo local y el servidor de CI.
- No se requieren herramientas externas adicionales en local.
- Se resuelve y cierra formalmente el punto de decisión PD-06.

### Negativas / Restricciones
- `.security/patterns.txt` no admite comentarios en línea ni líneas vacías debido a la semántica de `grep -E -f`.
