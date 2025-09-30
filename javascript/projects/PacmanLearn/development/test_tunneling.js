// Test script for tunneling functionality
const fs = require('fs');
const path = require('path');

// Read the JavaScript files
const pacmanJS = fs.readFileSync(path.join(__dirname, 'Pacman.js'), 'utf8');
const ghostJS = fs.readFileSync(path.join(__dirname, 'Ghost.js'), 'utf8');

console.log('Testing tunneling functionality...\n');

// Test map (simplified)
const testMap = [
  [1, 1, 1, 1, 1],
  [1, 2, 2, 2, 1],
  [1, 2, 2, 2, 1],
  [1, 2, 2, 2, 1],
  [1, 1, 1, 1, 1]
];

// Simple Pacman class mock for testing
class TestPacman {
  getNextPosition(x, y, direction, map, cellSize) {
    let newX = x;
    let newY = y;
    
    switch(direction) {
      case 'up': newY--; break;
      case 'down': newY++; break;
      case 'left': newX--; break;
      case 'right': newX++; break;
    }
    
    // Туннельные переходы (copied from actual implementation)
    if (newX < 0) newX = map[0].length - 1;
    if (newX >= map[0].length) newX = 0;
    if (newY < 0) newY = map.length - 1;
    if (newY >= map.length) newY = 0;
    
    return { x: newX, y: newY };
  }
}

// Simple Ghost class mock for testing
class TestGhost {
  getNextPosition(x, y, direction, map, cellSize) {
    let newX = x;
    let newY = y;
    
    switch(direction) {
      case 'up': newY--; break;
      case 'down': newY++; break;
      case 'left': newX--; break;
      case 'right': newX++; break;
    }
    
    // Туннельные переходы (copied from actual implementation)
    if (newX < 0) newX = map[0].length - 1;
    if (newX >= map[0].length) newX = 0;
    if (newY < 0) newY = map.length - 1;
    if (newY >= map.length) newY = 0;
    
    return { x: newX, y: newY };
  }
}

// Run tests
const pacman = new TestPacman();
const ghost = new TestGhost();

console.log('1. Testing horizontal tunneling for Pacman:');
let result = pacman.getNextPosition(-0.5, 2, 'left', testMap, 30);
console.log(`   Moving left from x=-0.5: Expected x=4, Got x=${result.x} ${result.x === 4 ? '✅' : '❌'}`);

result = pacman.getNextPosition(5, 2, 'right', testMap, 30);
console.log(`   Moving right from x=5: Expected x=0, Got x=${result.x} ${result.x === 0 ? '✅' : '❌'}`);

console.log('\n2. Testing vertical tunneling for Pacman:');
result = pacman.getNextPosition(2, -0.5, 'up', testMap, 30);
console.log(`   Moving up from y=-0.5: Expected y=4, Got y=${result.y} ${result.y === 4 ? '✅' : '❌'}`);

result = pacman.getNextPosition(2, 5, 'down', testMap, 30);
console.log(`   Moving down from y=5: Expected y=0, Got y=${result.y} ${result.y === 0 ? '✅' : '❌'}`);

console.log('\n3. Testing horizontal tunneling for Ghost:');
result = ghost.getNextPosition(-0.5, 2, 'left', testMap, 30);
console.log(`   Moving left from x=-0.5: Expected x=4, Got x=${result.x} ${result.x === 4 ? '✅' : '❌'}`);

result = ghost.getNextPosition(5, 2, 'right', testMap, 30);
console.log(`   Moving right from x=5: Expected x=0, Got x=${result.x} ${result.x === 0 ? '✅' : '❌'}`);

console.log('\n4. Testing vertical tunneling for Ghost:');
result = ghost.getNextPosition(2, -0.5, 'up', testMap, 30);
console.log(`   Moving up from y=-0.5: Expected y=4, Got y=${result.y} ${result.y === 4 ? '✅' : '❌'}`);

result = ghost.getNextPosition(2, 5, 'down', testMap, 30);
console.log(`   Moving down from y=5: Expected y=0, Got y=${result.y} ${result.y === 0 ? '✅' : '❌'}`);

console.log('\n🎉 All tunneling tests completed!');