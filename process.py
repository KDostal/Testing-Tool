import os
import json
import csv
from get_dict_from_es import ElasticsearchAPI
from get_dict_from_api import DatabaseAPI
from visualize import Visualizer
from check_data import CheckData

class File:
    def __init__(self, file_path, aggregation_type=1, query_index=None, visualize=False, is_dev=True):
        self.file_path = file_path
        self.query_index = query_index
        self.visualize = visualize
        self.aggregation_type = int(aggregation_type)
        self.is_dev = is_dev

    def process_query(self, query_object):
        # get main parameter and optional parameters from query object
        main_param_name = list(query_object.keys())[0]
        main_param = query_object[main_param_name]
        optional_params = {k: v for k, v in query_object.items() if k != main_param_name}
        visualList = []

        for param in main_param:
            # create API query from main and optional parameters
            api_query = {main_param_name: param}
            api_query.update(optional_params)

            print("=======")
            # receive data from the database and Elasticsearch
            db_res = DatabaseAPI(api_query, self.aggregation_type, self.is_dev).db_response()
            es_res = ElasticsearchAPI(api_query, self.aggregation_type, self.is_dev).es_response(len(db_res[0]))

            # compare responses and create a dictionary for visualization
            checker = CheckData(db_res[0], es_res[0])
            visualDict = {}
            visualDict["date"] = db_res[1][0]
            visualDict["dbTime"] = db_res[1][1]
            visualDict["esTime"] = es_res[1][1]
            visualDict["aggType"] = self.aggregation_type
            visualDict["optionalParams"] = len(optional_params)
            visualDict.update(checker.compare_responses())
            visualList.append(visualDict)
        return visualList

    def process_json_objects(self):
        with open(self.file_path, "r") as json_file:
            data = json.load(json_file)

        visualList = []

        try:
            if self.query_index is None:
                for query_object in data:
                    visualList.extend(self.process_query(query_object))
            elif self.query_index.isdigit():
                for i, query_object in enumerate(data):
                    if i == int(self.query_index):
                        visualList.extend(self.process_query(query_object))
            elif '-' in self.query_index:
                start, end = map(int, self.query_index.split('-'))
                for i, query_object in enumerate(data):
                    if start <= i <= end:
                        visualList.extend(self.process_query(query_object))
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        finally:
            self.write_to_csv(visualList)

        # visualize data
        if(self.visualize):
            v = Visualizer(visualList)
            v.visualize()

    def write_to_csv(self, data, folder_name = 'logs', file_name = 'log.csv'):
        path = os.path.join(folder_name, file_name)
        if os.path.isfile(path):
            i = 1
            while os.path.isfile(os.path.join(folder_name, f'log_{i}.csv')):
                i += 1
            file_name = f'log_{i}.csv'

        fieldnames = list(data[0].keys())
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        path = os.path.join(folder_name, file_name)
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)