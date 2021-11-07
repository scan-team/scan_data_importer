from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.types import BINARY, TEXT, VARCHAR, JSON
from sqlalchemy.orm import relationship

# from service.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GRRMMap(Base):
    __tablename__ = u"maps"

    id = Column(BINARY(16), primary_key=True)

    atom_name = Column(JSON)
    initxyz = Column(JSON)
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
    siml_tempearture_kelvin = Column(JSON)
    siml_pressure_atm = Column(Float)
    energyshiftvalue_au = Column(Float)
    level = Column(VARCHAR(256))
    spinmulti = Column(Integer)
    totalcharge = Column(Float)
    jobstatus = Column(VARCHAR(20))
    ngradient = Column(Integer)
    nhessian = Column(Integer)
    elapsedtime_sec = Column(Float)

    registrant = Column(VARCHAR(256))
    creator = Column(VARCHAR(256))

    accessibility = Column(Integer)


class Eq(Base):
    __tablename__ = u"eqs"

    id = Column(BINARY(16), primary_key=True)
    map_id = Column("map_id", BINARY(16), ForeignKey("maps.id"))

    nid = Column(Integer)
    category = Column(VARCHAR(20))
    symmetry = Column(VARCHAR(20))
    xyz = Column(JSON)
    energy = Column(JSON)
    gradient = Column(JSON)
    s2_value = Column(Float)
    dipole = Column(JSON)
    comment = Column(TEXT)
    hess_eigenvalue_au = Column(JSON)

    trafficvolume = Column(JSON)
    population = Column(JSON)
    reactionyield = Column(JSON)

    map = relationship("GRRMMap")


class Edge(Base):
    __tablename__ = u"edges"

    id = Column(BINARY(16), primary_key=True)
    map_id = Column("map_id", BINARY(16), ForeignKey("maps.id"))

    edge_id = Column(Integer)
    category = Column(VARCHAR(20))
    symmetry = Column(VARCHAR(20))
    xyz = Column(JSON)
    energy = Column(JSON)
    gradient = Column(JSON)
    s2_value = Column(Float)
    dipole = Column(JSON)
    comment = Column(TEXT)
    hess_eigenvalue_au = Column(JSON)

    connection0 = Column(Integer)
    connection1 = Column(Integer)
    pathdata = Column(JSON)

    map = relationship("GRRMMap")


class PNode(Base):
    __tablename__ = u"path_nodes"

    id = Column(BINARY(16), primary_key=True)
    map_id = Column("map_id", BINARY(16), ForeignKey("maps.id"))
    edge_id = Column("edge_id", BINARY(16), ForeignKey("edges.id"))

    nid = Column(Integer)
    category = Column(VARCHAR(20))
    symmetry = Column(VARCHAR(20))
    xyz = Column(JSON)
    energy = Column(JSON)
    gradient = Column(JSON)
    s2_value = Column(Float)
    dipole = Column(JSON)
    comment = Column(TEXT)
    hess_eigenvalue_au = Column(JSON)

    map = relationship("GRRMMap")
    edge = relationship("Edge")
