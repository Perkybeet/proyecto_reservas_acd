import flet as ft
from views.reserva_view import ReservaView

def main_view(page: ft.Page):
    page.title = "Libro de Reservas"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Instanciar ReservaView pasando la instancia de Page
    reserva_view = ReservaView(page)

    def navigate_to_reservas(e):
        # Limpiar vistas existentes
        page.views.clear()
        # Añadir la vista de reservas
        page.views.append(reserva_view.get_view())
        page.update()

    # Botones de navegación
    nav_bar = ft.Row(
        controls=[
            ft.TextButton("Reservas", on_click=navigate_to_reservas),
            # Puedes agregar más botones para Usuarios, Recursos, etc.
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Agregar elementos a la página
    page.add(nav_bar)
    # Mostrar la vista de reservas por defecto
    navigate_to_reservas(None)
