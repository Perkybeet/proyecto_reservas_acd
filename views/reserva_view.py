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
        self.reservas = []  # Lista para almacenar reservas
        self.mesas = []     # Lista para almacenar mesas
        self.usuarios = []  # Lista para almacenar usuarios
        self.list_view = ft.Column(spacing=15)  # Columna para listar tarjetas de reservas
        self.load_mesas()   # Carga inicial de mesas
        self.load_usuarios()# Carga inicial de usuarios
        self.selected_date = None  # Fecha seleccionada para filtrar reservas

    def load_reservas(self, fecha=None):
        # Carga reservas desde la base de datos, opcionalmente filtradas por fecha
        self.reservas = leer_reservas(fecha)

    def load_mesas(self):
        # Carga mesas desde la base de datos
        self.mesas = leer_mesas()

    def load_usuarios(self):
        # Carga usuarios desde la base de datos
        self.usuarios = leer_usuarios()

    def get_view(self):
        # Botón de DatePicker para filtrar reservas por fecha
        date_picker_button = ft.IconButton(
            icon=ft.icons.DATE_RANGE,
            tooltip="Seleccionar Fecha",
            on_click=self.pick_filter_date,
            icon_color=ft.colors.BLUE_500
        )

        # Texto para mostrar la fecha seleccionada o indicar que se muestran todas las reservas
        date_display = ft.Text(
            value="Todas las reservas",
            size=16,
            weight="bold",
            color=ft.colors.BLUE_700
        )
        self.date_display = date_display  # Guarda referencia para actualizar el texto

        date_picker_row = ft.Row(
            controls=[date_display, date_picker_button],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        # Botón para crear una nueva reserva
        btn_nueva_reserva = ft.FilledButton(
            "Nueva Reserva",
            icon=ft.icons.ADD,
            on_click=self.show_form_crear,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(left=20, right=20, top=10, bottom=10)
            )
        )

        self.refresh_list()  # Carga inicial de reservas

        # Construcción de la vista principal de reservas
        view = ft.Column(
            controls=[
                date_picker_row,  # Fila con DatePicker para filtrar por fecha
                ft.Row(
                    controls=[btn_nueva_reserva],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Divider(thickness=2, color=ft.colors.GREY_300),
                ft.Container(
                    content=self.list_view,  # Contenedor que muestra la lista de reservas
                    bgcolor=ft.colors.WHITE,
                    padding=ft.padding.all(20),
                    shadow=ft.BoxShadow(
                        blur_radius=10,
                        color=ft.colors.GREY_200,
                        offset=ft.Offset(0, 4)
                    ),
                    border_radius=ft.border_radius.all(12)
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            expand=True
        )
        return view

    def refresh_list(self, fecha=None):
        # Actualiza la lista de reservas, opcionalmente filtrando por fecha
        self.page.update()
        self.load_reservas(fecha)
        self.list_view.controls.clear()
        for reserva in self.reservas:
            reserva_id = str(reserva["id"])
            cliente_id = reserva["cliente_id"]
            mesa_id = reserva["mesa_id"]
            fecha_reserva_str = reserva["fecha_reserva"]
            estado = reserva["estado"]

            # Obtiene el nombre del usuario y número de mesa relacionados a la reserva
            usuario = next((u for u in self.usuarios if str(u["id"]) == cliente_id), None)
            usuario_nombre = usuario["nombre"] if usuario else "Desconocido"

            mesa = next((m for m in self.mesas if str(m["id"]) == mesa_id), None)
            mesa_numero = mesa["numero_mesa"] if mesa else "Desconocida"

            # Crea una tarjeta para cada reserva con detalles y botones de editar/eliminar
            reserva_card = ft.Card(
                elevation=4,
                content=ft.Container(
                    padding=ft.padding.all(15),
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(f"Usuario: {usuario_nombre}", size=16, weight="bold"),
                                    ft.Text(f"Mesa: {mesa_numero}", size=16),
                                    ft.Text(f"Fecha: {fecha_reserva_str}", size=16),
                                    ft.Text(f"Estado: {estado}", size=16, color=self.get_estado_color(estado)),
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                ft.icons.EDIT,
                                                tooltip="Editar Reserva",
                                                on_click=lambda e, rid=reserva_id: self.show_form_editar(rid),
                                                icon_color=ft.colors.BLUE_500
                                            ),
                                            ft.IconButton(
                                                ft.icons.DELETE,
                                                tooltip="Eliminar Reserva",
                                                on_click=lambda e, rid=reserva_id: self.confirm_delete(rid),
                                                icon_color=ft.colors.RED_500
                                            ),
                                        ],
                                        spacing=10,
                                        alignment=ft.MainAxisAlignment.START
                                    ),
                                ],
                                spacing=5
                            ),
                            ft.Icon(
                                ft.icons.LIBRARY_BOOKS_SHARP,
                                color=ft.colors.BLUE_500,
                                size=40,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                ),
                margin=ft.margin.only(bottom=15),
            )
            self.list_view.controls.append(reserva_card)
        self.page.update()

    def get_estado_color(self, estado):
        # Devuelve un color basado en el estado de la reserva
        colores = {
            "Pendiente": ft.colors.ORANGE_500,
            "Confirmada": ft.colors.GREEN_500,
            "Cancelada": ft.colors.RED_500,
        }
        return colores.get(estado, ft.colors.GREY_500)

    def close_dialog(self):
        # Cierra cualquier diálogo abierto
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def show_form_crear(self, e):
        # Muestra el formulario para crear una nueva reserva
        # Prepara opciones para seleccionar usuario y mesa desde dropdowns
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

        # Campos del formulario para reserva
        self.reserva_id_field = ft.TextField(label="ID", visible=False)
        self.cliente_dropdown = ft.Dropdown(label="Usuario", options=opciones_usuarios, expand=True)
        self.mesa_id_dropdown = ft.Dropdown(label="Mesa", options=opciones_mesas, expand=True)

        # Campos para seleccionar fecha y hora
        self.fecha_field = ft.TextField(label="Fecha", read_only=True, expand=True)
        self.hora_field = ft.TextField(label="Hora", read_only=True, expand=True)

        # Botones para abrir pickers de fecha y hora
        btn_seleccionar_fecha = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=self.pick_form_date,
            tooltip="Seleccionar Fecha",
            icon_color=ft.colors.BLUE_500
        )
        btn_seleccionar_hora = ft.IconButton(
            icon=ft.icons.ACCESS_TIME,
            on_click=self.pick_time,
            tooltip="Seleccionar Hora",
            icon_color=ft.colors.BLUE_500
        )

        # Dropdown para seleccionar el estado de la reserva y campo de notas
        self.estado_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option(text="Pendiente"),
                ft.dropdown.Option(text="Confirmada"),
                ft.dropdown.Option(text="Cancelada"),
            ],
            value="Pendiente",
            expand=True,
        )
        self.notas_field = ft.TextField(label="Notas", multiline=True, expand=True)

        # Configuración del diálogo de creación de reserva
        self.form = ft.AlertDialog(
            title=ft.Text("Crear Nueva Reserva", size=20, weight="bold"),
            content=ft.Container(
                content=ft.Column([
                    self.cliente_dropdown,
                    self.mesa_id_dropdown,
                    ft.Row([self.fecha_field, btn_seleccionar_fecha], spacing=10),
                    ft.Row([self.hora_field, btn_seleccionar_hora], spacing=10),
                    self.estado_field,
                    self.notas_field
                ]),
                width=400,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: self.close_dialog()
                ),
                ft.ElevatedButton(
                    "Crear",
                    on_click=self.crear_reserva,
                    bgcolor=ft.colors.BLUE_500,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.Padding(left=20, right=20, top=10, bottom=10)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
        )
        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    def on_date_change(self, e):
        # Maneja cambios en la selección de fecha del DatePicker del formulario
        if e.control.value:
            self.selected_date = e.control.value
            self.fecha_field.value = self.selected_date.strftime("%Y-%m-%d")
            self.page.update()

    def on_date_dismiss(self, e):
        pass  # No se requiere acción adicional al descartar el DatePicker

    def on_time_change(self, e):
        # Maneja cambios en la selección de hora del TimePicker
        tp: ft.TimePicker = e.control
        if tp.value:
            self.selected_time = tp.value
            self.hora_field.value = self.selected_time.strftime("%H:%M")
            self.page.update()

    def on_time_dismiss(self, e):
        pass  # No se requiere acción adicional al descartar el TimePicker

    def pick_form_date(self, e):
        # Abre un DatePicker para seleccionar la fecha en el formulario
        date_picker = ft.DatePicker(
            first_date=datetime(year=2024, month=10, day=1),
            last_date=datetime(year=2050, month=10, day=1),
            on_change=self.on_date_change,
            on_dismiss=self.on_date_dismiss,
            cancel_text="Cancelar",
            confirm_text="Seleccionar",
        )
        self.page.overlay.append(date_picker)
        date_picker.open = True
        self.page.update()

    def pick_time(self, e):
        # Abre un TimePicker para seleccionar la hora en el formulario
        time_picker = ft.TimePicker(
            on_change=self.on_time_change,
            on_dismiss=self.on_time_dismiss,
            cancel_text="Cancelar",
            confirm_text="Seleccionar",
        )
        self.page.overlay.append(time_picker)
        time_picker.open = True
        self.page.update()

    def crear_reserva(self, e):
        # Recoge datos del formulario para crear una nueva reserva
        cliente_id = self.cliente_dropdown.value
        mesa_id = self.mesa_id_dropdown.value
        estado = self.estado_field.value
        notas = self.notas_field.value.strip()

        # Combina la fecha y hora seleccionadas para formar la fecha completa de la reserva
        if self.selected_date and self.selected_time:
            fecha_reserva = datetime.combine(self.selected_date, self.selected_time)
        else:
            fecha_reserva = None

        # Validaciones de campos obligatorios
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
            return  # No procede si hay errores en la validación

        try:
            # Valida la fecha seleccionada
            validate_fecha(fecha_reserva)
            # Crea el modelo de reserva y lo inserta en la base de datos
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
            # Notificación de éxito
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Reserva creada exitosamente!", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError as ve:
            # Muestra error si la validación de fecha falla
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(ve), color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def show_form_editar(self, reserva_id):
        # Muestra el formulario para editar una reserva existente
        reserva = next((r for r in self.reservas if str(r["id"]) == reserva_id), None)
        if not reserva:
            return

        # Prepara opciones de usuario y mesa para dropdowns
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

        # Parsear la fecha y hora de la reserva para llenar los campos
        fecha_completa = reserva["fecha_reserva"]
        if isinstance(fecha_completa, str):
            try:
                fecha_completa = datetime.strptime(fecha_completa, "%Y-%m-%d %H:%M")
            except ValueError:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Formato de fecha inválido para la reserva ID {reserva_id}"),
                    bgcolor=ft.colors.RED_500,
                    duration=3000
                )
                self.page.snack_bar.open = True
                self.page.update()
                return

        fecha_val = fecha_completa.strftime("%Y-%m-%d")
        hora_val = fecha_completa.strftime("%H:%M")

        # Establece fecha y hora seleccionadas para el formulario
        self.selected_date = fecha_completa.date()
        self.selected_time = fecha_completa.time()

        # Campos del formulario de edición con valores preexistentes
        self.reserva_id_field = ft.TextField(label="ID", disabled=True, value=str(reserva["id"]))
        self.cliente_dropdown = ft.Dropdown(
            label="Usuario",
            options=opciones_usuarios,
            value=str(reserva["cliente_id"]),
            expand=True,
        )
        self.mesa_id_dropdown = ft.Dropdown(
            label="Mesa",
            options=opciones_mesas,
            value=str(reserva["mesa_id"]),
            expand=True,
        )
        self.fecha_field = ft.TextField(label="Fecha", read_only=True, value=fecha_val, expand=True)
        self.hora_field = ft.TextField(label="Hora", read_only=True, value=hora_val, expand=True)

        btn_seleccionar_fecha = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            on_click=self.pick_form_date,
            tooltip="Seleccionar Fecha",
            icon_color=ft.colors.BLUE_500
        )
        btn_seleccionar_hora = ft.IconButton(
            icon=ft.icons.ACCESS_TIME,
            on_click=self.pick_time,
            tooltip="Seleccionar Hora",
            icon_color=ft.colors.BLUE_500
        )

        self.estado_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option(text="Pendiente"),
                ft.dropdown.Option(text="Confirmada"),
                ft.dropdown.Option(text="Cancelada"),
            ],
            value=reserva["estado"],
            expand=True,
        )
        self.notas_field = ft.TextField(
            label="Notas",
            value=reserva.get("notas", ""),
            multiline=True,
            expand=True
        )

        # Configura el diálogo para editar reserva
        self.form = ft.AlertDialog(
            title=ft.Text("Editar Reserva", size=20, weight="bold"),
            content=ft.Container(
                content=ft.Column([
                    self.reserva_id_field,
                    self.cliente_dropdown,
                    self.mesa_id_dropdown,
                    ft.Row([self.fecha_field, btn_seleccionar_fecha], spacing=10),
                    ft.Row([self.hora_field, btn_seleccionar_hora], spacing=10),
                    self.estado_field,
                    self.notas_field
                ]),
                width=400,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: self.close_dialog()
                ),
                ft.ElevatedButton(
                    "Actualizar",
                    on_click=lambda e: self.actualizar_reserva(reserva_id),
                    bgcolor=ft.colors.BLUE_500,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.Padding(left=20, right=20, top=10, bottom=10)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
        )
        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    def actualizar_reserva(self, reserva_id):
        # Recoge datos del formulario para actualizar la reserva
        cliente_id = self.cliente_dropdown.value
        mesa_id = self.mesa_id_dropdown.value
        estado = self.estado_field.value
        notas = self.notas_field.value.strip()

        # Combina fecha y hora para obtener la fecha completa de la reserva
        fecha = self.fecha_field.value.strip()
        hora = self.hora_field.value.strip()

        if fecha and hora:
            try:
                fecha_reserva = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            except ValueError:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Fecha y hora inválidas. Formato esperado: YYYY-MM-DD HH:MM", color=ft.colors.WHITE),
                    bgcolor=ft.colors.RED_500,
                    duration=3000
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
        else:
            fecha_reserva = None

        # Validaciones de campos obligatorios
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
            # Valida la nueva fecha de la reserva
            validate_fecha(fecha_reserva)
            # Crea el modelo de reserva actualizado y guarda los cambios
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
            self.refresh_list()  # Refresca la lista filtrada por fecha si aplica
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Reserva actualizada exitosamente!", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError as ve:
            # Muestra error si la validación falla
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(ve), color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def confirm_delete(self, reserva_id):
        # Muestra diálogo para confirmar eliminación de reserva
        confirm = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación", size=18, weight="bold"),
            content=ft.Text("¿Estás seguro de que deseas eliminar esta reserva?", size=16),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: self.close_dialog()
                ),
                ft.ElevatedButton(
                    "Eliminar",
                    on_click=lambda e: self.eliminar_reserva(reserva_id),
                    bgcolor=ft.colors.RED_500,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.Padding(left=20, right=20, top=10, bottom=10)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
        )
        self.page.dialog = confirm
        confirm.open = True
        self.page.update()

    def eliminar_reserva(self, reserva_id):
        # Elimina la reserva de la base de datos y actualiza la lista
        eliminar_reserva(reserva_id)
        self.close_dialog()
        self.refresh_list(self.selected_date)  # Refresca la lista con la fecha filtrada si aplica
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Reserva eliminada exitosamente!", color=ft.colors.WHITE),
            bgcolor=ft.colors.RED_500,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()

    def pick_filter_date(self, e):
        # Abre un DatePicker para filtrar reservas por fecha
        date_picker = ft.DatePicker(
            first_date=datetime(year=2024, month=10, day=1),
            last_date=datetime(year=2050, month=10, day=1),
            on_change=self.on_filter_date_change,
            on_dismiss=self.on_date_dismiss,
            cancel_text="Cancelar",
            confirm_text="Seleccionar",
        )
        self.page.overlay.append(date_picker)
        date_picker.open = True
        self.page.update()

    def on_filter_date_change(self, e):
        # Maneja el cambio de fecha para filtrar reservas
        if e.control.value:
            self.selected_date = e.control.value
            self.date_display.value = f"Reservas para: {self.selected_date.strftime('%Y-%m-%d')}"
            self.refresh_list(self.selected_date)
        else:
            self.selected_date = None
            self.date_display.value = "Todas las reservas"
            self.refresh_list()
        self.page.update()
