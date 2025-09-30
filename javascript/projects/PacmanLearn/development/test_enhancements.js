// Test script for Pacman enhancements
const fs = require('fs');
const path = require('path');

console.log('Testing Pacman Game Enhancements...\n');

// Test 1: Particle Manager enhancements
console.log('1. Testing Particle Manager enhancements:');
try {
    const particleManagerContent = fs.readFileSync(path.join(__dirname, 'ParticleManager.js'), 'utf8');
    
    if (particleManagerContent.includes('maxParticles')) {
        console.log('   ✅ maxParticles property found');
    } else {
        console.log('   ❌ maxParticles property not found');
    }
    
    if (particleManagerContent.includes('particlesToAdd')) {
        console.log('   ✅ Particle limit logic found');
    } else {
        console.log('   ❌ Particle limit logic not found');
    }
} catch (error) {
    console.log('   ❌ Error testing Particle Manager:', error.message);
}

// Test 2: Fruit Manager enhancements
console.log('\n2. Testing Fruit Manager enhancements:');
try {
    const fruitManagerContent = fs.readFileSync(path.join(__dirname, 'FruitManager.js'), 'utf8');
    
    if (fruitManagerContent.includes('banana') && fruitManagerContent.includes('grapes')) {
        console.log('   ✅ New fruit types (banana, grapes) found');
    } else {
        console.log('   ❌ New fruit types not found');
    }
    
    if (fruitManagerContent.includes('levelAdjustedSpawnChance')) {
        console.log('   ✅ Enhanced spawn logic found');
    } else {
        console.log('   ❌ Enhanced spawn logic not found');
    }
} catch (error) {
    console.log('   ❌ Error testing Fruit Manager:', error.message);
}

// Test 3: Achievement Manager enhancements
console.log('\n3. Testing Achievement Manager enhancements:');
try {
    const achievementManagerContent = fs.readFileSync(path.join(__dirname, 'AchievementManager.js'), 'utf8');
    
    if (achievementManagerContent.includes('speed_demon') && achievementManagerContent.includes('perfectionist')) {
        console.log('   ✅ New achievements (speed_demon, perfectionist) found');
    } else {
        console.log('   ❌ New achievements not found');
    }
    
    if (achievementManagerContent.includes('setLevelStartTime') && 
        achievementManagerContent.includes('setLevelFoodCount') && 
        achievementManagerContent.includes('incrementFoodEaten')) {
        console.log('   ✅ New tracking methods found');
    } else {
        console.log('   ❌ New tracking methods not found');
    }
} catch (error) {
    console.log('   ❌ Error testing Achievement Manager:', error.message);
}

// Test 4: PacmanGame.js integration
console.log('\n4. Testing PacmanGame.js integration:');
try {
    const pacmanGameContent = fs.readFileSync(path.join(__dirname, 'PacmanGame.js'), 'utf8');
    
    if (pacmanGameContent.includes('setLevelStartTime')) {
        console.log('   ✅ setLevelStartTime integration found');
    } else {
        console.log('   ❌ setLevelStartTime integration not found');
    }
    
    if (pacmanGameContent.includes('incrementFoodEaten')) {
        console.log('   ✅ incrementFoodEaten integration found');
    } else {
        console.log('   ❌ incrementFoodEaten integration not found');
    }
} catch (error) {
    console.log('   ❌ Error testing PacmanGame.js integration:', error.message);
}

console.log('\n🎉 Enhancement tests completed!');