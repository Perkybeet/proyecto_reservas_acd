import flet as ft
from services.crud_operations import (
    insertar_usuario,
    leer_usuarios,
    actualizar_usuario,
    eliminar_usuario
)
from models.user_model import UserModel
from utils.validators import validate_email, validate_telefono

class UsuarioView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.usuarios = []
        self.list_view = ft.Column(spacing=15)
        self.load_usuarios()

    def load_usuarios(self):
        self.usuarios = leer_usuarios()

    def get_view(self):
        btn_nuevo_usuario = ft.FilledButton(
            "Nuevo Cliente",
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
                    controls=[btn_nuevo_usuario],
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
        self.load_usuarios()
        self.list_view.controls.clear()
        for usuario in self.usuarios:
            usuario_id = str(usuario["id"])
            nombre = usuario["nombre"]
            email = usuario["email"]
            telefono = usuario["telefono"]

            usuario_card = ft.Card(
                elevation=4,
                content=ft.Container(
                    padding=ft.padding.all(15),
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(f"Nombre: {nombre}", size=16, weight="bold"),
                                    ft.Text(f"Email: {email}", size=16),
                                    ft.Text(f"Teléfono: {telefono}", size=16),
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                ft.icons.EDIT,
                                                tooltip="Editar Usuario",
                                                on_click=lambda e, uid=usuario_id: self.show_form_editar(uid),
                                                icon_color=ft.colors.BLUE_500
                                            ),
                                            ft.IconButton(
                                                ft.icons.DELETE,
                                                tooltip="Eliminar Usuario",
                                                on_click=lambda e, uid=usuario_id: self.confirm_delete(uid),
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
                                ft.icons.PERSON,
                                color=ft.colors.BLUE_500,
                                size=40,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                ),
                margin=ft.margin.only(bottom=15)
            )
            self.list_view.controls.append(usuario_card)
        self.page.update()

    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def show_form_crear(self, e):
        self.nombre_field = ft.TextField(label="Nombre", autofocus=True)
        self.email_field = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
        self.telefono_field = ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.PHONE)
        self.direccion_field = ft.TextField(label="Dirección")

        self.form = ft.AlertDialog(
            title=ft.Text("Crear Nuevo Cliente", size=20, weight="bold"),
            content=ft.Container(
                content=ft.Column([
                    self.nombre_field,
                    self.email_field,
                    self.telefono_field,
                    self.direccion_field
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
                    on_click=self.crear_usuario,
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

    def crear_usuario(self, e):
        nombre = self.nombre_field.value.strip()
        email = self.email_field.value.strip()
        telefono = self.telefono_field.value.strip()
        direccion = self.direccion_field.value.strip()

        # Inicializar un flag para detectar errores
        hay_error = False

        # Validar campos obligatorios
        if not nombre:
            self.nombre_field.error_text = "Este campo es obligatorio."
            hay_error = True
        else:
            self.nombre_field.error_text = None

        if not email:
            self.email_field.error_text = "Este campo es obligatorio."
            hay_error = True
        else:
            self.email_field.error_text = None

        if not telefono:
            self.telefono_field.error_text = "Este campo es obligatorio."
            hay_error = True
        else:
            self.telefono_field.error_text = None

        self.page.update()

        if hay_error:
            return  # Detener la ejecución si hay errores

        try:
            validate_email(email)
            validate_telefono(telefono)
            usuario = UserModel(
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion
            )
            insertar_usuario(usuario)
            self.close_dialog()
            self.refresh_list()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Usuario creado exitosamente!", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError as ve:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(ve), color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def show_form_editar(self, usuario_id):
        usuario = next((u for u in self.usuarios if str(u["id"]) == usuario_id), None)
        if not usuario:
            return

        self.usuario_id_field = ft.TextField(label="ID", disabled=True, value=str(usuario["id"]))
        self.nombre_field = ft.TextField(label="Nombre", value=usuario["nombre"], autofocus=True)
        self.email_field = ft.TextField(label="Email", value=usuario["email"], keyboard_type=ft.KeyboardType.EMAIL)
        self.telefono_field = ft.TextField(label="Teléfono", value=usuario["telefono"], keyboard_type=ft.KeyboardType.PHONE)
        self.direccion_field = ft.TextField(label="Dirección", value=usuario.get("direccion", ""))

        self.form = ft.AlertDialog(
            title=ft.Text("Editar Usuario", size=20, weight="bold"),
            content=ft.Container(
                content=ft.Column([
                    self.usuario_id_field,
                    self.nombre_field,
                    self.email_field,
                    self.telefono_field,
                    self.direccion_field
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
                    on_click=lambda e: self.actualizar_usuario(usuario_id),
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

    def actualizar_usuario(self, usuario_id: str):
        nombre = self.nombre_field.value.strip()
        email = self.email_field.value.strip()
        telefono = self.telefono_field.value.strip()
        direccion = self.direccion_field.value.strip()

        # Inicializar un flag para detectar errores
        hay_error = False

        # Validar campos obligatorios
        if not nombre:
            self.nombre_field.error_text = "Este campo es obligatorio."
            hay_error = True
        else:
            self.nombre_field.error_text = None

        if not email:
            self.email_field.error_text = "Este campo es obligatorio."
            hay_error = True
        else:
            self.email_field.error_text = None

        if not telefono:
            self.telefono_field.error_text = "Este campo es obligatorio."
            hay_error = True
        else:
            self.telefono_field.error_text = None

        self.page.update()

        if hay_error:
            return  # Detener la ejecución si hay errores

        try:
            validate_email(email)
            validate_telefono(telefono)
            usuario = UserModel(
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion
            )
            actualizar_usuario(usuario_id, usuario)
            self.close_dialog()
            self.refresh_list()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Usuario actualizado exitosamente!", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
        except ValueError as ve:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(ve), color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_500,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def confirm_delete(self, usuario_id):
        confirm = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación", size=18, weight="bold"),
            content=ft.Text("¿Estás seguro de que deseas eliminar este usuario?", size=16),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: self.close_dialog()
                ),
                ft.ElevatedButton(
                    "Eliminar",
                    on_click=lambda e: self.eliminar_usuario(usuario_id),
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

    def eliminar_usuario(self, usuario_id):
        eliminar_usuario(usuario_id)
        self.close_dialog()
        self.refresh_list()
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Usuario eliminado exitosamente!", color=ft.colors.WHITE),
            bgcolor=ft.colors.RED_500,
            duration=3000
        )
        self.page.snack_bar.open = True
        self.page.update()