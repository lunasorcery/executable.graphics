// adapted from https://dev.to/ananyaneogi/create-a-dark-light-mode-switch-with-css-variables-34l8

const toggleSwitch = document.querySelector('input[type="checkbox"]#checkbox');
const userDefaultTheme = (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
const currentTheme = localStorage?.getItem('theme') ?? userDefaultTheme;

function setTheme(themeStr, shouldSave=true) {
	document.documentElement.setAttribute('data-theme', themeStr);
	if (shouldSave) {
		localStorage?.setItem('theme', themeStr);
	}
}

function setThemeFromToggle() {
	setTheme(toggleSwitch.checked ? 'dark' : 'light');
}

setTheme(currentTheme);
toggleSwitch.checked = (currentTheme === 'dark');

toggleSwitch.addEventListener('change', setThemeFromToggle, false);
