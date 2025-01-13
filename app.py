import flet as ft
from views.main_view import main_view

# Diccionario con las credenciales permitidas
CREDENTIALS = {
    "admin": "admin"
}

def login_view(page: ft.Page):
    # Campos de entrada para usuario y contraseña
    user_field = ft.TextField(label="Usuario", width=300)
    pass_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)

    def do_login(e):
        usuario = user_field.value
        contraseña = pass_field.value
        
        # Verificar si las credenciales son correctas
        if CREDENTIALS.get(usuario) == contraseña:
            # Limpiar la página y cargar la vista principal
            page.controls.clear()
            main_view(page)  # Cargar main_view
            page.update()
        else:
            # Mostrar un Snackbar indicando error
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Credenciales inválidas, intente nuevamente.", color="white"),
                bgcolor="red",
                open=True
            )
            page.update()

    # Botón de login
    login_button = ft.ElevatedButton(text="Iniciar sesión", on_click=do_login, width=300)

    # Contenedor principal centrado vertical y horizontalmente
    login_form = ft.Column(
        [
            ft.Text("Iniciar sesión", style="headlineMedium"),
            user_field,
            pass_field,
            login_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    # Configurar la página para mostrar el formulario de login
    page.title = "Login"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(login_form)

def main(page: ft.Page):
    login_view(page)  # Iniciar con la vista de login

if __name__ == "__main__":
    ft.app(target=main)
