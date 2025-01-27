import flet as ft
from views.reserva_view import ReservaView
from views.usuario_view import UsuarioView
from views.mesa_view import MesaView
from services.crud_operations import contar_usuarios, contar_mesas, contar_reservas

def main_view(page: ft.Page):
    # Configuración básica de la página
    page.title = "Libro de Reservas"
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE_700,
            secondary=ft.colors.BLUE_500,
            background=ft.colors.WHITE,
            surface=ft.colors.WHITE,
            error=ft.colors.RED_500,
            on_primary=ft.colors.WHITE,
            on_secondary=ft.colors.WHITE,
            on_background=ft.colors.BLACK,
            on_surface=ft.colors.BLACK,
            on_error=ft.colors.WHITE,
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
    )
    page.update()

    # Definición de los elementos del menú lateral de navegación
    nav_items = [
        ft.NavigationRailDestination(icon=ft.icons.HOME, label="Resumen"),
        ft.NavigationRailDestination(icon=ft.icons.LIBRARY_BOOKS_SHARP, label="Reservas"),
        ft.NavigationRailDestination(icon=ft.icons.PEOPLE, label="Clientes"),
        ft.NavigationRailDestination(icon=ft.icons.TABLE_CHART, label="Mesas"),
    ]

    # Creación de la barra de navegación lateral
    nav_bar = ft.NavigationRail(
        destinations=nav_items,
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # Llama a la función navigate al cambiar de selección
        on_change=lambda e: navigate(e.control.selected_index),
        min_width=80,
        extended=False,
    )

    # Contenedor principal donde se mostrará el contenido según la selección
    main_content = ft.Container(
        padding=20,
        expand=True,
        bgcolor=ft.colors.GREY_50,
    )

    # Función para manejar la navegación entre vistas
    def navigate(selected_index):
        if selected_index == 0:
            # Muestra el resumen global
            mostrar_resumen()
        elif selected_index == 1:
            # Crea y muestra la vista de Reservas
            reserva_view = ReservaView(page)
            main_content.content = ft.AnimatedSwitcher(
                duration=300,
                transition=ft.AnimatedSwitcherTransition.FADE,
                content=reserva_view.get_view(),
            )
        elif selected_index == 2:
            # Crea y muestra la vista de Usuarios
            usuario_view = UsuarioView(page)
            main_content.content = ft.AnimatedSwitcher(
                duration=300,
                transition=ft.AnimatedSwitcherTransition.FADE,
                content=usuario_view.get_view(),
            )
        elif selected_index == 3:
            # Crea y muestra la vista de Mesas
            mesa_view = MesaView(page)
            main_content.content = ft.AnimatedSwitcher(
                duration=300,
                transition=ft.AnimatedSwitcherTransition.FADE,
                content=mesa_view.get_view(),
            )
        # Actualiza la página para reflejar los cambios
        page.update()

    # Función para mostrar el resumen global de la base de datos
    def mostrar_resumen():
        # Obtiene los totales de usuarios, mesas y reservas
        total_usuarios = contar_usuarios()
        total_mesas = contar_mesas()
        total_reservas = contar_reservas()

        # Construye la vista de resumen con tarjetas informativas
        resumen = ft.Column(
            controls=[
                ft.Text("Resumen Global", size=32, weight="bold", color=ft.colors.BLUE_700),
                ft.Divider(height=20),
                ft.Row(
                    controls=[
                        create_summary_card("Usuarios", total_usuarios, ft.icons.PEOPLE),
                        create_summary_card("Mesas", total_mesas, ft.icons.TABLE_CHART),
                        create_summary_card("Reservas", total_reservas, ft.icons.LIBRARY_BOOKS_SHARP),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Muestra la vista de resumen en el contenedor principal con una animación
        main_content.content = ft.AnimatedSwitcher(
            duration=300,
            transition=ft.AnimatedSwitcherTransition.FADE,
            content=resumen,
        )
        page.update()

    # Función auxiliar para crear una tarjeta resumen con título, valor e ícono
    def create_summary_card(title, value, icon):
        return ft.Card(
            elevation=4,
            content=ft.Container(
                padding=20,
                width=200,
                height=120,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(icon, color=ft.colors.BLUE_500, size=30),
                                ft.VerticalDivider(width=20),
                                ft.Text(title, size=20, weight="bold"),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Text(str(value), size=28, weight="bold", color=ft.colors.BLUE_700),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ),
        )

    # Agrega la barra de navegación y el contenedor principal a la página
    page.add(
        ft.Row(
            controls=[
                nav_bar,
                main_content
            ],
            expand=True,
        )
    )

    # Muestra el resumen global al iniciar la aplicación
    mostrar_resumen()
