"""
Created on 17 11 2020

@author: Enzo Cocca
"""

from geoalchemy2 import Geometry
from sqlalchemy import Table, Column, Integer, Text, MetaData, create_engine, UniqueConstraint

from modules.db.pyarchinit_conn_strings import Connection


class pycampioni:
    @classmethod
    def define_table(cls, metadata):
        return Table('pyarchinit_campionature', metadata,
                       Column('gid', Integer, primary_key=True),  # 0
                       Column('id_campion', Integer),
                       Column('sito', Text),
                       Column('tipo_camp', Text),
                       Column('dataz', Text),
                       Column('cronologia', Integer),
                       Column('link_immag', Text),
                       Column('sigla_camp', Text),
                       Column('the_geom', Geometry(geometry_type='POINT')),
                       # explicit/composite unique constraint.  'name' is optional.
                       UniqueConstraint('gid')
                       )