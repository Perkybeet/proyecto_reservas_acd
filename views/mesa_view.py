import flet as ft
from services.crud_operations import (
    insertar_mesa,
    leer_mesas,
    actualizar_mesa,
    eliminar_mesa
)
from models.mesa_model import MesaModel
from utils.validators import validate_nmesa

class MesaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.mesas = []  # Lista para almacenar mesas cargadas desde la base de datos
        self.list_view = ft.Column(spacing=15)  # Columna para listar tarjetas de mesas
        self.load_mesas()  # Carga inicial de mesas desde la BD

    def load_mesas(self):
        # Leer todas las mesas desde la base de datos y almacenarlas en self.mesas
        self.mesas = leer_mesas()

    def get_view(self):
        # Botón para crear una nueva mesa
        btn_nueva_mesa = ft.FilledButton(
            "Nueva Mesa",
            icon=ft.icons.ADD,
            on_click=self.show_form_crear,  # Llama a la función para mostrar formulario de creación
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(left=20, right=20, top=10, bottom=10)
            )
        )

        # Refrescar la lista de mesas mostradas
        self.refresh_list()

        # Vista principal de la sección de mesas con el botón y la lista
        view = ft.Column(
            controls=[
                ft.Row(
                    controls=[btn_nueva_mesa],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Divider(thickness=2, color=ft.colors.GREY_300),
                ft.Container(
                    content=self.list_view,  # Contenedor que muestra la lista de mesas
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
        # Actualiza la lista de mesas: recarga datos y reconstruye la vista
        self.load_mesas()
        self.list_view.controls.clear()
        for mesa in self.mesas:
            mesa_id = str(mesa["id"])
            numero_mesa = mesa["numero_mesa"]
            capacidad = mesa["capacidad"]
            ubicacion = mesa["ubicacion"]

            # Crea una tarjeta para cada mesa con detalles y botones de editar/eliminar
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
                                            # Botón para editar mesa
                                            ft.IconButton(
                                                ft.icons.EDIT,
                                                tooltip="Editar Mesa",
                                                on_click=lambda e, mid=mesa_id: self.show_form_editar(mid),
                                                icon_color=ft.colors.BLUE_500
                                            ),
                                            # Botón para eliminar mesa
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
        self.page.update()  # Actualiza la página para reflejar los cambios en la UI

    def close_dialog(self):
        # Cierra cualquier diálogo abierto en la página
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def show_form_crear(self, e):
        # Muestra un formulario en un diálogo para crear una nueva mesa
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
                    on_click=self.crear_mesa,  # Llama a la función para procesar creación
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
        # Recoge valores del formulario para crear una nueva mesa
        numero_mesa = self.numero_mesa_field.value.strip()
        capacidad = self.capacidad_field.value.strip()
        ubicacion = self.ubicacion_field.value.strip()

        # Bandera para detectar errores en la validación
        error = False

        # Validación de campos obligatorios
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
            return  # Termina si hay errores en la validación

        try:
            # Validación específica para número de mesa
            validate_nmesa(numero_mesa)
            numero_mesa = int(numero_mesa)
            capacidad = int(capacidad)
            # Crea un objeto MesaModel con los datos del formulario
            mesa = MesaModel(
                numero_mesa=numero_mesa,
                capacidad=capacidad,
                ubicacion=ubicacion
            )
            # Inserta la nueva mesa en la base de datos
            insertar_mesa(mesa)
            self.close_dialog()  # Cierra el diálogo de formulario
            self.refresh_list()  # Actualiza la lista de mesas mostrada
            # Muestra una notificación de éxito
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Mesa creada exitosamente!", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError:
            # Manejo de error si los campos numéricos no son válidos
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Número de mesa y capacidad deben ser números válidos.", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            # Manejo de error genérico, por ejemplo, si el número de mesa ya existe
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("El número de mesa ya existe", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def show_form_editar(self, mesa_id):
        # Encuentra la mesa a editar según el ID proporcionado
        mesa = next((m for m in self.mesas if str(m["id"]) == mesa_id), None)
        if not mesa:
            return

        # Prepara campos del formulario con los datos actuales de la mesa
        self.mesa_id_field = ft.TextField(label="ID", disabled=True, value=str(mesa["id"]))
        self.numero_mesa_field = ft.TextField(label="Número de Mesa", value=str(mesa["numero_mesa"]), autofocus=True)
        self.capacidad_field = ft.TextField(label="Capacidad", value=str(mesa["capacidad"]), keyboard_type=ft.KeyboardType.NUMBER)
        self.ubicacion_field = ft.TextField(label="Ubicación", value=mesa["ubicacion"])

        # Configura un diálogo similar al de creación, pero para editar
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
        # Recoge valores del formulario para actualizar la mesa
        numero_mesa = self.numero_mesa_field.value.strip()
        capacidad = self.capacidad_field.value.strip()
        ubicacion = self.ubicacion_field.value.strip()

        error = False  # Flag para errores en la validación

        # Validación de campos obligatorios
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
            return

        try:
            # Validación y conversión de datos numéricos
            validate_nmesa
            numero_mesa = int(numero_mesa)
            capacidad = int(capacidad)
            # Crea un objeto MesaModel con los datos actualizados
            mesa = MesaModel(
                numero_mesa=numero_mesa,
                capacidad=capacidad,
                ubicacion=ubicacion
            )
            # Actualiza la mesa en la base de datos
            actualizar_mesa(mesa_id, mesa)
            self.close_dialog()  # Cierra el diálogo
            self.refresh_list()   # Actualiza la lista de mesas en la UI
            # Notificación de éxito
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Mesa actualizada exitosamente!", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError:
            # Error si número_mesa o capacidad no son números válidos
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Número de mesa y capacidad deben ser números válidos.", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            # Error genérico, por ejemplo si el número de mesa ya existe
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("El número de mesa ya existe", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def confirm_delete(self, mesa_id):
        # Muestra un diálogo para confirmar la eliminación de una mesa
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
        # Elimina la mesa de la base de datos y actualiza la interfaz de usuario
        eliminar_mesa(mesa_id)
        self.close_dialog()
        self.refresh_list()
        # Notificación de eliminación exitosa
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Mesa eliminada exitosamente!", color=ft.colors.WHITE),
            bgcolor=ft.colors.RED_500,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()
