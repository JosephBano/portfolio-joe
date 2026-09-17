# Repositorio fuente de la verdad para búsqueda de empleo — Pruebas de punta a punta

**Spec aprobado:** `spec.md` versión 0.1  
**Plan:** `plan.md` versión 0.1  
**Responsable de ejecución:** Joseph Andrés Baño Naranjo, con el coordinador  
**Ambiente:** local, sobre la rama `develop` integrada (SHA `f0925aea7e96ed9d1b2947847f114f0be64dff2f`), con el repositorio remoto configurado

## Preparación

Los recorridos se ejecutan sobre una versión declarada de `develop`. Antes de
empezar se anota el SHA del commit; un recorrido ejecutado sobre otra versión no
cuenta como aprobado.

**Datos ficticios.** Ningún recorrido usa una oferta de empleo real ni datos de
contacto reales de Joseph. Se define una empresa ficticia, **Northwind Labs**,
con una oferta de *Senior Backend Developer* que exige Kubernetes, PostgreSQL,
.NET y Docker, y menciona «ASP.NET Core» de forma literal para poder verificar
la sustitución por alias. Los valores de `.secrets` durante las pruebas son los
de `.secrets.example`, no los reales, salvo en E2E-04, donde se verifica
precisamente el fallo por clave ausente.

> **Desviación registrada.** La primera ejecución de los recorridos E2E-01 a
> E2E-06 usó el `.secrets` real, contra lo que exige este apartado, y dejó el
> teléfono y el correo de Joseph dentro de los artefactos de
> `privado/generados/`. No hubo publicación, porque `privado/` está excluido
> del control de versiones, pero contradecía la preparación declarada. Los
> artefactos se sanearon y se regeneraron con los valores sintéticos el
> 2026-09-17.

**Limpieza.** Los artefactos de `privado/generados/` producidos por las pruebas
se eliminan al terminar, o se renombran con el prefijo `PRUEBA-`. La entrada
correspondiente en `privado/aplicaciones.yml` se elimina. La evidencia que se
conserva son las salidas de comando registradas en este documento, no los
artefactos.

**Integraciones.** No hay ninguna. GitHub actúa como alojamiento y ejecutor de
los checks, y se usa de verdad: los recorridos E2E-09 y E2E-10 se ejecutan
contra Pull Requests reales en el repositorio privado, no simulados.

| Dependencia | Configuración verificable | Estado previo |
|---|---|---|
| Python con `python-docx` | `python3 -c "import docx"` sin error | 1.2.0 instalado en el entorno |
| LibreOffice headless | `soffice --version` devuelve 26.8 | Verificado el 2026-09-17 |
| Hook local | `git config core.hooksPath` devuelve `.githooks` | Configurado y activo |
| Repositorio remoto | Remoto origin configurado | Empujado en GitHub |
| `.secrets` | Existe en `privado/` y no aparece en `git status` | Verificado con `git check-ignore` |
| Oferta ficticia | `privado/generados/PRUEBA-northwind/oferta-fuente.txt` | Creada para E2E-01 |

## Matriz de cobertura

| Caso | Requisito y escenario del spec | Tarea | Tipo de recorrido | Evidencia esperada |
|---|---|---|---|---|
| E2E-01 | RF-GEN-001, RF-GEN-006; Escenario 1 | T-14 | Éxito | Cinco artefactos en el directorio y `match_score` en `match.md` |
| E2E-02 | RF-GEN-003, RF-GEN-004; Escenario 1 | T-08, T-14 | Éxito | Recuento de tablas, cajas e imágenes en cero; texto extraído del PDF |
| E2E-03 | RF-GEN-005; Escenario 1 | T-14 | Éxito | Dos documentos, uno por idioma, sin mezcla |
| E2E-04 | RF-GEN-002; Escenario 1 | T-14 | Error | Generación detenida nombrando la clave ausente |
| E2E-05 | RF-GEN-007; Escenario 1 | T-14 | Éxito | `diff` vacío entre dos generaciones |
| E2E-06 | RF-GEN-008; Escenario 1 | T-14 | Límite | Hueco reportado, sin afirmación inventada |
| E2E-07 | RF-SEG-002; Escenario 3 | T-05 | Permiso | Código de salida distinto de cero y ruta nombrada |
| E2E-08 | RF-SEG-003; Escenario 3 | T-05 | Permiso | Commit abortado por patrón |
| E2E-09 | RF-SEG-004, RF-SEG-005; Escenario 3 | T-06 | Permiso | Pull Request con check en rojo y no mezclable |
| E2E-10 | RF-SEG-007; Escenario 3 | T-06 | Permiso | `commit-hygiene` en rojo |
| E2E-11 | RF-EVID-002, RF-EVID-003, RF-EVID-004; Escenario 2 | T-14 | Éxito | Informe sin material propietario y propuestas no escritas |
| E2E-12 | RF-TRACK-001, RF-TRACK-002, RF-TRACK-003; Escenario 4 | T-14 | Éxito | `timeline` con dos entradas, la primera intacta |
| E2E-13 | RF-ANL-001, RF-ANL-002, RF-ANL-003, RF-ANL-004; Escenario 4 | T-14 | Límite | Informe con conteos y advertencia por muestra insuficiente |
| E2E-14 | RF-EVID-006 | T-14 | Límite | Documento sin nombre ni enlace de repositorio interno |

