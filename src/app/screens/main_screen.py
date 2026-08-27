import asyncio

from textual.widgets import Header, Footer
from textual.screen import Screen
from textual.containers import Horizontal

from src.app.widgets.custom_panel import CustomPanel
from src.app.widgets.custom_process_log import CustomProcessLog
from src.app.widgets.custom_data_table import CustomDataTable
from src.app.widgets.custom_label import CustomLabel
from src.app.widgets.custom_rule import CustomRule
from src.app.widgets.custom_progress_bar import CustomProgressBar
from src.app.widgets.custom_popup import CustomPopup
from src.core.scraper import Scraper
from src.core.request import Request
from src.core.export_csv import ExportCSV


class MainScreen(Screen):
    BINDINGS = [
        ("q", "quit", "Cerrar Aplicación"),
        ("s", "scraper", "Ejecutar Scraper")
    ]

    def __init__(self):
        super().__init__()

        self.title = "Job Listings Scraper"

    def compose(self):
        yield Header(show_clock=True)
        with Horizontal(id="main_layout"):
            yield CustomProcessLog(id="left_panel")
            yield CustomPanel("Resultado Scraper", id="right_panel")
        yield Footer()

    def on_mount(self):
        job_table = CustomDataTable(
            columns=["Nombre Puesto", "Nombre de la compañia", "Ubicación", "URL Detalle oferta"],
            rows=[]
        )

        self.query_one("#right_panel", CustomPanel).show_widget(job_table)

    def update_custom_process_log(self, widget):
        log = self.query_one("#left_panel", CustomProcessLog)
        log.add_widget(widget)

    async def action_scraper(self):
        # Limpiar el panel de logs de una ejecucion anterior
        logs = self.query_one("#left_panel", CustomProcessLog)
        await logs.remove_children()

        # Eliminar filas de una ejecucion anterior, conservando las columnas
        self.query_one("#right_panel", CustomPanel).query_one(CustomDataTable).clear()

        jobs_links = []

        self.update_custom_process_log(CustomLabel(text="[red]\u27F2 Inicializando Scraper[/red]"))
        self.update_custom_process_log(
            CustomLabel(text="[red]\u27F2 Obteniendo links para extraer información[/red]"))
        self.update_custom_process_log(CustomRule(orientation="horizontal", line_style="dashed"))

        try:
            # Obtener el HTML de la pagina principal de "fake-jobs" para
            # extraer los links de cada oferta de trabajo
            response = Request("https://realpython.github.io/fake-jobs/")
            s = Scraper(response.get_request())
            footer_card = s.get_html().find_all("footer", attrs={"class": "card-footer"})

            for card in footer_card:
                links = card.find_all("a")
                href = links[1].get("href")
                jobs_links.append(href)
                self.update_custom_process_log(CustomLabel(f"\u2713 {href}"))
                await asyncio.sleep(0.1)
            self.update_custom_process_log(CustomRule(orientation="horizontal", line_style="dashed"))

            job_table = self.query_one("#right_panel", CustomPanel).query_one(CustomDataTable)
            self.update_custom_process_log(
                CustomLabel(text="[red bold]\u27F2 Actualizando tabla de resultados...[/red bold]"))

            # Barra de progreso: el total corresponde a la cantidad de
            # ofertas de trabajo encontradas en la página principal
            progress_bar = CustomProgressBar(total=len(jobs_links), show_eta=False)
            self.update_custom_process_log(progress_bar)

            # Visitar cada oferta de trabajo y extraer:
            # título del puesto, nombre de la empresa, ubicación y URL de detalle
            for link in jobs_links:
                response = Request(link)
                s = Scraper(response.get_request())
                div_job_offer = s.get_html().find("div", attrs={"class": "box"})

                job_title = div_job_offer.find("h1", attrs={"class": "title is-2"}).get_text(strip=True)
                company_name = div_job_offer.find("h2", attrs={"class": "subtitle is-4 company"}).get_text(strip=True)

                location = div_job_offer.find("p", id="location")
                location.strong.decompose()
                location = location.get_text(strip=True)

                job_detail_url = link

                # Agregar la fila a la tabla ya montada (actualización en vivo, sin recrear el widget)
                job_table.add_row(job_title, company_name, location, job_detail_url)

                # actualizar la barra de progreso en 1 unidad
                progress_bar.advance(1)

                # Pausa entre peticiones para no saturar el servidor y reducir
                # el riesgo de bloqueo por comportamiento tipo bot
                await asyncio.sleep(0.2)

            self.update_custom_process_log(CustomRule(orientation="horizontal", line_style="dashed"))
            self.update_custom_process_log(CustomLabel(text="[red bold]\u2713 Scraper finalizado[/red bold]"))
            self.update_custom_process_log(CustomRule(orientation="horizontal", line_style="dashed"))
            self.update_custom_process_log(CustomLabel(text="[red bold]\u2713 Exportando datos[/red bold]"))
            self.update_custom_process_log(CustomRule(orientation="horizontal", line_style="dashed"))

            await self.__exportar_datos()

            self.update_custom_process_log(CustomLabel(text="[red bold]\u2713 Proceso finalizado[/red bold]"))
        except Exception as e:
            self.update_custom_process_log(CustomLabel(text=str(f"\u274C  {e}")))


    async def __exportar_datos(self):
        # Obtener la CustomDataTable ubicada dentro del panel derecho,
        # que contiene los resultados a exportar
        job_table_rows = self.query_one("#right_panel", CustomPanel).query_one(CustomDataTable)

        # Contar el número total de filas de la tabla (define también
        # el total que usará la barra de progreso)
        count_row = job_table_rows.row_count

        # Filas a exportar a CSV. La primera fila debe contener los nombres
        # de columna (cabecera); el resto son los datos, en el mismo orden
        # de columnas.
        data_rows = [["Nombre Puesto", "Nombre de la compañia", "Ubicacion", "URL Detalle oferta"]]

        # Poblar data_rows leyendo cada fila directamente desde la tabla en pantalla
        for row in range(count_row):
            data_row = job_table_rows.get_row_at(row)
            data_rows.append(data_row)

        # Objeto encargado de escribir data_rows como archivo CSV en disco
        file_csv = ExportCSV(data_rows)

        # Barra de progreso configurada con el total de filas a exportar
        pgb = CustomProgressBar(count_row, False)

        # Popup modal que se muestra mientras dura la exportación
        popup = CustomPopup("Exportando datos extraído a archivo CSV.\nEn directorio /data.",
                            id="popup")
        # espera a que el popup esté montado
        await self.app.push_screen(popup)

        # monta la barra de progreso dentro del popup
        await popup.show_widget(pgb)

        # breve pausa para que el popup termine de renderizarse
        await asyncio.sleep(0.05)

        # Escribe el CSV fila por fila; cada iteración avanza la barra
        # de progreso y cede el control al event loop para refrescar la UI
        for i in file_csv.create_csv_file():
            pgb.advance(i)
            await asyncio.sleep(0.02)

        # Cierra el popup una vez finalizada la exportación
        await self.app.pop_screen()
