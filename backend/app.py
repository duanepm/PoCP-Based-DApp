from flask import Flask, render_template, request, jsonify
from web3 import Web3
import json
import sqlite3
import os

if os.path.exists("pocp.db"):
    os.remove("pocp.db")

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.default_account = w3.eth.accounts[0]

with open("backend/contract_data.json") as f:
    contract_json = json.load(f)
    abi = contract_json["contracts"]["PoCP.sol"]["PoCP"]["abi"]
    bytecode = contract_json["contracts"]["PoCP.sol"]["PoCP"]["evm"]["bytecode"]["object"]

PoCP = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = PoCP.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_instance = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

conn = sqlite3.connect("pocp.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS miners (
        address TEXT PRIMARY KEY
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cp_data (
        address TEXT,
        time REAL,
        cp REAL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS rewards (
        address TEXT PRIMARY KEY,
        reward INTEGER DEFAULT 0
    )
""")
conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    address = request.json["address"]
    try:
        tx = contract_instance.functions.registerMiner(address).transact()
        w3.eth.wait_for_transaction_receipt(tx)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    cursor.execute("INSERT OR IGNORE INTO miners (address) VALUES (?)", (address,))
    cursor.execute("INSERT OR IGNORE INTO rewards (address) VALUES (?)", (address,))
    conn.commit()
    return jsonify({"status": "Miner registered."})

@app.route("/submit_time", methods=["POST"])
def submit_time():
    data = request.json
    address = data["address"]
    time_taken = float(data["time"])
    raw_cp = 1 / time_taken if time_taken > 0 else 0

    cursor.execute("SELECT cp FROM cp_data WHERE address = ?", (address,))
    cps = [row[0] for row in cursor.fetchall()]

    if cps:
        avg_cp = sum(cps) / len(cps)
        variance = sum((cp - avg_cp) ** 2 for cp in cps) / len(cps)
        std_dev = variance ** 0.5
        penalty = 0.5 * std_dev
        adjusted_cp = max(raw_cp - penalty, 0)
    else:
        adjusted_cp = raw_cp

    try:
        tx = contract_instance.functions.submitCP(address, int(adjusted_cp * 1000)).transact()
        w3.eth.wait_for_transaction_receipt(tx)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    cursor.execute("INSERT INTO cp_data (address, time, cp) VALUES (?, ?, ?)", (address, time_taken, adjusted_cp))

    cursor.execute("UPDATE rewards SET reward = reward + 10 WHERE address = ?", (address,))
    conn.commit()

    return jsonify({"status": "Time and adjusted CP submitted."})

@app.route("/select_validator", methods=["GET"])
def select_validator():
    try:
        validator = contract_instance.functions.selectValidator().call()
        if validator:
            cursor.execute("UPDATE rewards SET reward = reward + 50 WHERE address = ?", (validator,))
            conn.commit()
        return jsonify({"validator": validator})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/miners", methods=["GET"])
def get_miners():
    cursor.execute("SELECT address FROM miners")
    miners = [row[0] for row in cursor.fetchall()]
    return jsonify({"miners": miners})

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    cursor.execute("SELECT address, time, cp FROM cp_data ORDER BY cp DESC")
    entries = [{"miner": row[0], "time": row[1], "cp": row[2]} for row in cursor.fetchall()]
    return jsonify({"entries": entries})

@app.route("/reset_round", methods=["POST"])
def reset_round():
    try:
        tx = contract_instance.functions.resetAllCP().transact()
        w3.eth.wait_for_transaction_receipt(tx)

        cursor.execute("DELETE FROM cp_data")
        conn.commit()

        return jsonify({"status": "CP and leaderboard reset."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/get_reward", methods=["GET"])
def get_rewards():
    cursor.execute("SELECT address, reward FROM rewards")
    rewards = [{"address": row[0], "reward": row[1]} for row in cursor.fetchall()]
    return jsonify({"rewards": rewards})

@app.route('/hardhat_addresses', methods=['GET'])
def get_hardhat_addresses():
    try:
        accounts = w3.eth.accounts
        return jsonify({'addresses': accounts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
