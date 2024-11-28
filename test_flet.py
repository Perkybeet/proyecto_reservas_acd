import flet as ft

def main(page: ft.Page):
    page.title = "Test Flet App"
    page.add(ft.Text("¡Hola, Flet!"))

if __name__ == "__main__":
    ft.app(target=main) 