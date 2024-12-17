import flet as ft
from datetime import datetime
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

        # Referencias a campos del formulario para actualizarlos después de seleccionar fecha/hora
        self.fecha_field = None
        self.hora_field = None

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
            fecha_reserva_str = reserva["fecha_reserva"]
            estado = reserva["estado"]

            # Depuración: Imprimir el valor de fecha_reserva_str
            print(f"Procesando reserva ID {reserva_id}: fecha_reserva = {fecha_reserva_str}")

            # Convertir la cadena de fecha a objeto datetime
            fecha_reserva = None
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    fecha_reserva = datetime.strptime(fecha_reserva_str, fmt)
                    break  # Salir del ciclo si la conversión fue exitosa
                except ValueError:
                    continue  # Intentar el siguiente formato

            if not fecha_reserva:
                # Manejar el error si el formato no coincide
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Formato de fecha inválido para la reserva ID {reserva_id}"))
                self.page.snack_bar.open = True
                self.page.update()
                continue  # Saltar a la siguiente reserva

            # Obtener el nombre del usuario y número de mesa
            usuario = next((u for u in self.usuarios if str(u["id"]) == cliente_id), None)
            usuario_nombre = usuario["nombre"] if usuario else "Desconocido"

            mesa = next((m for m in self.mesas if str(m["id"]) == mesa_id), None)
            mesa_numero = mesa["numero_mesa"] if mesa else "Desconocida"

            reserva_item = ft.Row(
                controls=[
                    ft.Text(f"Usuario: {usuario_nombre}"),
                    ft.Text(f"Mesa: {mesa_numero}"),
                    ft.Text(f"Fecha: {fecha_reserva.strftime('%Y-%m-%d %H:%M')}"),
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
        opciones_usuarios.insert(0, ft.dropdown.Option(text="Seleccione un usuario", key=""))

        mesas = self.mesas
        opciones_mesas = [
            ft.dropdown.Option(text=f"{mesa['numero_mesa']}", key=str(mesa["id"]))
            for mesa in mesas
        ]
        opciones_mesas.insert(0, ft.dropdown.Option(text="Seleccione una mesa", key=""))

        self.reserva_id_field = ft.TextField(label="ID", visible=False)
        self.cliente_dropdown = ft.Dropdown(label="Usuario", options=opciones_usuarios)
        self.mesa_id_dropdown = ft.Dropdown(label="Mesa", options=opciones_mesas)

        # Campos para fecha y hora
        self.fecha_field = ft.TextField(label="Fecha", read_only=True)
        self.hora_field = ft.TextField(label="Hora", read_only=True)

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
                    self.cliente_dropdown,
                    self.mesa_id_dropdown,
                    ft.Row([self.fecha_field, btn_seleccionar_fecha]),
                    ft.Row([self.hora_field, btn_seleccionar_hora]),
                    self.estado_field,
                    self.notas_field
                ]),
                width=350,
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

    def on_date_change(self, e):
        if e.control.value:
            self.selected_date = e.control.value
            self.fecha_field.value = self.selected_date.strftime("%Y-%m-%d")
            self.page.update()

    def on_date_dismiss(self, e):
        pass  # No se requiere acción adicional

    def on_time_change(self, e):
        tp: ft.TimePicker = e.control
        if tp.value:
            self.selected_time = tp.value
            self.hora_field.value = self.selected_time.strftime("%H:%M")
            self.page.update()

    def on_time_dismiss(self, e):
        pass  # No se requiere acción adicional

    def pick_date(self, e):
        date_picker = ft.DatePicker(
            first_date=datetime(year=2024, month=10, day=1),
            last_date=datetime(year=2050, month=10, day=1),
            on_change=self.on_date_change,
            on_dismiss=self.on_date_dismiss,
        )
        self.page.overlay.append(date_picker)
        date_picker.open = True
        self.page.update()

    def pick_time(self, e):
        time_picker = ft.TimePicker(
            on_change=self.on_time_change,
            on_dismiss=self.on_time_dismiss,
        )
        self.page.overlay.append(time_picker)
        time_picker.open = True
        self.page.update()

    def crear_reserva(self, e):
        cliente_id = self.cliente_dropdown.value
        mesa_id = self.mesa_id_dropdown.value
        estado = self.estado_field.value
        notas = self.notas_field.value.strip()

        # Combinar fecha y hora usando objetos datetime
        if self.selected_date and self.selected_time:
            fecha_reserva = datetime.combine(self.selected_date, self.selected_time)
        else:
            fecha_reserva = None

        print(f"Fecha seleccionada: {self.selected_date}")
        print(f"Hora seleccionada: {self.selected_time}")
        print(f"Fecha y Hora combinadas: {fecha_reserva}")

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

        if not fecha_reserva:
            if not self.selected_date:
                self.fecha_field.error_text = "Seleccione fecha."
            else:
                self.fecha_field.error_text = None

            if not self.selected_time:
                self.hora_field.error_text = "Seleccione hora."
            else:
                self.hora_field.error_text = None
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
            ft.dropdown.Option(text=f"{user['nombre']}", key=str(user["id"]))
            for user in usuarios
        ]
        opciones_usuarios.insert(0, ft.dropdown.Option(text="Seleccione un usuario", key=""))

        mesas = self.mesas
        opciones_mesas = [
            ft.dropdown.Option(text=f"{mesa['numero_mesa']}", key=str(mesa["id"]))
            for mesa in mesas
        ]
        opciones_mesas.insert(0, ft.dropdown.Option(text="Seleccione una mesa", key=""))

        fecha_completa = reserva["fecha_reserva"]
        if isinstance(fecha_completa, str):
            # Si fecha_completa es una cadena, parsearla
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    fecha_completa = datetime.strptime(fecha_completa, fmt)
                    break
                except ValueError:
                    continue
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Formato de fecha inválido para la reserva ID {reserva_id}"))
                self.page.snack_bar.open = True
                self.page.update()
                return

        fecha_val = fecha_completa.strftime("%Y-%m-%d")
        hora_val = fecha_completa.strftime("%H:%M")

        self.selected_date = fecha_completa.date()
        self.selected_time = fecha_completa.time()

        self.reserva_id_field = ft.TextField(label="ID", disabled=True, value=str(reserva["id"]))
        self.cliente_dropdown = ft.Dropdown(
            label="Usuario",
            options=opciones_usuarios,
            value=str(reserva["cliente_id"]),
        )

        self.mesa_id_dropdown = ft.Dropdown(
            label="Mesa",
            options=opciones_mesas,
            value=str(reserva["mesa_id"]),
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
                width=350,
            ),
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

        # Combinar fecha y hora
        fecha = self.fecha_field.value.strip()
        hora = self.hora_field.value.strip()

        if fecha and hora:
            try:
                fecha_reserva = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            except ValueError:
                self.page.snack_bar = ft.SnackBar(ft.Text("Fecha y hora inválidas. Formato esperado: YYYY-MM-DD HH:MM"))
                self.page.snack_bar.open = True
                self.page.update()
                return
        else:
            fecha_reserva = None

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
            if not fecha:
                self.fecha_field.error_text = "Seleccione fecha."
            else:
                self.fecha_field.error_text = None

            if not hora:
                self.hora_field.error_text = "Seleccione hora."
            else:
                self.hora_field.error_text = None
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