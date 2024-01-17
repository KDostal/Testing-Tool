import time
from elastic_client import Client
from get_query import Query
import config

class ElasticsearchAPI:
    def __init__(self, api_query, index_type=1, is_dev=True) -> None:
        if index_type == 1:
            self.query = Query(api_query).get_task_query()
        else:
            self.query = Query(api_query).get_opportunity_offer_query()
        self.client = Client(is_dev).initialize_client()
        self.index_endpoint = config.INDEXES[index_type]

    def es_response(self, buckets=100): #buckets corresponds to number of buckets returned from DB API ie. lenght of list returned from DatabaseAPI(api_query).db_response()
        start = time.time()
        resp = self.client.search(index=self.index_endpoint, body=self.query)
        end = time.time()
        if(len(resp["aggregations"]["agg_buckets"]["buckets"])>0):
            resp = resp["aggregations"]["agg_buckets"]["buckets"]
            es_list = []

            bucket_count = len(resp) if len(resp) < buckets else buckets
            for i in range(bucket_count):
                bucket = resp[i]

                single_bucket = [x for x in bucket["key"]]
                single_bucket.append(bucket["doc_count"])

                es_list.append(single_bucket)
            
            # sort es_list buckets by partner_key - aby se list dal porovnat s db listem kdyz je vstup org_unit
            es_list.sort(key=lambda x: int(x[0]))
            print("Elasticsearch list: {l}".format(l=es_list))
            print("Elasticsearch response took {0} seconds.".format(end-start))
            return (es_list, (start, end-start))
        else:
            
            print("Elasticsearch list: []")
            print("Elasticsearch response took {0} seconds.".format(end-start))
            return ([], (start, end-start))
