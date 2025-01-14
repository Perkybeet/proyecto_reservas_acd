import flet as ft
from views.reserva_view import ReservaView
from views.usuario_view import UsuarioView
from views.mesa_view import MesaView
from services.crud_operations import contar_usuarios, contar_mesas, contar_reservas

def main_view(page: ft.Page):
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

    # Sidebar de navegación
    nav_items = [
        ft.NavigationRailDestination(icon=ft.icons.HOME, label="Resumen"),
        ft.NavigationRailDestination(icon=ft.icons.LIBRARY_BOOKS_SHARP, label="Reservas"),
        ft.NavigationRailDestination(icon=ft.icons.PEOPLE, label="Clientes"),
        ft.NavigationRailDestination(icon=ft.icons.TABLE_CHART, label="Mesas"),
    ]

    nav_bar = ft.NavigationRail(
        destinations=nav_items,
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        on_change=lambda e: navigate(e.control.selected_index),
        min_width=80,
        extended=False,
    )

    # Contenedor principal para el contenido
    main_content = ft.Container(
        padding=20,
        expand=True,
        bgcolor=ft.colors.GREY_50,
    )
    # Navegacion de la base de datos
    def navigate(selected_index):
        if selected_index == 0:
            mostrar_resumen()
        elif selected_index == 1:
            reserva_view = ReservaView(page)
            main_content.content = ft.AnimatedSwitcher(
                duration=300,
                transition=ft.AnimatedSwitcherTransition.FADE,
                content=reserva_view.get_view(),
            )
        elif selected_index == 2:
            usuario_view = UsuarioView(page)
            main_content.content = ft.AnimatedSwitcher(
                duration=300,
                transition=ft.AnimatedSwitcherTransition.FADE,
                content=usuario_view.get_view(),
            )
        elif selected_index == 3:
            mesa_view = MesaView(page)
            main_content.content = ft.AnimatedSwitcher(
                duration=300,
                transition=ft.AnimatedSwitcherTransition.FADE,
                content=mesa_view.get_view(),
            )
        page.update()

    def mostrar_resumen():
        total_usuarios = contar_usuarios()
        total_mesas = contar_mesas()
        total_reservas = contar_reservas()

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

        main_content.content = ft.AnimatedSwitcher(
            duration=300,
            transition=ft.AnimatedSwitcherTransition.FADE,
            content=resumen,
        )
        page.update()

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

    # Agregar la barra de navegación y el contenido principal a la página
    page.add(
        ft.Row(
            controls=[
                nav_bar,
                main_content
            ],
            expand=True,
        )
    )

    # Mostrar el resumen global por defecto al iniciar
    mostrar_resumen()