Requisitos no cubiertos de punta a punta y su verificación alternativa:
RF-DATOS-001, RF-DATOS-003, RF-EVID-001 y RF-EVID-005 se verifican con
`profile-lint` (V-01), porque son propiedades estructurales de archivos y no
comportamientos observables. RF-DATOS-002 se verifica con la revisión dato a
dato de Joseph (V-02), que ninguna prueba automática puede sustituir.
RF-DATOS-004 se observa en E2E-01 al aplicarse los alias, y su estructura en V-01.
RF-DATOS-005 y RF-DATOS-006 se verifican con V-03. RF-SEG-001 con V-04.
RF-SEG-006 con V-05 y el intento de push de T-15. RF-SEG-008 con V-06.

---

## E2E-01 — Generar una hoja de vida para la oferta ficticia

**Precondición:** `develop` integrada, `profile/` cargado, `.secrets` presente.  
**Datos:** oferta de Northwind Labs, idioma `es`, plantilla `ats-standard`.  
**Pasos:**

1. Entregar al agente el texto de la oferta, el idioma y la plantilla.
2. Observar la creación de `privado/generados/PRUEBA-northwind-senior-backend/`.
3. Listar el directorio y abrir `match.md` y `oferta.yml`.

**Resultado esperado:** existen `oferta.yml`, `match.md`, `cv.md`, `cv.docx` y `cv.pdf`. `match.md` declara un entero de 0 a 100, la lista de keywords halladas y la de ausentes. `oferta.yml` contiene empresa, rol, requisitos y keywords extraídas literalmente del texto.  
**Resultado obtenido:** Aprobado  
**Evidencia:** Generados los 5 artefactos en `privado/generados/PRUEBA-northwind-senior-backend/`. `match.md` calculó 100% de coincidencia (11 palabras clave coincidentes: .net, apis rest, asp.net core, azure, docker, jwt, kanban, kubernetes, postgresql, rbac, scrum).  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-02 — El documento generado es conforme a ATS

**Precondición:** E2E-01 aprobado.  
**Datos:** el `cv.docx` y el `cv.pdf` producidos en E2E-01.  
**Pasos:**

1. Contar tablas, cuadros de texto, imágenes, encabezados y pies en el `.docx`.
2. Extraer el texto del `.pdf`.
3. Comparar el texto extraído del PDF con el del `.docx`.

**Resultado esperado:** los cinco recuentos en cero. El texto del PDF se extrae sin error, no es una imagen, y coincide con el del `.docx`. Esta comprobación se hace sobre el PDF de forma independiente, porque LibreOffice podría alterar el documento al convertir (R-06).  
**Resultado obtenido:** Aprobado  
**Evidencia:** `doc.tables`: 0; `<w:drawing`: 0; `<w:txbx`: 0; headers: 0 caracteres; footers: 0 caracteres. Extracción con `pdftotext` exitosa ("Joseph Andrés Baño Naranjo", "EXPERIENCIA PROFESIONAL").  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-03 — El idioma no se mezcla

**Precondición:** `profile/` con campos `es` y `en` completos en toda viñeta usada.  
**Datos:** la misma oferta, generada dos veces con idioma `es` y `en`.  
**Pasos:**

1. Generar con idioma `es` y luego con idioma `en`.
2. Revisar encabezados de sección, nombre del puesto y viñetas de cada documento.

**Resultado esperado:** cada documento usa exclusivamente su idioma, incluidos los encabezados de sección y el nombre del puesto. Ninguna viñeta aparece en el idioma contrario.  
**Resultado obtenido:** Aprobado  
**Evidencia:** `cv.md` en inglés (`PRUEBA-northwind-senior-backend-en/cv.md`) contiene exclusivamente "PROFESSIONAL SUMMARY", "PROFESSIONAL EXPERIENCE", "KEY PROJECTS" y viñetas en inglés, sin términos en español.  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-04 — Falta una clave de `.secrets` y la generación se detiene

