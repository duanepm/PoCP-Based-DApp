# PoCP-Based DApp – Sustainable Consensus for Energy-Efficient Blockchain Networks

&#x20;

## 📌 Project Overview

This project introduces a novel consensus mechanism: **Proof of Computational Power (PoCP)** — an energy-efficient, fair, and decentralized alternative to traditional blockchain consensus models like Proof of Work (PoW) and Proof of Stake (PoS).

PoCP selects validators based on real-time computational performance rather than financial stake or brute-force mining. It integrates:

* A lightweight performance benchmarking mechanism.
* Weighted probabilistic validator selection.
* Smart contract-based transparency and automation.

Built as a **full-stack decentralized application (DApp)** using:

* 🐍 Flask (Backend)
* 💾 SQLite (Database)
* 🧾 Solidity (Smart Contract)
* 🌐 HTML/CSS/JS (Frontend)

---

## 🎯 Objectives

* ✅ Reduce energy consumption of block validation.
* 🔐 Maintain transparency and decentralization.
* ⚖️ Ensure fair validator selection based on real-time performance.
* 📈 Provide an intuitive and interactive DApp interface.
* 🏅 Implement reward and leaderboard tracking mechanisms.

---

## 📁 Project Structure

```
├── backend
│   ├── app.py                    # Flask backend + API logic
│   ├── compile_contract.py       # Contract compilation using solcx
│   ├── contract
│   │   └── PoCP.sol              # Solidity smart contract
│   ├── contract_data.json        # ABI & bytecode
│   └── miners.db                 # SQLite database
│
├── frontend
│   ├── static
│   │   ├── app.js                # Frontend interactivity
│   │   ├── background.jpg        # Background image
│   │   └── style.css             # Custom styles
│   └── templates
│       └── index.html            # Main HTML interface
│
└── pocp.db                       # Main runtime DB (auto-generated)
```

---

## 🧠 PoCP Consensus Algorithm

### 🔧 CP Calculation:

$\text{CP}_i = \frac{1}{T_i} \times e^{-k \cdot \sigma_i}$
Where:

* $T_i$: Time taken by miner $i$
* $\sigma_i$: Standard deviation across submissions (to penalize inconsistency)

### 🎯 Validator Selection (Probabilistic):

**P(i)** = CPᵢ / Σ(CPⱼ) for j = 1 to n
* One validator is chosen using weighted random selection.

### 🏅 Reward Logic:

* Validator: +50 tokens
* Participants: +10 tokens

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* Node.js & Hardhat
* MetaMask (optional)

### Install Dependencies

```bash
pip install flask web3 py-solc-x
npm install --save hardhat
```

### Compile Smart Contract

```bash
python backend/compile_contract.py
```

### Run Hardhat Local Node

```bash
npx hardhat node
```

### Start Flask Server

```bash
python backend/app.py
```

### Access the DApp

Navigate to: `http://127.0.0.1:5000`

---

## 🖥️ DApp Interface Features

* ✅ Miner Registration (Hardhat accounts)
* 🛠️ Benchmarking with a visual timer
* 🎲 Probabilistic Validator Selection
* 📊 Leaderboard with CP ranking
* 💰 Rewards Table updated live

---

## 🔒 Smart Contract Functions

| Function                           | Description                              |
| ---------------------------------- | ---------------------------------------- |
| `registerMiner(address)`           | Registers a miner                        |
| `submitCP(address, cp)`            | Submits a miner's CP                     |
| `selectValidator()`                | Randomly selects a validator             |
| `getReward(address)`               | Gets total reward of a miner             |
| `resetAllCP()`                     | Resets CPs and validator state           |
| `incrementReward(address, amount)` | Manually increase reward (used by Flask) |

---

## 📈 Sample Simulation Results

* **Fairness:** Validators selected based on CP distribution.
* **Inclusion:** All miners rewarded for participation.
* **Consistency:** Penalization incentivizes stable miners.

| Round | Validator   | CP   | Reward |
| ----- | ----------- | ---- | ------ |
| 1     | 0xABC...123 | 20.5 | +50    |
| 2     | 0xDEF...456 | 18.9 | +50    |

---

## 📌 Limitations & Future Enhancements

### ❌ Current Limitations

* CP submission depends on frontend timer (subject to spoofing).

### ✅ Proposed Enhancements

* Backend CP verification
* Game-theoretic reward tuning
* ML for dynamic difficulty prediction
* Deployment to a live testnet (e.g. Goerli)
* Slashing for malicious nodes

---

## 📚 References

* Nakamoto, S. (2008). [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
* A, I., Chembakassery, D. (2024). [Proof of Computational Power: An Innovative Consensus Algorithm for Blockchain Systems](https://doi.org/10.1007/978-981-97-3442-9_29)

---

## 🙌 Acknowledgements

Special thanks to all open-source contributors and blockchain researchers who laid the foundation for consensus innovation.

---

> "Replacing brute-force with brains – PoCP is a step toward smarter, greener blockchains." 🌱
