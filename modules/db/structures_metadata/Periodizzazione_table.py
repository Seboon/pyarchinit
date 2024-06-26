'''
Created on 19 feb 2018

@author: Enzo Cocca <enzo.ccc@gmail.com>
'''
from sqlalchemy import Table, Column, Integer, String, Text, MetaData, create_engine, UniqueConstraint

from modules.db.pyarchinit_conn_strings import Connection


class Periodizzazione_table:

    @classmethod
    def define_table(cls, metadata):
        return Table('periodizzazione_table', metadata,
                                  Column('id_perfas', Integer, primary_key=True),
                                  Column('sito', Text),
                                  Column('periodo', Integer),
                                  Column('fase', Text),
                                  Column('cron_iniziale', Integer),
                                  Column('cron_finale', Integer),
                                  Column('descrizione', Text),
                                  Column('datazione_estesa', String(300)),
                                  Column('cont_per', Integer),

                                  # explicit/composite unique constraint.  'name' is optional.
                                  UniqueConstraint('sito', 'periodo', 'fase', name='ID_perfas_unico')
                                  )


