# sistema-software-fj
Fase 4 - componente práctico -- Sistema integral orientado a objetos para gestión de clientes, servicios y reservas


 **Estudiante: Mauricio Zapata (trabajo desarrollado individualmente por dificultades de disponibilidad de tiempo)
 **Curso:** Programación / Universidad Nacional Abierta y a Distancia (UNAD)

---

## Arquitectura y Principios de POO
El sistema aplica estrictamente los pilares fundamentales de la Programación Orientada a Objetos:
1. **Abstracción:** Uso de clases abstractas (`EntidadBase`, `Servicio`) mediante el módulo `abc` para definir contratos obligatorios.
2. **Herencia:** Clases especializadas que heredan comportamiento y atributos de la clase base (`ReservaSalas`, `AlquilerEquipos`, `AsesoriaEspecializada`).
3. **Polimorfismo:** Implementación de métodos sobrescritos (`calcular_costo` y `describir_servicio`) con comportamientos adaptados a cada tipo de servicio.
4. **Encapsulación:** Protección de datos personales y atributos críticos mediante propiedades (`@property` y setters) con validaciones estrictas.

---

# Manejo Avanzado de Excepciones y Logs
La aplicación garantiza estabilidad continua ante fallos mediante:
 **Excepciones Personalizadas:** `SoftwareFJError`, `InvalidDataError`, `ServiceUnavailableError` e `InvalidReservationError`.
 **Estructuras de Control Avanzadas:** Uso intensivo de bloques `try / except / else / finally`.
 **Encadenamiento de Excepciones:** Trazabilidad limpia usando `from e`.
 **Sistema de Auditoría:** Registro automático de todos los eventos y errores críticos en el archivo `sistema_software_fj.log`.

---

## Requisitos y Ejecución

### Requisitos previos
* Tener instalado **Python 3.x** en el computador que ejecutará el codigo

### Instrucciones de ejecución
1. Clonar el repositorio en equipo local:
   ```bash
   git clone [https://github.com/m4urozv/sistema-software-fj.git](https://github.com/m4urozv/sistema-software-fj.git)
   cd sistema-software-fj