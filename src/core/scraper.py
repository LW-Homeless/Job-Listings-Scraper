from bs4 import BeautifulSoup


class Scraper:
    """
    Analiza (parsea) un documento HTML y lo convierte en un objeto navegable.

    Envuelve BeautifulSoup para transformar una cadena de texto HTML
    en un arbol de elementos que puede recorrerse y consultarse mediante
    los metodos de busqueda de BeautifulSoup (`find`, `find_all`, `select`, etc.).

    Attributes:
        __html_doc (str): Contenido HTML crudo a analizar, recibido
            en el constructor.
    """
    def __init__(self, html_doc):
        """
        Inicializa el scraper con el documento HTML a procesar.

        Args:
            html_doc (str): Cadena de texto con el contenido HTML
                a analizar (por ejemplo, la respuesta obtenida de
                una peticion HTTP mediante la clase `Request`).
        """
        self.__html_doc = html_doc

    def get_html(self):
        """
        Analiza el documento HTML y retorna su representación navegable.

        Utiliza el parser `html.parser` (incluido en la librería estándar
        de Python, sin dependencias externas adicionales) para construir
        el arbol de elementos del documento.

        Returns:
            BeautifulSoup: Objeto navegable que representa el documento
                HTML, listo para realizar busquedas de elementos mediante
                los metodos de BeautifulSoup (`find`, `find_all`, `select`,
                `select_one`, etc.).
        """
        soup = BeautifulSoup(self.__html_doc, 'html.parser')
        return soup
