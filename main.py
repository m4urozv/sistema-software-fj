from abc import ABC, abstractmethod
from datetime import datetime
import logging
import os

# ==========================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================
LOG_FILENAME = "sistema_software_fj.log"

logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================
class SoftwareFJError(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""

    pass


class InvalidDataError(SoftwareFJError):
    """Se lanza cuando los datos ingresados no cumplen con las validaciones."""

    pass


class ServiceUnavailableError(SoftwareFJError):
    """Se lanza cuando un servicio no está disponible o no se puede procesar."""

    pass


class InvalidReservationError(SoftwareFJError):
    """Se lanza cuando una operación de reserva es incorrecta o inválida."""

    pass


# ==========================================
# CLASE ABSTRACTA BASE (ENTIDAD GENERAL)
# ==========================================
class EntidadBase(ABC):

    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self) -> str:
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass


# ==========================================
# CLASE CLIENTE
# ==========================================
class Cliente(EntidadBase):

    def __init__(
        self, identificador: str, nombre: str, correo: str, telefono: str
    ):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise InvalidDataError(
                "El nombre del cliente no puede estar vacío."
            )
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise InvalidDataError(f"El correo electrónico '{valor}' es inválido.")
        self._correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise InvalidDataError(
                f"El número de teléfono '{valor}' es inválido (debe contener solo dígitos y al menos 7 caracteres)."
            )
        self._telefono = valor.strip()

    def obtener_detalles(self) -> str:
        return f"Cliente [ID: {self.identificador}] - Nombre: {self.nombre}, Correo: {self.correo}, Teléfono: {self.telefono}"


# ==========================================
# CLASE ABSTRACTA SERVICIO
# ==========================================
class Servicio(ABC):

    def __init__(self, codigo: str, nombre: str, costo_base: float):
        self._codigo = codigo
        self._nombre = nombre
        self._costo_base = costo_base

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def costo_base(self) -> float:
        return self._costo_base

    @costo_base.setter
    def costo_base(self, valor: float):
        if valor < 0:
            raise InvalidDataError("El costo base no puede ser negativo.")
        self._costo_base = valor

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass


# ==========================================
# SERVICIOS ESPECIALIZADOS
# ==========================================
class ReservaSalas(Servicio):

    def __init__(
        self,
        codigo: str,
        nombre: str,
        costo_base: float,
        capacidad: int,
        tiene_proyector: bool,
    ):
        super().__init__(codigo, nombre, costo_base)
        self.capacidad = capacidad
        self.tiene_proyector = tiene_proyector

    @property
    def capacidad(self) -> str:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int):
        if valor <= 0:
            raise InvalidDataError("La capacidad de la sala debe ser mayor a 0.")
        self._capacidad = valor

    # Métodos sobrecargados simulados mediante argumentos opcionales
    def calcular_costo(
        self, horas: int, aplicar_impuesto: bool = True, descuento: float = 0.0
    ) -> float:
        try:
            if horas <= 0:
                raise InvalidDataError(
                    "Las horas de reserva deben ser mayores a cero."
                )
            if descuento < 0 or descuento > 1:
                raise InvalidDataError(
                    "El porcentaje de descuento debe estar entre 0 y 1."
                )

            subtotal = self.costo_base * horas
            if self.tiene_proyector:
                subtotal += 20.0  # Cargo extra por proyector

            subtotal_con_descuento = subtotal * (1 - descuento)

            if aplicar_impuesto:
                total = subtotal_con_descuento * 1.19  # IVA 19%
            else:
                total = subtotal_con_descuento

            return round(total, 2)
        except Exception as e:
            if not isinstance(e, SoftwareFJError):
                raise SoftwareFJError(
                    f"Error inesperado en cálculo de sala: {e}"
                ) from e
            raise

    def describir_servicio(self) -> str:
        proyector_str = "Sí" if self.tiene_proyector else "No"
        return f"Reserva de Sala [Código: {self.codigo}] - {self.nombre} | Capacidad: {self.capacidad} personas | Proyector: {proyector_str} | Costo Base/h: ${self.costo_base}"


