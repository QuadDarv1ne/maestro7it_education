/**
 * Date Utilities для Simple HR
 * Вспомогательные функции для работы с датами
 */
class DateUtils {
    /**
     * Форматировать дату
     */
    static format(date, format = 'DD.MM.YYYY') {
        if (!(date instanceof Date)) {
            date = new Date(date);
        }

        if (isNaN(date.getTime())) {
            return '';
        }

        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');

        const replacements = {
            'DD': day,
            'MM': month,
            'YYYY': year,
            'YY': String(year).slice(-2),
            'HH': hours,
            'mm': minutes,
            'ss': seconds
        };

        let result = format;
        Object.entries(replacements).forEach(([key, value]) => {
            result = result.replace(key, value);
        });

        return result;
    }

    /**
     * Форматировать дату на русском языке
     */
    static formatRu(date, format = 'long') {
        if (!(date instanceof Date)) {
            date = new Date(date);
        }

        if (isNaN(date.getTime())) {
            return '';
        }

        const monthsShort = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'];
        const monthsLong = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];

        const day = date.getDate();
        const month = date.getMonth();
        const year = date.getFullYear();

        switch (format) {
            case 'short':
                return `${day} ${monthsShort[month]}`;
            case 'long':
                return `${day} ${monthsLong[month]} ${year} г.`;
            case 'full':
                const hours = String(date.getHours()).padStart(2, '0');
                const minutes = String(date.getMinutes()).padStart(2, '0');
                return `${day} ${monthsLong[month]} ${year} г. в ${hours}:${minutes}`;
            default:
                return this.format(date, format);
        }
    }

    /**
     * Относительное время
     */
    static relative(date) {
        if (!(date instanceof Date)) {
            date = new Date(date);
        }

        const now = new Date();
        const diff = now - date;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        const months = Math.floor(days / 30);
        const years = Math.floor(days / 365);

        if (seconds < 60) return 'только что';
        if (minutes < 60) return `${minutes} ${this.pluralize(minutes, 'минуту', 'минуты', 'минут')} назад`;
        if (hours < 24) return `${hours} ${this.pluralize(hours, 'час', 'часа', 'часов')} назад`;
        if (days < 30) return `${days} ${this.pluralize(days, 'день', 'дня', 'дней')} назад`;
        if (months < 12) return `${months} ${this.pluralize(months, 'месяц', 'месяца', 'месяцев')} назад`;
        return `${years} ${this.pluralize(years, 'год', 'года', 'лет')} назад`;
    }

    /**
     * Парсить дату
     */
    static parse(dateString, format = 'DD.MM.YYYY') {
        if (!dateString) return null;

        // ISO формат
        if (dateString.includes('T') || dateString.includes('-')) {
            return new Date(dateString);
        }

        // DD.MM.YYYY
        if (format === 'DD.MM.YYYY') {
            const parts = dateString.split('.');
            if (parts.length === 3) {
                const day = parseInt(parts[0], 10);
                const month = parseInt(parts[1], 10) - 1;
                const year = parseInt(parts[2], 10);
                return new Date(year, month, day);
            }
        }

        return new Date(dateString);
    }

    /**
     * Проверить валидность даты
     */
    static isValid(date) {
        if (!(date instanceof Date)) {
            date = new Date(date);
        }
        return !isNaN(date.getTime());
    }

    /**
     * Добавить дни
     */
    static addDays(date, days) {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    }

    /**
     * Добавить месяцы
     */
    static addMonths(date, months) {
        const result = new Date(date);
        result.setMonth(result.getMonth() + months);
        return result;
    }

    /**
     * Добавить годы
     */
    static addYears(date, years) {
        const result = new Date(date);
        result.setFullYear(result.getFullYear() + years);
        return result;
    }

    /**
     * Разница между датами в днях
     */
    static diffInDays(date1, date2) {
        const d1 = new Date(date1);
        const d2 = new Date(date2);
        const diff = Math.abs(d2 - d1);
        return Math.ceil(diff / (1000 * 60 * 60 * 24));
    }

    /**
     * Начало дня
     */
    static startOfDay(date) {
        const result = new Date(date);
        result.setHours(0, 0, 0, 0);
        return result;
    }

    /**
     * Конец дня
     */
    static endOfDay(date) {
        const result = new Date(date);
        result.setHours(23, 59, 59, 999);
        return result;
    }

    /**
     * Начало месяца
     */
    static startOfMonth(date) {
        const result = new Date(date);
        result.setDate(1);
        result.setHours(0, 0, 0, 0);
        return result;
    }

    /**
     * Конец месяца
     */
    static endOfMonth(date) {
        const result = new Date(date);
        result.setMonth(result.getMonth() + 1);
        result.setDate(0);
        result.setHours(23, 59, 59, 999);
        return result;
    }

    /**
     * Начало года
     */
    static startOfYear(date) {
        const result = new Date(date);
        result.setMonth(0);
        result.setDate(1);
        result.setHours(0, 0, 0, 0);
        return result;
    }

    /**
     * Конец года
     */
    static endOfYear(date) {
        const result = new Date(date);
        result.setMonth(11);
        result.setDate(31);
        result.setHours(23, 59, 59, 999);
        return result;
    }

    /**
     * Проверить, сегодня ли дата
     */
    static isToday(date) {
        const today = new Date();
        const d = new Date(date);
        return d.getDate() === today.getDate() &&
               d.getMonth() === today.getMonth() &&
               d.getFullYear() === today.getFullYear();
    }

    /**
     * Проверить, вчера ли дата
     */
    static isYesterday(date) {
        const yesterday = this.addDays(new Date(), -1);
        const d = new Date(date);
        return d.getDate() === yesterday.getDate() &&
               d.getMonth() === yesterday.getMonth() &&
               d.getFullYear() === yesterday.getFullYear();
    }

    /**
     * Проверить, завтра ли дата
     */
    static isTomorrow(date) {
        const tomorrow = this.addDays(new Date(), 1);
        const d = new Date(date);
        return d.getDate() === tomorrow.getDate() &&
               d.getMonth() === tomorrow.getMonth() &&
               d.getFullYear() === tomorrow.getFullYear();
    }

    /**
     * Проверить, выходной ли день
     */
    static isWeekend(date) {
        const d = new Date(date);
        const day = d.getDay();
        return day === 0 || day === 6;
    }

    /**
     * Получить название дня недели
     */
    static getDayName(date, short = false) {
        const d = new Date(date);
        const days = short
            ? ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
            : ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
        return days[d.getDay()];
    }

    /**
     * Получить название месяца
     */
    static getMonthName(date, format = 'long') {
        const d = new Date(date);
        const monthsShort = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];
        const monthsLong = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
        return format === 'short' ? monthsShort[d.getMonth()] : monthsLong[d.getMonth()];
    }

    /**
     * Получить диапазон дат
     */
    static getRange(startDate, endDate) {
        const dates = [];
        let current = new Date(startDate);
        const end = new Date(endDate);

        while (current <= end) {
            dates.push(new Date(current));
            current = this.addDays(current, 1);
        }

        return dates;
    }

    /**
     * Плюрализация
     */
    static pluralize(count, one, few, many) {
        const mod10 = count % 10;
        const mod100 = count % 100;

        if (mod10 === 1 && mod100 !== 11) {
            return one;
        } else if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) {
            return few;
        } else {
            return many;
        }
    }

    /**
     * Форматировать диапазон дат
     */
    static formatRange(startDate, endDate, format = 'DD.MM.YYYY') {
        const start = this.format(startDate, format);
        const end = this.format(endDate, format);
        return `${start} — ${end}`;
    }

    /**
     * Возраст по дате рождения
     */
    static getAge(birthDate) {
        const today = new Date();
        const birth = new Date(birthDate);
        let age = today.getFullYear() - birth.getFullYear();
        const monthDiff = today.getMonth() - birth.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
            age--;
        }

        return age;
    }

    /**
     * Рабочие дни между датами (без выходных)
     */
    static getWorkingDays(startDate, endDate) {
        const dates = this.getRange(startDate, endDate);
        return dates.filter(date => !this.isWeekend(date)).length;
    }

    /**
     * Форматировать продолжительность
     */
    static formatDuration(milliseconds) {
        const seconds = Math.floor(milliseconds / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        if (days > 0) {
            return `${days} ${this.pluralize(days, 'день', 'дня', 'дней')}`;
        } else if (hours > 0) {
            return `${hours} ${this.pluralize(hours, 'час', 'часа', 'часов')}`;
        } else if (minutes > 0) {
            return `${minutes} ${this.pluralize(minutes, 'минута', 'минуты', 'минут')}`;
        } else {
            return `${seconds} ${this.pluralize(seconds, 'секунда', 'секунды', 'секунд')}`;
        }
    }

    /**
     * Преобразовать в ISO строку для input[type="date"]
     */
    static toInputValue(date) {
        if (!(date instanceof Date)) {
            date = new Date(date);
        }
        return date.toISOString().split('T')[0];
    }

    /**
     * Квартал года
     */
    static getQuarter(date) {
        const d = new Date(date);
        return Math.floor(d.getMonth() / 3) + 1;
    }

    /**
     * Неделя года
     */
    static getWeekNumber(date) {
        const d = new Date(date);
        d.setHours(0, 0, 0, 0);
        d.setDate(d.getDate() + 4 - (d.getDay() || 7));
        const yearStart = new Date(d.getFullYear(), 0, 1);
        return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    }
}

// Глобальный экспорт
window.DateUtils = DateUtils;