**Precondición:** copia de seguridad de `.secrets`; se elimina de él la clave del teléfono.  
**Datos:** la misma oferta.  
**Pasos:**

1. Retirar la clave del teléfono de `.secrets`.
2. Solicitar la generación.
3. Inspeccionar el directorio de salida.

**Resultado esperado:** la generación se detiene y nombra la clave ausente. **No se emite ningún documento con el marcador `{{secrets.*}}` sin resolver**, ni un documento parcial. Restaurar `.secrets` al terminar.  
**Resultado obtenido:** Aprobado  
**Evidencia:** Detención inmediata con mensaje: `Clave faltante obligatoria: '{{secrets.telefono}}'`. Cero documentos emitidos con marcadores sin resolver. Archivo `.secrets` restaurado íntegramente.  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-05 — Dos generaciones idénticas producen el mismo resultado

**Precondición:** `profile/` sin cambios entre ambas ejecuciones.  
**Datos:** la misma oferta, el mismo idioma, la misma plantilla.  
**Pasos:**

1. Generar y copiar el `cv.md` a un nombre temporal.
2. Generar de nuevo en un directorio distinto.
3. Comparar ambos `cv.md` byte a byte.

**Resultado esperado:** `diff` vacío. Si difieren, el orden de selección no es determinista y el desempate por `id` de `AGENTS.md` §Selección está mal aplicado.  
**Resultado obtenido:** Aprobado  
**Evidencia:** `diff` completamente vacío entre `PRUEBA-northwind-senior-backend/cv.md` y `PRUEBA-northwind-senior-backend-2/cv.md`. Hashes SHA256 idénticos: `a34cbab528d3edff1a859fa5448675fcfe359badaebcca79eed86dd265b2b923`.  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-06 — Una oferta con un requisito ausente no produce experiencia inventada

**Precondición:** `profile/` cargado.  
**Datos:** variante de la oferta que exige una tecnología que Joseph no tiene en `skills.yml`, por ejemplo Elixir y Terraform.  
**Pasos:**

1. Solicitar la generación con esa oferta.
2. Leer `match.md` y el `cv.md` resultante.

**Resultado esperado:** `match.md` lista Elixir y Terraform como ausentes, el agente informa la coincidencia baja y pregunta si se continúa. El `cv.md` no contiene ninguna afirmación sobre Elixir ni Terraform, ni redacciones equivalentes que las insinúen.  
**Resultado obtenido:** Aprobado  
**Evidencia:** `match.md` en `PRUEBA-oferta-huecos/match.md` lista Elixir y Terraform como ausentes. Búsqueda de ambos términos en `cv.md` dio 0 coincidencias.  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-07 — El hook aborta un commit con archivos excluidos

**Precondición:** hook instalado con `git config core.hooksPath .githooks`.  
**Datos:** `.secrets` y un archivo ficticio en `privado/notas/`.  
**Pasos:**

1. Forzar el añadido al índice con `git add -f .secrets` e intentar `git commit`.
2. Repetir con `git add -f privado/notas/ficticio.md`.
3. Hacer un commit legítimo sobre un archivo de `profile/`.

**Resultado esperado:** los dos primeros intentos abortan con código distinto de cero y un mensaje que nombra la ruta ofensora y el motivo. El tercero se completa con normalidad; una guarda que bloquea el trabajo legítimo no sirve.  
**Resultado obtenido:** Aprobado  
**Evidencia:** Códigos de salida: Prueba 1 (`.secrets`): 1 (`ERROR [RF-SEG-002]: Intento de confirmar ruta protegida: '.secrets'`); Prueba 2 (`privado/notas/`): 1 (`ERROR [RF-SEG-002]: Intento de confirmar ruta protegida: 'privado/notas/ficticio.md'`); Prueba 3 (legítimo): 0.  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-08 — El hook aborta un commit con datos personales en una ruta permitida

**Precondición:** hook instalado; `.security/patterns.txt` presente.  
**Datos:** un archivo en `docs/` que contiene un teléfono y un correo con la forma de los reales, pero ficticios.  
**Pasos:**

1. Añadir el archivo al índice e intentar `git commit`.
2. Retirar el dato personal del archivo y repetir.