class AlquilerEquipos(Servicio):

    def __init__(
        self, codigo: str, nombre: str, costo_base: float, serial_equipo: str
    ):
        super().__init__(codigo, nombre, costo_base)
        self.serial_equipo = serial_equipo

    def calcular_costo(
        self, dias: int, seguro_adicional: bool = False
    ) -> float:
        try:
            if dias <= 0:
                raise InvalidDataError(
                    "Los días de alquiler deben ser mayores a cero."
                )

            subtotal = self.costo_base * dias
            if seguro_adicional:
                subtotal += 15.0 * dias  # Costo diario del seguro

            total = subtotal * 1.19  # IVA
            return round(total, 2)
        except Exception as e:
            if not isinstance(e, SoftwareFJError):
                raise SoftwareFJError(
                    f"Error inesperado en cálculo de equipo: {e}"
                ) from e
            raise

    def describir_servicio(self) -> str:
        return f"Alquiler de Equipo [Código: {self.codigo}] - {self.nombre} | Serial: {self.serial_equipo} | Costo Base/día: ${self.costo_base}"


class AsesoriaEspecializada(Servicio):

    def __init__(
        self,
        codigo: str,
        nombre: str,
        costo_base: float,
        area_experticia: str,
    ):
        super().__init__(codigo, nombre, costo_base)
        self.area_experticia = area_experticia

    def calcular_costo(
        self, sesiones: int, complejidad_alta: bool = False
    ) -> float:
        try:
            if sesiones <= 0:
                raise InvalidDataError(
                    "El número de sesiones debe ser mayor a cero."
                )

            factor_complejidad = 1.5 if complejidad_alta else 1.0
            total = (self.costo_base * sesiones * factor_complejidad) * 1.19
            return round(total, 2)
        except Exception as e:
            if not isinstance(e, SoftwareFJError):
                raise SoftwareFJError(
                    f"Error inesperado en cálculo de asesoría: {e}"
                ) from e
            raise

    def describir_servicio(self) -> str:
        return f"Asesoría Especializada [Código: {self.codigo}] - {self.nombre} | Área: {self.area_experticia} | Costo Base/sesión: ${self.costo_base}"


# ==========================================
# CLASE RESERVA
# ==========================================
class Reserva:

    contador_reservas = 1000

    def __init__(self, cliente: Cliente, servicio: Servicio, cantidad: int):
        Reserva.contador_reservas += 1
        self.id_reserva = f"RES-{Reserva.contador_reservas}"
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def procesar_reserva(self, *args, **kwargs):
        """Bloques try/except/else/finally con manejo robusto y encadenamiento"""
        try:
            logging.info(
                f"Iniciando procesamiento de reserva {self.id_reserva} para cliente {self.cliente.identificador}."
            )
            if not self.cliente or not self.servicio:
                raise InvalidReservationError(
                    "La reserva carece de cliente o servicio válido."
                )

            # Polimorfismo en cálculo de costo según tipo de servicio
            if isinstance(self.servicio, ReservaSalas):
                horas = self.cantidad
                aplicar_imp = kwargs.get("aplicar_impuesto", True)
                desc = kwargs.get("descuento", 0.0)
                self.costo_total = self.servicio.calcular_costo(
                    horas, aplicar_impuesto=aplicar_imp, descuento=desc
                )
            elif isinstance(self.servicio, AlquilerEquipos):
                dias = self.cantidad
                seguro = kwargs.get("seguro_adicional", False)
                self.costo_total = self.servicio.calcular_costo(
                    dias, seguro_adicional=seguro
                )
            elif isinstance(self.servicio, AsesoriaEspecializada):
                sesiones = self.cantidad
                complejidad = kwargs.get("complejidad_alta", False)
                self.costo_total = self.servicio.calcular_costo(
                    sesiones, complejidad_alta=complejidad
                )
            else:
                raise ServiceUnavailableError(
                    "Tipo de servicio no reconocido por el sistema."
                )

        except (InvalidDataError, ServiceUnavailableError) as e:
            self.estado = "FALLIDA"
            logging.error(
                f"Fallo controlado en reserva {self.id_reserva}: {e}"
            )
            # Encadenamiento de excepciones
            raise InvalidReservationError(
                f"No se pudo completar la reserva {self.id_reserva} debido a un error de validación."
            ) from e
        except Exception as e:
            self.estado = "ERROR_CRITICO"
            logging.critical(
                f"Error crítico no controlado en reserva {self.id_reserva}: {e}"
            )
            raise SoftwareFJError(
                f"Error crítico procesando la reserva {self.id_reserva}."
            ) from e
        else:
            self.estado = "CONFIRMADA"
            logging.info(
                f"Reserva {self.id_reserva} confirmada con éxito. Costo Total: ${self.costo_total}"
            )
        finally:
            logging.info(
                f"Finalizó el ciclo de procesamiento para la reserva {self.id_reserva}. Estado actual: {self.estado}."
            )

    def cancelar_reserva(self):
        try:
            if self.estado == "CANCELADA":
                raise InvalidReservationError(
                    "La reserva ya se encontraba cancelada."
                )
            self.estado = "CANCELADA"
            logging.info(
                f"La reserva {self.id_reserva} ha sido cancelada exitosamente."
            )
        except Exception as e:
            logging.error(
                f"Error al intentar cancelar la reserva {self.id_reserva}: {e}"
            )
            raise


