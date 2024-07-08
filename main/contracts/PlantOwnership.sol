
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PlantOwnership {
    struct Plant {
        address owner;
        uint plantId;
        string plantName;
        
    }

    struct Hybrid {
        address owner;
        uint hybridId;
        string hybridName;
        
    }

    mapping(uint => Plant) public plants;
    mapping(uint => Hybrid) public hybrids;

    event PlantRegistered(uint indexed plantId, address indexed owner);
    event HybridRegistered(uint indexed hybridId, address indexed owner);

    function registerPlant(uint plantId, string memory plantName) public {
        require(plants[plantId].owner == address(0), "Plant ID already registered");
        plants[plantId] = Plant(msg.sender, plantId, plantName);
        emit PlantRegistered(plantId, msg.sender);
    }

    function registerHybrid(uint hybridId, string memory hybridName) public {
        require(hybrids[hybridId].owner == address(0), "Hybrid ID already registered");
        hybrids[hybridId] = Hybrid(msg.sender, hybridId, hybridName);
        emit HybridRegistered(hybridId, msg.sender);
    }

    function transferPlantOwnership(uint plantId, address newOwner) public {
        require(msg.sender == plants[plantId].owner, "You are not the owner of this plant");
        plants[plantId].owner = newOwner;
    }

    function transferHybridOwnership(uint hybridId, address newOwner) public {
        require(msg.sender == hybrids[hybridId].owner, "You are not the owner of this hybrid");
        hybrids[hybridId].owner = newOwner;
    }

    
}
