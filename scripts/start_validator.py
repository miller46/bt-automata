import argparse
import time
import subprocess
import bt_automata
from bt_automata.utils import get_version

default_chain_endpoint = "wss://bittensor-finney.api.onfinality.io/public-ws"

def update_and_restart(pm2_name, wallet_name, wallet_hotkey, address):
    while True:
        current_version = bt_automata.__version__
        latest_version = get_version()
        print(f"Current version: {current_version}")
        print(f"Latest version: {latest_version}")

        if current_version != latest_version:
            print("Updating to the latest version...")
            subprocess.run(["pm2", "delete", pm2_name])
            subprocess.run(["git", "pull"])
            subprocess.run(["pip", "install", "-e", "."])
            subprocess.run(["pm2", "start", "validators/validator.py", "--interpreter", "python3", "--name", pm2_name, "--", "--wallet.name", wallet_name, "--wallet.hotkey", wallet_hotkey, "--netuid", "18", "--subtensor.network", "local", "--subtensor.chain_endpoint", address])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automatically update and restart the validator process when a new version is released.",
        epilog="Example usage: python start_validator.py --pm2_name 'ca-validator' --wallet_name 'wallet1' --wallet_hotkey 'key123' [--address 'wss://...']"
    )

    parser.add_argument("--pm2_name", required=True, help="Name of the PM2 process.")
    parser.add_argument("--wallet_name", required=True, help="Name of the wallet.")
    parser.add_argument("--wallet_hotkey", required=True, help="Hotkey for the wallet.")
    parser.add_argument("--address", default=default_chain_endpoint, help="Subtensor chain_endpoint, defaults to 'wss://bittensor-finney.api.onfinality.io/public-ws' if not provided.")

    args = parser.parse_args()

    try:
        update_and_restart(args.pm2_name, args.wallet_name, args.wallet_hotkey, args.address)
        time.sleep(900) # sleep for 15 mins
    except Exception as e:
        parser.error(f"An error occurred: {e}")