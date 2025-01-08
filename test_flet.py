import datetime
import flet as ft

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- MANEJADORES DE EVENTOS PARA DATEPICKER ---
    def date_change(e):
        page.add(ft.Text(f"Fecha seleccionada: {e.control.value.strftime('%Y-%m-%d')}"))

    def date_dismiss(e):
        page.add(ft.Text(f"DatePicker cerrado sin seleccionar fecha."))

    # Creamos el DatePicker
    date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=2023, month=10, day=1),
        last_date=datetime.datetime(year=2024, month=10, day=1),
        on_change=date_change,
        on_dismiss=date_dismiss,
    )

    # --- MANEJADORES DE EVENTOS PARA TIMEPICKER ---
    def time_change(e):
        page.add(ft.Text(f"Hora seleccionada: {time_picker.value}"))

    def time_dismiss(e):
        page.add(ft.Text(f"TimePicker cerrado. Último valor: {time_picker.value}"))

    def time_entry_mode_change(e):
        page.add(ft.Text(f"Modo de entrada cambiado a {e.entry_mode}"))

    # Creamos el TimePicker
    time_picker = ft.TimePicker(
        confirm_text="Confirmar",
        error_invalid_text="Hora fuera de rango",
        help_text="Selecciona tu franja horaria",
        on_change=time_change,
        on_dismiss=time_dismiss,
        on_entry_mode_change=time_entry_mode_change,
    )

    # Botones para abrir DatePicker y TimePicker
    btn_fecha = ft.ElevatedButton(
        "Seleccionar Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: page.open(date_picker),
    )

    btn_hora = ft.ElevatedButton(
        "Seleccionar Hora",
        icon=ft.Icons.TIME_TO_LEAVE,
        on_click=lambda _: page.open(time_picker),
    )

    page.add(btn_fecha, btn_hora)


ft.app(target=main)
