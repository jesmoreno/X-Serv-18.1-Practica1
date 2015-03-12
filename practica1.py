#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import cgitb

class servidor(webapp.webApp):

    urlsStored = {}
    checkUrls = {}

    def parse(self, request):

        verb = request.split()[0]
        resource = request.split()[1]
        body = request.split("\r\n\r\n")[1]
 
        return (verb, resource, body)

    def process(self, parsedRequest):

        #imagenFondo = "http://lorenabarba.com/wp-content/uploads/2014/05/keep-calm-and-code-python_BW.png"
        (verb, resource, body) = parsedRequest
        
        #Creo dos strings donde almaceno las paginas reales y acortadas
        paginaAcortada = "http://localhost:1234/"
        keys = ""
        values = ""
        if len(self.urlsStored) != 0:
                for index in range(0,len(self.urlsStored)):
                        keys += "<p>("+ str(index+1) + ")" + paginaAcortada + str(index) + "</p>"
                        values += "<p>("+ str(index+1) + ")" + self.urlsStored[str(index)] + "</p>"

        if resource == '/':
            if verb == "GET":

                httpCode = "200 OK"
                htmlCode = ("<html>"
                           "<body bgcolor= #8181F7>"
                           "<h1>CORTADOR DE URL'S</h1>" +
                           "<form name= search  action= /  method= POST >" +
                           "Insertar URL: <input type= text  name= url >" +
                           "<input type= submit value= Buscar >" +
                           "<hr>"+
                           "<table align = center border=1>"+
                           "<td bgcolor = #BDBDBD>" +"URL'S REALES"+"</td>"+
                           "<td bgcolor = #BDBDBD>" +"URL'S ACORTADAS"+"</td>"+
                           "<tr><td bgcolor= #FBFBEF>"+
                           values +
                           "<td bgcolor= #FBFBEF>"+ 
                           keys +
                           "</td></table>"+
                           
                           "</body>"
                           "</html>")

            elif verb == "POST":

                url = body.split('=')[1]

                #Sustituyo la parte del string con caracteres especiales(: = %3A,// = %2F%2F)
                if(url == ("http%3A%2F%2F" + url[13:]) or url == ("https%3A%2F%2F" + url[14:])):

                    url =url.replace("%3A",':')
                    url =url.replace("%2F",'/')
                
                else:
                    #Completo la url si no empieza por http o http
                    url = "http://" + url
              

                #Calculo el numero de urls almacenadas en mi diccionario
                numUrls = len(self.urlsStored)

                #Almaceno en diccionario si no hay nada o si no la tiene
                if not self.checkUrls.has_key(url) or numUrls == 0:

                    self.urlsStored[str(numUrls)] = url
                    self.checkUrls[url] = str(numUrls)
                
                #Genero los Strings de la pagina real y acortada para imprimir
                index = self.checkUrls[url]
                paginaFinal = paginaAcortada + index        
                
                httpCode = "200 OK"
                htmlCode = ("<html>"
                           "<body bgcolor= #8181F7>"
                           "<h1>CORTADOR DE URL'S</h1>" +
                           "<table border=1>"+
                           "<td bgcolor = #BDBDBD>" +"Real"+"</td>"+
                           "<td bgcolor = #BDBDBD>" +"Acortada"+"</td>"+
                           "<tr><td bgcolor= #FBFBEF>"+
                           "<a href="+url+">"+url.split("//",1)[1]+"</a></p>"+
                           "<td bgcolor= #FBFBEF>"
                           "<a href="+paginaFinal+">"+paginaFinal.split("//",1)[1]+"</a></p>"
                           "</td></table>"+
                           "<hr>"+
                           "<form method= get action= http://localhost:1234>"
                           "<input type= submit  value= Volver a página inicial/>"+
                           "</form>"
                           "</body>"
                           "</html>")

        elif verb == "GET" and resource[0] == '/' and len(resource) > 1:
            key = resource[1]

            if (self.urlsStored.has_key(key)):
                url = self.urlsStored[key]

                httpCode = "301 Mudado permanentemente"   
                htmlCode = ("<html>"
                            "<h1>"
                            "HTTP REDIRECT"
                            "</h1>"
                            "<head>"
                            "<meta http-equiv= Refresh  content= 2;url="+url+">"
                            "</head>"
                            "<body>"
                            "<p>URL ="+ url +"</p>"
                            "</body>"
                            "</html>")       
            else:
                httpCode = "404 Error"
                htmlCode = ("<html><body><h1>HTTP ERROR"+
                        "</h1>"+
                        "<p>Recurso no disponible</p>"+
                        "</body></html>")

        return(httpCode,htmlCode)

if __name__ == "__main__":
        testServidor = servidor('localhost', 1234)
