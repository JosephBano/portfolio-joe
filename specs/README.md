# Specs — portfolio-joe

Un spec describe un cambio antes de implementarlo. Cada iniciativa vive en
`specs/NNN-slug/` y, al completar el flujo, contiene exactamente cuatro
archivos: `spec.md`, `plan.md`, `tasks.md` y `test-e2e.md`. Las plantillas
están en [`plantillas/`](plantillas/) y provienen del flujo Spec Kit usado en
`istpet-dev/gitlab/departamento-medico/specs`.

## Numeración e identificadores

Cada iniciativa recibe un número secuencial de tres dígitos, asignado en el
momento de crear la carpeta y **nunca reutilizado**. Un spec abandonado o
sustituido conserva su número; el reemplazo toma el siguiente libre y cita al
anterior en «Fuentes y decisiones vigentes».

| Elemento | Formato | Ejemplo |
|---|---|---|
| Carpeta | `NNN-slug` en minúsculas y guiones, tres a cinco palabras | `001-repo-cv-ats` |
| Campo `ID` dentro de `spec.md` | `SPEC-NNN` | `SPEC-001` |
| Rama de trabajo | `spec/NNN-slug`, **una sola por spec** | `spec/001-repo-cv-ats` |
| Requisito | `RF-<ÁREA>-NNN`, numerado dentro de su área y único en el spec | `RF-SEG-004` |
| Tarea | `T-NN`, única dentro de `tasks.md` | `T-03` |
| Punto de decisión | `PD-NN`, único dentro del spec | `PD-02` |
| Caso de punta a punta | `E2E-NN`, único dentro de `test-e2e.md` | `E2E-01` |
| ADR derivado | `ADR-NNN-slug.md` en `docs/adr/`, con numeración propia e independiente de la de los specs | `docs/adr/ADR-001-render-docx.md` |

Un spec, una rama. Las tareas de `tasks.md` no abren rama propia: se integran
sobre la rama del spec, en el orden que fija `plan.md`, cada una con su commit.
La rama del spec entra a `develop` por un único Pull Request y se borra al
mezclarse. Abrir una rama por tarea multiplica las ramas sin aportar
aislamiento, porque todas comparten el mismo spec y el mismo revisor.

El número siguiente se obtiene mirando las carpetas existentes en `specs/`,
no el índice: el índice puede quedar desactualizado, las carpetas no. Si dos
specs se crean en paralelo y colisionan, el segundo en integrarse renumera su
carpeta, su campo `ID` y su rama antes de mezclar.

Los identificadores internos (`RF-`, `T-`, `PD-`, `E2E-`) se numeran dentro de
su propio documento y no llevan el número del spec; la carpeta ya da el
contexto. Una referencia desde otro spec se escribe completa:
`SPEC-001 / RF-SEG-004`.

## Índice

| Spec | Nombre | Estado |
|---|---|---|
| [001](001-repo-cv-ats/spec.md) | Repositorio fuente de la verdad para búsqueda de empleo | Aprobado (v0.1, 2026-09-17) |

Cada spec actualiza esta tabla al crearse y al cambiar de estado.

## Orden de trabajo

| Fase | Archivo | Resultado necesario para avanzar |
|---|---|---|
| 1. Definir | `spec.md` | Joseph revisa alcance, reglas, escenarios, exclusiones y puntos abiertos. |
| 2. Validar | `spec.md` | Joseph registra aprobación y versión dentro del archivo, o devuelve ajustes. Sin aprobación no se generan los otros tres documentos. |
| 3. Diseñar | `plan.md` | Se fija la solución, archivos, contratos, formatos y riesgos. |
| 4. Descomponer | `tasks.md` | Cada tarea tiene resultado verificable, dependencias, dueño o subagente, y forma de integración. |
| 5. Verificar | `test-e2e.md` | Se definen recorridos de punta a punta, datos ficticios, ambiente y evidencias antes de implementar. |
| 6. Implementar | Los cuatro | La IA ejecuta tareas aprobadas, integra cambios y registra resultados. |

Si se pide **«crea un spec»**, se crea solo `specs/NNN-slug/spec.md` desde la
plantilla, con el siguiente número libre. Se investiga el estado real del repositorio, se separan hechos de
supuestos y se pide la revisión funcional del documento. No se crean
`plan.md`, `tasks.md` ni `test-e2e.md` por anticipado.

Si se dice **«validé el spec»** o se aprueba una versión concreta, se
registra la aprobación en `spec.md` y se generan los otros tres archivos en
esa misma carpeta. Cada requisito y escenario del spec debe aparecer en el
plan, en una tarea y en una prueba, o llevar una justificación explícita de
por qué no se prueba a ese nivel. Si cambia el alcance después, se vuelve a
revisión funcional antes de ejecutar tareas dependientes del cambio.

Si se dice **«implementa el spec con subagentes»**, `tasks.md` es la lista de
trabajo. Cada subagente recibe objetivo, rutas, contrato de entrada y salida,
prueba y criterio de aceptación. Solo se paralelizan tareas independientes,
con archivos o áreas de edición separados. El coordinador revisa los cambios,
resuelve la integración y comprueba las pruebas; el mensaje «terminado» de un
subagente no constituye evidencia.

## Ubicación y fuentes

Este repositorio es único (no hay separación backend/frontend), por lo que
`plan.md` y `tasks.md` indican rutas relativas a la raíz. Consulta primero
`README.md` y `AGENTS.md` en la raíz; `AGENTS.md` es el contrato operativo
que gobierna cómo se generan los documentos y qué información nunca sale del
equipo local.

Los documentos aprobados no se editan para hacerlos encajar con una
implementación: se registra la contradicción y se solicita decisión.

## Relación con los ADR

Un ADR registra una **decisión de arquitectura**: contexto, opciones,
decisión, consecuencias y estado. Vive en `docs/adr/` de este repositorio.
Esa carpeta se crea cuando exista una decisión que registrar.

Antes de redactar `spec.md`, busca ADR vigentes. Cita en el spec el **ID,
estado y ruta** de cada ADR relevante y explica qué restricción aporta. No
cites «ADR pendiente» como si fuera una decisión aceptada. Si el spec
descubre una decisión de arquitectura nueva, descríbela como punto abierto
sin escoger la opción por Joseph. Después de validar el alcance, el plan
identifica qué ADR debe redactarse; la decisión debe quedar registrada y
revisada antes de ejecutar tareas que dependan de ella.