# ==========================================
# SIMULACIÓN DE 10 OPERACIONES COMPLETAS
# ==========================================
def ejecutar_simulacion():
    print("=" * 70)
    print(" INICIO DE LA SIMULACIÓN - SISTEMA SOFTWARE FJ")
    print("=" * 70)

    # Limpiar archivo de log anterior si existe para una ejecución limpia
    if os.path.exists(LOG_FILENAME):
        open(LOG_FILENAME, "w").close()

    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    # Operación 1: Registro Válido de Cliente
    print(
        "\n--- Operación 1: Registro Válido de Cliente y Creación de Servicio ---"
    )
    try:
        cliente1 = Cliente(
            "C101",
            "Carlos Mendoza",
            "carlos.mendoza@email.com",
            "3101234567",
        )
        lista_clientes.append(cliente1)
        print(f"[ÉXITO] {cliente1.obtener_detalles()}")

        sala1 = ReservaSalas(
            "S001", "Sala Ejecutiva Alpha", 50.0, 10, tiene_proyector=True
        )
        lista_servicios.append(sala1)
        print(f"[ÉXITO] {sala1.describir_servicio()}")
    except Exception as e:
        print(f"[ERROR ESPERADO] {e}")

    # Operación 2: Registro Inválido de Cliente (Correo incorrecto)
    print("\n--- Operación 2: Registro Inválido de Cliente (Correo) ---")
    try:
        cliente_malo = Cliente(
            "C102", "Ana Gómez", "correo_invalido_sin_arroba", "3209876543"
        )
        lista_clientes.append(cliente_malo)
    except InvalidDataError as e:
        print(
            f"[CAPTURA DE EXCEPCIÓN CORRECTA] Error detectado y registrado: {e}"
        )
        logging.warning(
            f"Operación 2 rechazada correctamente por validación: {e}"
        )

    # Operación 3: Creación correcta de servicio de Alquiler de Equipos
    print("\n--- Operación 3: Creación de Servicio Alquiler de Equipos ---")
    try:
        equipo1 = AlquilerEquipos(
            "E001",
            "Laptop Core i7 Alta Gama",
            30.0,
            serial_equipo="SN-998877",
        )
        lista_servicios.append(equipo1)
        print(f"[ÉXITO] {equipo1.describir_servicio()}")
    except Exception as e:
        print(f"[ERROR ESPERADO] {e}")

    # Operación 4: Creación de Asesoría Especializada con costo negativo (Inválido)
    print(
        "\n--- Operación 4: Creación de Asesoría con Costo Base Inválido ---"
    )
    try:
        asesoria_mala = AsesoriaEspecializada(
            "A001", "Consultoría Cloud", -100.0, "AWS Architecture"
        )
        lista_servicios.append(asesoria_mala)
    except InvalidDataError as e:
        print(
            f"[CAPTURA DE EXCEPCIÓN CORRECTA] Error detectado y registrado: {e}"
        )
        logging.warning(
            f"Operación 4 rechazada correctamente por validación: {e}"
        )

    # Operación 5: Creación correcta de Asesoría Especializada
    print(
        "\n--- Operación 5: Creación Exitosa de Asesoría Especializada ---"
    )
    try:
        asesoria1 = AsesoriaEspecializada(
            "A002", "Consultoría Ciberseguridad", 80.0, "Ethical Hacking"
        )
        lista_servicios.append(asesoria1)
        print(f"[ÉXITO] {asesoria1.describir_servicio()}")
    except Exception as e:
        print(f"[ERROR ESPERADO] {e}")

    # Operación 6: Reserva Exitosa de Sala (Polimorfismo y Sobrecarga)
    print("\n--- Operación 6: Procesamiento de Reserva Exitosa (Sala) ---")
    try:
        reserva1 = Reserva(cliente1, sala1, cantidad=4)  # 4 horas
        reserva1.procesar_reserva(
            aplicar_impuesto=True, descuento=0.1
        )  # 10% descuento
        lista_reservas.append(reserva1)
        print(
            f"[ÉXITO] Reserva ID: {reserva1.id_reserva} | Estado: {reserva1.estado} | Costo Total: ${reserva1.costo_total}"
        )
    except Exception as e:
        print(f"[ERROR] {e}")

    # Operación 7: Reserva Fallida por Cantidad Inválida de Días (Alquiler de Equipos)
    print(
        "\n--- Operación 7: Reserva Fallida por Cantidad de Días Negativa ---"
    )
    try:
        cliente2 = Cliente(
            "C103",
            "Lucía Pérez",
            "lucia.perez@email.com",
            "3154443322",
        )
        reserva2 = Reserva(cliente2, equipo1, cantidad=-3)  # Días negativos
        reserva2.procesar_reserva(seguro_adicional=True)
        lista_reservas.append(reserva2)
    except (InvalidReservationError, InvalidDataError) as e:
        print(
            f"[CAPTURA DE EXCEPCIÓN CORRECTA] Excepción controlada: {e.__cause__ or e}"
        )

    # Operación 8: Reserva Exitosa de Asesoría Especializada
    print(
        "\n--- Operación 8: Procesamiento de Reserva Exitosa (Asesoría) ---"
    )
    try:
        reserva3 = Reserva(
            cliente2, asesoria1, cantidad=2
        )  # 2 sesiones, complejidad alta
        reserva3.procesar_reserva(complejidad_alta=True)
        lista_reservas.append(reserva3)
        print(
            f"[ÉXITO] Reserva ID: {reserva3.id_reserva} | Estado: {reserva3.estado} | Costo Total: ${reserva3.costo_total}"
        )
    except Exception as e:
        print(f"[ERROR] {e}")

    # Operación 9: Cancelación de Reserva Existente
    print("\n--- Operación 9: Cancelación de una Reserva ---")
    try:
        print(f"Estado previo de {reserva1.id_reserva}: {reserva1.estado}")
        reserva1.cancelar_reserva()
        print(f"Estado posterior de {reserva1.id_reserva}: {reserva1.estado}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # Operación 10: Intento de Cancelar una Reserva Ya Cancelada (Excepción Controlada)
    print(
        "\n--- Operación 10: Intento de Recancelar una Reserva Cancelada ---"
    )
    try:
        reserva1.cancelar_reserva()
    except Exception as e:
        print(
            f"[CAPTURA DE EXCEPCIÓN CORRECTA] Operación bloqueada con éxito: {e}"
        )
        logging.warning(f"Operación 10 controlada correctamente: {e}")

    print("=" * 70)
    print(" FIN DE LA SIMULACIÓN - SISTEMA ESTABLE Y OPERATIVO")
    print(f" Revise el archivo '{LOG_FILENAME}' para verificar el registro de eventos.")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_simulacion()