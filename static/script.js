// adapted from https://dev.to/ananyaneogi/create-a-dark-light-mode-switch-with-css-variables-34l8

const currentTheme = localStorage?.getItem('theme') ?? 'auto';

function setTheme(themeStr, shouldSave=true) {
	document.documentElement.setAttribute('data-theme', themeStr);
	if (shouldSave) {
		localStorage?.setItem('theme', themeStr);
	}
}

function isAprilFoolsDay() {
	var now = new Date();
	return (now.getMonth() == 3 && now.getDate() == 1);
}

if (isAprilFoolsDay()) {
	setTheme('pouet', false);
} else {
	setTheme(currentTheme);
}

document.body.addEventListener('touchstart', (e)=>{
	// fix for dropdown getting stuck on mobile Safari

	// if we're touching somewhere outside the active element, blur it
	if (!document.activeElement.contains(e.target)) {
		document.activeElement.blur();
	}
});

function setThemeFromElementAndDismissContextMenu(element) {
	setTheme(element.getAttribute('data-theme-option'));
	document.activeElement.blur();
}

function onThemeClick(e) {
	setThemeFromElementAndDismissContextMenu(e.target);
}

function onThemeKeyDown(e) {
	if (e.keyCode == 13) {
		setThemeFromElementAndDismissContextMenu(e.target);
	}
}
