import sys
import discord
import datetime
from dotenv import load_dotenv
from warning import Warning

def main() -> None:

    curr_warning = Warning("tor_warn.TOR")

    print(curr_warning.hazard)

if __name__ == "__main__":
    main()