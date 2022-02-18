#!/usr/bin/env python3

import os
import json
import sass
import shutil
import chevron
import binascii
import datetime


def maybe_mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)


def crc32_file(filename):
	buf = open(filename,'rb').read()
	buf = (binascii.crc32(buf) & 0xffffffff)
	return f"{buf:08x}"


# fail the build if localization strings are missing
validateMissingLocalization = True


# Seasonal events
meteorikJurorApplicationOpen = False
meteorikPublicNominationsOpen = True


# folder structure
buildFolder = "gen/"

rootFolder = os.path.join(buildFolder, "root")
rootImgFolder = os.path.join(rootFolder, "img")

netscapeFolder = os.path.join(buildFolder, "web1")
netscapeImgFolder = os.path.join(netscapeFolder, "img")


# load languages
with open('languages/list.json') as file:
	languages = sorted(
		[lang for lang in json.load(file) if lang.get('visible', True)],
		key=lambda l: l['name'])


# ensure no overlapping root folders
for a in languages:
	for b in languages:
		if a != b and a['root'] == b['root']:
			print(f"language root folders must be unique, but '{a['id']}' and '{b['id']}' both use '{a['root']}'")
			quit(1)


# enumerate translators
translators = []
for lang in languages:
	for translator in lang.get('translators', []):
		translators.append(translator)


# load prods
with open('prods.json') as file:
	prods = [prod for prod in json.load(file) if not prod.get('hidden', False)]

# figure out the meteorik prods
for idx,prod in enumerate(prods):
	if 'meteorik-type' in prod:
		prods[idx]['meteorik-winner']  = (prod['meteorik-type'] == 'winner')
		prods[idx]['meteorik-nominee'] = (prod['meteorik-type'] == 'nominee')
meteorikProds = sorted(
	[prod for prod in prods if 'meteorik-year' in prod],
	key = lambda x: (x['meteorik-year'], x['meteorik-type']),
	reverse=True)


maybe_mkdir(buildFolder)
maybe_mkdir(rootFolder)
maybe_mkdir(rootImgFolder)
maybe_mkdir(netscapeFolder)
maybe_mkdir(netscapeImgFolder)


print("generating icons...")
appleTouchIconPath = os.path.join(rootFolder, 'apple-touch-icon.png')
faviconIcoPath = os.path.join(rootFolder, 'favicon.ico')
if not os.path.exists(appleTouchIconPath):
	os.system(f"inkscape -w 160 -h 160 -o {appleTouchIconPath} icons/mobile-icon.svg")
if not os.path.exists(faviconIcoPath):
	faviconSizes = [16,32,48]
	for size in faviconSizes:
		os.system(f"inkscape -w {size} -h {size} -o favicon-{size}.png icons/favicon.svg")
	faviconPngs = [f"favicon-{size}.png" for size in faviconSizes]
	os.system(f"magick convert {' '.join(faviconPngs)} {faviconIcoPath}")
	for faviconPng in faviconPngs:
		os.remove(faviconPng)


print("copying static assets...")
staticAssets = [
	'fonts.css',
	'script.js',
	'manifest.json',
	'Muli-Regular.ttf',
	'Muli-Bold.ttf',
	'Muli-ExtraBoldItalic.ttf',
]
for asset in staticAssets:
	shutil.copyfile(f'static/{asset}', os.path.join(rootFolder, asset))


print("processing CSS...")
cssFiles = [
	'style.scss'
]
for asset in cssFiles:
	with open(asset) as fIn:
		outpath = os.path.join(rootFolder, asset.replace('.scss','.css'))
		print(outpath)
		with open(outpath, 'w') as fOut:
			fOut.write(sass.compile(string=fIn.read()))


