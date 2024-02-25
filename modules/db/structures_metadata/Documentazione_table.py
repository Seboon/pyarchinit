'''
Created on 15 feb 2018

@author: Serena Sensini; Enzo Cocca <enzo.ccc@gmail.com>
'''
from sqlalchemy import Table, Column, Integer, Text, MetaData, create_engine, UniqueConstraint




class Documentazione_table:

    @classmethod
    def define_table(cls, metadata):
        return Table('documentazione_table', metadata,
                     Column('id_documentazione', Integer, primary_key=True),
                     Column('sito', Text),
                     Column('nome_doc', Text),
                     Column('data', Text),
                     Column('tipo_documentazione', Text),
                     Column('sorgente', Text),
                     Column('scala', Text),
                     Column('disegnatore', Text),
                     Column('note', Text),

                     # explicit/composite unique constraint.  'name' is optional.
                     UniqueConstraint('sito', 'tipo_documentazione', 'nome_doc', name='ID_invdoc_unico')
                     )


