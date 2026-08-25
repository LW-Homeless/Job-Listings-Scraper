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
from src.core.scraper import Scraper
from src.core.request import Request


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
            CustomLabel(text="[red]\u27F2 Obteniendo links para extraer la información[/red]"))
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

                #actualizar la barra de progreso en 1 unidad
                progress_bar.advance(1)

                # Pausa entre peticiones para no saturar el servidor y reducir
                # el riesgo de bloqueo por comportamiento tipo bot
                await asyncio.sleep(1)
            self.update_custom_process_log(CustomRule(orientation="horizontal", line_style="dashed"))
            self.update_custom_process_log(CustomLabel(text="[red bold]\u2713 Scraper finalizado[/red bold]"))
        except Exception as e:
            self.update_custom_process_log(CustomLabel(text=str(f"\u274C  {e}")))
