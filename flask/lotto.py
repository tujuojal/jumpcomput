#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
import cgitb
cgitb.enable()
import cgi
import random

__author__="vellu"
__date__ ="$19.1.2010 19:38:19$"

#Lottopeli 1.0
#TJTA 270 Viikkotehtävä 2
#Laajuus: 5
#Käyttäjältä kysellään numeroita, joita sitten verrataan generoituihin
#numeroihin. Vastaavuuksien määrä tulostetaan käyttäjälle muun tiedon ohella.

def anna_nimi (maara):
    #Antaa arvonnalle nimen numeromäärän mukaan
    nimi = ""
    if maara == 7:
        nimi = "Lotto"
    elif maara == 6:
        nimi = "Viking Lotto"
    else:
        nimi = "Tuntematon lottoarvonta"
    return nimi


def arvonumerot (maara, pieni, suuri, aikaisempi):
    #Arpoo halutun määrän numeroita tietyltä väliltä listaan
    #Ei laita kahta samaa numeroa listaan
    #Järjestää listan
    y = 1
    lista = []
    while (y <= maara):
        numero = random.randint(pieni, suuri)
        while numero in lista or numero in aikaisempi:
            numero = random.randint(pieni, suuri)
        lista.append(numero)
        y = y + 1
    lista.sort()
    return lista

def tarkista_oikeat (numerot, syotetyt):
    #Vertaa listoja
    #Palauttaa numeroiden määrän, jotka löytyvät molemmista listoista
    kierroksia = len(numerot)
    i = 0
    oikeita = 0
    while i < kierroksia:
        if syotetyt.count(numerot[i]) == 1:
            oikeita = oikeita + 1
        i = i + 1
    return oikeita


def sivu0():
    #Ensimmäinen sivu
    #Keräilee tietoja käyttäjältä lomakkeella
    print """
    <form action="lotto_vt2.cgi" method="post">
	<h3>Anna asetukset lottokoneelle</h3>
        <p><input name="sivu" type="hidden" value="1" /></p>
        <p><label for="nro_maara">Kuinka monta numeroa arvotaan</label>
	<input id="nro_maara" name="nro_maara" size="2" type="text" value="6" /></p>
        <p><label for="lisa_nro_maara">Kuinka monta lisänumeroa arvotaan</label>
	<input id="lisa_nro_maara" name="lisa_nro_maara" size="2" type="text" value="3" /></p>
	<p><label for="pienin_numero">Pienin numero</label>
	<input id="pienin_numero" name="pienin_numero" size="2" type="text" value="1" /></p>
        <p><label for="suurin_numero">Suurin numero</label>
	<input id="suurin_numero" name="suurin_numero" size="2" type="text" value="39" /></p>
        <p><input name="submit" type="submit" value="Lottoarvonta" /></p>
    </form>"""

def sivu1(form):
    #Toinen sivu
    #Keräilee tietoja käyttäjältä lomakkeella
    #Generoi lomaketta
    maara = int(form.getvalue('nro_maara'))
    y = 1
    print """
    <h3>Syötä haluamasi numerot</h3>
    <form>
        <form action="lotto.cgi" method="post">
        <p><input name="sivu" type="hidden" value="2" /></p>"""
    while y <= maara:
        print """
        <p><label for="numero_%i">%i. numero:</label>
        <input id="numero_%i" name="numero" size=8" type="text" />
        </p>""" % (y,y,y)
        y = y + 1
    print """<p>"""
    print """   <input type="hidden" name="nro_maara" value="%s" />""" % form.getvalue('nro_maara')
    print """   <input type="hidden" name="lisa_nro_maara" value="%s" />""" % form.getvalue('lisa_nro_maara')
    print """   <input type="hidden" name="pienin_numero" value="%s" />""" % form.getvalue('pienin_numero')
    print """   <input type="hidden" name="suurin_numero" value="%s" />""" % form.getvalue('suurin_numero')
    print """</p>"""

    print """
        <p><input name="submit" type="submit" value="Suorita arvonta" /> </p>
    </form>"""

def sivu2(form):
    #Viimeinen sivu
    #Tulostelee tietoja käyttäjälle

    numeroiden_maara = int(form["nro_maara"].value)
    pienin = int(form["pienin_numero"].value)
    suurin = int(form["suurin_numero"].value)
    lisa_nro_maara = int(form["lisa_nro_maara"].value)

    pelin_nimi = ""
    pelin_nimi = anna_nimi(numeroiden_maara)

    aikaisempi = []
    arvotut_numerot = []
    arvotut_numerot = arvonumerot(numeroiden_maara, pienin, suurin, aikaisempi)
    aikaisempi = arvotut_numerot
    lisa_numerot = []
    lisa_numerot = arvonumerot(lisa_nro_maara, pienin, suurin, aikaisempi)

    print """<h2>%s</h2>""" % pelin_nimi
    #Tulostaa syötetyt lottonumerot
    print """<h3>Syöttämäsi lottonumerot</h3>"""
    syotetyt = []
    item = 1
    for item in form.getvalue('numero'):
        syotetyt.append(int(item))
    syotetyt.sort()

    print """<table border="1">
    <tr>"""
    item = 1
    for item in syotetyt:
        print """<td>%i</td>""" % item
    print """</tr>
    </table><br/>"""

    #Tulostaa lottonumerot
    print """<h3>Arvotut lottonumerot</h3><table border="1">
    <tr>"""
    item = 1
    for item in arvotut_numerot:
        print """<td>%i</td>""" % item
    print """</tr>
    </table><br/>"""

    #Tulostaa lisänumerot
    print """<h3>Arvotut lisänumerot</h3><table border="1">
    <tr>"""
    item = 1
    for item in lisa_numerot:
        print """<td>%i</td>""" % item
    print """</tr>
    </table>"""

    #Tulostaa oikein osuneet
    varsinaisia_oikein = 0
    varsinaisia_oikein = tarkista_oikeat(arvotut_numerot, syotetyt)
    lisanumeroita_oikein = 0
    lisanumeroita_oikein = tarkista_oikeat(lisa_numerot, syotetyt)
    print """<h3>Tulos</h3>"""
    print """<p>Sait oikein %i varsinaista numeroa
                ja %i lisänumeroa.</p>""" % (varsinaisia_oikein, lisanumeroita_oikein)

def main():
    #Pääohjelma
    #Tarkistaa lähinnä mikä sivu näytetään käyttäjälle
    print """Content-type: text/html\n"""
    print """<?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fi">
    <head>
      <title>Lottorivin arpoja</title>
    </head>
    <body>
    <h1>Lottorivin arpoja</h1>"""
    form = cgi.FieldStorage()
    sivu = form.getvalue('sivu')

    if sivu == '1':
        sivu1(form)
    elif sivu == '2':
        sivu2(form)
    else:
        sivu0()
    print """
    </body>
    </html>
    """

#Aloitetaan pääohjelma
main()
