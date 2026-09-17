# Detección de secretos y datos personales — portfolio-joe

Este directorio contiene las reglas y patrones compartidos para la detección de datos sensibles, PII (Personally Identifiable Information) y credenciales en el repositorio.

## Componentes

- **`patterns.txt`**: Archivo canónico con una expresión regular extendida (POSIX ERE) por línea. Es consumido directamente por:
  1. El hook local `.githooks/pre-commit` mediante `git diff --cached` y `grep -E -f .security/patterns.txt`.
  2. El job `pii-scan` en el flujo de GitHub Actions `.github/workflows/secret-guard.yml`.

## Reglas de formato para `patterns.txt`

1. **Una expresión regular por línea.**
2. **Sin líneas vacías ni comentarios en el archivo:** `grep -E -f` interpreta cada línea como un patrón literal. Una línea en blanco haría coincidir cualquier línea de cualquier archivo, y una línea con `#` coincidiría con encabezados Markdown legítimos.
3. Utilizar sintaxis estándar POSIX ERE compatible con `grep -E` (evitar extensiones específicas de Perl como `\s` o `(?i)`).

## Política de gestión de falsos positivos

- **Prohibición:** Está terminantemente prohibido omitir el hook con `git commit --no-verify` en commits destinados a ramas públicas, o relajar / desactivar los checks en GitHub Actions.
- **Ajuste:** Si un commit legítimo genera un falso positivo comprobado, la expresión regular correspondiente en `.security/patterns.txt` debe ajustarse mediante un Pull Request explicativo antes de integrar el cambio.
