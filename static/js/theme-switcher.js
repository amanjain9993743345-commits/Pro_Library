(() => {
    'use strict';

    // Theme configuration
    const themes = ['light', 'dark', 'sepia', 'mint', 'plum'];
    const themeKey = 'prolibrary-theme';

    // Get current theme from localStorage or system preference
    function getPreferredTheme() {
        if (localStorage.getItem(themeKey)) {
            return localStorage.getItem(themeKey);
        }
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    // Apply theme to document
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-bs-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-bs-theme', 'light');
        }
        localStorage.setItem(themeKey, theme);
        console.log('Theme applied:', theme);
    }

    // Theme buttons handler
    document.addEventListener('click', (e) => {
        if (e.target.matches('.theme-btn')) {
            e.preventDefault();
            e.stopPropagation();
            const theme = e.target.dataset.theme;
            applyTheme(theme);
            // Close dropdown
            const dropdown = e.target.closest('.dropdown');
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) bsDropdown.hide();
        }
    });

    // System preference change listener
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
        if (!localStorage.getItem(themeKey)) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });

    // Initialize
    document.addEventListener('DOMContentLoaded', () => {
        applyTheme(getPreferredTheme());
    });

})();

