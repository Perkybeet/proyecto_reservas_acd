import flet as ft
from services.crud_operations import (
    insertar_mesa,
    leer_mesas,
    actualizar_mesa,
    eliminar_mesa
)
from models.mesa_model import MesaModel

class MesaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.mesas = []
        self.list_view = ft.Column()
        self.load_mesas()

    def load_mesas(self):
        self.mesas = leer_mesas()

    def get_view(self):
        btn_nueva_mesa = ft.ElevatedButton("Nueva Mesa", on_click=self.show_form_crear)

        # Obtenemos el listado de mesas
        self.refresh_list()

        # Agregar controles a la vista
        view = ft.Column(
            controls=[
                btn_nueva_mesa,
                self.list_view
            ],
            scroll=ft.ScrollMode.AUTO
        )
        return view

    def refresh_list(self):
        self.load_mesas()
        self.list_view.controls.clear()
        for mesa in self.mesas:
            mesa_id = str(mesa["id"])
            numero_mesa = mesa["numero_mesa"]
            capacidad = mesa["capacidad"]
            ubicacion = mesa["ubicacion"]

            mesa_item = ft.Row(
                controls=[
                    ft.Text(f"ID: {mesa_id}"),
                    ft.Text(f"Número: {numero_mesa}"),
                    ft.Text(f"Capacidad: {capacidad}"),
                    ft.Text(f"Ubicación: {ubicacion}"),
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, mid=mesa_id: self.show_form_editar(mid)),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, mid=mesa_id: self.confirm_delete(mid)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.list_view.controls.append(mesa_item)
        self.page.update()

    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def show_form_crear(self, e):
        self.mesa_id_field = ft.TextField(label="ID", value="")
        self.numero_mesa_field = ft.TextField(label="Número de Mesa", value="")
        self.capacidad_field = ft.TextField(label="Capacidad", value="")
        self.ubicacion_field = ft.TextField(label="Ubicación")

        self.form = ft.AlertDialog(
            title=ft.Text("Crear Nueva Mesa"),
            content=ft.Column([
                self.mesa_id_field,
                self.numero_mesa_field,
                self.capacidad_field,
                self.ubicacion_field
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Crear", on_click=self.crear_mesa),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    def crear_mesa(self, e):
        mesa_id = self.mesa_id_field.value.strip()
        numero_mesa = self.numero_mesa_field.value.strip()
        capacidad = self.capacidad_field.value.strip()
        ubicacion = self.ubicacion_field.value.strip()

        # Inicializar un flag para detectar errores
        error = False

        # Validar campos obligatorios
        if not numero_mesa:
            self.numero_mesa_field.error_text = "Este campo es obligatorio."
            error = True
        else:
            self.numero_mesa_field.error_text = None

        if not capacidad:
            self.capacidad_field.error_text = "Este campo es obligatorio."
            error = True
        else:
            self.capacidad_field.error_text = None

        if not ubicacion:
            self.ubicacion_field.error_text = "Este campo es obligatorio."
            error = True
        else:
            self.ubicacion_field.error_text = None

        self.page.update()

        if error:
            return  # Detener la ejecución si hay errores

        try:
            numero_mesa = int(numero_mesa)
            capacidad = int(capacidad)
            mesa = MesaModel(
                id=mesa_id,
                numero_mesa=numero_mesa,
                capacidad=capacidad,
                ubicacion=ubicacion
            )
            insertar_mesa(mesa)
            self.close_dialog()
            self.refresh_list()
        except ValueError:
            self.page.snack_bar = ft.SnackBar(ft.Text("Número de mesa y capacidad deben ser números válidos."))
            self.page.snack_bar.open = True
            self.page.update()

    def show_form_editar(self, mesa_id):
        mesa = next((m for m in self.mesas if str(m["id"]) == mesa_id), None)
        if not mesa:
            return

        self.mesa_id_field = ft.TextField(label="ID", disabled=True, value=str(mesa["id"]))
        self.numero_mesa_field = ft.TextField(label="Número de Mesa", value=str(mesa["numero_mesa"]))
        self.capacidad_field = ft.TextField(label="Capacidad", value=str(mesa["capacidad"]))
        self.ubicacion_field = ft.TextField(label="Ubicación", value=mesa["ubicacion"])

        self.form = ft.AlertDialog(
            title=ft.Text("Editar Mesa"),
            content=ft.Column([
                self.mesa_id_field,
                self.numero_mesa_field,
                self.capacidad_field,
                self.ubicacion_field
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Actualizar", on_click=lambda e: self.actualizar_mesa(mesa_id)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.form
        self.form.open = True
        self.page.update()

    def actualizar_mesa(self, mesa_id):
        numero_mesa = self.numero_mesa_field.value.strip()
        capacidad = self.capacidad_field.value.strip()
        ubicacion = self.ubicacion_field.value.strip()

        # Inicializar un flag para detectar errores
        error = False

        # Validar campos obligatorios
        if not numero_mesa:
            self.numero_mesa_field.error_text = "Este campo es obligatorio."
            error = True
        else:
            self.numero_mesa_field.error_text = None

        if not capacidad:
            self.capacidad_field.error_text = "Este campo es obligatorio."
            error = True
        else:
            self.capacidad_field.error_text = None

        if not ubicacion:
            self.ubicacion_field.error_text = "Este campo es obligatorio."
            error = True
        else:
            self.ubicacion_field.error_text = None

        self.page.update()

        if error:
            return  # Detener la ejecución si hay errores

        try:
            numero_mesa = int(numero_mesa)
            capacidad = int(capacidad)
            mesa = MesaModel(
                id=mesa_id,
                numero_mesa=numero_mesa,
                capacidad=capacidad,
                ubicacion=ubicacion
            )
            actualizar_mesa(mesa_id, mesa)
            self.close_dialog()
            self.refresh_list()
        except ValueError:
            self.page.snack_bar = ft.SnackBar(ft.Text("Número de mesa y capacidad deben ser números válidos."))
            self.page.snack_bar.open = True
            self.page.update()

    def confirm_delete(self, mesa_id):
        confirm = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Estás seguro de que deseas eliminar esta mesa?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Eliminar", on_click=lambda e: self.eliminar_mesa(mesa_id)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = confirm
        confirm.open = True
        self.page.update()

    def eliminar_mesa(self, mesa_id):
        eliminar_mesa(mesa_id)
        self.close_dialog()
        self.refresh_list()
