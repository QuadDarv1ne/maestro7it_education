document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('numbersForm');
    
    form.addEventListener('submit', function(e) {
        const numbersInput = document.getElementById('numbers');
        const numbersValue = numbersInput.value.trim();
        
        if (!numbersValue) {
            alert('Пожалуйста, введите числа для обработки.');
            e.preventDefault();
            return;
        }
        
        // Проверяем, что введены только числа и запятые
        const numbersArray = numbersValue.split(',');
        let hasError = false;
        
        for (let i = 0; i < numbersArray.length; i++) {
            const num = numbersArray[i].trim();
            if (num && isNaN(num)) {
                hasError = true;
                break;
            }
        }
        
        if (hasError) {
            if (!confirm('Некоторые введенные значения не являются числами. Они будут проигнорированы. Продолжить?')) {
                e.preventDefault();
            }
        }
    });
    
    // Динамическое обновление примера ввода
    const numbersInput = document.getElementById('numbers');
    numbersInput.addEventListener('focus', function() {
        if (!this.value) {
            this.placeholder = 'Например: 5, 2, 8, 10, 3';
        }
    });
    
    numbersInput.addEventListener('blur', function() {
        if (!this.value) {
            this.placeholder = 'Введите числа через запятую';
        }
    });
});