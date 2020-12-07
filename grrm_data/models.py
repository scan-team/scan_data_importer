from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.types import BINARY, TEXT, VARCHAR
from sqlalchemy.orm import relationship

# from service.database import Base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class GRRMMap(Base):
    __tablename__ = u'maps'

    id = Column(BINARY(16), primary_key=True)

    atom_name = Column(TEXT)
    initxyz = Column(TEXT)
    fname_top_abs = Column(VARCHAR(1024))
    fname_top_rel = Column(VARCHAR(256))
    natoms = Column(Integer)
    lowest_energy = Column(Float)
    highest_energy = Column(Float)
    neq = Column(Integer)
    nts = Column(Integer)
    npt = Column(Integer)
    jobtime = Column(DateTime)
    universal_gamma = Column(Float)
    infile = Column(VARCHAR(256))
    scpathpara = Column(VARCHAR(256))
    jobtype = Column(VARCHAR(20))
    pathtype = Column(VARCHAR(20))
    nobondrearrange = Column(Integer)
    siml_tempearture_kelvin = Column(TEXT)
    siml_pressure_atm = Column(Float)
    energyshiftvalue_au = Column(Float)
    level = Column(VARCHAR(256))
    spinmulti = Column(Integer)
    totalcharge = Column(Float)
    jobstatus = Column(VARCHAR(20))
    ngradient = Column(Integer)
    nhessian = Column(Integer)
    elapsedtime_sec = Column(Float)


class Eq(Base):
    __tablename__ = u'eqs'

    id = Column(BINARY(16), primary_key=True)
    map_id = Column('map_id', BINARY(16), ForeignKey('maps.id'))

    nid = Column(Integer)
    category = Column(VARCHAR(20))
    symmetry = Column(VARCHAR(20))
    xyz = Column(TEXT)
    energy = Column(TEXT)
    gradient = Column(TEXT)
    s2_value = Column(Float)
    dipole = Column(TEXT)
    comment = Column(TEXT)
    electronic_energy_au = Column(TEXT)
    hess_eigenvalue_au = Column(TEXT)

    map = relationship("GRRMMap")


class Edge(Base):
    __tablename__ = u'edges'

    id = Column(BINARY(16), primary_key=True)
    map_id = Column('map_id', BINARY(16), ForeignKey('maps.id'))

    edge_id = Column(Integer)
    category = Column(VARCHAR(20))
    symmetry = Column(VARCHAR(20))
    xyz = Column(TEXT)
    energy = Column(TEXT)
    gradient = Column(TEXT)
    s2_value = Column(Float)
    dipole = Column(TEXT)
    comment = Column(TEXT)
    electronic_energy_au = Column(TEXT)
    hess_eigenvalue_au = Column(TEXT)

    connection0 = Column(Integer)
    connection1 = Column(Integer)
    pathdata = Column(TEXT)

    map = relationship("GRRMMap")


class PNode(Base):
    __tablename__ = u'path_nodes'

    id = Column(BINARY(16), primary_key=True)
    map_id = Column('map_id', BINARY(16), ForeignKey('maps.id'))
    edge_id = Column('edge_id', BINARY(16), ForeignKey('edges.id'))

    nid = Column(Integer)
    category = Column(VARCHAR(20))
    symmetry = Column(VARCHAR(20))
    xyz = Column(TEXT)
    energy = Column(TEXT)
    gradient = Column(TEXT)
    s2_value = Column(Float)
    dipole = Column(TEXT)
    comment = Column(TEXT)
    electronic_energy_au = Column(TEXT)
    hess_eigenvalue_au = Column(TEXT)

    map = relationship("GRRMMap")
    edge = relationship("Edge")
