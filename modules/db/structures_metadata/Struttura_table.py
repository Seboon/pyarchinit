'''
Created on 19 feb 2018

@author: Serena Sensini; Enzo Cocca <enzo.ccc@gmail.com>
'''
from sqlalchemy import Table, Column, Integer, String, Text, MetaData, create_engine, UniqueConstraint

from modules.db.pyarchinit_conn_strings import Connection


class Struttura_table:
    @classmethod
    def define_table(cls, metadata):
        return Table('struttura_table', metadata,
                      Column('id_struttura', Integer, primary_key=True),
                      Column('sito', Text),
                      Column('sigla_struttura', Text),
                      Column('numero_struttura', Integer),
                      Column('categoria_struttura', Text),
                      Column('tipologia_struttura', Text),
                      Column('definizione_struttura', Text),
                      Column('descrizione', Text),
                      Column('interpretazione', Text),
                      Column('periodo_iniziale', Integer),
                      Column('fase_iniziale', Integer),
                      Column('periodo_finale', Integer),
                      Column('fase_finale', Integer),
                      Column('datazione_estesa', String(300)),
                      Column('materiali_impiegati', Text),
                      Column('elementi_strutturali', Text),
                      Column('rapporti_struttura', Text),
                      Column('misure_struttura', Text),

                      # explicit/composite unique constraint.  'name' is optional.
                      UniqueConstraint('sito', 'sigla_struttura', 'numero_struttura', name='ID_struttura_unico')
                      )


