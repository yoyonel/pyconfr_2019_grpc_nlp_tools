import codecs
import functools
import json
import os
from dataclasses import dataclass
from typing import Optional

import grpc
import mongomock
import pytest
from bson import json_util


@dataclass
class ServersCache:
    # Code highly inspired from pytest-mongodb
    # https://github.com/mdomke/pytest-mongodb/blob/develop/pytest_mongodb/plugin.py
    cache: Optional[dict] = None
    server_instance: Optional[grpc.Server] = None
    grpc_host_and_port: Optional[str] = None


@pytest.fixture(autouse=True, scope="session")
def servers_cache() -> ServersCache:
    return ServersCache()


@pytest.fixture(scope='function')
def mongodb(pytestconfig, servers_cache):
    def make_mongo_client():
        return mongomock.MongoClient()

    @dataclass
    class MongoWrapper:
        def get_db(self, fixture_name: str = None, db_name: str = 'pyconfr_2019_grpc_nlp'):
            client = make_mongo_client()
            db = client[db_name]
            self.clean_database(db)
            if fixture_name is not None:
                self.load_fixtures(db, fixture_name)
            return db

        @staticmethod
        def load_fixtures(db: mongomock.Database, fixture_name: str):
            basedir = (pytestconfig.getoption('mongodb_fixture_dir')
                       or pytestconfig.getini('mongodb_fixture_dir'))
            fixture_path = os.path.join(pytestconfig.rootdir, basedir,
                                        '{}.json'.format(fixture_name))

            if not os.path.exists(fixture_path):
                raise FileNotFoundError(fixture_path)

            loader = functools.partial(json.load,
                                       object_hook=json_util.object_hook)
            try:
                collections = servers_cache.cache[fixture_path]
            except KeyError:
                with codecs.open(fixture_path, encoding='utf-8') as fp:
                    servers_cache.cache[fixture_path] = collections = loader(fp)

            for collection, docs in collections.items():
                mongo_collection = db[collection]  # type: mongomock.Collection
                mongo_collection.insert_many(docs)

        @staticmethod
        def clean_database(db):
            for name in db.collection_names(include_system_collections=False):
                db.drop_collection(name)

    return MongoWrapper()
