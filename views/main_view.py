import flet as ft
from views.reserva_view import ReservaView
from views.usuario_view import UsuarioView
from views.mesa_view import MesaView
from services.crud_operations import contar_usuarios, contar_mesas, contar_reservas


def main_view(page: ft.Page):
    page.title = "Libro de Reservas"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Definir un contenedor para el contenido principal
    main_content = ft.Container()

    def navigate_to_reservas(e):
        print("Navegando a Reservas")
        # Reemplaza el contenido actual por el seleccionado
        reserva_view = ReservaView(page)
        main_content.content = reserva_view.get_view()
        page.update()

    def navigate_to_usuarios(e):
        print("Navegando a Usuarios")
        # Reemplaza el contenido actual por el seleccionado
        usuario_view = UsuarioView(page)
        main_content.content = usuario_view.get_view()
        page.update()

    def navigate_to_mesas(e):
        print("Navegando a Mesas")
        # Reemplaza el contenido actual por el seleccionado
        mesa_view = MesaView(page)
        main_content.content = mesa_view.get_view()
        page.update()

    def navigate_to_main(e):
        # Muestra el resumen global
        mostrar_resumen()
        page.update()

    def mostrar_resumen():
        total_usuarios = contar_usuarios()
        total_mesas = contar_mesas()
        total_reservas = contar_reservas()

        resumen = ft.Column(
            controls=[
                ft.Text("Resumen Global", size=30, weight="bold", color="blue"),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                padding=10,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Usuarios", size=20),
                                        ft.Text(str(total_usuarios), size=25, weight="bold"),
                                    ]
                                )
                            ),
                            width=150,
                            height=100,
                        ),
                        ft.Card(
                            content=ft.Container(
                                padding=10,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Mesas", size=20),
                                        ft.Text(str(total_mesas), size=25, weight="bold"),
                                    ]
                                )
                            ),
                            width=150,
                            height=100,
                        ),
                        ft.Card(
                            content=ft.Container(
                                padding=10,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Reservas", size=20),
                                        ft.Text(str(total_reservas), size=25, weight="bold"),
                                    ]
                                )
                            ),
                            width=150,
                            height=100,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        main_content.content = resumen

    # Botones de navegación
    nav_bar = ft.Row(
        controls=[
            ft.TextButton("Resumen", on_click=navigate_to_main),
            ft.TextButton("Reservas", on_click=navigate_to_reservas),
            ft.TextButton("Usuarios", on_click=navigate_to_usuarios),
            ft.TextButton("Mesas", on_click=navigate_to_mesas),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    # Agregar la barra de navegación y el contenido principal a la página
    page.add(
        ft.Column(
            controls=[
                nav_bar,
                ft.Divider(),
                main_content
            ],
            expand=True,
        )
    )

    # Mostrar el resumen global por defecto al iniciar
    mostrar_resumen()