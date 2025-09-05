import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RTP Audio Stream Muxer")
    parser.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="List of input RTP stream addresses in the format [ip_addr]:[port]"
    )
    args = parser.parse_args()

    print("Input streams:", args.inputs)