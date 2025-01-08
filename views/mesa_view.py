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
        self.list_view = ft.Column(spacing=15)
        self.load_mesas()

    def load_mesas(self):
        self.mesas = leer_mesas()

    def get_view(self):
        btn_nueva_mesa = ft.FilledButton(
            "Nueva Mesa",
            icon=ft.icons.ADD,
            on_click=self.show_form_crear,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(left=20, right=20, top=10, bottom=10)
            )
        )

        self.refresh_list()

        view = ft.Column(
            controls=[
                ft.Row(
                    controls=[btn_nueva_mesa],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Divider(thickness=2, color=ft.colors.GREY_300),
                ft.Container(
                    content=self.list_view,
                    bgcolor=ft.colors.WHITE,
                    border_radius=ft.border_radius.all(12),
                    padding=ft.padding.all(20),
                    shadow=ft.BoxShadow(
                        blur_radius=10,
                        color=ft.colors.GREY_200,
                        offset=ft.Offset(0, 4)
                    )
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            expand=True
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

            mesa_card = ft.Card(
                elevation=4,
                content=ft.Container(
                    padding=ft.padding.all(15),
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(f"Número: {numero_mesa}", size=16, weight="bold"),
                                    ft.Text(f"Capacidad: {capacidad}", size=16),
                                    ft.Text(f"Ubicación: {ubicacion}", size=16),
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                ft.icons.EDIT,
                                                tooltip="Editar Mesa",
                                                on_click=lambda e, mid=mesa_id: self.show_form_editar(mid),
                                                icon_color=ft.colors.BLUE_500
                                            ),
                                            ft.IconButton(
                                                ft.icons.DELETE,
                                                tooltip="Eliminar Mesa",
                                                on_click=lambda e, mid=mesa_id: self.confirm_delete(mid),
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
                                ft.icons.TABLE_CHART,
                                color=ft.colors.BLUE_500,
                                size=40,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                ),
                margin=ft.margin.only(bottom=15)
            )
            self.list_view.controls.append(mesa_card)
        self.page.update()

    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def show_form_crear(self, e):
        self.numero_mesa_field = ft.TextField(label="Número de Mesa", autofocus=True)
        self.capacidad_field = ft.TextField(label="Capacidad", keyboard_type=ft.KeyboardType.NUMBER)
        self.ubicacion_field = ft.TextField(label="Ubicación")

        self.form = ft.AlertDialog(
            title=ft.Text("Crear Nueva Mesa", size=20, weight="bold"),
            content=ft.Container(
                content=ft.Column([
                    self.numero_mesa_field,
                    self.capacidad_field,
                    self.ubicacion_field
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
                    on_click=self.crear_mesa,
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

    def crear_mesa(self, e):
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
                numero_mesa=numero_mesa,
                capacidad=capacidad,
                ubicacion=ubicacion
            )
            insertar_mesa(mesa)
            self.close_dialog()
            self.refresh_list()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Mesa creada exitosamente!", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Número de mesa y capacidad deben ser números válidos.", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def show_form_editar(self, mesa_id):
        mesa = next((m for m in self.mesas if str(m["id"]) == mesa_id), None)
        if not mesa:
            return

        self.mesa_id_field = ft.TextField(label="ID", disabled=True, value=str(mesa["id"]))
        self.numero_mesa_field = ft.TextField(label="Número de Mesa", value=str(mesa["numero_mesa"]), autofocus=True)
        self.capacidad_field = ft.TextField(label="Capacidad", value=str(mesa["capacidad"]), keyboard_type=ft.KeyboardType.NUMBER)
        self.ubicacion_field = ft.TextField(label="Ubicación", value=mesa["ubicacion"])

        self.form = ft.AlertDialog(
            title=ft.Text("Editar Mesa", size=20, weight="bold"),
            content=ft.Container(
                content=ft.Column([
                    self.mesa_id_field,
                    self.numero_mesa_field,
                    self.capacidad_field,
                    self.ubicacion_field
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
                    on_click=lambda e: self.actualizar_mesa(mesa_id),
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
                numero_mesa=numero_mesa,
                capacidad=capacidad,
                ubicacion=ubicacion
            )
            actualizar_mesa(mesa_id, mesa)
            self.close_dialog()
            self.refresh_list()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Mesa actualizada exitosamente!", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Número de mesa y capacidad deben ser números válidos.", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def confirm_delete(self, mesa_id):
        confirm = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación", size=18, weight="bold"),
            content=ft.Text("¿Estás seguro de que deseas eliminar esta mesa?", size=16),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: self.close_dialog()
                ),
                ft.ElevatedButton(
                    "Eliminar",
                    on_click=lambda e: self.eliminar_mesa(mesa_id),
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

    def eliminar_mesa(self, mesa_id):
        eliminar_mesa(mesa_id)
        self.close_dialog()
        self.refresh_list()
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Mesa eliminada exitosamente!", color=ft.colors.WHITE),
            bgcolor=ft.colors.RED_500,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()