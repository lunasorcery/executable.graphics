#!/usr/bin/env python3

import os
import json
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


# WIP features
enableLanguageDropdown = False
validateMissingLocalization = True



with open('languages/list.json') as file:
	languages = json.load(file)

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


maybe_mkdir('gen/')
maybe_mkdir('gen/img/')


print("generating icons...")
if not os.path.exists('gen/apple-touch-icon.png'):
	os.system(f"inkscape -w 160 -h 160 -o gen/apple-touch-icon.png icons/mobile-icon.svg")
if not os.path.exists('gen/favicon.ico'):
	faviconSizes = [16,32,48]
	for size in faviconSizes:
		os.system(f"inkscape -w {size} -h {size} -o gen/favicon-{size}.png icons/favicon.svg")
	faviconPngs = [f"gen/favicon-{size}.png" for size in faviconSizes]
	os.system(f"convert {' '.join(faviconPngs)} gen/favicon.ico")
	for faviconPng in faviconPngs:
		os.remove(faviconPng)


print("copying static assets...")
staticAssets = [
	'fonts.css',
	'style.css',
	'script.js',
	'manifest.json',
	'Muli-Regular.ttf',
	'Muli-Bold.ttf',
	'Muli-ExtraBoldItalic.ttf',
]
for asset in staticAssets:
	shutil.copyfile(asset, f'gen/{asset}')


print("converting images...")
for idx,prod in enumerate(prods):
	slug = prod['slug']
	src_jpg = f"raw-images/{slug}.jpg"
	src_png = f"raw-images/{slug}.png"
	dst_jpg = f"gen/img/{slug}.jpg"
	dst_png = f"gen/img/{slug}.png"

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
		os.system(f"convert -interlace Plane -quality 95 {src_jpg} {dst_jpg}")
		prods[idx]['image_url'] = f"img/{slug}.jpg"

		# if we've made it bigger, ditch the quality=95 flag
		if os.path.getsize(dst_jpg) > os.path.getsize(src_jpg):
			os.system(f"convert -interlace Plane {src_jpg} {dst_jpg}")

		print(f"   src_jpg: {os.path.getsize(src_jpg): 10,}b")
		print(f"   dst_jpg: {os.path.getsize(dst_jpg): 10,}b")

	elif os.path.exists(src_png):
		# if the source is a png, resave it as a jpg
		os.system(f"convert -interlace Plane -quality 95 {src_png} {dst_jpg}")

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


sharedTemplate = {
	'meta-title': "executable.graphics",
	'meta-image': prods[0]['image_url'],

	'current-year': datetime.datetime.now().year,

	'meteoriks-juror-application-open': False,
	'meteoriks-nominations-open': False,

	'enable-language-dropdown': enableLanguageDropdown,
	'languages': languages,

	'external-url-meteoriks':        'https://meteoriks.org/',
	'external-url-meteoriks-jurors': 'https://meteoriks.org/taking_part/juror',
	'external-url-pouet':            'https://pouet.net/',
	'external-url-demozoo':          'https://demozoo.org/',

	'hash-fonts-css':            crc32_file('fonts.css'),
	'hash-style-css':            crc32_file('style.css'),
	'hash-favicon-ico':          crc32_file('gen/favicon.ico'),
	'hash-apple-touch-icon-png': crc32_file('gen/apple-touch-icon.png'),
	'hash-manifest-json':        crc32_file('manifest.json'),

	'svg-globe': open('icons/globe.svg').read(),
	'svg-moon':  open('icons/moon.svg').read()
}


print("applying templates...")
for lang in languages:
	outdir = f"gen{lang['root']}"
	maybe_mkdir(outdir)
	with open(f"languages/{lang['id']}.json") as file:
		langData = json.load(file)

	def template_localize(text, render):
		keys = text.strip().split('.')
		value = langData
		for key in keys:
			if key not in value:
				if validateMissingLocalization:
					print(f"ERROR: Missing i18n key '{text}' for language '{lang['name']}'")
					quit()
				else:
					return f"[[{text.strip()}]]"
			value = value[key]
		return render(value)

	langTemplate = { 'i18n': template_localize }

	with open('templates/index.mustache', 'r') as f:
		with open(f"{outdir}/index.html", 'w') as fout:
			fout.write(chevron.render(
				template = f,
				partials_path = 'templates/',
				data = sharedTemplate | langTemplate | {
					'meta-description': "A curated gallery of 4K Executable Graphics works from the demoscene.",
					'meta-twitter-card-type': "summary_large_image",
					'currpage-canonical-filename' : '',
					'page-gallery': True,
					'entries': prods }))

	with open('templates/meteoriks.mustache', 'r') as f:
		with open(f"{outdir}/meteoriks.html", 'w') as fout:
			fout.write(chevron.render(
				template = f,
				partials_path = 'templates/',
				data = sharedTemplate | langTemplate | {
					'meta-subtitle': "Meteoriks",
					'meta-description': "Nominees and winners of the 'Best Executable Graphics' Meteorik award.",
					'meta-twitter-card-type': "summary",
					'meta-image': meteorikProds[0]['image_url'],
					'currpage-canonical-filename' : 'meteoriks.html',
					'page-meteoriks': True,
					'entries': meteorikProds }))

	with open('templates/about.mustache', 'r') as f:
		with open(f"{outdir}/about.html", 'w') as fout:
			fout.write(chevron.render(
				template = f,
				partials_path = 'templates/',
				data = sharedTemplate | langTemplate | {
					'meta-subtitle': "About",
					'meta-description': "What is Executable Graphics?",
					'meta-twitter-card-type': "summary",
					'currpage-canonical-filename' : 'about.html',
					'page-about': True }))
