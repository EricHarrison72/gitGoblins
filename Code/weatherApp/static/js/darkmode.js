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

function switchAndLoadMode() {
    switchMode();
    loadPageWithCorrectMode();
}

function updateToggleText() {
    const button = document.getElementById('mode-toggle-button');
    if (darkModeIsEnabled()) {
        button.innerHTML = "LIGHT<br>MODE";
    }
    else {
        button.innerHTML = "DARK<br>MODE";
    }
}

function updateGraph() {
    var darkModeGraph = document.getElementById("dark-mode-graph");
    var lightModeGraph = document.getElementById("light-mode-graph");

    if (darkModeIsEnabled()) {
        darkModeGraph.style.display = "block";
        lightModeGraph.style.display = "none";
    }
    else {
        darkModeGraph.style.display = "none";
        lightModeGraph.style.display = "block";
    }
}

function updateTextAndGraph() {
    updateToggleText();
    updateGraph();
}
