/**
 * Components JavaScript
 * Интерактивность для UI компонентов
 */

(function() {
    'use strict';
    
    // ============================================
    // DROPDOWN
    // ============================================
    function initDropdowns() {
        document.querySelectorAll('.dropdown-modern').forEach(dropdown => {
            const toggle = dropdown.querySelector('.dropdown-toggle-modern');
            const menu = dropdown.querySelector('.dropdown-menu-modern');
            
            if (!toggle || !menu) return;
            
            toggle.addEventListener('click', (e) => {
                e.stopPropagation();
                
                // Close other dropdowns
                document.querySelectorAll('.dropdown-modern.show').forEach(other => {
                    if (other !== dropdown) {
                        other.classList.remove('show');
                    }
                });
                
                dropdown.classList.toggle('show');
            });
            
            // Close on item click
            menu.querySelectorAll('.dropdown-item-modern').forEach(item => {
                item.addEventListener('click', () => {
                    dropdown.classList.remove('show');
                });
            });
        });
        
        // Close dropdowns on outside click
        document.addEventListener('click', () => {
            document.querySelectorAll('.dropdown-modern.show').forEach(dropdown => {
                dropdown.classList.remove('show');
            });
        });
        
        // Close on ESC key
        document.addEve