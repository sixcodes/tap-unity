#!/usr/bin/env python3
import singer
from singer import utils as singer_utils
from tap_unity.runner import TapUnityRunner


REQUIRED_CONFIG_KEYS = ["auth_token", "organization_id"]
LOGGER = singer.get_logger()



def main():
    args = singer_utils.parse_args(REQUIRED_CONFIG_KEYS)
    config = args.config

    runner = TapUnityRunner(config)
    runner.sync()


##############################  version 1 ##############################
# @singer_utils.handle_top_exception(LOGGER)
# def main():
#     # Parse command line arguments
#     args = singer_utils.parse_args(REQUIRED_CONFIG_KEYS)

#     runner = TapUnityRunner(args.config)

#     # If discover flag was passed, run discovery mode and dump output to stdout
#     if args.discover:
#         catalog = runner.discover()
#         catalog.dump()
#     # Otherwise run in sync mode
#     else:
#         if args.catalog:
#             catalog = args.catalog
#         else:
#             catalog = runner.discover()
#         runner.do_sync(args.state, catalog)

################################ version 2 #####################################
# @singer_utils.handle_top_exception(LOGGER)
# def main():
#     # Parse command line arguments
#     args = singer_utils.parse_args(REQUIRED_CONFIG_KEYS)

#     runner = TapUnityRunner(args.config)

#     # If discover flag was passed, run discovery mode and dump output to stdout
    
#     catalog = runner.discover()
#     print("CHEGOU AQUI 1")
#     # print(args.state)
#     # print(ct.__dict__  for ct in catalog.__dict__["streams"])
#     runner.do_sync(args.state, catalog)
#     print("CHEGOU AQUI 2")


if __name__ == "__main__":
    main()
