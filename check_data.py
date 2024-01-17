import itertools

class CheckData:
    def __init__(self, db_list, es_list):
        self.db_list = db_list
        self.es_list = es_list
        self.diffDict = {
            "diffIndex": [],
          "diffDbValue": [],
          "diffEsValue": [],
          "elements": len(list(itertools.chain.from_iterable(self.db_list))),
          "mistakes": 0      
        }

    def compare_responses(self, db_list=None, es_list=None):
        if db_list is None and es_list is None:
            db_list = self.db_list
            es_list = self.es_list

        if len(db_list) != len(es_list):
            print("Different length responses")
            self.diffDict["mistakes"] = -1
            return self.diffDict

        for i in range(len(db_list)):
            if isinstance(db_list[i], list) and isinstance(es_list[i], list):
                self.compare_responses(db_list[i], es_list[i])
            elif str(db_list[i]) != str(es_list[i]):
                print(f"The responses have different values at index {i}: {db_list[i]} and {es_list[i]}")
                self.diffDict["diffIndex"].append(i)
                self.diffDict["diffDbValue"].append(db_list[i])
                self.diffDict["diffEsValue"].append(es_list[i])
                self.diffDict["mistakes"] += 1
        return self.diffDict