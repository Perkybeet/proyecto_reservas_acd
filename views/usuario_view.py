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
        self.list_view = ft.Column()
        self.load_usuarios()

    def load_usuarios(self):
        self.usuarios = leer_usuarios()

    def get_view(self):
        btn_nuevo_usuario = ft.ElevatedButton("Nuevo Usuario", on_click=self.show_form_crear)

        # Obtener el listado de usuarios
        self.refresh_list()

        # Agrega controles a la vista
        view = ft.Column(
            controls=[
                btn_nuevo_usuario,
                self.list_view
            ],
            scroll=ft.ScrollMode.AUTO
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

            usuario_item = ft.Row(
                controls=[
                    ft.Text(f"Nombre: {nombre}"),
                    ft.Text(f"Email: {email}"),
                    ft.Text(f"Teléfono: {telefono}"),
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, uid=usuario_id: self.show_form_editar(uid)),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, uid=usuario_id: self.confirm_delete(uid)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.list_view.controls.append(usuario_item)
        self.page.update()

    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def show_form_crear(self, e):
        self.nombre_field = ft.TextField(label="Nombre")
        self.email_field = ft.TextField(label="Email")
        self.telefono_field = ft.TextField(label="Teléfono")
        self.direccion_field = ft.TextField(label="Dirección")

        self.form = ft.AlertDialog(
            title=ft.Text("Crear Nuevo Usuario"),
            content=ft.Column([
                self.nombre_field,
                self.email_field,
                self.telefono_field,
                self.direccion_field
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Crear", on_click=self.crear_usuario),
            ],
            actions_alignment=ft.MainAxisAlignment.END
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
        except ValueError as ve:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            self.page.snack_bar.open = True
            self.page.update()

    def show_form_editar(self, usuario_id):
        usuario = next((u for u in self.usuarios if str(u["id"]) == usuario_id), None)
        if not usuario:
            return

        self.usuario_id_field = ft.TextField(label="ID", disabled=True, value=str(usuario["id"]))
        self.nombre_field = ft.TextField(label="Nombre", value=usuario["nombre"])
        self.email_field = ft.TextField(label="Email", value=usuario["email"])
        self.telefono_field = ft.TextField(label="Teléfono", value=usuario["telefono"])
        self.direccion_field = ft.TextField(label="Dirección", value=usuario.get("direccion", ""))

        self.form = ft.AlertDialog(
            title=ft.Text("Editar Usuario"),
            content=ft.Column([
                self.usuario_id_field,
                self.nombre_field,
                self.email_field,
                self.telefono_field,
                self.direccion_field
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Actualizar", on_click=lambda e: self.actualizar_usuario(usuario_id)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
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
        except ValueError as ve:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            self.page.snack_bar.open = True
            self.page.update()

    def confirm_delete(self, usuario_id):
        confirm = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Estás seguro de que deseas eliminar este usuario?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton("Eliminar", on_click=lambda e: self.eliminar_usuario(usuario_id)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = confirm
        confirm.open = True
        self.page.update()

    def eliminar_usuario(self, usuario_id):
        eliminar_usuario(usuario_id)
        self.close_dialog()
        self.refresh_list()
