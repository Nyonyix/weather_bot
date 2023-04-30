import sys
import discord
import datetime
from dotenv import load_dotenv
from warning import Warning

def main() -> None:

    curr_warning = Warning("2023041500.SVR")

    print(f"Type: {curr_warning.type}")
    print(f"Hazard: {curr_warning.hazard}")
    print(f"Source: {curr_warning.source}")
    print(f"Time Issued: {curr_warning.time_issued}")
    print(f"Time Expire: {curr_warning.time_expire}")
    for county in curr_warning.counties:
        print(f"Warning Active for: {county}")

if __name__ == "__main__":
    main()