print("converting images...")
for idx,prod in enumerate(prods):
	slug = prod['slug']
	src_jpg = f"raw-images/{slug}.jpg"
	src_png = f"raw-images/{slug}.png"
	dst_jpg = os.path.join(rootImgFolder, f"{slug}.jpg")
	dst_png = os.path.join(rootImgFolder, f"{slug}.png")

	print(f"- {slug}")

	if os.path.exists(dst_jpg):
		prods[idx]['image_url'] = f"/img/{slug}.jpg"
		print("   already exists, skipping...")
		continue
	elif os.path.exists(dst_png):
		prods[idx]['image_url'] = f"/img/{slug}.png"
		print("   already exists, skipping...")
		continue

	if os.path.exists(src_jpg):
		# if the source is a jpg, use that
		#shutil.copyfile(src_jpg, dst_jpg)

		# actually, let's make sure it's progressive
		os.system(f"magick convert -interlace Plane -quality 95 {src_jpg} {dst_jpg}")
		prods[idx]['image_url'] = f"img/{slug}.jpg"

		# if we've made it bigger, ditch the quality=95 flag
		if os.path.getsize(dst_jpg) > os.path.getsize(src_jpg):
			os.system(f"magick convert -interlace Plane {src_jpg} {dst_jpg}")

		print(f"   src_jpg: {os.path.getsize(src_jpg): 10,}b")
		print(f"   dst_jpg: {os.path.getsize(dst_jpg): 10,}b")

	elif os.path.exists(src_png):
		# if the source is a png, resave it as a jpg
		os.system(f"magick convert -interlace Plane -quality 95 {src_png} {dst_jpg}")

		# ...and use the smaller one
		print(f"   src_png: {os.path.getsize(src_png): 10,}b")
		if os.path.getsize(dst_jpg) < os.path.getsize(src_png):
			prods[idx]['image_url'] = f"/img/{slug}.jpg"
			print(f"   dst_jpg: {os.path.getsize(dst_jpg): 10,}b")
		else:
			os.remove(dst_jpg)
			shutil.copyfile(src_png, dst_png)
			prods[idx]['image_url'] = f"/img/{slug}.png"
			print(f"   dst_png: {os.path.getsize(dst_png): 10,}b")
	else:
		print("   missing raw image!")
		raise hell


print("converting images for web1 site")
for idx,prod in enumerate(prods):
	slug = prod['slug']
	src_jpg = f"raw-images/{slug}.jpg"
	src_png = f"raw-images/{slug}.png"
	dst_img = os.path.join(netscapeImgFolder, f"{slug}.gif")

	print(f"- {slug}")

	if os.path.exists(dst_img):
		print("   already exists, skipping...")
		continue

	src_img=""
	if os.path.exists(src_jpg):
		src_img = src_jpg
	elif os.path.exists(src_png):
		src_img = src_png
	else:
		print("   missing raw image!")
		raise hell

	print(src_img)
	print(dst_img)
	os.system(f"magick convert -quality 50 -resize 640X480 -dither FloydSteinberg -remap netscape: {src_img} {dst_img}")
	print(f"   src: {os.path.getsize(src_img): 10,}b")
	print(f"   dst: {os.path.getsize(dst_img): 10,}b")


sharedTemplate = {
	'meta-title': "executable.graphics",
	'meta-image': prods[0]['image_url'],

	'current-year': datetime.datetime.now().year,

	'meteoriks-juror-application-open': meteorikJurorApplicationOpen,
	'meteoriks-nominations-open': meteorikPublicNominationsOpen,

	'languages': languages,
	'translators': ', '.join(sorted(set(translators), key=str.casefold)),

	'external-url-meteoriks':        'https://meteoriks.org/',
	'external-url-meteoriks-jurors': 'https://meteoriks.org/taking_part/juror',
	'external-url-pouet':            'https://pouet.net/',
	'external-url-demozoo':          'https://demozoo.org/',

	'hash-fonts-css':            crc32_file(os.path.join(rootFolder, 'fonts.css')),
	'hash-style-css':            crc32_file(os.path.join(rootFolder, 'style.css')),
	'hash-favicon-ico':          crc32_file(os.path.join(rootFolder, 'favicon.ico')),
	'hash-apple-touch-icon-png': crc32_file(os.path.join(rootFolder, 'apple-touch-icon.png')),
	'hash-manifest-json':        crc32_file(os.path.join(rootFolder, 'manifest.json')),

	'svg-globe': open('icons/globe.svg').read(),
	'svg-moon':  open('icons/moon.svg').read()
}


