// darkmode.js

function toggleDarkMode() {
    const body = document.getElementById('body');
    const darkModeEnabled = localStorage.getItem('darkMode') === 'enabled';
    
    if (darkModeEnabled) {
        body.classList.add('dark-mode');
    } else {
        body.classList.remove('dark-mode');
    }
}

function saveDarkModePreference() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    darkModeToggle.addEventListener('change', function() {
        const darkModeEnabled = this.checked;
        localStorage.setItem('darkMode', darkModeEnabled ? 'enabled' : 'disabled');
        toggleDarkMode();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    saveDarkModePreference();
    toggleDarkMode();
});
