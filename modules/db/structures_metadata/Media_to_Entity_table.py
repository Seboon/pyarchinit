'''
Created on 19 feb 2018

@author: Serena Sensini; Enzo Cocca <enzo.ccc@gmail.com>
'''
from sqlalchemy import Table, Column, Integer, Text, MetaData, create_engine, UniqueConstraint

from modules.db.pyarchinit_conn_strings import Connection


class Media_to_Entity_table:
    @classmethod
    def define_table(cls, metadata):
        return Table('media_to_entity_table', metadata,
                                  Column('id_mediaToEntity', Integer, primary_key=True),
                                  Column('id_entity', Integer),
                                  Column('entity_type', Text),
                                  Column('table_name', Text),
                                  Column('id_media', Integer),
                                  Column('filepath', Text),
                                  Column('media_name', Text),

                                  # explicit/composite unique constraint.  'name' is optional.
                                  UniqueConstraint('id_entity', 'entity_type', 'id_media',
                                                   name='ID_mediaToEntity_unico')
                                  )


