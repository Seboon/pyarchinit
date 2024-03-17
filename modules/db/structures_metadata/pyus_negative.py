"""
Created on 17 11 2020

@author: Enzo Cocca
"""

from geoalchemy2 import Geometry
from sqlalchemy import Table, Column, Integer, Text, MetaData, create_engine, UniqueConstraint

from modules.db.pyarchinit_conn_strings import Connection


class pyus_negative:
    @classmethod
    def define_table(cls, metadata):
        return Table('pyarchinit_us_negative_doc', metadata,
                          Column('gid', Integer, primary_key=True),
                          Column('sito_n', Text),
                          Column('area_n', Integer),
                          Column('us_n', Integer),
                          Column('tipo_doc_n', Text),
                          Column('nome_doc_n', Text),
                          Column('the_geom', Geometry(geometry_type='LINESTRING')),
                          # explicit/composite unique constraint.  'name' is optional.
                          UniqueConstraint('gid')
                          )