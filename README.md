# Skell's ADO

> Este repositorio es una completa reestructuración de mi software "Skell's ADO", al momento de culminarlo se transferirá la propiedad a la organización "Skell's Software"

Este repositorio fue creado con la intención de modificar y reestructurar la aplicación Skell's ADO, desde su funcionalidad hasta su modularidad y versatilidad.

Tambien planeo la posibilidad de implementar ahora el uso de clases para mejorar la usabilidad de los modulos.

## Idea de Reestructuración de Manejo de Datos

```mermaid
flowchart TD
    A[Principal] --> B[Paginas]
    C[Modulos]
    A --> C
    B --> A
    B --> C
    C --> DB[Database]
    DB --> CDB[Conexion a MariaDB]
    CDB --> DB
        