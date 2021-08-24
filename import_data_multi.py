import argparse
import os
from typing import Optional

from sqlalchemy import orm
from sqlalchemy.engine import create_engine
import ulid

from grrmlog_parser.core import parse
from grrmlog_parser.utility import get_filename_list_abs_path

from grrm_data.models import Edge, GRRMMap, Eq, PNode
from import_data import import_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_path", help="path to the target_base")
    parser.add_argument("-r", "--root-path", help="path to the root folder")
    parser.add_argument("-d", "--depth", default=10, help="search depth")
    parser.add_argument("-n", "--dry_run", help="dry run", action="store_true")

    args = parser.parse_args()

    base_path = args.base_path
    root_path = args.root_path
    depth = args.depth
    dry_run = args.dry_run

    print("base:", base_path)
    print("root:", root_path)
    print("depth:", depth)
    print("dry_run:", dry_run)

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

    path_list = get_filename_list_abs_path(base_path, depth)
    # print(path_list)

    print(f"{len(path_list)} maps are found.")

    for p in path_list:
        if dry_run:
            print(p)
        else:
            import_data(p, root_path, session, dry_run)

    # import_data(path)
