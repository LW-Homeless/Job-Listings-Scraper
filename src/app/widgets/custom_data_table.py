import webbrowser
from textual.widgets import DataTable


class CustomDataTable(DataTable):
    DEFAULT_CSS = """
               CustomDataTable {
                   border: round rgb(120, 120, 120);
                   height: 98%;
                   scrollbar-background: rgb(120, 120, 120);
                   scrollbar-gutter: stable;
                   scrollbar-color: rgb(252, 192, 0);
                   scrollbar-color-hover: rgb(255, 221, 97);
                   scrollbar-background-hover: rgb(120, 120, 120);
                   scrollbar-background-active: rgb(120, 120, 120);
                   scrollbar-color-active: rgb(252, 192, 0);
               }

               CustomDataTable > .datatable--header {
                  color: rgb(252, 192, 0);
               }
               """

    URL_COLUMN_INDEX = 3

    def __init__(self, columns, rows, **kwargs):
        super().__init__(**kwargs)

        self.__columns = columns
        self.__rows = rows

    def on_mount(self):
        self.update_custom_datatable()

    def update_custom_datatable(self):
        self.add_columns(*self.__columns)
        for row in self.__rows:
            self.add_row(*row)

    def on_data_table_cell_highlighted(self, event: DataTable.CellHighlighted):
        if event.coordinate.column == self.URL_COLUMN_INDEX:
            self.tooltip = "Click o Ctrl+Click para abrir la página en el navegador."
        else:
            self.tooltip = None

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        if event.coordinate.column == self.URL_COLUMN_INDEX:
            webbrowser.open(str(event.value))