print("applying templates...")
for lang in languages:
	localizedRootFolder = f"{rootFolder}{lang['root']}"
	localizedNetscapeFolder = f"{netscapeFolder}{lang['root']}"
	maybe_mkdir(localizedRootFolder)
	maybe_mkdir(localizedNetscapeFolder)

	with open(f"languages/{lang['id']}.json") as file:
		langData = json.load(file)

	def localize(text):
		keys = text.strip().split('.')
		value = langData
		for key in keys:
			if key not in value:
				if validateMissingLocalization:
					print(f"ERROR: Missing i18n key '{text}' for language '{lang['name']}'")
					quit(1)
				else:
					return f"[[{text.strip()}]]"
			value = value[key]
		return value

	def template_localize(text, render):
		return render(localize(text))

	langTemplate = { 'i18n': template_localize }

	indexData = sharedTemplate | langTemplate | {
		'meta-subtitle': localize('nav.gallery'),
		'meta-description': localize('meta.desc-gallery'),
		'meta-twitter-card-type': "summary_large_image",
		'currpage-canonical-filename' : '',
		'page-gallery': True,
		'entries': prods }

	meteoriksData = sharedTemplate | langTemplate | {
		'meta-subtitle': localize('nav.meteoriks'),
		'meta-description': localize('meta.desc-meteoriks'),
		'meta-twitter-card-type': "summary",
		'meta-image': meteorikProds[0]['image_url'],
		'currpage-canonical-filename' : 'meteoriks.html',
		'page-meteoriks': True,
		'entries': meteorikProds }

	aboutData = sharedTemplate | langTemplate | {
		'meta-subtitle': localize('nav.about'),
		'meta-description': localize('meta.desc-about'),
		'meta-twitter-card-type': "summary",
		'currpage-canonical-filename' : 'about.html',
		'page-about': True }

	with open('templates/index.mustache', 'r') as f:
		with open(os.path.join(localizedRootFolder, "index.html"), 'w') as fout:
			fout.write(chevron.render(
				template = f,
				partials_path = 'templates/',
				data = indexData))

	with open('templates/meteoriks.mustache', 'r') as f:
		with open(os.path.join(localizedRootFolder, "meteoriks.html"), 'w') as fout:
			fout.write(chevron.render(
				template = f,
				partials_path = 'templates/',
				data = meteoriksData))

	with open('templates/about.mustache', 'r') as f:
		with open(os.path.join(localizedRootFolder, "about.html"), 'w') as fout:
			fout.write(chevron.render(
				template = f,
				partials_path = 'templates/',
				data = aboutData))


	with open('templates/netscape/index.mustache', 'r') as f:
		with open(os.path.join(localizedNetscapeFolder, "index.html"), 'w') as fout:
			fout.write(chevron.render(
				template = f,
				partials_path = 'templates/netscape/',
				data = indexData))

	with open('templates/netscape/meteoriks.mustache', 'r') as f:
		with open(os.path.join(localizedNetscapeFolder, "meteoriks.html"), 'w') as fout:
			fout.write(chevron.render(
				template = f,
				partials_path = 'templates/netscape/',
				data = meteoriksData))

	with open('templates/netscape/about.mustache', 'r') as f:
		with open(os.path.join(localizedNetscapeFolder, "about.html"), 'w') as fout:
			fout.write(chevron.render(
				template = f,
				partials_path = 'templates/netscape/',
				data = aboutData))
