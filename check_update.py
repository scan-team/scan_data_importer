import argparse
import json
import os
from typing import Optional

from sqlalchemy import orm
from sqlalchemy.engine import create_engine
import ulid

from grrmlog_parser.core import parse

from grrm_data.models import Edge, GRRMMap, Eq, PNode


def create_eq_obj(session, n, map_obj):
    eq = {}

    eq_id = ulid.new()
    eq["id"] = eq_id.bytes
    eq["map"] = map_obj

    eq["nid"] = n.id  # read from the original log
    eq["category"] = n.category
    eq["symmetry"] = n.symmetry
    eq["xyz"] = n.xyz
    eq["energy"] = n.energy
    eq["gradient"] = n.gradient
    eq["s2_value"] = n.s2_value
    eq["dipole"] = n.dipole
    eq["comment"] = n.comment
    eq["hess_eigenvalue_au"] = n.hess_eigenvalue_au

    eq_obj = Eq(**eq)

    session.add(eq_obj)


def create_edge_obj(session, e, map_obj):
    edge = {}

    id = ulid.new()
    edge["id"] = id.bytes
    edge["map"] = map_obj

    edge["edge_id"] = e.id  # read from the original log
    edge["category"] = e.category
    edge["symmetry"] = e.symmetry
    edge["xyz"] = e.xyz
    edge["energy"] = e.energy
    edge["gradient"] = e.gradient
    edge["s2_value"] = e.s2_value
    edge["dipole"] = e.dipole
    edge["comment"] = e.comment
    edge["hess_eigenvalue_au"] = e.hess_eigenvalue_au

    edge["connection0"] = e.connection[0]
    edge["connection1"] = e.connection[1]

    pathdata = [ulid.new().str for _ in e.pathdata]
    edge["pathdata"] = pathdata

    edge_obj = Edge(**edge)
    session.add(edge_obj)

    # Process passdata
    for i, p_node in enumerate(e.pathdata):
        pnode_dict = {}

        pnode_dict["id"] = ulid.from_str(pathdata[i]).bytes
        pnode_dict["map"] = map_obj
        pnode_dict["edge"] = edge_obj

        pnode_dict["nid"] = p_node.id  # read from the original log
        pnode_dict["category"] = p_node.category
        pnode_dict["symmetry"] = p_node.symmetry
        pnode_dict["xyz"] = p_node.xyz
        pnode_dict["energy"] = p_node.energy
        pnode_dict["gradient"] = p_node.gradient
        pnode_dict["s2_value"] = p_node.s2_value
        pnode_dict["dipole"] = p_node.dipole
        pnode_dict["comment"] = p_node.comment
        pnode_dict["hess_eigenvalue_au"] = p_node.hess_eigenvalue_au

        pn_obj = PNode(**pnode_dict)
        session.add(pn_obj)


def check_map(map_obj, map):

    updated = False
    # m["id"] = mid.bytes
    print("map: ", map_obj.id)

    # m["atom_name"] = map.atom_name
    if map_obj.atom_name != map.atom_name:
        print("atom_name:")
        print(map_obj.atom_name)
        print(map.atom_name)
        map_obj.atom_name = map.atom_name
        updated = True

    # m["initxyz"] = map.initxyz
    if str(map_obj.initxyz) != str(map.initxyz):
        print("initxyz:")
        print(map_obj.initxyz)
        print(map.initxyz)
        map_obj.initxyz = map.initxyz
        updated = True

    # m["fname_top_abs"] = path
    # m["fname_top_rel"] = map.fname_top_rel
    # m["natoms"] = map.natoms
    # m["lowest_energy"] = map.lowest_energy
    # m["highest_energy"] = map.highest_energy
    # m["neq"] = map.neq
    # m["nts"] = map.nts
    # m["npt"] = map.npt
    # m["jobtime"] = map.jobtime
    # m["universal_gamma"] = map.universal_gamma
    # m["infile"] = map.infile
    # m["scpathpara"] = map.scpathpara
    # m["jobtype"] = map.jobtype
    # m["pathtype"] = map.pathtype
    # m["nobondrearrange"] = map.nobondrearrange
    # m["siml_tempearture_kelvin"] = map.siml_tempearture_kelvin
    # m["siml_pressure_atm"] = map.siml_pressure_atm
    # m["energyshiftvalue_au"] = map.energyshiftvalue_au
    # m["level"] = map.level
    # m["spinmulti"] = map.spinmulti
    # m["totalcharge"] = map.totalcharge
    # m["jobstatus"] = map.jobstatus
    # m["ngradient"] = map.ngradient
    # m["nhessian"] = map.nhessian
    # m["elapsedtime_sec"] = map.elapsedtime_sec

    return updated


