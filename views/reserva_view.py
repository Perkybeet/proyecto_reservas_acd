# views/reserva_view.py

import flet as ft
from services.crud_operations import leer_reservas, insertar_reserva, actualizar_reserva, eliminar_reserva
from models.reserva_model import ReservaModel
from bson.objectid import ObjectId
from utils.validators import validate_fecha

class ReservaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.reservas = []
        self.list_view = ft.Column()
        self.load_reservas()

    def load_reservas(self):
        self.reservas = leer_reservas()

    def get_view(self):
        # Botón para crear nueva reserva
        btn_nueva_reserva = ft.ElevatedButton("Nueva Reserva", on_click=self.show_form_crear)

        # Listado de reservas
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
            reserva_id = str(reserva["_id"])
            cliente_id = reserva["cliente_id"]
            mesa_id = reserva["mesa_id"]
            fecha_reserva = reserva["fecha_reserva"]
            estado = reserva["estado"]

            reserva_item = ft.Row(
                controls=[
                    ft.Text(f"Usuario ID: {cliente_id}"),
                    ft.Text(f"Recurso ID: {mesa_id}"),
                    ft.Text(f"Fecha: {fecha_reserva}"),
                    ft.Text(f"Estado: {estado}"),
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, rid=reserva_id: self.show_form_editar(rid)),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, rid=reserva_id: self.confirm_delete(rid)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.list_view.controls.append(reserva_item)
        self.page.update()

    def show_form_crear(self, e):
        # Asignar cada campo a una variable
        self.cliente_id_field = ft.TextField(label="Usuario ID")
        self.mesa_id_field = ft.TextField(label="Recurso ID")
        self.fecha_reserva_field = ft.TextField(label="Fecha Reserva (YYYY-MM-DD)")
        self.estado_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("Confirmada"),
                ft.dropdown.Option("Cancelada"),
            ],
            value="Pendiente"
        )

        self.form = ft.AlertDialog(
            title=ft.Text("Crear Nueva Reserva"),
            content=ft.Column([
                self.reserva_id_field,
                self.cliente_id_field,
                self.mesa_id_field,
                self.fecha_reserva_field,
                self.estado_field,
                self.notas_field
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.dialog.close()),
                ft.ElevatedButton("Crear", on_click=self.crear_reserva),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    def crear_reserva(self, e):
        id = self.reserva_id_field.value
        cliente_id = self.cliente_id_field.value
        mesa_id = self.mesa_id_field.value
        fecha_reserva = self.fecha_reserva_field.value
        estado = self.estado_field.value
        notas = self.notas_field.value

        try:
            validate_fecha(fecha_reserva)
            reserva = ReservaModel(
                _id=id,
                cliente_id=cliente_id,
                mesa_id=mesa_id,
                fecha_reserva=fecha_reserva,
                estado=estado,
                notas=notas
            )
            insertar_reserva(reserva)
            self.page.dialog.close()
            self.refresh_list()
        except ValueError as ve:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            self.page.snack_bar.open = True
            self.page.update()

    def show_form_editar(self, reserva_id):
        reserva = next((r for r in self.reservas if str(r["_id"]) == reserva_id), None)
        if not reserva:
            return

        # Asignar cada campo a una variable
        self.reserva_id_field = ft.TextField(label="ID", value=reserva["_id"], id="reserva_id")
        self.cliente_id_field = ft.TextField(label="Usuario ID", value=reserva["cliente_id"], id="cliente_id")
        self.mesa_id_field = ft.TextField(label="Recurso ID", value=reserva["mesa_id"], id="mesa_id")
        self.fecha_reserva_field = ft.TextField(label="Fecha Reserva (YYYY-MM-DD)", value=reserva["fecha_reserva"], id="fecha_reserva")
        self.estado_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("Confirmada"),
                ft.dropdown.Option("Cancelada"),
            ],
            value=reserva["estado"],
            id="estado"
        )

        self.notas_field = ft.TextField(label="Notas", value=reserva["notas"], id="notas")

        self.form = ft.AlertDialog(
            title=ft.Text("Editar Reserva"),
            content=ft.Column([
                self.cliente_id_field,
                self.mesa_id_field,
                self.fecha_reserva_field,
                self.estado_field,
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.dialog.close()),
                ft.ElevatedButton("Actualizar", on_click=lambda e: self.actualizar_reserva(reserva_id)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    def actualizar_reserva(self, reserva_id):
        cliente_id = self.cliente_id_field.value
        mesa_id = self.mesa_id_field.value
        fecha_reserva = self.fecha_reserva_field.value
        estado = self.estado_field.value

        try:
            validate_fecha(fecha_reserva)
            reserva = ReservaModel(
                cliente_id=cliente_id,
                mesa_id=mesa_id,
                fecha_reserva=fecha_reserva,
                estado=estado
            )
            actualizar_reserva(reserva_id, reserva)
            self.page.dialog.close()
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
                ft.TextButton("Cancelar", on_click=lambda e: self.page.dialog.close()),
                ft.ElevatedButton("Eliminar", on_click=lambda e: self.eliminar_reserva(reserva_id)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = confirm
        confirm.open = True
        self.page.update()

    def eliminar_reserva(self, reserva_id):
        eliminar_reserva(reserva_id)
        self.page.dialog.close()
        self.refresh_list()
