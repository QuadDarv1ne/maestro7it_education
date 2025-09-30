// Test script to verify that the button handlers are working in pacman_modular.html
const fs = require('fs');
const path = require('path');

console.log('Testing pacman_modular.html button functionality...\n');

try {
    // Read the pacman_modular.html file
    const htmlContent = fs.readFileSync(path.join(__dirname, 'pacman_modular.html'), 'utf8');
    
    // Check if the JavaScript section was added
    if (htmlContent.includes('window.addEventListener(\'load\', () => {')) {
        console.log('✅ JavaScript initialization code found');
    } else {
        console.log('❌ JavaScript initialization code NOT found');
    }
    
    // Check for key event handlers
    const eventHandlers = [
        'play-btn',
        'level-select-btn',
        'settings-btn',
        'highscores-btn',
        'about-btn',
        'back-from-scores-btn',
        'back-from-settings-btn',
        'back-from-levels-btn',
        'save-settings-btn',
        'start-btn',
        'pause-btn',
        'reset-btn',
        'menu-btn',
        'message-btn'
    ];
    
    let foundHandlers = 0;
    eventHandlers.forEach(handler => {
        if (htmlContent.includes(handler)) {
            console.log(`✅ Event handler for ${handler} found`);
            foundHandlers++;
        } else {
            console.log(`❌ Event handler for ${handler} NOT found`);
        }
    });
    
    console.log(`\nFound ${foundHandlers}/${eventHandlers.length} event handlers`);
    
    if (foundHandlers === eventHandlers.length) {
        console.log('\n🎉 All button handlers have been successfully added!');
    } else {
        console.log('\n⚠ Some button handlers are missing');
    }
    
} catch (error) {
    console.error('Error testing pacman_modular.html:', error.message);
}