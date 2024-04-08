// ----------------------------------------------------
// darkmode.js
/*
Functions for controlling website darkmode.
*/
// -----------------------------------------------------

function darkModeIsEnabled() {
    return localStorage.getItem('darkMode') === 'enabled'
}

function switchMode() {
    if (darkModeIsEnabled()) {
        localStorage.setItem('darkMode', 'disabled');
    }
    else {
        localStorage.setItem('darkMode', 'enabled');
    }
}

function loadPageWithCorrectMode() {
    const body = document.getElementById('body');
    
    if (darkModeIsEnabled()) {
        body.classList.add('dark-mode');
    } else {
        body.classList.remove('dark-mode');
    }
}

function onToggleSwitchMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');

    darkModeToggle.addEventListener('change', function() {
        switchMode();
        loadPageWithCorrectMode();
    });
}