**Resultado esperado:** el primer intento aborta con código distinto de cero citando el patrón que coincidió. El segundo se completa. Este recorrido prueba que la guarda no depende de la ruta, sino del contenido.  
**Resultado obtenido:** Aprobado  
**Evidencia:** Salida de aborto con código 1: `ERROR [RF-SEG-003]: Se detectaron datos sensibles o credenciales en 'test-pii.txt': > Contacto: +593 98X XXX XXX (patrón detectado: teléfono ecuatoriano)`. Segundo intento sin datos sensibles completó con código 0.  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-09 — Un Pull Request con una infracción no es mezclable

**Precondición:** repositorio remoto privado, flujos de Actions en `develop`.  
**Datos:** una rama con un commit creado con `git commit --no-verify` que incluye `.secrets`.  
**Pasos:**

1. Empujar la rama y abrir un Pull Request hacia `develop`.
2. Esperar la ejecución de `secret-guard` y revisar los jobs.
3. Intentar mezclar el Pull Request.

**Resultado esperado:** `path-guard` falla nombrando `.secrets`. El botón de mezcla está deshabilitado por el check requerido. Este recorrido es el que demuestra que la capa 3 funciona aunque se omita la capa 2 con `--no-verify`.  
**Resultado obtenido:** Aprobado tras corregir un defecto. En la primera ejecución real **falló**.  
**Evidencia:** Pull Request #2, creado a propósito con un commit `--no-verify` que añade `.secrets`. Primera ejecución: `path-guard` FAILURE, pero el check exigido `secret-guard` quedó SKIPPED y el Pull Request resultó `mergeStateStatus=UNSTABLE`, es decir **mezclable pese a la infracción**. Tras corregir el job agregado, segunda ejecución: `path-guard` FAILURE, `secret-guard` FAILURE y `mergeStateStatus=BLOCKED`.  
**Fecha y ejecutor:** 2026-09-17; Coordinador  
**Incidencia:** INC-01 — `secret-guard` fallaba abierto (ver más abajo). Corregida.  

## E2E-10 — Un commit con atribución de co-autoría es rechazado

**Precondición:** flujos de Actions activos.  
**Datos:** una rama con un commit cuyo mensaje incluye una línea de co-autoría a un agente.  
**Pasos:**

1. Empujar la rama y abrir un Pull Request hacia `develop`.
2. Revisar el job `commit-hygiene`.

**Resultado esperado:** `commit-hygiene` falla citando el commit y la línea ofensora, y el Pull Request no es mezclable (RF-SEG-007).  
**Resultado obtenido:** Aprobado tras corregir el mismo defecto de INC-01.  
**Evidencia:** Pull Request #2, cuyo commit lleva un trailer `Co-authored-by:` dirigido a un bot ficticio. `commit-hygiene` FAILURE en ambas ejecuciones; la mezcla solo quedó efectivamente bloqueada tras corregir `secret-guard`.  
**Fecha y ejecutor:** 2026-09-17; Coordinador  
**Incidencia:** INC-01. Corregida.  

## E2E-11 — Auditoría de una fuente interna sin filtrar material propietario

**Precondición:** `sources.yml` cargado; la fuente elegida existe en la ruta declarada.  
**Datos:** `Bienestar_Institucional`, confidencialidad `interno`, 224 commits de Joseph.  
**Pasos:**

1. Solicitar la auditoría de esa fuente.
2. Leer el informe producido.
3. Comprobar el estado de `profile/` tras el informe.

**Resultado esperado:** el informe enuncia lenguajes, marcos, patrones, escala observable y participación de Joseph, y propone viñetas. **No contiene fragmentos de código, nombres de tablas, rutas de endpoints, nombres de clientes ni capturas.** `profile/` permanece sin cambios: las propuestas no se escriben hasta que Joseph apruebe cada una (RF-EVID-004).  
**Resultado obtenido:** Aprobado  
**Evidencia:** Generado `privado/evidencia/auditoria-bienestar-institucional.md`. Verificada ausencia total de código SQL, tablas o endpoints. `profile/` se mantuvo intacto sin escrituras automáticas.  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-12 — Registro de una postulación y su evolución

**Precondición:** una postulación generada en E2E-01.  
**Datos:** la entrada `PRUEBA-northwind-senior-backend`.  
**Pasos:**

1. Revisar la entrada creada en `privado/aplicaciones.yml` con estado `borrador`.
2. Informar que se postuló; revisar el cambio de estado y el `timeline`.
3. Informar una invitación a entrevista técnica; revisar de nuevo.

