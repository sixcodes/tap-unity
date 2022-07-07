#!/usr/bin/env python3
import singer
from singer import utils as singer_utils
from tap_unity.runner import TapUnityRunner


REQUIRED_CONFIG_KEYS = ["auth_token", "organization_id"]
LOGGER = singer.get_logger()


@singer_utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = singer_utils.parse_args(REQUIRED_CONFIG_KEYS)

    runner = TapUnityRunner(args.config)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = runner.discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = runner.discover()
        runner.do_sync(args.state, catalog)


if __name__ == "__main__":
    main()
