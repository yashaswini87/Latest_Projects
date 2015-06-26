from cassandra.cluster import Cluster
from cassandra.query import dict_factory

servers = {"PROD": "kaos-cass00.sv.walmartlabs.com"}
keyspaces = {'genome': "ProductGenomeProd"}

class ProductGenome(object):
    def __init__(self, server_url, keyspace='ProductGenomeProd',port=9042,timeout=30):
        nodes = [server_url]
        cluster = Cluster(nodes, port=port, protocol_version=1, compression=True)
        self.session = cluster.connect(keyspace)
        self.session.row_factory = dict_factory
        self.session.default_timeout = timeout


    def get_variant_wpids(self, item_id):
        row_key = 'DCITEM' + '-' + item_id
        prepared_stmt = self.session.prepare ('SELECT * FROM "SRC_OFFER" WHERE (key = ?)')
        bound_stmt = prepared_stmt.bind([row_key])
        rows = self.session.execute(bound_stmt)
        wpids = {row.get('WUPCID') for row in rows}
        return wpids



    def close(self):
        self.session.shutdown()


if __name__ == '__main__':
    pg = ProductGenome(server_url=servers.get("PROD"))
    print pg.get_variant_wpids("4408441")