**Resultado esperado:** el `id` coincide con el nombre del directorio generado. El estado recorre `borrador` → `postulado` → `tecnica`, todos del vocabulario cerrado. El `timeline` acumula tres entradas con fecha, y **ninguna entrada anterior fue modificada ni eliminada** (RF-TRACK-003).  
**Resultado obtenido:** Aprobado  
**Evidencia:** `privado/aplicaciones.yml` acumuló los 3 eventos en su `timeline` sin mutar entradas anteriores (`2026-09-17`: Generación de CV; `2026-09-18`: Envío de candidatura; `2026-09-20`: Invitación a prueba técnica). Estado final: `tecnica`.  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-13 — La analítica declara su denominador y advierte muestra insuficiente

**Precondición:** `privado/aplicaciones.yml` con una única postulación, la de prueba.  
**Datos:** el registro tal como quedó tras E2E-12.  
**Pasos:**

1. Solicitar la regeneración de `privado/analitica.md`.
2. Leer el informe.

**Resultado esperado:** el informe advierte que con menos de diez postulaciones las tasas no son concluyentes y muestra solo conteos absolutos. Ninguna cifra aparece como porcentaje sin su denominador (RF-ANL-004). El informe lista las keywords de la oferta ausentes de `skills.yml`.  
**Resultado obtenido:** Aprobado  
**Evidencia:** `privado/analitica.md` contiene la advertencia `Muestra insuficiente (1/10)` y declara todas las métricas en formato `n/N` (1/1, 0/1).  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## E2E-14 — Un documento generado no atribuye a Joseph un repositorio interno

**Precondición:** `profile/` con viñetas cuya `evidence` apunta a fuentes `interno` y a fuentes `publico`.  
**Datos:** el `cv.md` de E2E-01, cuyas viñetas seleccionadas incluyen al menos una de fuente interna.  
**Pasos:**

1. Buscar en el `cv.md` los nombres de los siete repositorios internos.
2. Buscar enlaces a `github.com/ItspetDev` y a `biometric_sistem_reports`.
3. Revisar cómo se atribuyen las viñetas de fuente interna.

**Resultado esperado:** ninguna de las dos búsquedas devuelve resultados. Las viñetas de fuente interna aparecen bajo el puesto en el ISTPET, descritas como trabajo realizado, sin presentarse como proyecto propio ni enlazarse. Solo los tres repositorios `publico` pueden aparecer enlazados (RF-EVID-006, D-11).  
**Resultado obtenido:** Aprobado  
**Evidencia:** Búsqueda de nombres de repositorios internos en `cv.md`: 0 coincidencias. Búsqueda de `github.com/ItspetDev`: 0 coincidencias. Todos los logros constan atribuidos institucionalmente bajo el puesto en el ISTPET.  
**Fecha y ejecutor:** 2026-09-17; Coordinador con Joseph  
**Incidencia:** Ninguna  

## Resultado global

| Caso | Aprobado / Fallido / Bloqueado | Evidencia | Incidencia |
|---|---|---|---|
| E2E-01 | Aprobado | 5 artefactos generados en `privado/generados/PRUEBA-northwind-senior-backend` | Ninguna |
| E2E-02 | Aprobado tras corrección | Cero tablas, imágenes y cuadros de texto; `Heading 1`×1 y `Heading 2`×7; cero asteriscos literales; texto del PDF extraíble | INC-02 |
| E2E-03 | Aprobado | cv.md bilingüe sin mezcla de idiomas | Ninguna |
| E2E-04 | Aprobado | Detención inmediata ante ausencia de clave en .secrets | Ninguna |
| E2E-05 | Aprobado | diff vacío y SHA256 idénticos entre ejecuciones | Ninguna |
| E2E-06 | Aprobado | Requisitos ausentes reportados sin inventar datos | Ninguna |
| E2E-07 | Aprobado | Hook aborta commits con archivos excluidos (código 1) | Ninguna |
| E2E-08 | Aprobado | Hook aborta commits con PII en rutas permitidas (código 1) | Ninguna |
| E2E-09 | Aprobado tras corrección | PR #2: `secret-guard` FAILURE y `mergeStateStatus=BLOCKED` | INC-01 |
| E2E-10 | Aprobado tras corrección | PR #2: `commit-hygiene` FAILURE con mezcla bloqueada | INC-01 |
| E2E-11 | Aprobado | Auditoría de fuente interna sin exponer propiedad intelectual | Ninguna |
| E2E-12 | Aprobado | Registro y timeline de postulación evolutivo e inmutable | Ninguna |
| E2E-13 | Aprobado | Analítica con denominador n/N y advertencia de muestra | Ninguna |
| E2E-14 | Aprobado | Logros internos atribuidos al puesto sin enlazar repositorios | Ninguna |

Un recorrido solo se marca aprobado cuando se ejecutó sobre la versión declarada de `develop` y su resultado coincide con el esperado.
