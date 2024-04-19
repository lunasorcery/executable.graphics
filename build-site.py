#!/usr/bin/env python3

import os
import json
import shutil
import chevron
import binascii
import datetime
import subprocess
from PIL import Image


# fail the build if localization strings are missing
validateMissingLocalization = False


# Seasonal events
meteorikJurorApplicationOpen = False
meteorikPublicNominationsOpen = False


def maybe_mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)


def crc32_file(filename):
	buf = open(filename,'rb').read()
	buf = (binascii.crc32(buf) & 0xffffffff)
	return f"{buf:08x}"


def get_ext(path: str):
    return os.path.splitext(path)[1]


def find_raw_image_for_prod(prod):
	slug = prod['slug']
	src_jpg = f"raw-images/{slug}.jpg"
	src_png = f"raw-images/{slug}.png"
	
	if os.path.exists(src_jpg):
		return src_jpg
	if os.path.exists(src_png):
		return src_png
	print(f"failed to find raw image for prod '{slug}'")
	exit(1)


def check_transcode_result(result, dst_path):
    if result.returncode != 0 or not os.path.exists(dst_path) or os.stat(dst_path).st_size == 0:
        print(f"- transcode failed!")
        print(f"- return code: {result.returncode}")
        print(f"- output file exists: {os.path.exists(dst_path)}")
        print(f"- output file size: {os.path.getsize(dst_path)}")
        sys.exit(1)


def transcode_to_jpg(src_path: str, dst_path: str):
	result = subprocess.run(['convert', '-interlace', 'Plane', '-quality', '95', src_path, dst_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	check_transcode_result(result, dst_path)

    # if we've made it bigger, just copy the original instead
	if get_ext(src_path) in ['.jpg','.jpeg'] and os.path.getsize(dst_path) > os.path.getsize(src_path):
		shutil.copyfile(src_path, dst_path)


def transcode_to_avif(src_path: str, dst_path: str):
    result = subprocess.run(['avifenc', '-q', '90', src_path, '-o', dst_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check_transcode_result(result, dst_path)


def transcode_to_webp(src_path: str, dst_path: str):
	result = subprocess.run(['cwebp', '-metadata', 'all', '-q', '90', src_path, '-o', dst_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	check_transcode_result(result, dst_path)


def get_image_dimensions(local_img_path: str):
    img = Image.open(local_img_path)
    return img.size


def convert_image_for_prod(prod):
	slug = prod['slug']
	print(f"- {slug}")

	src = find_raw_image_for_prod(prod)
	width,height = get_image_dimensions(src)
	prod['image_width'] = width
	prod['image_height'] = height

	if not prod.get('transcode',True):
		dst_filename = f"img/{slug}{get_ext(src)}"
		print(f"  -> {dst_filename}")
		shutil.copy(src, f"gen/{dst_filename}")
		prod[f"image_url"] = f"/{dst_filename}"
	else:
		transcodes = [
			('image_url', transcode_to_jpg, f"img/{slug}.jpg"),
			('image_url_avif', transcode_to_avif, f"img/{slug}.avif"),
			('image_url_webp', transcode_to_webp, f"img/{slug}.webp"),
		]
		for field, transcode_func, dst_filename in transcodes:
			print(f"  -> {dst_filename}")
			dst_filepath = f"gen/{dst_filename}"
			if not os.path.exists(dst_filepath):
				transcode_func(src, dst_filepath)
			prod[field] = f"/{dst_filename}"


def main():
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
	for prod in prods:
		if 'meteorik-type' in prod:
			prod['meteorik-winner']   = (prod['meteorik-type'] == 'winner')
			prod['meteorik-runnerup'] = (prod['meteorik-type'] == 'runnerup')
			prod['meteorik-nominee']  = (prod['meteorik-type'] == 'nominee')
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
		'script.js',
		'manifest.json',
		'Muli-Regular.ttf',
		'Muli-Bold.ttf',
		'Muli-ExtraBoldItalic.ttf',
	]
	for asset in staticAssets:
		shutil.copyfile(f'static/{asset}', f'gen/{asset}')


	print("processing CSS...")
	cssFiles = [
		'style.scss'
	]
	for asset in cssFiles:
		assetOut = f"gen/{asset.replace('.scss','.css')}"
		print(f"{asset} -> {assetOut}")
		# requires dart sass
		subprocess.run(['sass', asset, assetOut])
		os.remove(f"{assetOut}.map")


	print("converting images...")
	for prod in prods:
		convert_image_for_prod(prod)


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

		'hash-fonts-css':            crc32_file('gen/fonts.css'),
		'hash-style-css':            crc32_file('gen/style.css'),
		'hash-favicon-ico':          crc32_file('gen/favicon.ico'),
		'hash-apple-touch-icon-png': crc32_file('gen/apple-touch-icon.png'),
		'hash-manifest-json':        crc32_file('gen/manifest.json'),

		'svg-globe': open('icons/globe.svg').read(),
		'svg-moon':  open('icons/moon.svg').read()
	}


	print("applying templates...")
	for lang in languages:
		outdir = f"gen{lang['root']}"
		maybe_mkdir(outdir)
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

		with open('templates/index.mustache', 'r') as f:
			with open(f"{outdir}/index.html", 'w') as fout:
				fout.write(chevron.render(
					template = f,
					partials_path = 'templates/',
					data = sharedTemplate | langTemplate | {
						'meta-subtitle': localize('nav.gallery'),
						'meta-description': localize('meta.desc-gallery'),
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
						'meta-subtitle': localize('nav.meteoriks'),
						'meta-description': localize('meta.desc-meteoriks'),
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
						'meta-subtitle': localize('nav.about'),
						'meta-description': localize('meta.desc-about'),
						'meta-twitter-card-type': "summary",
						'currpage-canonical-filename' : 'about.html',
						'page-about': True }))

if __name__ == "__main__":
	main()
