/**
 * API Client для Simple HR
 * Упрощенный HTTP клиент для работы с REST API
 */
class APIClient {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
        this.interceptors = {
            request: [],
            response: []
        };
    }

    /**
     * Добавить заголовок по умолчанию
     */
    setDefaultHeader(name, value) {
        this.defaultHeaders[name] = value;
    }

    /**
     * Удалить заголовок по умолчанию
     */
    removeDefaultHeader(name) {
        delete this.defaultHeaders[name];
    }

    /**
     * Установить токен авторизации
     */
    setAuthToken(token) {
        this.setDefaultHeader('Authorization', `Bearer ${token}`);
    }

    /**
     * Добавить перехватчик запроса
     */
    addRequestInterceptor(fn) {
        this.interceptors.request.push(fn);
    }

    /**
     * Добавить перехватчик ответа
     */
    addResponseInterceptor(fn) {
        this.interceptors.response.push(fn);
    }

    /**
     * Выполнить запрос
     */
    async request(url, options = {}) {
        // Полный URL
        const fullURL = url.startsWith('http') ? url : this.baseURL + url;

        // Объединить заголовки
        const headers = {
            ...this.defaultHeaders,
            ...options.headers
        };

        // Подготовить опции
        let requestOptions = {
            ...options,
            headers
        };

        // Применить перехватчики запроса
        for (const interceptor of this.interceptors.request) {
            requestOptions = await interceptor(requestOptions);
        }

        try {
            // Выполнить запрос
            let response = await fetch(fullURL, requestOptions);

            // Применить перехватчики ответа
            for (const interceptor of this.interceptors.response) {
                response = await interceptor(response);
            }

            // Обработать ошибки HTTP
            if (!response.ok) {
                const error = new Error(`HTTP Error: ${response.status}`);
                error.response = response;
                error.status = response.status;
                
                // Попытаться получить тело ошибки
                try {
                    error.data = await response.json();
                } catch (e) {
                    error.data = await response.text();
                }
                
                throw error;
            }

            // Вернуть ответ
            return response;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    /**
     * GET запрос
     */
    async get(url, params = {}, options = {}) {
        // Добавить параметры в URL
        const queryString = new URLSearchParams(params).toString();
        const fullURL = queryString ? `${url}?${queryString}` : url;

        const response = await this.request(fullURL, {
            method: 'GET',
            ...options
        });

        return await response.json();
    }

    /**
     * POST запрос
     */
    async post(url, data = null, options = {}) {
        const response = await this.request(url, {
            method: 'POST',
            body: data ? JSON.stringify(data) : null,
            ...options
        });

        return await response.json();
    }

    /**
     * PUT запрос
     */
    async put(url, data = null, options = {}) {
        const response = await this.request(url, {
            method: 'PUT',
            body: data ? JSON.stringify(data) : null,
            ...options
        });

        return await response.json();
    }

    /**
     * PATCH запрос
     */
    async patch(url, data = null, options = {}) {
        const response = await this.request(url, {
            method: 'PATCH',
            body: data ? JSON.stringify(data) : null,
            ...options
        });

        return await response.json();
    }

    /**
     * DELETE запрос
     */
    async delete(url, options = {}) {
        const response = await this.request(url, {
            method: 'DELETE',
            ...options
        });

        // DELETE может не возвращать тело
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        
        return { success: true };
    }

    /**
     * Загрузить файл
     */
    async upload(url, file, fieldName = 'file', additionalData = {}) {
        const formData = new FormData();
        formData.append(fieldName, file);

        // Добавить дополнительные данные
        Object.entries(additionalData).forEach(([key, value]) => {
            formData.append(key, value);
        });

        const response = await this.request(url, {
            method: 'POST',
            body: formData,
            headers: {} // Не устанавливать Content-Type, браузер сделает это автоматически
        });

        return await response.json();
    }

    /**
     * Скачать файл
     */
    async download(url, filename = null) {
        const response = await this.request(url, {
            method: 'GET'
        });

        const blob = await response.blob();
        
        // Определить имя файла
        if (!filename) {
            const contentDisposition = response.headers.get('content-disposition');
            if (contentDisposition) {
                const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
                if (matches && matches[1]) {
                    filename = matches[1].replace(/['"]/g, '');
                }
            }
        }
        
        filename = filename || 'download';

        // Создать ссылку для скачивания
        const downloadURL = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadURL;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(downloadURL);

        return { success: true, filename };
    }

    /**
     * Batch запросы (параллельно)
     */
    async batch(requests) {
        const promises = requests.map(req => {
            const { method = 'GET', url, data, options = {} } = req;
            
            switch (method.toUpperCase()) {
                case 'GET':
                    return this.get(url, data, options);
                case 'POST':
                    return this.post(url, data, options);
                case 'PUT':
                    return this.put(url, data, options);
                case 'PATCH':
                    return this.patch(url, data, options);
                case 'DELETE':
                    return this.delete(url, options);
                default:
                    throw new Error(`Unknown method: ${method}`);
            }
        });

        return await Promise.all(promises);
    }
}

/**
 * Simple HR API Client
 * Специализированный клиент для Simple HR API
 */
class SimpleHRAPI extends APIClient {
    constructor() {
        super('/api/v1');
    }

    // ===== Employees =====
    async getEmployees(params = {}) {
        return await this.get('/employees', params);
    }

    async getEmployee(id) {
        return await this.get(`/employees/${id}`);
    }

    async createEmployee(data) {
        return await this.post('/employees', data);
    }

    async updateEmployee(id, data) {
        return await this.put(`/employees/${id}`, data);
    }

    async deleteEmployee(id) {
        return await this.delete(`/employees/${id}`);
    }

    async searchEmployees(query) {
        return await this.get('/employees/search', { q: query });
    }

    // ===== Departments =====
    async getDepartments(params = {}) {
        return await this.get('/departments', params);
    }

    async getDepartment(id) {
        return await this.get(`/departments/${id}`);
    }

    async createDepartment(data) {
        return await this.post('/departments', data);
    }

    async updateDepartment(id, data) {
        return await this.put(`/departments/${id}`, data);
    }

    async deleteDepartment(id) {
        return await this.delete(`/departments/${id}`);
    }

    // ===== Positions =====
    async getPositions(params = {}) {
        return await this.get('/positions', params);
    }

    async getPosition(id) {
        return await this.get(`/positions/${id}`);
    }

    async createPosition(data) {
        return await this.post('/positions', data);
    }

    async updatePosition(id, data) {
        return await this.put(`/positions/${id}`, data);
    }

    async deletePosition(id) {
        return await this.delete(`/positions/${id}`);
    }

    // ===== Vacations =====
    async getVacations(params = {}) {
        return await this.get('/vacations', params);
    }

    async getVacation(id) {
        return await this.get(`/vacations/${id}`);
    }

    async createVacation(data) {
        return await this.post('/vacations', data);
    }

    async updateVacation(id, data) {
        return await this.put(`/vacations/${id}`, data);
    }

    async deleteVacation(id) {
        return await this.delete(`/vacations/${id}`);
    }

    async approveVacation(id) {
        return await this.post(`/vacations/${id}/approve`);
    }

    async rejectVacation(id, reason = '') {
        return await this.post(`/vacations/${id}/reject`, { reason });
    }

    // ===== Orders =====
    async getOrders(params = {}) {
        return await this.get('/orders', params);
    }

    async getOrder(id) {
        return await this.get(`/orders/${id}`);
    }

    async createOrder(data) {
        return await this.post('/orders', data);
    }

    async updateOrder(id, data) {
        return await this.put(`/orders/${id}`, data);
    }

    async deleteOrder(id) {
        return await this.delete(`/orders/${id}`);
    }

    // ===== Reports =====
    async getReports(params = {}) {
        return await this.get('/reports', params);
    }

    async generateReport(type, params = {}) {
        return await this.post('/reports/generate', { type, ...params });
    }

    async downloadReport(id) {
        return await this.download(`/reports/${id}/download`);
    }

    // ===== Analytics =====
    async getAnalytics(type, params = {}) {
        return await this.get(`/analytics/${type}`, params);
    }

    async getDashboardStats() {
        return await this.get('/analytics/dashboard');
    }

    async getEmployeeStatistics() {
        return await this.get('/analytics/employees');
    }

    async getVacationAnalysis() {
        return await this.get('/analytics/vacations');
    }

    async getHiringTrends() {
        return await this.get('/analytics/hiring');
    }

    // ===== Notifications =====
    async getNotifications(params = {}) {
        return await this.get('/notifications', params);
    }

    async getUnreadNotifications() {
        return await this.get('/notifications/unread');
    }

    async markNotificationRead(id) {
        return await this.post(`/notifications/${id}/read`);
    }

    async markAllNotificationsRead() {
        return await this.post('/notifications/read-all');
    }

    async deleteNotification(id) {
        return await this.delete(`/notifications/${id}`);
    }
}

// Глобальные экземпляры
const apiClient = new APIClient();
const hrAPI = new SimpleHRAPI();

// Добавить перехватчик для показа уведомлений об ошибках
hrAPI.addResponseInterceptor(async (response) => {
    if (!response.ok && window.notificationManager) {
        try {
            const error = await response.clone().json();
            notificationManager.error(
                error.message || `Ошибка: ${response.status}`,
                'Ошибка API'
            );
        } catch (e) {
            notificationManager.error(
                `HTTP ошибка: ${response.status}`,
                'Ошибка сервера'
            );
        }
    }
    return response;
});

// Экспорт
window.APIClient = APIClient;
window.SimpleHRAPI = SimpleHRAPI;
window.apiClient = apiClient;
window.hrAPI = hrAPI;
