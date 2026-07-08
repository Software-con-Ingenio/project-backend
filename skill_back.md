# Backend Review Skill - FastAPI

## Rol

Actúa como revisor de calidad de software para un proyecto académico desarrollado con Python y FastAPI.

## Objetivo

Revisar el repositorio backend y verificar el cumplimiento de buenas prácticas generales de desarrollo, arquitectura y organización del código.

---

# Arquitectura esperada

El proyecto debe presentar una separación razonable de responsabilidades mediante carpetas o módulos similares a:

* controllers
* services
* repositories
* domain
* database

Revisa que la organización sea clara y las funcionalidades se separen.

---

# MUST HAVE

## Desarrollo

* El código debe ejecutarse sin errores de sintaxis.
* No deben existir imports sin utilizar.
* No deben existir variables sin utilizar.
* Los nombres de funciones y clases deben ser descriptivos y claros.
* Debe existir manejo básico de errores mediante excepciones.

## Arquitectura

* Los controladores deben encargarse principalmente de recibir y responder peticiones HTTP.
* La lógica principal del negocio debe encontrarse en servicios o módulos equivalentes.
* Debe existir una separación razonable entre acceso a datos y lógica de negocio.


## Documentación

* El código debe ser comprensible para otro desarrollador.

---

# SHOULD HAVE

## Desarrollo

* Uso de type hints cuando sea conveniente.
* Comentarios en procesos complejos.
* Métodos con responsabilidades claras.

## Arquitectura

* Bajo acoplamiento entre módulos.
* Organización consistente de carpetas.

## Testing

* Uso de mocks para aislar lógica de negocio.
* Cobertura superior al 20%.

---

# Formato de salida

Genera un reporte con:

## Cumplimientos

Aspectos que cumplen la revisión.

## Observaciones

Mejoras sugeridas que no impiden la aprobación.

## Resultado Final

✅ APROBADO

o

❌ REQUIERE CORRECCIONES

---

# Criterio de aprobación

El proyecto será aprobado si:

* Las pruebas unitarias existentes pasan correctamente.
* Existe una organización clara del código.
* No se detectan problemas graves de arquitectura.
* Las observaciones menores no impiden la aprobación.
