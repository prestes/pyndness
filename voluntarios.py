#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
import soupselect; soupselect.monkeypatch()
import json
import re

class Entidade:

    def __init__(self):
        self.nome = ''
        self.area = ''
        self.responsavel = ''
        self.endereco = ''
        self.contato = ''
        self.fone = ''
        self.fundacao = ''
        self.banco = ''
        self.agencia = ''
        self.conta = ''
        self.email = ''
        self.site = ''
        self.voluntarios_url = ''

    def to_json(self):
        return json.dumps(self.__dict__)

class Voluntarios:
    count = 0
    entidades = []
    debug_mode = False

    def soupify_url(self, url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        document = response.read()
        return BeautifulSoup(document) 

    def get_entidade(self, entidade_url):
        entidade_data = self.soupify_url(entidade_url)
       
        entidade = Entidade()
        entidade_info = entidade_data.findSelect('table td[align=left]')
        entidade_info += entidade_data.findSelect('table td[valign=left]')

        entidade.nome = entidade_info[0].text
        entidade.area = entidade_info [1].text
        entidade.responsavel = entidade_info[2].text
        entidade.endereco = entidade_info[3].text
        entidade.contato = entidade_info[4].text
        entidade.fone = entidade_info[5].text
        entidade.fundacao = entidade_info[6].text
        entidade.banco = entidade_info[7].text
        entidade.agencia = entidade_info[8].text
        entidade.conta = entidade_info[9].text
        entidade.email = entidade_info[10].text
        entidade.site = entidade_info[11].text

        self.entidades.append(entidade)

        print entidade.to_json()

        print entidade_url

    def load_all(self):
        page_size = 10000
        if (self.debug_mode):
            page_size = 10
        url = "http://www.voluntarios.com.br/resultadoent.asp?whichpage=1&pagesize=%s&sqlQuery=select+*+from+qryPesquisa&fasocial=Todas" % page_size
        soup = self.soupify_url(url)
        links = soup.findSelect('div[align=left] div[align=center] table tr td a')

        for link in links:
            entidade_url = 'http://www.voluntarios.com.br/' + link.get('href')
            self.get_entidade(entidade_url)
            self.count += 1

voluntarios = Voluntarios()
voluntarios.debug_mode = True
voluntarios.load_all()
print voluntarios.count
