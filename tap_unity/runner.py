import os
import json
import statistics
import singer
import csv
import io

from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

from tap_unity.utils import get_abs_path
from tap_unity.client import UnityClient


LOGGER = singer.get_logger()

# timestamp
# target id
# target store id
# target name
# creative pack id
# creative pack name
# campaign id
# campaign name
# country
# starts
# views
# clicks
# installs
# spend
# cvr
# ctr
# ecpm
# cpi

statistics_schema = {
  "type": "SCHEMA",
  "stream": "statistics",
  "schema": {
    "properties": {
      "starts": {
        "type": "integer"
      },
      "timestamp": {
        "type": ['null', "string"],
        "format": "date-time"
      },
      "campaign_id": {
        "type": ['null', "string"]
      },
      "campaign_name": {
        "type": ['null', "string"]
      }
    }
  },
  "key_properties": [
    "campaign_id"
  ],
  "bookmark_properties": ["timestamp"]
}

class TapUnityRunner:

    def __init__(self, config):
        self.config = config
        self.unity_client = UnityClient(config)


    def __parse_csv_body(self):
        response_data_csv = self.unity_client.make_request()
        reader = csv.DictReader(io.StringIO(response_data_csv))
        return json.loads(list(reader))


    def load_schemas(self):
        """ Load schemas from schemas folder """
        schemas = {}
        for filename in os.listdir(get_abs_path('schemas')):
            path = get_abs_path('schemas') + '/' + filename
            file_raw = filename.replace('.json', '')
            with open(path) as file:
                schemas[file_raw] = Schema.from_dict(json.load(file))
        return schemas


    def discover(self):
        raw_schemas = self.load_schemas()
        streams = []
        for stream_id, schema in raw_schemas.items():
            # TODO: populate any metadata and stream's key properties here..
            stream_metadata = []
            key_properties = []
            streams.append(
                CatalogEntry(
                    tap_stream_id=stream_id,
                    stream=stream_id,
                    schema=schema,
                    key_properties=key_properties,
                    metadata=stream_metadata,
                    replication_key=None,
                    is_view=None,
                    database=None,
                    table=None,
                    row_count=None,
                    stream_alias=None,
                    replication_method=None,
                )
            )
        return Catalog(streams)


    @staticmethod
    def sync_stream(stream):
        """
        Sync a single stream
        """
        try:
            stream.sync()
        except OSError as e:
            LOGGER.error(str(e))
            exit(e.errno)

        except Exception as e:
            LOGGER.error(str(e))
            LOGGER.error('Failed to sync endpoint {}, moving on!'
                         .format(stream.STREAM_NAME))
            raise e

    def old_do_sync(self):
        """
        Sync all streams
        :return:
        """
        LOGGER.info("Starting sync.")

        # We need the list of product ids for the rankings report
        # so sync the products first
        product_ids = []
        for stream in self.streams:
            if stream.STREAM_NAME == 'products':
                self.sync_stream(stream)
                product_ids = stream.product_ids

        # Sync all but the products
        for stream in self.streams:
            if stream.STREAM_NAME == 'products':
                continue

            self.sync_stream(stream)
            stream.product_ids = product_ids


    def do_sync(self, state, catalog: Catalog):
        """ Sync data from tap source """
        # Loop over selected streams in catalog
        
        for stream in catalog.get_selected_streams(state):
            LOGGER.info("Syncing stream:" + stream.tap_stream_id)

            bookmark_column = stream.replication_key
            is_sorted = True  # TODO: indicate whether data is sorted ascending on bookmark value

            # singer.write_schema(
            #     stream_name=stream.tap_stream_id,
            #     schema=stream.schema,
            #     key_properties=stream.key_properties,
            # )

            singer.write_schema(
                stream_name="statistics",
                schema=statistics_schema,
                key_properties="timestamp",
            )

            # TODO: Olhar macetão do dia no appsfigures

            # TODO: delete and replace this inline function with your own data retrieval process:
            response_data = self.__parse_csv_body()
            
            print(response_data)

            max_bookmark = None
            for row in response_data:
                # TODO: place type conversions or transformations here

                # write one or more rows to the stream:
                # singer.write_records(stream.tap_stream_id, [row])
                singer.write_records("staticsts", [row])
                if bookmark_column:
                    if is_sorted:
                        # update bookmark to latest value
                        singer.write_state({stream.tap_stream_id: row})
                    else:
                        # if data unsorted, save max value until end of writes
                        max_bookmark = max(max_bookmark, row)
            if bookmark_column and not is_sorted:
                singer.write_state({stream.tap_stream_id: max_bookmark})
        return
