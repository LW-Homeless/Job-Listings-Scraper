import csv
from pathlib import Path


class ExportCSV:
    """
    Exporta un conjunto de datos tabulares a un archivo CSV.

    La clase recibe los datos ya procesados (por ejemplo, las filas
    extraídas de una CustomDataTable de Textual) y los escribe en un
    archivo CSV ubicado en 'data/jobs.csv', relativo a la raíz del
    proyecto.

    El método principal (create_csv_file) es un generador: yieldea el
    índice de cada fila a medida que se escribe, lo que permite a quien
    lo consume (por ejemplo, una pantalla de Textual) mostrar progreso
    en tiempo real sin bloquear la interfaz.

    Attributes:
        __file_data: Colección de filas a exportar. Cada elemento debe
            ser un iterable (lista) con los valores de una fila,
            en el mismo orden que las columnas esperadas del CSV.
    """

    def __init__(self, file_data):
        """
        Inicializa el exportador con los datos a escribir.

        Args:
            file_data: Iterable de filas (cada fila es a su vez un
                iterable de valores) que se escribirán en el CSV.
                No incluye encabezados de columna; si se necesitan,
                deben venir como la primera fila de file_data.
        """
        self.__file_data = file_data

    def create_csv_file(self):
        """
        Escribe self.__file_data en 'data/jobs.csv' y reporta el progreso.

        Calcula la carpeta raíz del proyecto subiendo 3 niveles desde la
        ubicación de este archivo, y escribe el CSV en la subcarpeta
        'data'. Si el archivo ya existe, lo sobrescribe por completo
        (modo 'w').

        Al ser un generador, la escritura ocurre de forma perezosa: cada
        fila se escribe y se yieldea su índice antes de continuar con la
        siguiente, permitiendo a quien lo itera actualizar una barra de
        progreso o un log en cada paso.

        Yields:
            int: El índice (0, 1, 2, ...) de la fila que se acaba de
                escribir en el archivo.

        Raises:
            OSError: Si el archivo no puede abrirse o escribirse (por
                ejemplo, por permisos insuficientes o si la carpeta
                'data' no existe).
            csv.Error: Si ocurre un error de formato al escribir alguna
                fila.
        """
        base_dir = Path(__file__).resolve().parent.parent.parent

        with open(base_dir.joinpath("data", "jobs.csv"), mode="w", newline="", encoding="utf-8") as file:
            cursor = csv.writer(file, delimiter=",")
            for i, line in enumerate(self.__file_data):
                cursor.writerow(line)
                yield i
