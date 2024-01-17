class Query:
    def __init__(self, api_query):
        self.api_query = api_query

    def get_task_string(self):
        json_to_es = {
        "partnerKeys": "PARTNER_KEY",
        "organizationUnitKeys": "ORG_UNIT_KEY",
        "taskCodes": "TP_CODE_ID",
        "taskCreatedByRpaFlag": "TASK_CRE_BY_RPA_FLAG",
        "taskProcessedFlag": "PROC_FLAG",
        "taskCreateDateFrom": ("CRE_DATE", "from"),
        "taskCreateDateTo": ("CRE_DATE", "to"),
        "taskClosureDateFrom": ("CLOS_DATE", "from"),
        "taskClosureDateTo": ("CLOS_DATE", "to"),
        "taskLastUpdateDateFrom": ("LAST_UPD_DATE", "from"),
        "taskStartDateFrom": ("START_DATE", "from"),
        "taskStartDateTo": ("START_DATE", "to"),
        "taskEndDateFrom": ("END_DATE", "from"),
        "taskEndDateTo": ("END_DATE", "to")
        }

        query_string = ""
        for key, value in self.api_query.items():
            if key in json_to_es:
                es_key = json_to_es[key]
                if isinstance(value, list): # partnerKeys, organizationUnitKeys, taskCodes
                    if key == "taskCodes":
                        codes = [d.get("entryId") for d in value]
                        query_string += f"({es_key}:{' OR '.join(str(v) for v in codes)}) AND "
                    else:
                        query_string += f"({es_key}:{' OR '.join(str(v) for v in value)}) AND "
                elif isinstance(value, bool):
                    query_string += f"({es_key}:{int(value)}) AND "
                elif isinstance(value, str):
                    value = value.split('T')[0] # split on time part
                    if isinstance(es_key, tuple): # handle date range values
                        es_key, direction = es_key
                        if direction == "from":
                            query_string += f"({es_key}:[{value} TO *]) AND "
                        elif direction == "to":
                            query_string += f"({es_key}:[* TO {value}]) AND "
                    else:
                        query_string += f"({es_key}:[{value} TO *]) AND "
        query_string = query_string[:-5]
        return query_string
    
    def get_task_query(self):
        query_string = self.get_task_string()

        query={
        "_source": "false",
            "aggs": {
                "agg_buckets": {
                "multi_terms": {
                "terms": [
                {
                    "field": "PARTNER_REL_DETAIL.PARTNER_KEY"
                },
                {
                    "field": "PARTNER_REL_DETAIL.ORG_UNIT_KEY"
                },
                {
                    "field": "PARTNER_REL_DETAIL.FIRST_NAME"
                },
                {
                    "field": "PARTNER_REL_DETAIL.LAST_NAME"
                }
                ]
                }
                }
            },
        "query": {
            "query_string": {
            "query": "x"
            }
        }
        }

        query["query"]["query_string"]["query"]=query_string
        #print("Elasticsearch Query: {q}".format(q=query))
        return query

    def get_opportunity_offer_string(self):
        json_to_es = {
        "partnerKeys": "PARTNER_KEY",
        "organizationUnitKeys": "ORG_UNIT_KEY",
        "opportunityStatus": "TP_OPRTY_STAT_ID",
        "opportunityProcessedFlag": "PROC_FLAG",
        "opportunityHasScheduledCallFlag": "SCHD_CALL_FLAG", # opportunityScheduledCallPlanedFlag MOZNA ZMENIT
        "opportunityLastCallStatusDetailFlag": "LAST_CALL_STAT_FLAG",
        "opportunityValidFromStart": ("START_DATE", "from"),
        "opportunityValidFromEnd": ("START_DATE", "to"),
        "opportunityValidToStart": ("END_DATE", "from"),
        "opportunityValidToEnd": ("END_DATE", "to"), # opportunityValidToEndOld WTF??
        "opportunityCalculateValidToStart": ("CALC_END_DATE", "from"),
        "opportunityCalculateValidToEnd": ("CALC_END_DATE", "to"),
        "opportunityScheduledCallFrom": ("SCHD_CALL_START_DATE", "from"),
        "opportunityScheduledCallTo": ("SCHD_CALL_START_DATE", "to"),
        "opportunityCreateDateFrom": ("CRE_DATE", "from"),
        "opportunityCreateDateTo": ("CRE_DATE", "to"),
        "opportunityLastCallDateTimeFrom": "LAST_CALL_DATE",
        "opportunityCodes": "TP_CODE_ID",
        "entityIdentificationSystem": "ENT_ID_TP_SYS_ID",
        "offerStatus": "TP_OFR_STAT_ID",
        "offerProcessedFlag": "PROC_FLAG", # nastavovat na 0 nebo dojde k zacyklení
        "offerValidFromStart": ("START_DATE", "from"),
        "offerValidFromEnd": ("START_DATE", "to"),
        "offerValidToStart": ("END_DATE", "from"),
        "offerValidToEnd": ("END_DATE", "to"),
        "offerCodes": "TP_CODE_ID"
        }

        query_string = ""
        for key, value in self.api_query.items():
            if key in json_to_es:
                es_key = json_to_es[key]
                if isinstance(value, list): # partnerKeys, organizationUnitKeys, opportunityCodes and offerCodes contain list of values
                    if key in ["opportunityCodes", "offerCodes"]:
                        codes = [d.get("entryId") for d in value]
                        query_string += f"({es_key}:{' OR '.join(str(v) for v in codes)}) AND "
                    else:
                        query_string += f"({es_key}:{' OR '.join(str(v) for v in value)}) AND "
                elif key in ["opportunityStatus", "entityIdentificationSystem", "offerStatus"]:
                    entry = value.get("entryId")
                    query_string += f"({es_key}:{str(entry)}) AND "
                elif isinstance(value, bool):
                    query_string += f"({es_key}:{int(value)}) AND "
                elif isinstance(value, str):
                    value = value.split('T')[0] # split on time part
                    if isinstance(es_key, tuple): # handle date range values
                        es_key, direction = es_key
                        if direction == "from":
                            query_string += f"({es_key}:[{value} TO *]) AND "
                        elif direction == "to":
                            query_string += f"({es_key}:[* TO {value}]) AND "
                    else:
                        query_string += f"({es_key}:[{value} TO *]) AND "
        query_string = query_string[:-5]
        return query_string
    
    def get_opportunity_offer_query(self):
        query_string = self.get_opportunity_offer_string()

        query={
        "_source": "false",
        "size": 0,
            "aggs": {
                "agg_buckets": {
                "multi_terms": {
                "size": 9999,
                "terms": [
                            {
                                "field": "PARTNER_KEY.keyword"
                            },
                            {
                                "field": "ORG_UNIT_KEY.keyword"
                            },
                            {
                                "field": "FIRST_NAME.keyword"
                            },
                            {
                                "field": "LAST_NAME.keyword"
                            }
                          ]
                                }
                                  }
                    },
        "query": {
            "query_string": {
            "query": "x"
            }
        }
}
        #print("QUERY S: {q}".format(q=query_string))
        query["query"]["query_string"]["query"]=query_string
        return query