// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PoCP {
    struct Miner {
        address addr;
        uint256 cp;
    }

    mapping(address => uint256) public minerCP;
    address[] public miners;
    mapping(address => bool) public isRegistered;

    // Rewards mapping
    mapping(address => uint256) public minerRewards;

    // Track if validator was selected this round
    address public lastValidator;
    bool public validatorSelected;

    // Events
    event MinerRegistered(address miner);
    event CPSubmitted(address miner, uint256 cp);
    event AllCPReset();
    event RewardDistributed(address validator, uint256 reward);
    event ManualRewardIncremented(address miner, uint256 amount);

    // Register a new miner
    function registerMiner(address _addr) public {
        if (!isRegistered[_addr]) {
            miners.push(_addr);
            isRegistered[_addr] = true;
            minerCP[_addr] = 1; // Default CP to ensure participation
            emit MinerRegistered(_addr);
        }
    }

    // Submit CP
    function submitCP(address _addr, uint256 _cp) public {
        require(isRegistered[_addr], "Miner not registered.");
        minerCP[_addr] = _cp;
        emit CPSubmitted(_addr, _cp);
    }

    // Get list of all miners
    function getMiners() public view returns (address[] memory) {
        return miners;
    }

    // Get CP of a miner
    function getCP(address _addr) public view returns (uint256) {
        return minerCP[_addr];
    }

    // Select validator based on weighted CP probability and reward them once per round
    function selectValidator() public returns (address) {
        require(!validatorSelected, "Validator already selected this round.");

        uint256 totalCP = 0;
        for (uint i = 0; i < miners.length; i++) {
            totalCP += minerCP[miners[i]];
        }

        if (totalCP == 0) return address(0);

        uint256 rand = uint256(keccak256(abi.encodePacked(block.timestamp, block.difficulty))) % totalCP;
        uint256 cumulative = 0;

        for (uint i = 0; i < miners.length; i++) {
            cumulative += minerCP[miners[i]];
            if (rand < cumulative) {
                address selected = miners[i];
                minerRewards[selected] += 10; // Fixed reward
                lastValidator = selected;
                validatorSelected = true;
                emit RewardDistributed(selected, 10);
                return selected;
            }
        }

        return address(0);
    }

    // View reward of a specific miner
    function getReward(address _addr) public view returns (uint256) {
        return minerRewards[_addr];
    }

    // Reset all CPs and validator state
    function resetAllCP() public {
        for (uint i = 0; i < miners.length; i++) {
            minerCP[miners[i]] = 0;
        }
        validatorSelected = false;
        lastValidator = address(0);
        emit AllCPReset();
    }

    // Manually increment reward (used in Flask mining step)
    function incrementReward(address _addr, uint256 amount) public {
        require(isRegistered[_addr], "Miner not registered.");
        minerRewards[_addr] += amount;
        emit ManualRewardIncremented(_addr, amount);
    }
}
