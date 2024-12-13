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
        # Variables para almacenar fecha y hora temporalmente
        self.selected_date = None
        self.selected_time = None

    def load_reservas(self):
        self.reservas = leer_reservas()

    def load_mesas(self):
        self.mesas = leer_mesas()

    def load_usuarios(self):
        self.usuarios = leer_usuarios()

    def get_view(self):
        btn_nueva_reserva = ft.ElevatedButton("Nueva Reserva", on_click=self.show_form_crear)
        self.refresh_list()
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
        opciones_usuarios.insert(0, ft.dropdown.Option(text="Seleccione un usuario"))

        mesas = self.mesas
        opciones_mesas = [
            ft.dropdown.Option(text=f"{mesa['numero_mesa']}", key=str(mesa["id"]))
            for mesa in mesas
        ]
        opciones_mesas.insert(0, ft.dropdown.Option(text="Seleccione una mesa"))

        # Campos del formulario
        self.reserva_id_field = ft.TextField(label="ID")
        self.cliente_dropdown = ft.Dropdown(label="Usuario", options=opciones_usuarios)
        self.mesa_id_dropdown = ft.Dropdown(label="Mesa", options=opciones_mesas)

        # Campos para fecha y hora
        self.fecha_field = ft.TextField(label="Fecha", read_only=True)
        self.hora_field = ft.TextField(label="Hora", read_only=True)

        # Botones para seleccionar fecha y hora
        btn_seleccionar_fecha = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=self.pick_date
        )
        btn_seleccionar_hora = ft.IconButton(
            icon=ft.icons.ACCESS_TIME,
            on_click=self.pick_time
        )

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
            content=ft.Container(
                content=ft.Column([
                    self.reserva_id_field,
                    self.cliente_dropdown,
                    self.mesa_id_dropdown,
                    ft.Row([self.fecha_field, btn_seleccionar_fecha]),
                    ft.Row([self.hora_field, btn_seleccionar_hora]),
                    self.estado_field,
                    self.notas_field
                ]),
                width=500,  # Ajusta este valor a tus necesidades
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Crear", on_click=self.crear_reserva),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    async def pick_date(self, e):
        selected = await self.page.show_date_picker()
        if selected:
            self.selected_date = selected.strftime("%Y-%m-%d")
            self.fecha_field.value = self.selected_date
            self.page.update()

    async def pick_time(self, e):
        selected = await self.page.show_time_picker()
        if selected:
            self.selected_time = selected.strftime("%H:%M")
            self.hora_field.value = self.selected_time
            self.page.update()

    def crear_reserva(self, e):
        reserva_id = self.reserva_id_field.value.strip()
        cliente_id = self.cliente_dropdown.value
        mesa_id = self.mesa_id_dropdown.value
        estado = self.estado_field.value
        notas = self.notas_field.value.strip()

        # Combinar fecha y hora
        fecha = self.fecha_field.value.strip()
        hora = self.hora_field.value.strip()
        fecha_reserva = ""
        if fecha and hora:
            fecha_reserva = f"{fecha} {hora}"
        else:
            fecha_reserva = ""  # Forzar error de validación si falta algo

        # Validaciones
        hay_error = False
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

        if not fecha or not hora:
            self.fecha_field.error_text = "Seleccione fecha."
            self.hora_field.error_text = "Seleccione hora."
            hay_error = True
        else:
            self.fecha_field.error_text = None
            self.hora_field.error_text = None

        self.page.update()

        if hay_error:
            return

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

        usuarios = self.usuarios
        opciones_usuarios = [
            ft.dropdown.Option(text=f"{user['nombre']}", key=user["id"])
            for user in usuarios
        ]
        opciones_usuarios.insert(0, ft.dropdown.Option(text="Seleccione un usuario"))

        mesas = self.mesas
        opciones_mesas = [
            ft.dropdown.Option(text=f"{mesa['numero_mesa']}", key=mesa["id"])
            for mesa in mesas
        ]
        opciones_mesas.insert(0, ft.dropdown.Option(text="Seleccione una mesa"))

        # Separar fecha y hora de la reserva actual
        # Asumiendo que reserva["fecha_reserva"] es algo como "YYYY-MM-DD HH:MM"
        fecha_completa = reserva["fecha_reserva"]
        fecha_partes = fecha_completa.split(" ")
        fecha_val = fecha_partes[0] if len(fecha_partes) > 0 else ""
        hora_val = fecha_partes[1] if len(fecha_partes) > 1 else ""

        # Guardar en variables para el picker
        self.selected_date = fecha_val
        self.selected_time = hora_val

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

        self.fecha_field = ft.TextField(label="Fecha", read_only=True, value=fecha_val)
        self.hora_field = ft.TextField(label="Hora", read_only=True, value=hora_val)

        btn_seleccionar_fecha = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=self.pick_date
        )
        btn_seleccionar_hora = ft.IconButton(
            icon=ft.icons.ACCESS_TIME,
            on_click=self.pick_time
        )

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
                ft.Row([self.fecha_field, btn_seleccionar_fecha]),
                ft.Row([self.hora_field, btn_seleccionar_hora]),
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
        estado = self.estado_field.value
        notas = self.notas_field.value.strip()

        fecha = self.fecha_field.value.strip()
        hora = self.hora_field.value.strip()

        if fecha and hora:
            fecha_reserva = f"{fecha} {hora}"
        else:
            fecha_reserva = ""

        # Validaciones
        hay_error = False
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

        if not fecha or not hora:
            self.fecha_field.error_text = "Seleccione fecha."
            self.hora_field.error_text = "Seleccione hora."
            hay_error = True
        else:
            self.fecha_field.error_text = None
            self.hora_field.error_text = None

        self.page.update()

        if hay_error:
            return

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
