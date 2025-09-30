// Test script for GameMap.js
const fs = require('fs');

// Read the GameMap.js file
const gameMapCode = fs.readFileSync('GameMap.js', 'utf8');

// Create a simple test to check the level structure
console.log('Testing GameMap.js...\n');

// Extract the level map array from the file
const mapMatch = gameMapCode.match(/this\.map = \[([\s\S]*?)\];/);
if (mapMatch) {
    console.log('✓ Found initial level map');
    
    // Count the dimensions
    const lines = mapMatch[1].split('\n').filter(line => line.trim().startsWith('[') && line.trim().endsWith(','));
    console.log(`✓ Level dimensions: ${lines.length} rows`);
    
    // Count food items
    const foodCount = (mapMatch[1].match(/2/g) || []).length;
    const superFoodCount = (mapMatch[1].match(/3/g) || []).length;
    console.log(`✓ Food count: ${foodCount} dots`);
    console.log(`✓ Super-food count: ${superFoodCount} dots`);
    
    // Check if it's a classic Pacman layout
    if (lines.length >= 15 && foodCount > 50 && superFoodCount >= 4) {
        console.log('✓ Level structure符合 classic Pacman design');
    } else {
        console.log('⚠ Level structure may need adjustment');
    }
} else {
    console.log('✗ Could not find initial level map');
}

console.log('\nTest completed.');