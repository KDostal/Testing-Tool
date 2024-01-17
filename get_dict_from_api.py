import requests
import time
from urllib3.exceptions import InsecureRequestWarning, SecurityWarning
from requests.auth import HTTPBasicAuth
import config

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) # disable because of ssl warning

class DatabaseAPI:
    def __init__(self, api_query, aggregation_type=1, is_dev=True) -> None:
        aggregation_type = aggregation_type+3 if not is_dev else aggregation_type # chose url with systest/test depending if we want to connect to dev
        self.api_url = config.API_URLS[aggregation_type]
        self.basic = HTTPBasicAuth(config.API_USER, config.API_PW)
        self.to_post = api_query

    def process_response(self, response):
        # response format: 
        # Index 1,3: [{@class, partnerKey, objectCount, organizationUnitKey, individualFirstName, individualSurname}]
        # Index 2: [{@class, partnerKey, objectCount, organizationUnitKey, individualFirstName, individualSurname, dailyStatistics}]
        db_list = []
        for x in response:
            try:
                single_bucket = list(x.values())
                single_bucket.pop(0)
                single_bucket.append(single_bucket.pop(1)) # move 'objectCount' to the back of the list so it matches with Elasticsearch list order

                # in index 2 remove 'dailyStatistics'
                if len(single_bucket) == 6:
                    single_bucket.pop(-2)

                db_list.append(single_bucket)
            except:
                print("Error: x is not a dictionary, but a string: {s}".format(s=x))
                continue
        db_list.sort(key=lambda x: int(x[0])) # sort by partner key so responses (also sorted) from Elastisearch can be compared
        return db_list

    def db_response(self):
        calltime = time.strftime("%d/%m/%Y, %H:%M:%S")
        start = time.time()
        response = requests.post(self.api_url, json=self.to_post, verify=False, auth=self.basic)
        end = time.time()
        db_list = self.process_response(response.json())

        print("Database list: {l}".format(l=db_list))
        print("Database response took {0} seconds.".format(end-start))
        return (db_list, (calltime, end-start))