from solcx import compile_standard, install_solc
import json
import os

install_solc("0.8.0")

with open("backend/contract/PoCP.sol", "r") as file:
    source_code = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"PoCP.sol": {"content": source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("backend/contract_data.json", "w") as file:
    json.dump(compiled_sol, file)
