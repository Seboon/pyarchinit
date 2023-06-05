
#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
        pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
                             stored in Postgres
                             -------------------
    begin                : 2007-12-01
    copyright            : (C) 2008 by Luca Mandolesi; Enzo Cocca <enzo.ccc@gmail.com>
    email                : mandoluca at gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import datetime
from datetime import date
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from builtins import object
from builtins import range
from builtins import str
from reportlab.lib import colors
from reportlab.lib.pagesizes import (A4,A3)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, PageBreak, SimpleDocTemplate, Spacer, TableStyle, Image
from reportlab.platypus.paragraph import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
# Registered font family
pdfmetrics.registerFont(TTFont('Cambria', 'Cambria.ttc'))
pdfmetrics.registerFont(TTFont('cambriab', 'cambriab.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
# Registered fontfamily
registerFontFamily('Cambria',normal='Cambria')
from ..db.pyarchinit_conn_strings import Connection

from .pyarchinit_OS_utility import *


class NumberedCanvas_Findssheet(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def define_position(self, pos):
        self.page_position(pos)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Cambria", 5)
        self.drawRightString(200 * mm, 20 * mm,
                             "Pag. %d di %d" % (self._pageNumber, page_count))  # scheda us verticale 200mm x 20 mm


class NumberedCanvas_FINDSindex(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def define_position(self, pos):
        self.page_position(pos)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Cambria", 5)
        self.drawRightString(270 * mm, 10 * mm,
                             "Pag. %d di %d" % (self._pageNumber, page_count))  # scheda us verticale 200mm x 20 mm


class NumberedCanvas_CASSEindex(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def define_position(self, pos):
        self.page_position(pos)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Cambria", 5)
        self.drawRightString(270 * mm, 10 * mm,
                             "Pag. %d di %d" % (self._pageNumber, page_count))  # scheda us verticale 200mm x 20 mm


class single_Finds_pdf_sheet(object):
    def __init__(self, data):
        self.id_invmat = data[0]
        self.sito = data[1]
        self.numero_inventario = data[2]
        self.tipo_reperto = data[3]
        self.criterio_schedatura = data[4]
        self.definizione = data[5]
        self.descrizione = data[6]
        self.area = data[7]
        self.us = data[8]
        self.lavato = data[9]
        self.nr_cassa = data[10]
        self.luogo_conservazione = data[11]
        self.stato_conservazione = data[12]
        self.datazione_reperto = data[13]
        self.elementi_reperto = data[14]
        self.misurazioni = data[15]
        self.rif_biblio = data[16]
        self.tecnologie = data[17]
        self.tipo = data[18]
        self.repertato = data[21]
        self.diagnostico = data[22]
        self.n_reperto = data[23]
        self.struttura = data[25]
        self.years = data[26]
        self.thumbnail= data[27]
        #self.map = data[27]
    def datestrfdate(self):
        now = date.today()
        today = now.strftime("%d-%m-%Y")
        return today

    def create_sheet(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 7
        styNormal.fontName = 'Cambria'
        styleSheet = getSampleStyleSheet()
        styDescrizione = styleSheet['Normal']
        styDescrizione.spaceBefore = 20
        styDescrizione.spaceAfter = 20
        styDescrizione.alignment = 4  # Justified
        styDescrizione.fontSize = 7
        styDescrizione.fontName = 'Cambria'

        # format labels

        # 0 row
        intestazione = Paragraph("<b>SCHEDA REPERTI<br/></b>", styNormal)
        # intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()


        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')

        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
            logo = Image(logo_path)
            logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
            logo.drawWidth = 1.5 * inch
        else:
            logo_path = lo_path_str
            # logo = Image(logo_path)
            # logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
            # logo.drawWidth = 1.5 * inch
            logo = Image(logo_path)
            width, height = logo.drawWidth, logo.drawHeight
            aspect = width / height

            max_width = .5 * inch
            max_height = .5 * inch

            if aspect > .4:
                # If image is wide
                logo.drawWidth = max_width
                logo.drawHeight = max_width / aspect
            else:
                # If image is tall or square
                logo.drawHeight = max_height
                logo.drawWidth = max_height * aspect
        try:
            if self.thumbnail:
                th= Image(self.thumbnail)
                th.drawHeight = 2.5 * inch * th.drawHeight / th.drawWidth
                th.drawWidth = 2.5 * inch
                th.hAlign = "CENTER"
        except:
            pass
        if not self.thumbnail.endswith('.png') :

            # else:
            #     # if th == None:
            th=Paragraph("<b>IMG</b><br/>" + str('Immagine non presente nel database'), styNormal)
        #QMessageBox.information(None,'',str(self.map))
        # if self.map:
        #
        #     mp= Image(self.map)
        #
        #     mp.drawHeight = 6 * inch * mp.drawHeight / mp.drawWidth
        #     mp.drawWidth = 6 * inch

        # elif not self.map:
        #     mp = Paragraph("<b>Map</b><br/>" + str('Localizzazione non inserita'), styNormal)

        # elif not self.map.endswith('.png'):
        #
        #     # else:
        #     #     # if th == None:
        #     mp=Paragraph("<b>Map</b><br/>" + str('Localizzazione non inserita'), styNormal)
        if str(self.n_reperto)=='0':
            print("no schede RA")
            pass
        else:
            # 1 row
            sito = Paragraph("<b>Sito</b><br/>" + str(self.sito), styNormal)
            n_reperto = Paragraph("<b>N° reperto</b><br/>" + str(self.n_reperto) +"<br/>" "<b>(n. inv.: </b>" + str(self.numero_inventario)+"<b>)</b>", styNormal)

            # 2 row
            #riferimenti_stratigrafici = Paragraph("<b>Riferimenti stratigrafici</b>", styNormal)
            area = Paragraph("<b>Area</b><br/>" + str(self.area), styNormal)
            us = Paragraph("<b>US</b><br/>" + str(self.us), styNormal)
            anno = Paragraph("<b>Anno</b><br/>" + str(self.years), styNormal)
            struttura = Paragraph("<b>Rif. Struttura</b><br/>" + str(self.struttura), styNormal)
            # 3 row
            criterio_schedatura = Paragraph("<b>Classe materiale</b><br/>" + self.criterio_schedatura, styNormal)

            tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>" + self.tipo_reperto, styNormal)

            definizione = Paragraph("<b>Definizione</b><br/>" + self.definizione, styNormal)

            # 4 row
            stato_conservazione = Paragraph("<b>Stato Conservazione</b><br/>" + self.stato_conservazione, styNormal)

            datazione = Paragraph("<b>Datazione</b><br/>" + self.datazione_reperto, styNormal)

            # 5 row
            descrizione = ''
            try:
                descrizione = Paragraph("<b>Descrizione</b><br/>" + str(self.descrizione), styNormal)
            except:
                pass

            # 6 row
            elementi_reperto = ''
            if eval(self.elementi_reperto):
                for i in eval(self.elementi_reperto):
                    if elementi_reperto == '':
                        try:
                            elementi_reperto += ("Elemento rinvenuto: %s, Unita' di misura: %s, Quantita': %s") % (
                            str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass
                    else:
                        try:
                            elementi_reperto += ("<br/>Elemento rinvenuto: %s, Unita' di misura: %s, Quantita': %s") % (
                            str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass

            elementi_reperto = Paragraph("<b>Elementi reperto</b><br/>" + elementi_reperto, styNormal)

            # 7 row
            misurazioni = ''
            if eval(self.misurazioni):
                for i in eval(self.misurazioni):
                    if misurazioni == '':
                        try:
                            misurazioni += ("%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass
                    else:
                        try:
                            misurazioni += ("<br/>%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass
            misurazioni = Paragraph("<b>Misurazioni</b><br/>" + misurazioni, styNormal)

            # 8 row
            tecnologie = ''
            if eval(self.tecnologie):
                for i in eval(self.tecnologie):
                    if tecnologie == '':
                        try:
                            tecnologie += (
                                          "Tipo tecnologia: %s, Posizione: %s, Tipo quantita': %s, Unita' di misura: %s, Quantita': %s") % (
                                          str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass
                    else:
                        try:
                            tecnologie += (
                                          "<br/>Tipo tecnologia: %s, Posizione: %s, Tipo quantita': %s, Unita' di misura: %s, Quantita': %s") % (
                                          str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass
            tecnologie = Paragraph("<b>Tecnologie</b><br/>" + tecnologie, styNormal)
            tipologia = Paragraph("<b>Tipologia</b><br/>" + self.tipo, styNormal)
            # 9 row
            rif_biblio = ''
            if eval(self.rif_biblio):
                for i in eval(self.rif_biblio):  # gigi
                    if rif_biblio == '':
                        try:
                            rif_biblio += ("Autore: %s, Anno: %s, Titolo: %s, Pag.: %s, Fig.: %s") % (
                            str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass
                    else:
                        try:
                            rif_biblio += ("<br/>Autore: %s, Anno: %s, Titolo: %s, Pag.: %s, Fig.: %s") % (
                            str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass

            rif_biblio = Paragraph("<b>Riferimenti bibliografici</b><br/>" + rif_biblio, styNormal)

            # 10 row
            repertato = Paragraph("<b>Repertato</b><br/>" + self.repertato, styNormal)
            diagnostico = Paragraph("<b>Diagnostico</b><br/>" + self.diagnostico, styNormal)

            # 11 row
            riferimenti_magazzino = Paragraph("<b>Riferimenti magazzino</b>", styNormal)

            # 12 row
            lavato = Paragraph("<b>Lavato</b><br/>" + self.lavato, styNormal)
            nr_cassa = Paragraph("<b>N° cassa</b><br/>" + self.nr_cassa, styNormal)
            luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + self.luogo_conservazione, styNormal)

            # schema
            cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
                [intestazione, '01', '02', '03', '04', '05', '06', '07', '08', logo, '10', '11', '12', '13', '14', '15', '16', '17'],  # 0 row ok
                [sito, '01', '02', '03', '04', n_reperto, '06', '07','08' , '09', '10', th, '12', '13', '14', '15', '16', '17'],  # 1 row ok
                [area, '01', '02', us, '04','05', anno, '07', struttura, '09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 2 row ok
                [tipo_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'],
                [criterio_schedatura, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'],
                [definizione, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'],
                [descrizione,'01', '02', '03', '04', '05', '06', '07', '08','09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 5 row ok
                ['00', '01', '02', '03', '04', '05', '06', '07', '08','09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 5 row ok
                ['00', '01', '02', '03', '04', '05', '06', '07', '08','09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 5 row ok
                ['00', '01', '02', '03', '04', '05', '06', '07', '08','09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 5 row ok
                # 3 row ok
                [datazione, '01', '02', '03', '04', stato_conservazione, '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 4 row ok

                [elementi_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 6 row ok
                [misurazioni, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 7 row ok
                [tecnologie, '01', '02', '03', '04', '05', '06', '07', '08', tipologia, '10', '11', '12', '13', '14', '15', '16', '17'],  # 8 row ok
                [rif_biblio, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 9 row ok
                [repertato, '01', '02', diagnostico, '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'],  # 10 row ok
                [lavato, '01', '02', nr_cassa, '04', '05', luogo_conservazione, '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'],
                #[mp, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 #'16', '17'],  # 5 row ok
                # 12 row ok
            ]

            # table style
            table_style = [

                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

                # 0 row
                ('SPAN', (0, 0), (8, 0)),  # intestazione
                ('SPAN', (9, 0), (17, 0)),  # intestazione
                ('VALIGN', (9, 0), (17, 9), 'MIDDLE'),
                ('ALIGN', (9, 0), (17, 0), 'CENTER'),
                # 1 row
                ('SPAN', (0, 1), (4, 1)),  # sito
                ('SPAN', (5, 1), (10, 1)),  # nr_inventario
                ('SPAN', (11, 1), (17, 5)),  # img
                ('VALIGN', (0, 1), (10, 1), 'TOP'),
                ('VALIGN', (11, 1), (17, 5), 'MIDDLE'),
                ('ALIGN', (11, 1), (17, 5), 'CENTER'),
                # 2 row
                #('SPAN', (0, 2), (3, 2)),  # rif stratigrafici
                ('SPAN', (0, 2), (2, 2)),  # area
                ('SPAN', (3, 2), (5, 2)),  # us
                ('SPAN', (6, 2), (7, 2)),  # anno
                ('SPAN', (8, 2), (10, 2)),  # struttura
                ('VALIGN', (0, 2), (10, 2), 'TOP'),

                # 3 row
                ('SPAN', (0, 3), (10, 3)),  # tipo_reperto
                ('SPAN', (0, 4), (10, 4)),  # criterio_schedatura
                ('SPAN', (0, 5), (10, 5)),  # definizione
                #('VALIGN', (0, 3), (17, 3), 'TOP'),
                ('SPAN', (0, 6), (17, 9)),  # descrizione
                ('VALIGN', (0, 6), (17, 17), 'TOP'),
                # 4 row
                ('SPAN', (0, 10), (4, 10)),  # datazione
                ('SPAN', (5, 10), (17, 10)),  # conservazione

                # 5 row


                # 6 row
                ('SPAN', (0, 11), (17, 11)),  # elementi_reperto

                # 7 row
                ('SPAN', (0, 12), (17, 12)),  # misurazioni

                # 8 row
                ('SPAN', (0, 13), (8, 13)),  # tecnologie
                ('SPAN', (9, 13), (17, 13)),  # tipologia

                # 17 row
                ('SPAN', (0, 14), (17, 14)),  # bibliografia

                # 10 row
                ('SPAN', (0, 15), (2, 15)),  # Repertato Diagnostico
                ('SPAN', (3, 15), (17, 15)),   # Repertato Diagnostico

                # 11 row
               # ('SPAN', (0, 15), (17, 15)),  # Riferimenti magazzino - Titolo

                # 12 row
                ('SPAN', (0, 16), (2, 16)),  # Riferimenti magazzino - lavato
                ('SPAN', (3, 16), (5, 16)),  # Riferimenti magazzino - nr_cassa
                ('SPAN', (6, 16), (17, 16)),  # Riferimenti magazzino - luogo conservazione
                #('SPAN', (0, 17), (17, 17)),  # localizzazione us su mappa
                #('VALIGN', (0, 17), (17, 17), 'MIDDLE'),
                #('ALIGN', (0, 17), (17, 17), 'CENTER'),


                ('VALIGN', (0, 10), (-1, -1), 'TOP')

            ]
            colWidths = (15, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 20, 30, 30, 30, 30,30)
            rowHeights = (30, 40, 30, 30, 30, 30, 130, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30)

            t = Table(cell_schema, colWidths = colWidths, rowHeights = rowHeights, style = table_style)
            #lst.append(logo)
            #t = Table(cell_schema, colWidths=50, rowHeights=None, style=table_style)

            return t

    def create_sheet_de(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 7
        styNormal.fontName = 'Cambria'
        styleSheet = getSampleStyleSheet()
        styDescrizione = styleSheet['Normal']
        styDescrizione.spaceBefore = 20
        styDescrizione.spaceAfter = 20
        styDescrizione.alignment = 4  # Justified
        styDescrizione.fontSize = 7
        styDescrizione.fontName = 'Cambria'

        # format labels

        # 0 row
        intestazione = Paragraph("<b>FORMULAR MATERIALINVENTAR<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
        # intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
            logo = Image(logo_path)
            logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
            logo.drawWidth = 1.5 * inch
        else:
            logo_path = lo_path_str
            # logo = Image(logo_path)
            # logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
            # logo.drawWidth = 1.5 * inch
            logo = Image(logo_path)
            width, height = logo.drawWidth, logo.drawHeight
            aspect = width / height

            max_width = .5 * inch
            max_height = .5 * inch

            if aspect > .4:
                # If image is wide
                logo.drawWidth = max_width
                logo.drawHeight = max_width / aspect
            else:
                # If image is tall or square
                logo.drawHeight = max_height
                logo.drawWidth = max_height * aspect
        if self.thumbnail:
            th = Image(self.thumbnail)
            th.drawHeight = 2.5 * inch * th.drawHeight / th.drawWidth
            th.drawWidth = 2.5 * inch
            th.hAlign = "CENTER"
        elif not self.thumbnail.endswith('.png'):

            # else:
            #     # if th == None:
            th=Paragraph("<b>IMG</b><br/>" + str('Image not present into the db'), styNormal)
        if str(self.n_reperto)=='0':
            print("no RA")
            pass
        else:
            # 1 row
            sito = Paragraph("<b>Ausgrabungsstättesstätte</b><br/>" + str(self.sito), styNormal)
            n_reperto = Paragraph("<b>N° RA</b><br/>" + str(self.n_reperto) + "<br/>" "<b>(Referenzmaterial Best.-Nr. </b>" + str(
                self.numero_inventario) + "<b>)</b>", styNormal)

            # 2 row
            riferimenti_stratigrafici = Paragraph("<b>Stratigraphische Referenz</b>", styNormal)
            area = Paragraph("<b>Areal</b><br/>" + str(self.area), styNormal)
            us = Paragraph("<b>SE</b><br/>" + str(self.us), styNormal)
            anno = Paragraph("<b>Year</b><br/>" + str(self.years), styNormal)
            tipologia = Paragraph("<b>Tipology</b><br/>" + self.tipo, styNormal)
            struttura = Paragraph("<b>Structure</b><br/>" + self.struttura, styNormal)
            # 3 row
            criterio_schedatura = Paragraph("<b>Anmeldeparameter</b><br/>" + self.criterio_schedatura, styNormal)
            tipo_reperto = Paragraph("<b>Art der Feststellung</b><br/>" + self.tipo_reperto, styNormal)
            definizione = Paragraph("<b>Definition</b><br/>" + self.definizione, styNormal)

            # 4 row
            stato_conservazione = Paragraph("<b>Erhaltungsstatus</b><br/>" + self.stato_conservazione, styNormal)
            datazione = Paragraph("<b>Datierung</b><br/>" + self.datazione_reperto, styNormal)

            # 5 row
            descrizione = ''
            try:
                descrizione = Paragraph("<b>Beschreibung</b><br/>" + str(self.descrizione), styDescrizione)
            except:
                pass

                # 6 row
            elementi_reperto = ''
            if eval(self.elementi_reperto):
                for i in eval(self.elementi_reperto):
                    if elementi_reperto == '':
                        try:
                            elementi_reperto += ("Gegenstand gefunden: %s, Maßeinheit: %s, Menge: %s") % (
                                str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass
                    else:
                        try:
                            elementi_reperto += ("Gegenstand gefunden: %s, Maßeinheit: %s, Menge: %s") % (
                                str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass

            elementi_reperto = Paragraph("<b>Artefakt - Teile</b><br/>" + elementi_reperto, styNormal)

            # 7 row
            misurazioni = ''
            if eval(self.misurazioni):
                for i in eval(self.misurazioni):
                    if misurazioni == '':
                        try:
                            misurazioni += ("%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass
                    else:
                        try:
                            misurazioni += ("<br/>%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass
            misurazioni = Paragraph("<b>Messungen</b><br/>" + misurazioni, styNormal)

            # 8 row
            tecnologie = ''
            if eval(self.tecnologie):
                for i in eval(self.tecnologie):
                    if tecnologie == '':
                        try:
                            tecnologie += (
                                              "<br/>Technologies: %s, Position: %s, Quantitätstyp: %s, Maßeinheit: %s, Quantita': %s") % (
                                              str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass
                    else:
                        try:
                            tecnologie += (
                                              "<br/>Technologies: %s, Position: %s, Quantitätstyp: %s, Maßeinheit: %s, Quantita': %s") % (
                                              str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass
            tecnologie = Paragraph("<b>Technologies</b><br/>" + tecnologie, styNormal)

            # 9 row
            rif_biblio = ''
            if eval(self.rif_biblio):
                for i in eval(self.rif_biblio):  # gigi
                    if rif_biblio == '':
                        try:
                            rif_biblio += ("<b>Autor: %s, Jahr: %s, Titel: %s, Seite: %s, Bild: %s") % (
                                str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass
                    else:
                        try:
                            rif_biblio += ("<b>Autor: %s, Jahr: %s, Titel: %s, Seite: %s, Bild: %s") % (
                                str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass

            rif_biblio = Paragraph("<b>Referenzen</b><br/>" + rif_biblio, styNormal)

            # 11 row
            repertato = Paragraph("<b>Abgerufen</b><br/>" + self.repertato, styNormal)
            diagnostico = Paragraph("<b>Diagnose</b><br/>" + self.diagnostico, styNormal)

            # 12 row
            riferimenti_magazzino = Paragraph("<b>Bestandsdaten</b>", styNormal)

            # 13 row
            lavato = Paragraph("<b>Gewaschen</b><br/>" + self.lavato, styNormal)
            nr_cassa = Paragraph("<b>N° Box</b><br/>" + self.nr_cassa, styNormal)
            luogo_conservazione = Paragraph("<b>Ort der Erhaltung</b><br/>" + self.luogo_conservazione, styNormal)

            # schema
            cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
                [intestazione, '01', '02', '03', '04', '05', '06', '07', '08', logo, '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 0 row ok
                [sito, '01', '02', '03', '04', n_reperto, '06', '07', '08', '09', '10', th, '12', '13', '14', '15',
                 '16', '17'],  # 1 row ok
                [area, '01', '02', us, '04', '05', anno, '07', struttura, '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 2 row ok
                [tipo_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],
                [criterio_schedatura, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
                 '14', '15', '16', '17'],
                [definizione, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],
                [descrizione, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 5 row ok
                ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                 '17'],  # 5 row ok
                ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                 '17'],  # 5 row ok
                ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                 '17'],  # 5 row ok
                # 3 row ok
                [datazione, '01', '02', '03', '04', stato_conservazione, '06', '07', '08', '09', '10', '11', '12', '13',
                 '14', '15', '16', '17'],  # 4 row ok

                [elementi_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
                 '15', '16', '17'],  # 6 row ok
                [misurazioni, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 7 row ok
                [tecnologie, '01', '02', '03', '04', '05', '06', '07', '08', tipologia, '10', '11', '12', '13', '14',
                 '15', '16', '17'],  # 8 row ok
                [rif_biblio, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 9 row ok
                [repertato, '01', '02', diagnostico, '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
                 '15', '16', '17'],  # 10 row ok
                [lavato, '01', '02', nr_cassa, '04', '05', luogo_conservazione, '07', '08', '09', '10', '11', '12',
                 '13', '14', '15', '16', '17'],
                # [mp, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                # '16', '17'],  # 5 row ok
                # 12 row ok
            ]

            # table style
            table_style = [

                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

                # 0 row
                ('SPAN', (0, 0), (8, 0)),  # intestazione
                ('SPAN', (9, 0), (17, 0)),  # intestazione
                ('VALIGN', (9, 0), (17, 9), 'MIDDLE'),
                ('ALIGN', (9, 0), (17, 0), 'CENTER'),
                # 1 row
                ('SPAN', (0, 1), (4, 1)),  # sito
                ('SPAN', (5, 1), (10, 1)),  # nr_inventario
                ('SPAN', (11, 1), (17, 5)),  # img
                ('VALIGN', (0, 1), (10, 1), 'TOP'),
                ('VALIGN', (11, 1), (17, 5), 'MIDDLE'),
                ('ALIGN', (11, 1), (17, 5), 'CENTER'),
                # 2 row
                # ('SPAN', (0, 2), (3, 2)),  # rif stratigrafici
                ('SPAN', (0, 2), (2, 2)),  # area
                ('SPAN', (3, 2), (5, 2)),  # us
                ('SPAN', (6, 2), (7, 2)),  # anno
                ('SPAN', (8, 2), (10, 2)),  # struttura
                ('VALIGN', (0, 2), (10, 2), 'TOP'),

                # 3 row
                ('SPAN', (0, 3), (10, 3)),  # tipo_reperto
                ('SPAN', (0, 4), (10, 4)),  # criterio_schedatura
                ('SPAN', (0, 5), (10, 5)),  # definizione
                # ('VALIGN', (0, 3), (17, 3), 'TOP'),
                ('SPAN', (0, 6), (17, 9)),  # descrizione
                ('VALIGN', (0, 6), (17, 17), 'TOP'),
                # 4 row
                ('SPAN', (0, 10), (4, 10)),  # datazione
                ('SPAN', (5, 10), (17, 10)),  # conservazione

                # 5 row

                # 6 row
                ('SPAN', (0, 11), (17, 11)),  # elementi_reperto

                # 7 row
                ('SPAN', (0, 12), (17, 12)),  # misurazioni

                # 8 row
                ('SPAN', (0, 13), (8, 13)),  # tecnologie
                ('SPAN', (9, 13), (17, 13)),  # tipologia

                # 17 row
                ('SPAN', (0, 14), (17, 14)),  # bibliografia

                # 10 row
                ('SPAN', (0, 15), (2, 15)),  # Repertato Diagnostico
                ('SPAN', (3, 15), (17, 15)),  # Repertato Diagnostico

                # 11 row
                # ('SPAN', (0, 15), (17, 15)),  # Riferimenti magazzino - Titolo

                # 12 row
                ('SPAN', (0, 16), (2, 16)),  # Riferimenti magazzino - lavato
                ('SPAN', (3, 16), (5, 16)),  # Riferimenti magazzino - nr_cassa
                ('SPAN', (6, 16), (17, 16)),  # Riferimenti magazzino - luogo conservazione
                # ('SPAN', (0, 17), (17, 17)),  # localizzazione us su mappa
                # ('VALIGN', (0, 17), (17, 17), 'MIDDLE'),
                # ('ALIGN', (0, 17), (17, 17), 'CENTER'),

                ('VALIGN', (0, 10), (-1, -1), 'TOP')

            ]
            colWidths = (15, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 20, 30, 30, 30, 30, 30)
            rowHeights = (30, 40, 30, 30, 30, 30, 130, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30)

            t = Table(cell_schema, colWidths=colWidths, rowHeights=rowHeights, style=table_style)
            # lst.append(logo)
            # t = Table(cell_schema, colWidths=50, rowHeights=None, style=table_style)

            return t

        
    def create_sheet_en(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 7
        styNormal.fontName = 'Cambria'
        styleSheet = getSampleStyleSheet()
        styDescrizione = styleSheet['Normal']
        styDescrizione.spaceBefore = 20
        styDescrizione.spaceAfter = 20
        styDescrizione.alignment = 4  # Justified
        styDescrizione.fontSize = 7
        styDescrizione.fontName = 'Cambria'

        # format labels

        # 0 row
        intestazione = Paragraph("<b>Artefact Card<br/></b>", styNormal)
        # intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()

        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')

        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
            logo = Image(logo_path)
            logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
            logo.drawWidth = 1.5 * inch
        else:
            logo_path = lo_path_str
            #logo = Image(logo_path)
            #logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
            #logo.drawWidth = 1.5 * inch
            logo = Image(logo_path)
            width, height = logo.drawWidth, logo.drawHeight
            aspect = width / height

            max_width = .5 * inch
            max_height = .5 * inch

            if aspect > .4:
                # If image is wide
                logo.drawWidth = max_width
                logo.drawHeight = max_width / aspect
            else:
                # If image is tall or square
                logo.drawHeight = max_height
                logo.drawWidth = max_height * aspect

        try:
            if self.thumbnail:
                th = Image(self.thumbnail)
                th.drawHeight = 2.5 * inch * th.drawHeight / th.drawWidth
                th.drawWidth = 2.5 * inch
                th.hAlign = "CENTER"
        except:
            pass
        if not self.thumbnail.endswith('.png'):
            # else:
            #     # if th == None:
            th = Paragraph("<b>IMG</b><br/>" + str('Immagine non presente nel database'), styNormal)

        if str(self.n_reperto) == '0':
            print("no RA")
            pass

        else:
            # 1 row
            sito = Paragraph("<b>Name Site</b><br/>" + str(self.sito), styNormal)
            n_reperto = Paragraph(
                "<b>N° RA</b><br/>" + str(self.n_reperto) + "<br/>" "<b>(Inv-Nr. </b>" + str(
                    self.numero_inventario) + "<b>)</b>", styNormal)

            # 2 row
            riferimenti_stratigrafici = Paragraph("<b>Stratigraphic Reference</b>", styNormal)
            area = Paragraph("<b>Area</b><br/>" + str(self.area), styNormal)
            us = Paragraph("<b>SU</b><br/>" + str(self.us), styNormal)
            anno = Paragraph("<b>Year</b><br/>" + str(self.years), styNormal)
            tipologia = Paragraph("<b>Tipology</b><br/>" + self.tipo, styNormal)
            struttura = Paragraph("<b>Structure</b><br/>" + self.struttura, styNormal)
            # 3 row
            criterio_schedatura = Paragraph("<b>Filing criteria</b><br/>" + self.criterio_schedatura, styNormal)
            tipo_reperto = Paragraph("<b>Artefact Type</b><br/>" + self.tipo_reperto, styNormal)
            definizione = Paragraph("<b>Definition</b><br/>" + self.definizione, styNormal)

            # 4 row
            stato_conservazione = Paragraph("<b>Status of conservation</b><br/>" + self.stato_conservazione, styNormal)
            datazione = Paragraph("<b>Epoch</b><br/>" + self.datazione_reperto, styNormal)

            # 5 row
            descrizione = ''
            try:
                descrizione = Paragraph("<b>Description</b><br/>" + str(self.descrizione), styDescrizione)
            except:
                pass

                # 6 row
            elementi_reperto = ''
            if eval(self.elementi_reperto):
                for i in eval(self.elementi_reperto):
                    if elementi_reperto == '':
                        try:
                            elementi_reperto += ("<br/>Finds: %s, Measure unit: %s, Quantity: %s") % (
                                str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass
                    else:
                        try:
                            elementi_reperto += ("<br/>Finds: %s, Measure unit: %s, Quantity: %s") % (
                                str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass

            elementi_reperto = Paragraph("<b>Finds</b><br/>" + elementi_reperto, styNormal)

            # 7 row
            misurazioni = ''
            if eval(self.misurazioni):
                for i in eval(self.misurazioni):
                    if misurazioni == '':
                        try:
                            misurazioni += ("%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass
                    else:
                        try:
                            misurazioni += ("<br/>%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                        except:
                            pass
            misurazioni = Paragraph("<b>Measurement</b><br/>" + misurazioni, styNormal)

            # 8 row
            tecnologie = ''
            if eval(self.tecnologie):
                for i in eval(self.tecnologie):
                    if tecnologie == '':
                        try:
                            tecnologie += (
                                              "<br/>Technologies: %s, Position: %s, Quantity type: %s, Measure unit: %s, Quantity: %s") % (
                                              str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass
                    else:
                        try:
                            tecnologie += (
                                              "<br/>Technologies: %s, Position: %s, Quantity type: %s, Measure unit: %s, Quantity: %s") % (
                                              str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass
            tecnologie = Paragraph("<b>Technologies</b><br/>" + tecnologie, styNormal)

            # 9 row
            rif_biblio = ''
            if eval(self.rif_biblio):
                for i in eval(self.rif_biblio):  # gigi
                    if rif_biblio == '':
                        try:
                            rif_biblio += ("<b>Author: %s, Year: %s, Title: %s, Pag.: %s, Fig.: %s</b>") % (
                                str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass
                    else:
                        try:
                            rif_biblio += ("<b>Author: %s, Year: %s, Title: %s, Pag.: %s, Fig.: %s</b>") % (
                                str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                        except:
                            pass

            rif_biblio = Paragraph("<b>Bibliography reference</b><br/>" + rif_biblio, styNormal)

            # 11 row
            repertato = Paragraph("<b>Found</b><br/>" + self.repertato, styNormal)
            diagnostico = Paragraph("<b>Diagnostico</b><br/>" + self.diagnostico, styNormal)

            # 12 row
            riferimenti_magazzino = Paragraph("<b>Store</b>", styNormal)

            # 13 row
            lavato = Paragraph("<b>Whashed</b><br/>" + self.lavato, styNormal)
            nr_cassa = Paragraph("<b>Box</b><br/>" + self.nr_cassa, styNormal)
            luogo_conservazione = Paragraph("<b>Place of conservation</b><br/>" + self.luogo_conservazione, styNormal)

            # schema
            cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
                [intestazione, '01', '02', '03', '04', '05', '06', '07', '08', logo, '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 0 row ok
                [sito, '01', '02', '03', '04', n_reperto, '06', '07', '08', '09', '10', th, '12', '13', '14', '15',
                 '16', '17'],  # 1 row ok
                [area, '01', '02', us, '04', '05', anno, '07', struttura, '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 2 row ok
                [tipo_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],
                [criterio_schedatura, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
                 '14', '15', '16', '17'],
                [definizione, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],
                [descrizione, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 5 row ok
                ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                 '17'],  # 5 row ok
                ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                 '17'],  # 5 row ok
                ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                 '17'],  # 5 row ok
                # 3 row ok
                [datazione, '01', '02', '03', '04', stato_conservazione, '06', '07', '08', '09', '10', '11', '12', '13',
                 '14', '15', '16', '17'],  # 4 row ok

                [elementi_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
                 '15', '16', '17'],  # 6 row ok
                [misurazioni, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 7 row ok
                [tecnologie, '01', '02', '03', '04', '05', '06', '07', '08', tipologia, '10', '11', '12', '13', '14',
                 '15', '16', '17'],  # 8 row ok
                [rif_biblio, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17'],  # 9 row ok
                [repertato, '01', '02', diagnostico, '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
                 '15', '16', '17'],  # 10 row ok
                [lavato, '01', '02', nr_cassa, '04', '05', luogo_conservazione, '07', '08', '09', '10', '11', '12',
                 '13', '14', '15', '16', '17'],
                # [mp, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                # '16', '17'],  # 5 row ok
                # 12 row ok
            ]

            # table style
            table_style = [

                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

                # 0 row
                ('SPAN', (0, 0), (8, 0)),  # intestazione
                ('SPAN', (9, 0), (17, 0)),  # intestazione
                ('VALIGN', (9, 0), (17, 9), 'MIDDLE'),
                ('ALIGN', (9, 0), (17, 0), 'CENTER'),
                # 1 row
                ('SPAN', (0, 1), (4, 1)),  # sito
                ('SPAN', (5, 1), (10, 1)),  # nr_inventario
                ('SPAN', (11, 1), (17, 5)),  # img
                ('VALIGN', (0, 1), (10, 1), 'TOP'),
                ('VALIGN', (11, 1), (17, 5), 'MIDDLE'),
                ('ALIGN', (11, 1), (17, 5), 'CENTER'),
                # 2 row
                # ('SPAN', (0, 2), (3, 2)),  # rif stratigrafici
                ('SPAN', (0, 2), (2, 2)),  # area
                ('SPAN', (3, 2), (5, 2)),  # us
                ('SPAN', (6, 2), (7, 2)),  # anno
                ('SPAN', (8, 2), (10, 2)),  # struttura
                ('VALIGN', (0, 2), (10, 2), 'TOP'),

                # 3 row
                ('SPAN', (0, 3), (10, 3)),  # tipo_reperto
                ('SPAN', (0, 4), (10, 4)),  # criterio_schedatura
                ('SPAN', (0, 5), (10, 5)),  # definizione
                # ('VALIGN', (0, 3), (17, 3), 'TOP'),
                ('SPAN', (0, 6), (17, 9)),  # descrizione
                ('VALIGN', (0, 6), (17, 17), 'TOP'),
                # 4 row
                ('SPAN', (0, 10), (4, 10)),  # datazione
                ('SPAN', (5, 10), (17, 10)),  # conservazione

                # 5 row

                # 6 row
                ('SPAN', (0, 11), (17, 11)),  # elementi_reperto

                # 7 row
                ('SPAN', (0, 12), (17, 12)),  # misurazioni

                # 8 row
                ('SPAN', (0, 13), (8, 13)),  # tecnologie
                ('SPAN', (9, 13), (17, 13)),  # tipologia

                # 17 row
                ('SPAN', (0, 14), (17, 14)),  # bibliografia

                # 10 row
                ('SPAN', (0, 15), (2, 15)),  # Repertato Diagnostico
                ('SPAN', (3, 15), (17, 15)),  # Repertato Diagnostico

                # 11 row
                # ('SPAN', (0, 15), (17, 15)),  # Riferimenti magazzino - Titolo

                # 12 row
                ('SPAN', (0, 16), (2, 16)),  # Riferimenti magazzino - lavato
                ('SPAN', (3, 16), (5, 16)),  # Riferimenti magazzino - nr_cassa
                ('SPAN', (6, 16), (17, 16)),  # Riferimenti magazzino - luogo conservazione
                # ('SPAN', (0, 17), (17, 17)),  # localizzazione us su mappa
                # ('VALIGN', (0, 17), (17, 17), 'MIDDLE'),
                # ('ALIGN', (0, 17), (17, 17), 'CENTER'),

                ('VALIGN', (0, 10), (-1, -1), 'TOP')

            ]
            colWidths = (15, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 20, 30, 30, 30, 30, 30)
            rowHeights = (30, 40, 30, 30, 30, 30, 130, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30)

            t = Table(cell_schema, colWidths=colWidths, rowHeights=rowHeights, style=table_style)
            # lst.append(logo)
            # t = Table(cell_schema, colWidths=50, rowHeights=None, style=table_style)

            return t


class Box_labels_Finds_pdf_sheet(object):
    def __init__(self, data, sito):
        self.sito = sito  # Sito
        self.cassa = data[0]  # 1 - Cassa
        self.elenco_inv_tip_rep = data[1]  # 2-  elenco US
        self.elenco_us = data[2]  # 3 - elenco Inventari
        self.luogo_conservazione = data[3]  # 4 - luogo conservazione

    def datestrfdate(self):
        now = date.today()
        today = now.strftime("%d-%m-%Y")
        return today

    def create_sheet(self):
        styleSheet = getSampleStyleSheet()

        styleSheet.add(ParagraphStyle(name='Cassa Label'))
        styleSheet.add(ParagraphStyle(name='Sito Label'))

        styCassaLabel = styleSheet['Cassa Label']
        styCassaLabel.spaceBefore = 0
        styCassaLabel.spaceAfter = 0
        styCassaLabel.alignment = 2  # RIGHT
        styCassaLabel.leading = 25
        styCassaLabel.fontSize = 30

        styCassaLabel.fontName = 'Cambria'
        stySitoLabel = styleSheet['Sito Label']
        stySitoLabel.spaceBefore = 0
        stySitoLabel.spaceAfter = 0
        stySitoLabel.alignment = 0  # LEFT
        stySitoLabel.leading = 25
        stySitoLabel.fontSize = 18
        stySitoLabel.fontStyle = 'bold'
        stySitoLabel.fontName = 'Cambria'
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 10
        styNormal.spaceAfter = 10
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 14
        styNormal.leading = 15
        styNormal.fontName = 'Cambria'

        # format labels
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path=lo_path_str
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch

        num_cassa = Paragraph("<b>N° Cassa </b>" + str(self.cassa), styCassaLabel)
        sito = Paragraph("<b>Sito: </b>" + str(self.sito), stySitoLabel)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>Elenco n. inv. / Tipo materiale</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>Elenco n. inv. / Tipo materiale</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>Elenco US/(struttura)</b>", styNormal)
        else:
            elenco_us = Paragraph("<b>Elenco US/(struttura)</b><br/>" + str(self.elenco_us), styNormal)

            # luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

            # schema
        cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
            [logo, '01', '02', '03', '04', '05', num_cassa, '07', '08', '09'],
            [sito, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_us, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_inv_tip_rep, '01', '02', '03', '04', '05', '06', '07', '08', '09']

        ]

        # table style
        table_style = [

            ('GRID', (0, 0), (-1, -1), 0, colors.white),  # ,0.0,colors.black
            # 0 row
            ('SPAN', (0, 0), (5, 0)),  # elenco US
            ('SPAN', (6, 0), (9, 0)),  # elenco US
            ('HALIGN', (0, 0), (9, 0), 'LEFT'),
            ('VALIGN', (6, 0), (9, 0), 'TOP'),
            ('HALIGN', (6, 0), (9, 0), 'RIGHT'),

            ('SPAN', (0, 1), (9, 1)),  # elenco US
            ('HALIGN', (0, 1), (9, 1), 'LEFT'),

            ('SPAN', (0, 2), (9, 2)),  # intestazione
            ('VALIGN', (0, 2), (9, 2), 'TOP'),
            # 1 row
            ('SPAN', (0, 3), (9, 3)),  # elenco US
            ('VALIGN', (0, 3), (9, 3), 'TOP')

        ]

        colWidths = None
        rowHeights = None
        # colWidths=[80,80,80, 80,80, 80,80,80,80, 80]
        t = Table(cell_schema, colWidths, rowHeights, style=table_style)

        return t

    def create_sheet_de(self):
        styleSheet = getSampleStyleSheet()

        styleSheet.add(ParagraphStyle(name='Cassa Label'))
        styleSheet.add(ParagraphStyle(name='Sito Label'))

        styCassaLabel = styleSheet['Cassa Label']
        styCassaLabel.spaceBefore = 0
        styCassaLabel.spaceAfter = 0
        styCassaLabel.alignment = 2  # RIGHT
        styCassaLabel.leading = 25
        styCassaLabel.fontSize = 30

        stySitoLabel = styleSheet['Sito Label']
        stySitoLabel.spaceBefore = 0
        stySitoLabel.spaceAfter = 0
        stySitoLabel.alignment = 0  # LEFT
        stySitoLabel.leading = 25
        stySitoLabel.fontSize = 18
        stySitoLabel.fontStyle = 'bold'

        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 10
        styNormal.spaceAfter = 10
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 14
        styNormal.leading = 15

        # format labels
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        num_cassa = Paragraph("<b>N° Box</b>" + str(self.cassa), styCassaLabel)
        sito = Paragraph("<b>Ausgrabungsstättesstätte: </b>" + str(self.sito), stySitoLabel)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>Liste N° Inv. / Art material</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>Liste N° Inv. / Art material</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>Liste SE/(Struktur)</b>", styNormal)
        else:
            elenco_us = Paragraph("<b>Liste SE/(Struktur)</b><br/>" + str(self.elenco_us), styNormal)

            # luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

            # schema
        cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
            [logo, '01', '02', '03', '04', '05', num_cassa, '07', '08', '09'],
            [sito, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_us, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_inv_tip_rep, '01', '02', '03', '04', '05', '06', '07', '08', '09']

        ]

        # table style
        table_style = [

            ('GRID', (0, 0), (-1, -1), 0, colors.white),  # ,0.0,colors.black
            # 0 row
            ('SPAN', (0, 0), (5, 0)),  # elenco US
            ('SPAN', (6, 0), (9, 0)),  # elenco US
            ('HALIGN', (0, 0), (9, 0), 'LEFT'),
            ('VALIGN', (6, 0), (9, 0), 'TOP'),
            ('HALIGN', (6, 0), (9, 0), 'RIGHT'),

            ('SPAN', (0, 1), (9, 1)),  # elenco US
            ('HALIGN', (0, 1), (9, 1), 'LEFT'),

            ('SPAN', (0, 2), (9, 2)),  # intestazione
            ('VALIGN', (0, 2), (9, 2), 'TOP'),
            # 1 row
            ('SPAN', (0, 3), (9, 3)),  # elenco US
            ('VALIGN', (0, 3), (9, 3), 'TOP')

        ]

        colWidths = None
        rowHeights = None
        # colWidths=[80,80,80, 80,80, 80,80,80,80, 80]
        t = Table(cell_schema, colWidths, rowHeights, style=table_style)

        return t
        
    def create_sheet_en(self):
        styleSheet = getSampleStyleSheet()

        styleSheet.add(ParagraphStyle(name='Cassa Label'))
        styleSheet.add(ParagraphStyle(name='Sito Label'))

        styCassaLabel = styleSheet['Cassa Label']
        styCassaLabel.spaceBefore = 0
        styCassaLabel.spaceAfter = 0
        styCassaLabel.alignment = 2  # RIGHT
        styCassaLabel.leading = 25
        styCassaLabel.fontSize = 30

        stySitoLabel = styleSheet['Sito Label']
        stySitoLabel.spaceBefore = 0
        stySitoLabel.spaceAfter = 0
        stySitoLabel.alignment = 0  # LEFT
        stySitoLabel.leading = 25
        stySitoLabel.fontSize = 18
        stySitoLabel.fontStyle = 'bold'

        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 10
        styNormal.spaceAfter = 10
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 14
        styNormal.leading = 15

        # format labels
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path=lo_path_str
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch

        num_cassa = Paragraph("<b>Box</b>" + str(self.cassa), styCassaLabel)
        sito = Paragraph("<b>Site: </b>" + str(self.sito), stySitoLabel)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>List N° Inv. / Material type</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>List N° Inv. / Material type</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>List SU/(Structure)</b>", styNormal)
        else:
            elenco_us = Paragraph("<b>List SU/(Structure)</b><br/>" + str(self.elenco_us), styNormal)

            # luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

            # schema
        cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
            [logo, '01', '02', '03', '04', '05', num_cassa, '07', '08', '09'],
            [sito, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_us, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_inv_tip_rep, '01', '02', '03', '04', '05', '06', '07', '08', '09']

        ]

        # table style
        table_style = [

            ('GRID', (0, 0), (-1, -1), 0, colors.white),  # ,0.0,colors.black
            # 0 row
            ('SPAN', (0, 0), (5, 0)),  # elenco US
            ('SPAN', (6, 0), (9, 0)),  # elenco US
            ('HALIGN', (0, 0), (9, 0), 'LEFT'),
            ('VALIGN', (6, 0), (9, 0), 'TOP'),
            ('HALIGN', (6, 0), (9, 0), 'RIGHT'),

            ('SPAN', (0, 1), (9, 1)),  # elenco US
            ('HALIGN', (0, 1), (9, 1), 'LEFT'),

            ('SPAN', (0, 2), (9, 2)),  # intestazione
            ('VALIGN', (0, 2), (9, 2), 'TOP'),
            # 1 row
            ('SPAN', (0, 3), (9, 3)),  # elenco US
            ('VALIGN', (0, 3), (9, 3), 'TOP')

        ]

        colWidths = None
        rowHeights = None
        # colWidths=[80,80,80, 80,80, 80,80,80,80, 80]
        t = Table(cell_schema, colWidths, rowHeights, style=table_style)

        return t    
class CASSE_index_pdf_sheet(object):
    def __init__(self, data):
        self.cassa = data[0]  # 1 - Cassa
        self.elenco_inv_tip_rep = data[1]  # 2-  elenco US
        self.elenco_us = data[2]  # 3 - elenco Inventari
        self.luogo_conservazione = data[3]  # 4 - luogo conservazione

    def getTable(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 10
        styNormal.fontName = 'Cambria'
        # self.unzip_rapporti_stratigrafici()

        num_cassa = Paragraph("<b>N.</b><br/>" + str(self.cassa), styNormal)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>N° inv./Tipo materiale</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>N° inv./Tipo materiale</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == 'None':
            elenco_us = Paragraph("<b>US(struttura)</b><br/>", styNormal)
        else:
            elenco_us = Paragraph("<b>US(struttura)</b><br/>" + str(self.elenco_us), styNormal)

        luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione), styNormal)

        data = [num_cassa,
                elenco_inv_tip_rep,
                elenco_us,
                luogo_conservazione]

        return data
        
    def getTable_de(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 10

        # self.unzip_rapporti_stratigrafici()

        num_cassa = Paragraph("<b>Nr.</b><br/>" + str(self.cassa), styNormal)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>Liste N° Inv. / Art material</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>Liste N° Inv. / Art material</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>SE(Struktur)</b><br/>", styNormal)
        else:
            elenco_us = Paragraph("<b>SE(Struktur)</b><br/>" + str(self.elenco_us), styNormal)

        luogo_conservazione = Paragraph("<b>Ort der Erhaltung</b><br/>" + str(self.luogo_conservazione), styNormal)

        data = [num_cassa,
                elenco_inv_tip_rep,
                elenco_us,
                luogo_conservazione]

        return data
        
    def getTable_en(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 10

        # self.unzip_rapporti_stratigrafici()

        num_cassa = Paragraph("<b>Nr.</b><br/>" + str(self.cassa), styNormal)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>N° Inv. / Material type</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>N° Inv. / Material type</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>SU(Structure)</b><br/>", styNormal)
        else:
            elenco_us = Paragraph("<b>SU(Structure)</b><br/>" + str(self.elenco_us), styNormal)

        luogo_conservazione = Paragraph("<b>Place of conservation</b><br/>" + str(self.luogo_conservazione), styNormal)

        data = [num_cassa,
                elenco_inv_tip_rep,
                elenco_us,
                luogo_conservazione]

        return data 
    def makeStyles(self):
        styles = TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.0, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP')])  # finale

        return styles


class FINDS_index_pdf_sheet(object):
    def __init__(self, data):
        self.sito = data[1]  # 1 - sito
        self.num_inventario = data[2]  # 2- numero_inventario
        self.tipo_reperto = data[3]  # 3 - tipo_reperto
        self.criterio_schedatura = data[4]  # 4 - criterio_schedatura
        self.definizione = data[5]  # 5 - definizione
        self.area = data[7]  # 7 - area
        self.us = data[8]  # 8 - us
        self.lavato = data[9]  # 9 - lavato
        self.numero_cassa = data[10]  # 10 - numero cassa
        self.repertato = data[21]  # 22 - repertato
        self.diagnostico = data[22]  # 23 - diagnostico
        self.n_reperto = data[23]  # 23 - diagnostico

    def getTable(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 7
        styNormal.fontName = 'Cambria'
        # self.unzip_rapporti_stratigrafici()

        num_inventario = Paragraph("<b>N° inv.</b><br/>" + str(self.num_inventario), styNormal)

        if self.tipo_reperto == None:
            tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>", styNormal)
        else:
            tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>" + str(self.tipo_reperto), styNormal)

        if self.criterio_schedatura == None:
            classe_materiale = Paragraph("<b>Classe materiale</b><br/>", styNormal)
        else:
            classe_materiale = Paragraph("<b>Classe materiale</b><br/>" + str(self.criterio_schedatura), styNormal)

        if self.definizione == None:
            definizione = Paragraph("<b>Definizione</b><br/>", styNormal)
        else:
            definizione = Paragraph("<b>Definizione</b><br/>" + str(self.definizione), styNormal)

        if str(self.area) == "None":
            area = Paragraph("<b>Area</b><br/>", styNormal)
        else:
            area = Paragraph("<b>Area</b><br/>" + str(self.area), styNormal)

        if str(self.us) == "None":
            us = Paragraph("<b>US</b><br/>", styNormal)
        else:
            us = Paragraph("<b>US</b><br/>" + str(self.us), styNormal)

        if self.lavato == None:
            lavato = Paragraph("<b>Lavato</b><br/>", styNormal)
        else:
            lavato = Paragraph("<b>Lavato</b><br/>" + str(self.lavato), styNormal)

        if self.repertato == None:
            repertato = Paragraph("<b>Repertato</b><br/>", styNormal)
        else:
            repertato = Paragraph("<b>Repertato</b><br/>" + str(self.repertato), styNormal)

        if self.diagnostico == None:
            diagnostico = Paragraph("<b>Diagnostico</b><br/>", styNormal)
        else:
            diagnostico = Paragraph("<b>Diagnostico</b><br/>" + str(self.diagnostico), styNormal)

        if str(self.numero_cassa) == "None":
            nr_cassa = Paragraph("<b>N° cassa</b><br/>", styNormal)
        else:
            nr_cassa = Paragraph("<b>N° cassa</b><br/>" + str(self.numero_cassa), styNormal)
        
        if str(self.n_reperto) == "None":
            n_reperto = Paragraph("<b>N° reperto</b><br/>", styNormal)
        else:
            n_reperto = Paragraph("<b>N° reperto</b><br/>" + str(self.n_reperto), styNormal)
        
        data = [num_inventario,
                tipo_reperto,
                classe_materiale,
                definizione,
                area,
                us,
                lavato,
                repertato,
                diagnostico,
                nr_cassa,
                n_reperto]

        return data
    
    def getTable_de(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 7
        styNormal.fontName = 'Cambria'
        # self.unzip_rapporti_stratigrafici()

        num_inventario = Paragraph("<b>N° Inv.</b><br/>" + str(self.num_inventario), styNormal)

        if self.tipo_reperto == None:
            tipo_reperto = Paragraph("<b>Funde Art</b><br/>", styNormal)
        else:
            tipo_reperto = Paragraph("<b>Funde Art</b><br/>" + str(self.tipo_reperto), styNormal)

        if self.criterio_schedatura == None:
            classe_materiale = Paragraph("<b>Materialklasse</b><br/>", styNormal)
        else:
            classe_materiale = Paragraph("<b>Materialklasse</b><br/>" + str(self.criterio_schedatura), styNormal)

        if self.definizione == None:
            definizione = Paragraph("<b>Definition</b><br/>", styNormal)
        else:
            definizione = Paragraph("<b>Definition</b><br/>" + str(self.definizione), styNormal)

        if str(self.area) == "None":
            area = Paragraph("<b>Areal</b><br/>", styNormal)
        else:
            area = Paragraph("<b>Areal</b><br/>" + str(self.area), styNormal)

        if str(self.us) == "None":
            us = Paragraph("<b>SE</b><br/>", styNormal)
        else:
            us = Paragraph("<b>SE</b><br/>" + str(self.us), styNormal)

        if self.lavato == None:
            lavato = Paragraph("<b>Gewaschen</b><br/>", styNormal)
        else:
            lavato = Paragraph("<b>Gewaschen</b><br/>" + str(self.lavato), styNormal)

        if self.repertato == None:
            repertato = Paragraph("<b>Abgerufen</b><br/>", styNormal)
        else:
            repertato = Paragraph("<b>Abgerufen</b><br/>" + str(self.repertato), styNormal)

        if self.diagnostico == None:
            diagnostico = Paragraph("<b>Diagnose</b><br/>", styNormal)
        else:
            diagnostico = Paragraph("<b>Diagnose</b><br/>" + str(self.diagnostico), styNormal)

        if str(self.numero_cassa) == "None":
            nr_cassa = Paragraph("<b>N° Box</b><br/>", styNormal)
        else:
            nr_cassa = Paragraph("<b>N° Box</b><br/>" + str(self.numero_cassa), styNormal)

        data = [num_inventario,
                tipo_reperto,
                classe_materiale,
                definizione,
                area,
                us,
                lavato,
                repertato,
                diagnostico,
                nr_cassa]

        return data
        
    def getTable_en(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 7

        # self.unzip_rapporti_stratigrafici()

        num_inventario = Paragraph("<b>Inventary Nr.</b><br/>" + str(self.num_inventario), styNormal)

        if self.tipo_reperto == None:
            tipo_reperto = Paragraph("<b>Find Type</b><br/>", styNormal)
        else:
            tipo_reperto = Paragraph("<b>Find Type</b><br/>" + str(self.tipo_reperto), styNormal)

        if self.criterio_schedatura == None:
            classe_materiale = Paragraph("<b>Material Class</b><br/>", styNormal)
        else:
            classe_materiale = Paragraph("<b>Material Class</b><br/>" + str(self.criterio_schedatura), styNormal)

        if self.definizione == None:
            definizione = Paragraph("<b>Definition</b><br/>", styNormal)
        else:
            definizione = Paragraph("<b>Definition</b><br/>" + str(self.definizione), styNormal)

        if str(self.area) == "None":
            area = Paragraph("<b>Area</b><br/>", styNormal)
        else:
            area = Paragraph("<b>Area</b><br/>" + str(self.area), styNormal)

        if str(self.us) == "None":
            us = Paragraph("<b>SU</b><br/>", styNormal)
        else:
            us = Paragraph("<b>SU</b><br/>" + str(self.us), styNormal)

        if self.lavato == None:
            lavato = Paragraph("<b>Whashed</b><br/>", styNormal)
        else:
            lavato = Paragraph("<b>Whashed</b><br/>" + str(self.lavato), styNormal)

        if self.repertato == None:
            repertato = Paragraph("<b>Found</b><br/>", styNormal)
        else:
            repertato = Paragraph("<b>Found</b><br/>" + str(self.repertato), styNormal)

        if self.diagnostico == None:
            diagnostico = Paragraph("<b>Diagnostic</b><br/>", styNormal)
        else:
            diagnostico = Paragraph("<b>Diagnostic</b><br/>" + str(self.diagnostico), styNormal)

        if str(self.numero_cassa) == "None":
            nr_cassa = Paragraph("<b>Box Nr.</b><br/>", styNormal)
        else:
            nr_cassa = Paragraph("<b>Box Nr.</b><br/>" + str(self.numero_cassa), styNormal)

        data = [num_inventario,
                tipo_reperto,
                classe_materiale,
                definizione,
                area,
                us,
                lavato,
                repertato,
                diagnostico,
                nr_cassa]

        return data 
    def makeStyles(self):
        styles = TableStyle([('GRID', (0, 0), (-1, -1), 0.0, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP')
                             ])  # finale

        return styles
class FOTO_index_pdf_sheet(object):
    

    def __init__(self, data):
        
        
        self.sito= data[0]
        self.n_reperto=data[1]
        self.thumbnail = data[2]
        self.us = data[3]
        self.definizione = data[4]
        self.datazione_reperto= data[5]
        self.stato_conservazione =data[6]
        self.tipo_contenitore =data[7]
        self.nr_cassa= data[8]
        
        
        
        
        
    def getTable(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 6
        styNormal.fontName = 'Cambria'
        


        
        n_reperto = Paragraph("<b>Numero reperto</b><br/>" + str(self.n_reperto), styNormal)
        us = Paragraph("<b>US</b><br/>" + str(self.us), styNormal)
        definizione = Paragraph("<b>Tipo materiale</b><br/>" + str(self.definizione), styNormal)
        datazione_reperto = Paragraph("<b>Datazione</b><br/>" + str(self.datazione_reperto), styNormal)
        stato_conservazione = Paragraph("<b>Stato di conservazione</b><br/>"+ str(self.stato_conservazione), styNormal)
        if self.tipo_contenitore=='None':
            tipo_contenitore = Paragraph("<b>Tipo di contenitore</b><br/>", styNormal)
        else:
            tipo_contenitore = Paragraph("<b>Tipo di contenitore</b><br/>"+ str(self.tipo_contenitore), styNormal)
        nr_cassa = Paragraph("<b>Numero contenitore</b><br/>"+ str(self.nr_cassa), styNormal)
        try:
            if bool(self.thumbnail):
                th = Image(self.thumbnail)
                th.drawHeight = 1 * inch * th.drawHeight / th.drawWidth
                th.drawWidth = 1 * inch
                th.hAlign = "CENTER"
                foto = th
            else:
                foto = Paragraph("<b>IMG</b><br/>" + str('Not in database'), styNormal)
        except:
            foto = Paragraph("<b>IMG</b><br/>" + str('Immagine taggata\n ma manca la thubmnail'), styNormal)

        
        data = [                
                n_reperto,
                foto,
                us,
                definizione,
                datazione_reperto,
                stato_conservazione,
                tipo_contenitore,
                nr_cassa
                ]

        return data
    
    def getTable_en(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 6

        

        conn = Connection()
    
        thumb_path = conn.thumb_path()

        n_reperto = Paragraph("<b>Aretfact number</b><br/>" + str(self.n_reperto), styNormal)
        us = Paragraph("<b>SU</b><br/>" + str(self.us), styNormal)
        definizione = Paragraph("<b>Artefact type</b><br/>" + str(self.definizione), styNormal)
        datazione_reperto = Paragraph("<b>Dating</b><br/>" + str(self.datazione_reperto), styNormal)
        stato_conservazione = Paragraph("<b>State of preservation</b><br/>"+ str(self.stato_conservazione), styNormal)
        if self.tipo_contenitore=='None':
            tipo_contenitore = Paragraph("<b>Container type</b><br/>", styNormal)
        else:
            tipo_contenitore = Paragraph("<b>Container type</b><br/>"+ str(self.tipo_contenitore), styNormal)
        nr_cassa = Paragraph("<b>Container number</b><br/>"+ str(self.nr_cassa), styNormal)
        try:
            if bool(self.thumbnail):
                th = Image(self.thumbnail)
                th.drawHeight = 1 * inch * th.drawHeight / th.drawWidth
                th.drawWidth = 1 * inch
                th.hAlign = "CENTER"
                foto = th
            else:
                foto = Paragraph("<b>IMG</b><br/>" + str('Not in database'), styNormal)
        except:
            foto = Paragraph("<b>IMG</b><br/>" + str('Tagged image \n but thubmnail missing'), styNormal)
        data = [                
                n_reperto,
                foto,
                us,
                definizione,
                datazione_reperto,
                stato_conservazione,
                tipo_contenitore,
                nr_cassa
                ]

        return data
    
    def getTable_de(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 6

        

        # conn = Connection()
    
        # thumb_path = conn.thumb_path()
        
        n_reperto = Paragraph("<b>Artefaktnummer</b><br/>" + str(self.n_reperto), styNormal)
        us = Paragraph("<b>SE</b><br/>" + str(self.us), styNormal)
        definizione = Paragraph("<b>Artefakttyp</b><br/>" + str(self.definizione), styNormal)
        datazione_reperto = Paragraph("<b>Datum</b><br/>" + str(self.datazione_reperto), styNormal)
        stato_conservazione = Paragraph("<b>Erhaltungszustand</b><br/>"+ str(self.stato_conservazione), styNormal)
        if self.tipo_contenitore=='None':
            tipo_contenitore = Paragraph("<b>Typ des Container</b><br/>", styNormal)
        else:
            tipo_contenitore = Paragraph("<b>Typ des Container</b><br/>"+ str(self.tipo_contenitore), styNormal)
        nr_cassa = Paragraph("<b>Container-Nummer</b><br/>"+ str(self.nr_cassa), styNormal)
        try:
            if bool(self.thumbnail):
                th = Image(self.thumbnail)
                th.drawHeight = 1 * inch * th.drawHeight / th.drawWidth
                th.drawWidth = 1 * inch
                th.hAlign = "CENTER"
                foto = th
            else:
                foto = Paragraph("<b>IMG</b><br/>" + str('Not in database'), styNormal)
        except:
            foto = Paragraph("<b>IMG</b><br/>" + str('Afbeelding getagd\n, maar dubbeltag ontbreekt'), styNormal)
        data = [                
                n_reperto,
                foto,
                us,
                definizione,
                datazione_reperto,
                stato_conservazione,
                tipo_contenitore,
                nr_cassa
                ]

        return data
    def makeStyles(self):
        styles = TableStyle([('GRID', (0, 0), (-1, -1), 0.0, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP')
                             ])  # finale

        return styles
class FOTO_index_pdf_sheet_2(object):
    

    def __init__(self, data):
        
        
        self.sito= data[0]
        self.numero_inventario= data[1]
        #self.foto = data[2]
        self.us = data[3]
        self.tipo_reperto = data[4]
        self.repertato= data[5]
        self.n_reperto=data[6]
        self.tipo_contenitore =data[7]
        self.nr_cassa= data[8]
        self.luogo_conservazione =data[9]
        self.years = data[10]
        
        
        
        
    def getTable(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 6
        styNormal.fontName = 'Cambria'
        

        
        numero_inventario = Paragraph("<b>Numero inv.</b><br/>" + str(self.numero_inventario), styNormal)
        us = Paragraph("<b>US</b><br/>" + str(self.us), styNormal)
        # if bool(self.foto):
        #     foto = Paragraph("<b>IMG</b><br/>" + str(self.foto), styNormal)
        # else:
        #     pass
        tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>" + str(self.tipo_reperto), styNormal)
        repertato = Paragraph("<b>Repertato</b><br/>" + str(self.repertato), styNormal)
        if self.repertato=='No':
            n_reperto = Paragraph("<b>Numero reperto</b><br/>", styNormal)
        else:
            n_reperto = Paragraph("<b>Numero reperto</b><br/>"+ str(self.n_reperto), styNormal)
        tipo_contenitore = Paragraph("<b>Tipo di contenitore</b><br/>"+ str(self.tipo_contenitore), styNormal)
        nr_cassa = Paragraph("<b>Numero contenitore</b><br/>"+ str(self.nr_cassa), styNormal)
        luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>"+ str(self.luogo_conservazione), styNormal)
        anno = Paragraph("<b>Anno</b><br/>" + str(self.years), styNormal)
        
        

        data = [
                numero_inventario,
                us ,
                #foto,
                tipo_reperto,
                repertato,
                n_reperto,
                tipo_contenitore,
                nr_cassa,
                luogo_conservazione,
                anno
                ]

        return data
    
    def getTable_en(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 6

        

        
        numero_inventario = Paragraph("<b>Inventory Number</b><br/>" + str(self.numero_inventario), styNormal)
        us = Paragraph("<b>SU</b><br/>" + str(self.us), styNormal)
        # if bool(self.foto):
        #     foto = Paragraph("<b>IMG</b><br/>" + str(self.foto), styNormal)
        # else:
        #     pass
        tipo_reperto = Paragraph("<b>Artefact type</b><br/>" + str(self.tipo_reperto), styNormal)
        repertato = Paragraph("<b>Aretfact</b><br/>" + str(self.repertato), styNormal)
        if self.repertato=='No':
            n_reperto = Paragraph("<b>Number artefact</b><br/>", styNormal)
        else:
            n_reperto = Paragraph("<b>Number artefact</b><br/>"+ str(self.n_reperto), styNormal)
        tipo_contenitore = Paragraph("<b>Container type</b><br/>"+ str(self.tipo_contenitore), styNormal)
        nr_cassa = Paragraph("<b>Container numebr</b><br/>"+ str(self.nr_cassa), styNormal)
        luogo_conservazione = Paragraph("<b>Place of conservation</b><br/>"+ str(self.luogo_conservazione), styNormal)
        years = Paragraph("<b>Year</b><br/>" + str(self.years), styNormal)
       
        data = [
                numero_inventario,
                us ,
                #foto,
                tipo_reperto,
                repertato,
                n_reperto,
                tipo_contenitore,
                nr_cassa,
                luogo_conservazione,
                years
                ]

        return data
    
    def getTable_de(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 6

        

        
        numero_inventario = Paragraph("<b>Artefaktnummer</b><br/>" + str(self.numero_inventario), styNormal)
        us = Paragraph("<b>SE</b><br/>" + str(self.us), styNormal)
        # if bool(self.foto):
        #     foto = Paragraph("<b>IMG</b><br/>" + str(self.foto), styNormal)
        # else:
        #     pass
        tipo_reperto = Paragraph("<b>Artefakttyp</b><br/>" + str(self.tipo_reperto), styNormal)
        repertato = Paragraph("<b>Artefakt</b><br/>" + str(self.repertato), styNormal)
        if self.repertato=='No':
            n_reperto = Paragraph("<b>Artefakt n.</b><br/>", styNormal)
        else:
            n_reperto = Paragraph("<b>Artefakt n.</b><br/>"+ str(self.n_reperto), styNormal)
        tipo_contenitore = Paragraph("<b>Container-Typ</b><br/>"+ str(self.tipo_contenitore), styNormal)
        nr_cassa = Paragraph("<b>Container-Nummer</b><br/>"+ str(self.nr_cassa), styNormal)
        luogo_conservazione = Paragraph("<b>Ort der Lagerung</b><br/>"+ str(self.luogo_conservazione), styNormal)
        years = Paragraph("<b>Years</b><br/>" + str(self.years), styNormal)
        
       
        data = [
                numero_inventario,
                us ,
                #foto,
                tipo_reperto,
                repertato,
                n_reperto,
                tipo_contenitore,
                nr_cassa,
                luogo_conservazione,
                years
                ]

        return data
    
    def makeStyles(self):
        styles = TableStyle([('GRID', (0, 0), (-1, -1), 0.0, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP')
                             ])  # finale

        return styles
   

class generate_reperti_pdf(object):
    HOME = os.environ['PYARCHINIT_HOME']

    PDF_path = '{}{}{}'.format(HOME, os.sep, "pyarchinit_PDF_folder")

    def datestrfdate(self):
        now = date.today()
        today = now.strftime("%d-%m-%Y")
        return today
    
    def build_index_Foto(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path=lo_path_str
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"
        
        # logo_2 = Image(logo_path2)
        # logo_2.drawHeight = 1.5 * inch * logo_2.drawHeight / logo_2.drawWidth
        # logo_2.drawWidth = 1.5 * inch
        # logo_2.hAlign = "CENTER"
        
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']
        styH1.fontName='Cambria'
        data = self.datestrfdate()

        lst = []
        #lst2=[]
        lst.append(logo)
        #lst2.append(logo_2)
        lst.append(
            Paragraph("<b>ELENCO REPERTI</b><br/><b> Scavo: %s </b><br/>" % (sito), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FOTO_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable())

        styles = exp_index.makeStyles()
        colWidths = [100, 100, 50, 100,100,100,100, 100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 2))

        dt = datetime.datetime.now()
        filename = ('%s%s%s') % (
        self.PDF_path, os.sep, 'Elenco Reperti thumbnail.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    
    def build_index_Foto_en(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path=lo_path_str
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"
        # logo_2 = Image(logo_path2)
        # logo_2.drawHeight = 1.5 * inch * logo_2.drawHeight / logo_2.drawWidth
        # logo_2.drawWidth = 1.5 * inch
        # logo_2.hAlign = "CENTER"
        
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()

        lst = []
        #lst2=[]
        lst.append(logo)
        #lst2.append(logo_2)
        lst.append(
            Paragraph("<b>INVENTORY LIST ARTIFACTS</b><br/><b> Site: %s </b><br/><b>  Date: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FOTO_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_en())

        styles = exp_index.makeStyles()
        colWidths = [100, 100, 50, 100,100,100,100, 100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 2))

        dt = datetime.datetime.now()
        filename = ('%s%s%s_%s_%s_%s_%s_%s_%s%s') % (
        self.PDF_path, os.sep, 'List Artefact thumnail', dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second, ".pdf")
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    
    
    def build_index_Foto_de(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = lo_path_str#'{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"
        # logo_2 = Image(logo_path2)
        # logo_2.drawHeight = 1.5 * inch * logo_2.drawHeight / logo_2.drawWidth
        # logo_2.drawWidth = 1.5 * inch
        # logo_2.hAlign = "CENTER"
        
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()

        lst = []
        #lst2=[]
        lst.append(logo)
        #lst2.append(logo_2)
        lst.append(
            Paragraph("<b>INVENTURLISTE gefertigter ARTIKEL</b><br/><b> Ausgrabungsstätte: %s </b><br/><b>  Datum: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FOTO_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_de())

        styles = exp_index.makeStyles()
        colWidths = [100, 100, 50, 100,100,100,100,100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 2))

        dt = datetime.datetime.now()
        filename = ('%s%s%s_%s_%s_%s_%s_%s_%s%s') % (
        self.PDF_path, os.sep, 'Liste der Artefakte', dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second, ".pdf")
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    
    def build_index_Foto_2(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"
        
        # logo_2 = Image(logo_path2)
        # logo_2.drawHeight = 1.5 * inch * logo_2.drawHeight / logo_2.drawWidth
        # logo_2.drawWidth = 1.5 * inch
        # logo_2.hAlign = "CENTER"
        
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']
        styH1.fontName='Cambria'
        data = self.datestrfdate()

        lst = []
        #lst2=[]
        lst.append(logo)
        #lst2.append(logo_2)
        lst.append(
            Paragraph("<b>ELENCO INVENTARIO</b><br/><b> Scavo: %s </b><br/>" % (sito), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FOTO_index_pdf_sheet_2(records[i])
            table_data.append(exp_index.getTable())

        styles = exp_index.makeStyles()
        colWidths = [50, 50, 50,100,100,100,150,100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 2))

        dt = datetime.datetime.now()
        filename = ('%s%s%s') % (
        self.PDF_path, os.sep, 'Elenco Inventario.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    
    def build_index_Foto_2_en(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path=lo_path_str
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"
        
        # logo_2 = Image(logo_path2)
        # logo_2.drawHeight = 1.5 * inch * logo_2.drawHeight / logo_2.drawWidth
        # logo_2.drawWidth = 1.5 * inch
        # logo_2.hAlign = "CENTER"
        
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()

        lst = []
        #lst2=[]
        lst.append(logo)
        #lst2.append(logo_2)
        lst.append(
            Paragraph("<b>INVENTORY LIST</b><br/><b> Site: %s </b><br/><b>  Date: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FOTO_index_pdf_sheet_2(records[i])
            table_data.append(exp_index.getTable_en())

        styles = exp_index.makeStyles()
        colWidths = [50, 50, 50,100,100,80,80,100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 2))

        dt = datetime.datetime.now()
        filename = ('%s%s%s_%s_%s_%s_%s_%s_%s%s') % (
        self.PDF_path, os.sep, 'List Inventory', dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second, ".pdf")
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    
    def build_index_Foto_2_de(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path=lo_path_str
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"
        
        # logo_2 = Image(logo_path2)
        # logo_2.drawHeight = 1.5 * inch * logo_2.drawHeight / logo_2.drawWidth
        # logo_2.drawWidth = 1.5 * inch
        # logo_2.hAlign = "CENTER"
        
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()

        lst = []
        #lst2=[]
        lst.append(logo)
        #lst2.append(logo_2)
        lst.append(
            Paragraph("<b>INVENTURLISTE</b><br/><b> Ausgrabungsstätte: %s </b><br/><b>  Datum: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FOTO_index_pdf_sheet_2(records[i])
            table_data.append(exp_index.getTable_de())

        styles = exp_index.makeStyles()
        colWidths = [50, 50, 50,100,100,100,150,100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 2))

        dt = datetime.datetime.now()
        filename = ('%s%s%s_%s_%s_%s_%s_%s_%s%s') % (
        self.PDF_path, os.sep, 'Inventurliste', dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second, ".pdf")
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    
    
    def build_Finds_sheets(self, records):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = single_Finds_pdf_sheet(records[i])
            elements.append(single_finds_sheet.create_sheet())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep,'Scheda Reperti.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f)
        doc.build(elements, canvasmaker=NumberedCanvas_Findssheet)
        f.close()
    def build_Finds_sheets_de(self, records):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = single_Finds_pdf_sheet(records[i])
            elements.append(single_finds_sheet.create_sheet_de())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'Formular_Finds.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f)
        doc.build(elements, canvasmaker=NumberedCanvas_Findssheet)
        f.close()
    def build_Finds_sheets_en(self, records):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = single_Finds_pdf_sheet(records[i])
            elements.append(single_finds_sheet.create_sheet_en())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'Finds_form.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f)
        doc.build(elements, canvasmaker=NumberedCanvas_Findssheet)
        f.close()   
    def build_index_Finds(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']
        styH1.fontName='Cambria'
        data = self.datestrfdate()

        lst = []
        lst.append(logo)
        lst.append(Paragraph("<b>ELENCO MATERIALI</b><br/><b>Scavo: %s</b>" % ('l'), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FINDS_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable())

        styles = exp_index.makeStyles()
        colWidths = [70, 110, 110, 110, 35, 35, 60, 60, 60, 60,60]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'Elenco Materiali.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    def build_index_Finds_de(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()

        lst = []
        lst.append(logo)
        lst.append(Paragraph("<b>LISTE MATERIAL</b><br/><b>Ausgrabungsstättesstätte: %s,  Datum: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FINDS_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_de())

        styles = exp_index.makeStyles()
        colWidths = [70, 110, 110, 110, 35, 35, 60, 60, 60, 60,60]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'liste_material.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    def build_index_Finds_en(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()

        lst = []
        lst.append(logo)
        lst.append(Paragraph("<b>LIST MATERIAL</b><br/><b>Site: %s,  Data: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FINDS_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_en())

        styles = exp_index.makeStyles()
        colWidths = [70, 110, 110, 110, 35, 35, 60, 60, 60, 60,60]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'list_material.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()   
    def build_index_Casse(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"
        # logo_2 = Image(logo_path2)
        # logo_2.drawHeight = 1.5 * inch * logo_2.drawHeight / logo_2.drawWidth
        # logo_2.drawWidth = 1.5 * inch
        # logo_2.hAlign = "CENTER"
        
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']
        styH1.fontName='Cambria'
        data = self.datestrfdate()

        lst = []
        #lst2=[]
        lst.append(logo)
        #lst2.append(logo_2)
        lst.append(
            Paragraph("<b>ELENCO CASSE</b><br/><b> Scavo: %s </b><br/>" % (sito), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = CASSE_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable())

        styles = exp_index.makeStyles()
        colWidths = [50, 350, 300, 300]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 2))

        dt = datetime.datetime.now()
        filename = ('%s%s%s') % (
        self.PDF_path, os.sep, 'Elenco Casse.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f, pagesize=(41 * cm, 29 * cm), showBoundary=0, topMargin=15, bottomMargin=40,leftMargin=30, rightMargin=30)
        # doc.build(lst, canvasmaker=NumberedCanvas_Sindex)
        doc.build(lst)
        
        
        f.close()

        f.close()
    def build_index_Casse_de(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()
        lst = [logo]
        lst.append(Paragraph("<b>LISTE BOX MATERIAL</b><br/><b>Scavo: %s,  Data: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = CASSE_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_de())

        styles = exp_index.makeStyles()
        colWidths = [20, 350, 250, 100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        # table_data_formatted.setStyle(styles)

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'liste_box.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(41 * cm, 29 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        # doc.build(lst, canvasmaker=NumberedCanvas_Sindex)
        doc.build(lst)

        f.close()
    def build_index_Casse_en(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        conn = Connection()
        lo_path = conn.logo_path()
        lo_path_str = lo_path['logo']
        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        if not bool(lo_path_str):
            logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        else:
            logo_path=lo_path_str
        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()
        lst = [logo]
        lst.append(Paragraph("<b>LISTE BOX MATERIAL</b><br/><b>Scavo: %s,  Data: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = CASSE_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_en())

        styles = exp_index.makeStyles()
        colWidths = [20, 350, 250, 100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        # table_data_formatted.setStyle(styles)

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'list_box.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(41 * cm, 29 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        # doc.build(lst, canvasmaker=NumberedCanvas_Sindex)
        doc.build(lst)

        f.close()   
    def build_box_labels_Finds(self, records, sito):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = Box_labels_Finds_pdf_sheet(records[i], sito)
            elements.append(single_finds_sheet.create_sheet())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'Etichette Casse Materiali.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0.0, topMargin=20, bottomMargin=20,
                                leftMargin=20, rightMargin=20)
        doc.build(elements)
        f.close()
    def build_box_labels_Finds_de(self, records, sito):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = Box_labels_Finds_pdf_sheet(records[i], sito)
            elements.append(single_finds_sheet.create_sheet_de())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'liste_box_material.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0.0, topMargin=20, bottomMargin=20,
                                leftMargin=20, rightMargin=20)
        doc.build(elements)
        f.close()
    def build_box_labels_Finds_en(self, records, sito):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = Box_labels_Finds_pdf_sheet(records[i], sito)
            elements.append(single_finds_sheet.create_sheet_en())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'list_box_material.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0.0, topMargin=20, bottomMargin=20,
                                leftMargin=20, rightMargin=20)
        doc.build(elements)
        f.close()   
