/**
 * i18n.js - Internationalization Handler
 */

class I18n {
    constructor() {
        this.currentLang = 'fr';
        this.translations = {};
        this.fallbackLang = 'fr';
    }

    /**
     * Load translation files
     */
    async loadTranslations() {
        try {
            const [fr, en] = await Promise.all([
                fetch('./locales/fr.json').then(r => r.json()),
                fetch('./locales/en.json').then(r => r.json())
            ]);
            
            this.translations = { fr, en };
            
            // Detect browser language
            const browserLang = navigator.language.split('-')[0];
            if (this.translations[browserLang]) {
                this.currentLang = browserLang;
            }
            
            return true;
        } catch (error) {
            console.error('Erreur de chargement des traductions:', error);
            return false;
        }
    }

    /**
     * Change active language
     */
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            this.updateUI();
            this.updateButtons();
        }
    }

    /**
     * Retrieve a translation by key path
     * Example: t('kpis.revenue.label')
     */
    t(key, params = {}) {
        const keys = key.split('.');
        let value = this.translations[this.currentLang];
        
        for (const k of keys) {
            if (value && typeof value === 'object') {
                value = value[k];
            } else {
                // Fallback on default language
                value = this.translations[this.fallbackLang];
                for (const fallbackKey of keys) {
                    if (value && typeof value === 'object') {
                        value = value[fallbackKey];
                    }
                }
                break;
            }
        }
        
        // Replace parameters {key} by their values
        if (typeof value === 'string' && Object.keys(params).length > 0) {
            return value.replace(/\{(\w+)\}/g, (match, paramKey) => {
                return params[paramKey] !== undefined ? params[paramKey] : match;
            });
        }
        
        return value || key;
    }

    /**
     * Update UI elements with data-i18n attributes
     */
    updateUI() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (translation) {
                el.textContent = translation;
            }
        });
    }

    /**
     * Update language switcher buttons
     */
    updateButtons() {
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        const activeBtn = document.getElementById(`btn-${this.currentLang}`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }
    }

    /**
     * Create a tooltip element
     */
    createTooltip(text, tooltipKey) {
        const tooltipText = this.t(tooltipKey);
        return `<span class="tooltip-term">${text}<span class="tooltip-content">${tooltipText}</span></span>`;
    }

    /**
     * Retrieve translated month names
     */
    getMonthNames() {
        return this.t('months.short') || [];
    }

    /**
     * Retrieve current language
     */
    getCurrentLang() {
        return this.currentLang;
    }
}

const i18n = new I18n();