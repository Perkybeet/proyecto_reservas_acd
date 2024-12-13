import flet as ft
from services.crud_operations import (
    leer_reservas,
    insertar_reserva,
    actualizar_reserva,
    eliminar_reserva,
    leer_mesas,
    leer_usuarios
)
from models.reserva_model import ReservaModel
from bson.objectid import ObjectId
from utils.validators import validate_fecha

class ReservaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.reservas = []
        self.mesas = []
        self.usuarios = []
        self.list_view = ft.Column()
        self.load_reservas()
        self.load_mesas()
        self.load_usuarios()

    def load_reservas(self):
        self.reservas = leer_reservas()

    def load_mesas(self):
        self.mesas = leer_mesas()

    def load_usuarios(self):
        self.usuarios = leer_usuarios()

    def get_view(self):
        btn_nueva_reserva = ft.ElevatedButton("Nueva Reserva", on_click=self.show_form_crear)

        # Obtener el listado de reservas
        self.refresh_list()

        # Agregar controles a la vista
        view = ft.Column(
            controls=[
                btn_nueva_reserva,
                self.list_view
            ],
            scroll=ft.ScrollMode.AUTO
        )
        return view

    def refresh_list(self):
        self.load_reservas()
        self.list_view.controls.clear()
        for reserva in self.reservas:
            reserva_id = str(reserva["id"])
            cliente_id = reserva["cliente_id"]
            mesa_id = reserva["mesa_id"]
            fecha_reserva = reserva["fecha_reserva"]
            estado = reserva["estado"]

            # Obtener el nombre del usuario y número de mesa
            usuario = next((u for u in self.usuarios if str(u["id"]) == cliente_id), None)
            usuario_nombre = usuario["nombre"] if usuario else "Desconocido"

            mesa = next((m for m in self.mesas if str(m["id"]) == mesa_id), None)
            mesa_numero = mesa["numero_mesa"] if mesa else "Desconocida"
            ###

            reserva_item = ft.Row(
                controls=[
                    ft.Text(f"Usuario: {usuario_nombre}"),
                    ft.Text(f"Mesa: {mesa_numero}"),
                    ft.Text(f"Fecha: {fecha_reserva}"),
                    ft.Text(f"Estado: {estado}"),
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, rid=reserva_id: self.show_form_editar(rid)),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, rid=reserva_id: self.confirm_delete(rid)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.list_view.controls.append(reserva_item)
        self.page.update()

    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def show_form_crear(self, e):
        usuarios = self.usuarios
        opciones_usuarios = [
            ft.dropdown.Option(text=f"{user['nombre']}", key=str(user["id"]))
            for user in usuarios
        ]
        # Agregar una opción predeterminada
        opciones_usuarios.insert(0, ft.dropdown.Option(text="Seleccione un usuario"))

        # Obtener todas las mesas para el Dropdown
        mesas = self.mesas
        opciones_mesas = [
            ft.dropdown.Option(text=f"{mesa['numero_mesa']}", key=str(mesa["id"]))
            for mesa in mesas
        ]
        # Agregar una opción predeterminada
        opciones_mesas.insert(0, ft.dropdown.Option(text="Seleccione una mesa"))

        # Campos del formulario
        self.reserva_id_field = ft.TextField(label="ID")
        self.cliente_dropdown = ft.Dropdown(label="Usuario", options=opciones_usuarios,)
        self.mesa_id_dropdown = ft.Dropdown(label="Mesa", options=opciones_mesas)
        self.fecha_reserva_field = ft.TextField(label="Fecha Reserva (YYYY-MM-DD)")
        self.estado_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option(text="Pendiente"),
                ft.dropdown.Option(text="Confirmada"),
                ft.dropdown.Option(text="Cancelada"),
            ],
            value="Pendiente"
        )
        self.notas_field = ft.TextField(label="Notas")

        self.form = ft.AlertDialog(
            title=ft.Text("Crear Nueva Reserva"),
            content=ft.Column([
                self.reserva_id_field,
                self.cliente_dropdown,
                self.mesa_id_dropdown,
                self.fecha_reserva_field,
                self.estado_field,
                self.notas_field
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Crear", on_click=self.crear_reserva),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    def crear_reserva(self, e):
        reserva_id = self.reserva_id_field.value.strip()
        cliente_id = self.cliente_dropdown.value
        mesa_id = self.mesa_id_dropdown.value
        fecha_reserva = self.fecha_reserva_field.value.strip()
        estado = self.estado_field.value
        notas = self.notas_field.value.strip()

        # Inicializar un flag para detectar errores
        hay_error = False

        # Validar campos obligatorios
        if not cliente_id:
            self.cliente_dropdown.error_text = "Seleccione un usuario."
            hay_error = True
        else:
            self.cliente_dropdown.error_text = None

        if not mesa_id:
            self.mesa_id_dropdown.error_text = "Seleccione una mesa."
            hay_error = True
        else:
            self.mesa_id_dropdown.error_text = None

        if not fecha_reserva:
            self.fecha_reserva_field.error_text = "Este campo es obligatorio."
            hay_error = True
        else:
            self.fecha_reserva_field.error_text = None

        self.page.update()

        if hay_error:
            return  # Detener la ejecución si hay errores

        try:
            validate_fecha(fecha_reserva)
            reserva = ReservaModel(
                id=reserva_id,
                cliente_id=cliente_id,
                mesa_id=mesa_id,
                fecha_reserva=fecha_reserva,
                estado=estado,
                notas=notas
            )
            insertar_reserva(reserva)
            self.close_dialog()
            self.refresh_list()
        except ValueError as ve:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            self.page.snack_bar.open = True
            self.page.update()

    def show_form_editar(self, reserva_id):
        reserva = next((r for r in self.reservas if str(r["id"]) == reserva_id), None)
        if not reserva:
            return

        # Obtener todos los usuarios para el Dropdown
        usuarios = self.usuarios
        opciones_usuarios = [
            ft.dropdown.Option(text=f"{user['nombre']}", key=user["id"])
            for user in usuarios
        ]
        opciones_usuarios.insert(0, ft.dropdown.Option(text="Seleccione un usuario"))

        # Obtener todas las mesas para el Dropdown
        mesas = self.mesas
        opciones_mesas = [
            ft.dropdown.Option(text=f"{mesa['numero_mesa']}", key=mesa["id"])
            for mesa in mesas
        ]
        opciones_mesas.insert(0, ft.dropdown.Option(text="Seleccione una mesa"))

        # Campos del formulario con valores prellenados
        self.reserva_id_field = ft.TextField(label="ID", disabled=True, value=str(reserva["id"]))
        self.cliente_dropdown = ft.Dropdown(
            label="Usuario",
            options=opciones_usuarios,
            value=reserva["cliente_id"],
        )

        self.mesa_id_dropdown = ft.Dropdown(
            label="Mesa",
            options=opciones_mesas,
            value=reserva["mesa_id"],
        )

        self.fecha_reserva_field = ft.TextField(label="Fecha Reserva (YYYY-MM-DD)", value=reserva["fecha_reserva"])
        self.estado_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option(text="Pendiente"),
                ft.dropdown.Option(text="Confirmada"),
                ft.dropdown.Option(text="Cancelada"),
            ],
            value=reserva["estado"]
        )
        self.notas_field = ft.TextField(label="Notas", value=reserva.get("notas", ""))

        self.form = ft.AlertDialog(
            title=ft.Text("Editar Reserva"),
            content=ft.Column([
                self.reserva_id_field,
                self.cliente_dropdown,
                self.mesa_id_dropdown,
                self.fecha_reserva_field,
                self.estado_field,
                self.notas_field
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Actualizar", on_click=lambda e: self.actualizar_reserva(reserva_id)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    def actualizar_reserva(self, reserva_id):
        cliente_id = self.cliente_dropdown.value
        mesa_id = self.mesa_id_dropdown.value
        fecha_reserva = self.fecha_reserva_field.value.strip()
        estado = self.estado_field.value
        notas = self.notas_field.value.strip()

        # Inicializar un flag para detectar errores
        hay_error = False

        # Validar campos obligatorios
        if not cliente_id:
            self.cliente_dropdown.error_text = "Seleccione un usuario."
            hay_error = True
        else:
            self.cliente_dropdown.error_text = None

        if not mesa_id:
            self.mesa_id_dropdown.error_text = "Seleccione una mesa."
            hay_error = True
        else:
            self.mesa_id_dropdown.error_text = None

        if not fecha_reserva:
            self.fecha_reserva_field.error_text = "Este campo es obligatorio."
            hay_error = True
        else:
            self.fecha_reserva_field.error_text = None

        self.page.update()

        if hay_error:
            return  # Detener la ejecución si hay errores

        try:
            validate_fecha(fecha_reserva)
            reserva = ReservaModel(
                id=reserva_id,
                cliente_id=cliente_id,
                mesa_id=mesa_id,
                fecha_reserva=fecha_reserva,
                estado=estado,
                notas=notas
            )
            actualizar_reserva(reserva_id, reserva)
            self.close_dialog()
            self.refresh_list()
        except ValueError as ve:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            self.page.snack_bar.open = True
            self.page.update()

    def confirm_delete(self, reserva_id):
        confirm = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Estás seguro de que deseas eliminar esta reserva?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Eliminar", on_click=lambda e: self.eliminar_reserva(reserva_id)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = confirm
        confirm.open = True
        self.page.update()

    def eliminar_reserva(self, reserva_id):
        eliminar_reserva(reserva_id)
        self.close_dialog()
        self.refresh_list()