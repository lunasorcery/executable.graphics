// adapted from https://dev.to/ananyaneogi/create-a-dark-light-mode-switch-with-css-variables-34l8

const toggleSwitch = document.querySelector('input[type="checkbox"]#theme-checkbox');
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

function isAprilFoolsDay() {
	var now = new Date();
	return (now.getMonth() == 3 && now.getDate() == 1);
}

if (isAprilFoolsDay()) {
	setTheme('pouet', false);
	window.addEventListener('load', ()=>{
		document.querySelector('div.footer').innerHTML += "<br/>Pouët graphics © mandarine"
	}, false);
} else {
	setTheme(currentTheme);
	toggleSwitch.checked = (currentTheme === 'dark');
	toggleSwitch.addEventListener('change', setThemeFromToggle, false);
}

document.body.addEventListener('touchstart', (e)=>{
	// fix for dropdown getting stuck on mobile Safari

	// if we're touching somewhere outside the active element, blur it
	if (!document.activeElement.contains(e.target)) {
		document.activeElement.blur();
	}
});
