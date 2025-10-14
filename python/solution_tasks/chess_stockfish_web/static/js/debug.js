// Debug script to test Socket.IO connection
console.log('Debug script loaded');

// Test Socket.IO connection
const socket = io();

socket.on('connect', () => {
    console.log('✅ Socket.IO connected successfully');
});

socket.on('connect_error', (error) => {
    console.error('❌ Socket.IO connection error:', error);
});

socket.on('disconnect', (reason) => {
    console.log('⚠️ Socket.IO disconnected:', reason);
});

// Test game initialization
function testGameInit() {
    console.log('Testing game initialization...');
    socket.emit('init_game', { color: 'white', level: 5 });
}

// Add to window for testing
window.testGameInit = testGameInit;