def check_update(path, root_path, session):
    map = parse(path)

    path = map.fname_top_abs
    if root_path:
        path = os.path.relpath(path, root_path)

    print(path)

    filteredMap = session.query(GRRMMap).filter(GRRMMap.fname_top_abs == path).first()

    print(filteredMap)

    if not filteredMap:
        id = ulid.from_bytes(filteredMap.id)
        print("The map is not existing!!!", id.hex)
        exit(0)

    # compare maps
    updated = check_map(filteredMap, map)

    print(updated)
    if updated:
        session.commit()

    print("end.")
    exit(0)

    m = {}

    mid = ulid.new()

    m["id"] = mid.bytes
    m["atom_name"] = map.atom_name
    m["initxyz"] = map.initxyz
    m["fname_top_abs"] = path
    m["fname_top_rel"] = map.fname_top_rel
    m["natoms"] = map.natoms
    m["lowest_energy"] = map.lowest_energy
    m["highest_energy"] = map.highest_energy
    m["neq"] = map.neq
    m["nts"] = map.nts
    m["npt"] = map.npt
    m["jobtime"] = map.jobtime
    m["universal_gamma"] = map.universal_gamma
    m["infile"] = map.infile
    m["scpathpara"] = map.scpathpara
    m["jobtype"] = map.jobtype
    m["pathtype"] = map.pathtype
    m["nobondrearrange"] = map.nobondrearrange
    m["siml_tempearture_kelvin"] = map.siml_tempearture_kelvin
    m["siml_pressure_atm"] = map.siml_pressure_atm
    m["energyshiftvalue_au"] = map.energyshiftvalue_au
    m["level"] = map.level
    m["spinmulti"] = map.spinmulti
    m["totalcharge"] = map.totalcharge
    m["jobstatus"] = map.jobstatus
    m["ngradient"] = map.ngradient
    m["nhessian"] = map.nhessian
    m["elapsedtime_sec"] = map.elapsedtime_sec

    print(map.jobtime)

    map_obj = GRRMMap(**m)

    q = session.add(map_obj)

    # Process eqs
    for n in map.eq_list:
        create_eq_obj(session, n, map_obj)

    # Process pt_list
    for pt in map.pt_list:
        create_edge_obj(session, pt, map_obj)

    # Process ts_list
    for ts in map.ts_list:
        create_edge_obj(session, ts, map_obj)

    # Process dc_list
    for dc in map.dc_list:
        create_edge_obj(session, dc, map_obj)

    session.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the target log top")
    parser.add_argument("-r", "--root_path", help="path to the root folder")

    args = parser.parse_args()

    path = args.path
    root_path = args.root_path

    print("target:", path)
    print("root:", root_path)

    mysql_host = os.environ["MYSQL_HOSTS"]
    user = os.environ["MYSQL_USER"]
    password = os.environ["MYSQL_PASSWORD"]
    db_name = os.environ["MYSQL_DATABASE"]

    print(mysql_host)
    print(db_name)

    CONNECT_INFO = f"mysql+pymysql://{user}:{password}@{mysql_host}/{db_name}"
    print(CONNECT_INFO)
    engine = create_engine(CONNECT_INFO)
    # engine = create_engine(CONNECT_INFO, echo=True)

    Session = orm.sessionmaker(bind=engine)
    session = Session()

    check_update(path, root_path, session)
