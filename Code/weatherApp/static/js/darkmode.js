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

// Call toggleDarkMode on page load
document.addEventListener('DOMContentLoaded', function() {
    toggleDarkMode();
});

// Call toggleDarkMode whenever dark mode preference changes
window.addEventListener('storage', function(event) {
    if (event.key === 'darkMode') {
        toggleDarkMode();
    }
});

// Save dark mode preference when toggled
saveDarkModePreference();
