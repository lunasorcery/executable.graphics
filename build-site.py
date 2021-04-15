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


# load prods
with open('prods.json') as file:
	prods = json.load(file)

prods = [prod for prod in prods if (not ('hidden' in prod)) or (not prod['hidden'])]

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
	os.system(f"inkscape -w 160 -h 160 -o gen/apple-touch-icon.png favicon.svg")
if not os.path.exists('gen/favicon.ico'):
	faviconSizes = [16,32,48]
	for size in faviconSizes:
		os.system(f"inkscape -w {size} -h {size} -o gen/favicon-{size}.png favicon.svg")
	faviconPngs = [f"gen/favicon-{size}.png" for size in faviconSizes]
	print(f"convert {' '.join(faviconPngs)} gen/favicon.ico")
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
		prods[idx]['image_url'] = f"img/{slug}.jpg"
		print("   already exists, skipping...")
		continue
	elif os.path.exists(dst_png):
		prods[idx]['image_url'] = f"img/{slug}.png"
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
			prods[idx]['image_url'] = f"img/{slug}.jpg"
			print(f"   dst_jpg: {os.path.getsize(dst_jpg): 10,}b")
		else:
			os.remove(dst_jpg)
			shutil.copyfile(src_png, dst_png)
			prods[idx]['image_url'] = f"img/{slug}.png"
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
	'hash-fonts-css':            crc32_file('fonts.css'),
	'hash-style-css':            crc32_file('style.css'),
	'hash-favicon-ico':          crc32_file('gen/favicon.ico'),
	'hash-apple-touch-icon-png': crc32_file('gen/apple-touch-icon.png'),
	'hash-manifest-json':        crc32_file('manifest.json'),
}


print("applying templates...")
with open('index.mustache', 'r') as f:
	with open('gen/index.html', 'w') as fout:
		fout.write(chevron.render(f, sharedTemplate | {
			'meta-description': "A curated gallery of 4K Executable Graphics works from the demoscene.",
			'meta-twitter-card-type': "summary_large_image",
			'page-gallery': True,
			'entries': prods }))

with open('meteoriks.mustache', 'r') as f:
	with open('gen/meteoriks.html', 'w') as fout:
		fout.write(chevron.render(f, sharedTemplate | {
			'meta-subtitle': "Meteoriks",
			'meta-description': "Nominees and winners of the 'Best Executable Graphics' Meteorik award.",
			'meta-twitter-card-type': "summary",
			'meta-image': meteorikProds[0]['image_url'],
			'page-meteoriks': True,
			'entries': meteorikProds }))

with open('about.mustache', 'r') as f:
	with open('gen/about.html', 'w') as fout:
		fout.write(chevron.render(f, sharedTemplate | {
			'meta-subtitle': "About",
			'meta-description': "What is Executable Graphics?",
			'meta-twitter-card-type': "summary",
			'page-about': True }))
