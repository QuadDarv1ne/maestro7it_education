/**
 * Social Sharing Module
 * Позволяет делиться турнирами в социальных сетях
 */

class SocialSharing {
    constructor() {
        this.init();
    }

    init() {
        console.log('[SocialSharing] Инициализация модуля социального шаринга');
        this.setupShareButtons();
        this.setupCopyLink();
    }

    setupShareButtons() {
        // Добавляем кнопки шаринга на карточки турниров
        document.addEventListener('click', (e) => {
            if (e.target.closest('.share-tournament-btn')) {
                e.preventDefault();
                const btn = e.target.closest('.share-tournament-btn');
                const tournamentId = btn.dataset.tournamentId;
                const tournamentName = btn.dataset.tournamentName;
                this.showShareModal(tournamentId, tournamentName);
            }
        });
    }

    showShareModal(tournamentId, tournamentName) {
        const url = `${window.location.origin}/tournament/${tournamentId}`;
        const text = `Шахматный турнир: ${tournamentName}`;

        // Создаём модальное окно
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'shareModal';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-share"></i> Поделиться турниром
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="share-options">
                            <button class="share-btn share-vk" data-network="vk">
                                <i class="bi bi-vk"></i>
                                <span>ВКонтакте</span>
                            </button>
                            <button class="share-btn share-telegram" data-network="telegram">
                                <i class="bi bi-telegram"></i>
                                <span>Telegram</span>
                            </button>
                            <button class="share-btn share-whatsapp" data-network="whatsapp">
                                <i class="bi bi-whatsapp"></i>
                                <span>WhatsApp</span>
                            </button>
                            <button class="share-btn share-twitter" data-network="twitter">
                                <i class="bi bi-twitter"></i>
                                <span>Twitter</span>
                            </button>
                            <button class="share-btn share-facebook" data-network="facebook">
                                <i class="bi bi-facebook"></i>
                                <span>Facebook</span>
                            </button>
                            <button class="share-btn share-email" data-network="email">
                                <i class="bi bi-envelope"></i>
                                <span>Email</span>
                            </button>
                        </div>
                        <div class="mt-3">
                            <label class="form-label">Ссылка на турнир:</label>
                            <div class="input-group">
                                <input type="text" class="form-control" id="shareUrl" value="${url}" readonly>
                                <button class="btn btn-primary" id="copyLinkBtn">
                                    <i class="bi bi-clipboard"></i> Копировать
                                </button>
                            </div>
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-outline-primary w-100" id="nativeShareBtn">
                                <i class="bi bi-share"></i> Поделиться через систему
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        // Обработчики кнопок
        modal.querySelectorAll('.share-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const network = btn.dataset.network;
                this.shareToNetwork(network, url, text);
            });
        });

        modal.querySelector('#copyLinkBtn').addEventListener('click', () => {
            this.copyToClipboard(url);
        });

        modal.querySelector('#nativeShareBtn').addEventListener('click', () => {
            this.nativeShare(url, text);
        });

        // Удаляем модал после закрытия
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    shareToNetwork(network, url, text) {
        const encodedUrl = encodeURIComponent(url);
        const encodedText = encodeURIComponent(text);
        let shareUrl = '';

        switch (network) {
            case 'vk':
                shareUrl = `https://vk.com/share.php?url=${encodedUrl}&title=${encodedText}`;
                break;
            case 'telegram':
                shareUrl = `https://t.me/share/url?url=${encodedUrl}&text=${encodedText}`;
                break;
            case 'whatsapp':
                shareUrl = `https://wa.me/?text=${encodedText}%20${encodedUrl}`;
                break;
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedText}`;
                break;
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`;
                break;
            case 'email':
                shareUrl = `mailto:?subject=${encodedText}&body=${encodedUrl}`;
                break;
        }

        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
            this.trackShare(network);
        }
    }

    async nativeShare(url, text) {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: text,
                    url: url
                });
                this.showToast('Успешно поделились!', 'success');
                this.trackShare('native');
            } catch (err) {
                if (err.name !== 'AbortError') {
                    console.error('[SocialSharing] Ошибка нативного шаринга:', err);
                }
            }
        } else {
            this.showToast('Функция недоступна в вашем браузере', 'warning');
        }
    }

    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showToast('Ссылка скопирована!', 'success');
                this.trackShare('copy');
            }).catch(err => {
                console.error('[SocialSharing] Ошибка копирования:', err);
                this.fallbackCopy(text);
            });
        } else {
            this.fallbackCopy(text);
        }
    }

    fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            this.showToast('Ссылка скопирована!', 'success');
            this.trackShare('copy');
        } catch (err) {
            console.error('[SocialSharing] Ошибка копирования:', err);
            this.showToast('Не удалось скопировать', 'error');
        }
        document.body.removeChild(textarea);
    }

    setupCopyLink() {
        // Добавляем возможность копирования ссылки из адресной строки
        const copyCurrentUrl = () => {
            this.copyToClipboard(window.location.href);
        };

        // Можно вызвать через глобальный объект
        if (window.ChessCalendar) {
            window.ChessCalendar.copyCurrentUrl = copyCurrentUrl;
        }
    }

    trackShare(network) {
        // Отслеживание шарингов для статистики
        const shares = JSON.parse(localStorage.getItem('tournament_shares') || '{}');
        shares[network] = (shares[network] || 0) + 1;
        localStorage.setItem('tournament_shares', JSON.stringify(shares));

        // Достижение за шаринг
        if (window.ChessCalendar && window.ChessCalendar.achievements) {
            const totalShares = Object.values(shares).reduce((a, b) => a + b, 0);
            if (totalShares === 1) {
                window.ChessCalendar.achievements.unlock('first_share');
            } else if (totalShares === 10) {
                window.ChessCalendar.achievements.unlock('social_butterfly');
            }
        }
    }

    showToast(message, type = 'info') {
        if (window.ChessCalendar && window.ChessCalendar.showToast) {
            window.ChessCalendar.showToast(message, type);
        }
    }

    // Получить статистику шарингов
    getShareStats() {
        return JSON.parse(localStorage.getItem('tournament_shares') || '{}');
    }
}

// Стили для кнопок шаринга
const style = document.createElement('style');
style.textContent = `
    .share-options {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .share-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        border: 2px solid var(--border-color);
        border-radius: 12px;
        background: var(--bg-primary);
        color: var(--text-primary);
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .share-btn:hover {
        transform: translateY(-3px);
        box-shadow: var(--box-shadow);
    }

    .share-btn i {
        font-size: 1.5rem;
    }

    .share-btn span {
        font-size: 0.875rem;
        font-weight: 500;
    }

    .share-vk:hover {
        background: #0077FF;
        color: white;
        border-color: #0077FF;
    }

    .share-telegram:hover {
        background: #0088cc;
        color: white;
        border-color: #0088cc;
    }

    .share-whatsapp:hover {
        background: #25D366;
        color: white;
        border-color: #25D366;
    }

    .share-twitter:hover {
        background: #1DA1F2;
        color: white;
        border-color: #1DA1F2;
    }

    .share-facebook:hover {
        background: #1877F2;
        color: white;
        border-color: #1877F2;
    }

    .share-email:hover {
        background: #EA4335;
        color: white;
        border-color: #EA4335;
    }

    @media (max-width: 576px) {
        .share-options {
            grid-template-columns: repeat(2, 1fr);
        }
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.ChessCalendar = window.ChessCalendar || {};
    window.ChessCalendar.socialSharing = new SocialSharing();
});
