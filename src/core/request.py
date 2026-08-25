from requests import get
from requests.exceptions import RequestException

from src.core.random_user_agent import RandomUserAgent


class Request:
    """
    Realiza Peticiones HTTP GET a una URL especifica.

    Encapsula la logica de una peticion HTTP simple usando la libreria 'Requests',
    asignando un user-agent aleatorio a cada instacia para evitar bloqueos por parte
    del servidor de destino

    Attributes:
        __url (str): URL a la que se realizara la peticion.
        __headers (dict): Cabecera enviada en la peticion,
            incluyendo un user-agent aleatorio.
        __response (str | None): Contenido de text de la ultima respuesta obtenida.
            Es 'None' hasta que se llama a 'get_request()'.
    """

    def __init__(self, url):
        """
        Inicializa la peticion con la URL de destino.

        Args:
            url (str): URL completa a la que se realizara la peticion GET.
        """
        self.__url = url
        self.__headers = {"user-agent": RandomUserAgent.get_user_agent()}
        self.__response = None

    def get_request(self):
        """
        Ejecuta la peticion GET y retorna el contenido de la respuesta.

        Realiza una petición HTTP GET a la URL configurada en el
        constructor, usando el user-agent generado aleatoriamente.
        El resultado se almacena internamente en `__response` ademas
        de ser retornado.

        Returns:
           str: Contenido HTML/texto de la respuesta del servidor.

        Raises:
           RequestException: Si ocurre un error de conexion, timeout,
               o cualquier otro problema al intentar comunicarse con
               el servidor (por ejemplo, DNS no resuelto, servidor
               caido, o conexion rechazada).
       """
        try:
            response = get(self.__url, headers=self.__headers)
            self.__response = response.text

            return self.__response
        except RequestException:
            raise RequestException("No se pudo establer la conexión con el servidor.")
