from gevent import monkey
monkey.patch_all()
import urllib3
import argparse
from process import File

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='path to the JSON file') # mandatory path to file with data to call
    parser.add_argument('-a', '--agg', default=1,
                        help='type of aggregation to call. chose from 1,2 or 3') # one of three possible services to call
    parser.add_argument('-i', '--index', default=None,
                        help='index of the query to process (e.g. 0 or 1-3)') # index of rows from data file to call, use when you want to test only subset of data from file
    parser.add_argument('--visualize', action='store_true', default=False) # if true at the end of script pyplot visualization of response times and not matching calls will also be shown
    parser.add_argument('--test', action='store_false', default=True) # if call should be made on Test or Development environments of Oracle and ElasticSearch
    args = parser.parse_args()

    f = File(args.file_path, int(args.agg), args.index, args.visualize, args.test)
    f.process_json_objects()