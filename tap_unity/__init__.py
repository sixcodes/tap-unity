#!/usr/bin/env python3
import singer
from singer import utils as singer_utils
from tap_unity.runner import TapUnityRunner


REQUIRED_CONFIG_KEYS = ["auth_token", "organization_id", "split_by", "fields"]
LOGGER = singer.get_logger()


@singer_utils.handle_top_exception(LOGGER)
def main():
    args = singer_utils.parse_args(REQUIRED_CONFIG_KEYS)
    config = args.config

    runner = TapUnityRunner(config)
    runner.sync()


if __name__ == "__main__":
    main()
