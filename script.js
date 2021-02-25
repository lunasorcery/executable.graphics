// adapted from https://dev.to/ananyaneogi/create-a-dark-light-mode-switch-with-css-variables-34l8

const toggleSwitch = document.querySelector('input[type="checkbox"]#checkbox');
const userDefaultTheme = (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
const currentTheme = localStorage?.getItem('theme') ?? userDefaultTheme;

document.documentElement.setAttribute('data-theme', currentTheme);
if (currentTheme === 'dark') {
	toggleSwitch.checked = true;
}

function switchTheme(e) {
	if (e.target.checked) {
		document.documentElement.setAttribute('data-theme', 'dark');
		localStorage?.setItem('theme', 'dark');
	}
	else {
		document.documentElement.setAttribute('data-theme', 'light');
		localStorage?.setItem('theme', 'light');
	}
}

toggleSwitch.addEventListener('change', switchTheme, false);
