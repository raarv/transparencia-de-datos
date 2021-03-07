import scrapy

# Preparamos los URLs iniciales
urls = []
a = [*range(57, 65, 1)]
b = [*range(1, 3, 1)]
# Aquí también se puede usar re.split() para separar el URL sin necesidad
# de incluir los # que puse para ahorrar tiempo.
urlMod = """http://sil.gobernacion.gob.mx/Reportes/Integracion/HCongreso
        /ResultIntegHCongreso.php
        ?SID=&Prin_El=0&Entidad=0&Legislatura=#&Camara=#&Partido=0&Orden="""
urlDividido = urlMod.split("#")

for i in range(len(a)):
    for j in range(len(b)):
        urls.append(urlDividido[0] + str(a[i]) + urlDividido[1] + str(b[j])
                    + urlDividido[2])

# Spider
URLlegis = """http://sil.gobernacion.gob.mx/Librerias
            /pp_PerfilLegislador.php?SID=&Referencia="""

cssPath = 'tr td.tddatosazul a[href^="#"]'


class SILSpider(scrapy.Spider):
    name = 'silspider'

    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        referencias = response.css(cssPath).re(r'(?<=Referencia=)\d+')

        links = [URLlegis + referencia for referencia in referencias]

        for link in links:
            yield response.follow(url=link, callback=self.parse2)

# Aquí debemos diseñar el diccionario con los campos que deseamos extraer,
# quizá sea más fácil con RegEx, las tags no tienen nada característico
# con lo cual podamos identificar cada cosa, lo único útil es que todo lo que
# buscamos está dentro de múltiples <table>, aunque extremadamente sucio

# Primero debemos, a partir del nombre y fecha de nacimiento, crear un ID
# para cada legislador (RegEx)

# Después, identificar todas las categorías que queremos para
# así poder extraer el texto que esté contenido en tablas tales que
# contengan el nombre de esta categoría en su título (creo que es una de las
# primeras entradas de la tabla)

# Luego usar esas categorías como llaves en nuestro diccionario y meter todo lo
# correspondiente como una lista bajo esa llave

    def parse2(self, response):
        yield "hello"
