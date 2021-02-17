#!/usr/bin/env python3

import os
import shutil
import chevron
from wand.image import Image


def maybemkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)


prods = [
	{
		'slug': 'blackpawn-containment',
		'demozoo_url': 'https://demozoo.org/graphics/284903/',
		'author': 'Blackpawn',
		'title': 'containment',
		'party': 'Inércia Demoparty 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'csc-reconstruction',
		'demozoo_url': 'https://demozoo.org/graphics/281254/',
		'author': 'Church of the Spinning Cube',
		'title': 'Reconstruction',
		'party': 'FieldFX 2020',
		'platform': 'macOS',
	},
	{
		'slug': 'blackle-enamel-pin',
		'demozoo_url': 'https://demozoo.org/graphics/280518/',
		'author': 'Blackle / Suricrasia Online',
		'title': 'Enamel Pin',
		'party': 'Solskogen 2020',
		'platform': 'Linux',
	},
	{
		'slug': 'bitnenfer-the-engineer',
		'demozoo_url': 'https://demozoo.org/graphics/280519/',
		'author': 'Bitnenfer / Latitude Independent Association',
		'title': 'The Engineer',
		'party': 'Solskogen 2020',
		'platform': 'Windows',
		'meteorik-year': 2021,
		'meteorik-type': 'nominee',
	},
	{
		'slug': 'wrigher-siaphalis',
		'demozoo_url': 'https://demozoo.org/graphics/280516/',
		'author': 'Wrighter',
		'title': 'Siaphalis',
		'party': 'Solskogen 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'tdhooper-phyllotaxes',
		'demozoo_url': 'https://demozoo.org/graphics/279419/',
		'author': 'tdhooper',
		'title': 'Phyllotaxes',
		'party': 'Nova Online 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'bitnenfer-orange-on-a-table',
		'demozoo_url': 'https://demozoo.org/graphics/279174/',
		'author': 'Bitnenfer / Latitude Independent Association',
		'title': 'Orange on a Table',
		'party': '@Party 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'wrighter-sunakai',
		'demozoo_url': 'https://demozoo.org/graphics/278496/',
		'author': 'Wrighter',
		'title': 'Sunakai',
		'party': 'Outline Online 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'mercury-mathketball',
		'demozoo_url': 'https://demozoo.org/graphics/277158/',
		'author': 'Mercury',
		'title': 'Mathketball',
		'party': 'Revision Online 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'pbr-narcissus',
		'demozoo_url': 'https://demozoo.org/graphics/277156/',
		'author': 'Beople / Prismbeings',
		'title': 'Narcissus',
		'party': 'Revision Online 2020',
		'platform': 'Windows',
		'meteorik-year': 2021,
		'meteorik-type': 'nominee',
	},
	{
		'slug': 'cpdt-backbone',
		'demozoo_url': 'https://demozoo.org/graphics/277152/',
		'author': 'cpdt / Monad',
		'title': 'Backbone',
		'party': 'Revision Online 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'musk-district-581c',
		'demozoo_url': 'https://demozoo.org/graphics/277153/',
		'author': 'Musk',
		'title': 'District 581c',
		'party': 'Revision Online 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'iq-hoody',
		'demozoo_url': 'https://demozoo.org/graphics/277165/',
		'author': 'iq / Rgba',
		'title': 'Hoody',
		'party': 'Revision Online 2020',
		'platform': 'Windows',
		'meteorik-year': 2021,
		'meteorik-type': 'winner',
	},
	{
		'slug': 'fizzer-the-real-party-is-in-your-pocket',
		'demozoo_url': 'https://demozoo.org/graphics/277164/',
		'author': 'Fizzer',
		'title': 'The Real Party is in Your Pocket',
		'party': 'Revision Online 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'nusan-waterfall',
		'demozoo_url': 'https://demozoo.org/graphics/277163/',
		'author': 'NuSan',
		'title': 'Waterfall',
		'party': 'Revision Online 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'yx-primitive-portrait',
		'demozoo_url': 'https://demozoo.org/graphics/277162/',
		'author': 'yx / Polarity',
		'title': 'Primitive Portrait',
		'party': 'Revision Online 2020',
		'platform': 'Windows',
		'meteorik-year': 2021,
		'meteorik-type': 'nominee',
	},
	{
		'slug': 'yx-long-way-from-home',
		'demozoo_url': 'https://demozoo.org/graphics/273891/',
		'author': 'yx / Polarity',
		'title': 'Long Way From Home',
		'party': 'SynchroNY 2020',
		'platform': 'Windows',
	},
	{
		'slug': 'musk-information-network',
		'demozoo_url': 'https://demozoo.org/graphics/202724/',
		'author': 'Musk',
		'title': 'information network',
		'party': 'Revision 2019',
		'platform': 'Windows',
	},
	{
		'slug': 'blackle-international-shipping',
		'demozoo_url': 'https://demozoo.org/graphics/202731/',
		'author': 'Blackle / Suricrasia Online',
		'title': 'International Shipping',
		'party': 'Revision 2019',
		'platform': 'Windows/Linux',
	},
	{
		'slug': 'fizzer-fish-best-served-cold',
		'demozoo_url': 'https://demozoo.org/graphics/202730/',
		'author': 'Fizzer',
		'title': 'A Fish Best Served Cold',
		'party': 'Revision 2019',
		'platform': 'Windows',
	},
	{
		'slug': 'boyc-leap-of-faith',
		'demozoo_url': 'https://demozoo.org/graphics/202723/',
		'author': 'BoyC',
		'title': 'Leap of Faith',
		'party': 'Revision 2019',
		'platform': 'Windows',
	},
	{
		'slug': 'pbr-devour',
		'demozoo_url': 'https://demozoo.org/graphics/202725/',
		'author': 'Prismbeings',
		'title': 'Devour',
		'party': 'Revision 2019',
		'platform': 'Windows',
	},
	{
		'slug': 'tomtebloss-unmortem',
		'demozoo_url': 'https://demozoo.org/graphics/185520/',
		'author': 'Tomtebloss / Fairlight',
		'title': 'Unmortem',
		'party': 'Revision 2018',
		'platform': 'Windows',
	},
	{
		'slug': 'fizzer-takochu-kiss',
		'demozoo_url': 'https://demozoo.org/graphics/168486/',
		'author': 'Fizzer',
		'title': 'Takochu Kiss',
		'party': 'TokyoDemoFest 2017',
		'platform': 'Windows',
	},
	{
		'slug': 'mercury-daisy',
		'demozoo_url': 'https://demozoo.org/graphics/152100/',
		'author': 'las + abductee / Mercury',
		'title': 'daisy',
		'party': 'Under Construction 2015',
		'platform': 'Windows',
	},
	{
		'slug': 'speckdrumm-binah',
		'demozoo_url': 'https://demozoo.org/graphics/136347/',
		'author': 'Speckdrumm',
		'title': 'Binah',
		'party': 'Revision 2015',
		'platform': 'Windows',
	},
	{
		'slug': 'fizzer-decay',
		'demozoo_url': 'https://demozoo.org/graphics/201654/',
		'author': 'Fizzer',
		'title': 'Decay',
		'party': 'November 2014',
		'platform': 'Windows',
	},
	{
		'slug': 'drift-future-decay',
		'demozoo_url': 'https://demozoo.org/graphics/124373/',
		'author': 'Drift',
		'title': 'Future Decay',
		'party': 'TRSAC 2014',
		'platform': 'Windows',
	},
	{
		'slug': 'westlicht-8ball',
		'demozoo_url': 'https://demozoo.org/graphics/87897/',
		'author': 'Westlicht / Horology',
		'title': '8 Ball',
		'party': 'Demodays 2013',
		'platform': 'Windows',
	},
	{
		'slug': 'noobody-milkdrop',
		'demozoo_url': 'https://demozoo.org/graphics/87898/',
		'author': 'Noobody / Horology',
		'title': 'Milkdrop',
		'party': 'Demodays 2013',
		'platform': 'Windows',
	},
	{
		'slug': 'mercury-brain-control',
		'demozoo_url': 'https://demozoo.org/graphics/60078/',
		'author': 'Mercury',
		'title': 'Brain Control',
		'party': 'Revision 2013',
		'platform': 'Windows',
	},
	{
		'slug': 'iq-fruxis',
		'demozoo_url': 'https://demozoo.org/graphics/43990/',
		'author': 'iq / Rgba',
		'title': 'Fruxis',
		'party': 'TRSAC 2012',
		'platform': 'Windows',
	},
	{
		'slug': 'rebels-strawberry',
		'demozoo_url': 'https://demozoo.org/graphics/266228/',
		'author': 'Rebels',
		'title': 'Strawberry',
		'party': 'May 2012',
		'platform': 'Windows',
	},
	{
		'slug': 'akad-megaherz',
		'demozoo_url': 'https://demozoo.org/graphics/31736/',
		'author': 'Abgestuerzte Akademiker',
		'title': 'Megaherz',
		'party': 'Revision 2012',
		'platform': 'Windows',
	},
	{
		'slug': 'mindo-sloppy-sketch',
		'demozoo_url': 'https://demozoo.org/graphics/31737/',
		'author': 'Mindo / Titan',
		'title': 'Sloppy Sketch of an Autumnal Afternoon',
		'party': 'Revision 2012',
		'platform': 'Windows',
	},
	{
		'slug': 'psycho-guideline-daily-amount',
		'demozoo_url': 'https://demozoo.org/graphics/30004/',
		'author': 'Psycho / Loonies',
		'title': 'Guideline Daily Amount?',
		'party': 'Solskogen 2011',
		'platform': 'Windows',
	},
	{
		'slug': 'rgba-ixaleno',
		'demozoo_url': 'https://demozoo.org/graphics/4767/',
		'author': 'Rgba',
		'title': 'Ixaleno',
		'party': 'Breakpoint 2008',
		'platform': 'Windows',
	},
	{
		'slug': 'minas-black-lines',
		'demozoo_url': 'https://demozoo.org/graphics/58998/',
		'author': 'Minas / Calodox',
		'title': 'Black Lines',
		'party': 'Buenzli 2007 (16)',
		'platform': 'Windows',
	},
]

maybemkdir('gen/')
maybemkdir('gen/img/')

shutil.copyfile('style.css', 'gen/style.css')
shutil.copyfile('script.js', 'gen/script.js')
shutil.copyfile('favicon.ico', 'gen/favicon.ico')

for idx,prod in enumerate(prods):
	slug = prod['slug']
	src_jpg = f"raw-images/{slug}.jpg"
	src_png = f"raw-images/{slug}.png"
	dst_jpg = f"gen/img/{slug}.jpg"
	dst_png = f"gen/img/{slug}.png"

	if os.path.exists(dst_jpg):
		prods[idx]['image_url'] = f"img/{slug}.jpg"
		continue
	elif os.path.exists(dst_png):
		prods[idx]['image_url'] = f"img/{slug}.png"
		continue

	if os.path.exists(src_jpg):
		# if there source is a jpg, use that
		shutil.copyfile(src_jpg, dst_jpg)
		prods[idx]['image_url'] = f"img/{slug}.jpg"
	elif os.path.exists(src_png):
		# if the source is a png, resave it as a jpg
		with Image(filename=src_png) as img:
			img.compression_quality = 95
			img.save(filename=dst_jpg)

		# ...and use the smaller one
		if os.path.getsize(dst_jpg) < os.path.getsize(src_png):
			prods[idx]['image_url'] = f"img/{slug}.jpg"
		else:
			os.remove(dst_jpg)
			shutil.copyfile(src_png, dst_png)
			prods[idx]['image_url'] = f"img/{slug}.png"
	else:
		print(f"missing raw image for {slug}!")
		raise hell

for idx,prod in enumerate(prods):
	if 'meteorik-type' in prod:
		prods[idx]['meteorik-winner']  = (prod['meteorik-type'] == 'winner')
		prods[idx]['meteorik-nominee'] = (prod['meteorik-type'] == 'nominee')

with open('index.mustache', 'r') as f:
	with open('gen/index.html', 'w') as fout:
		fout.write(chevron.render(f, { 'page-gallery': True, 'entries': prods }))

meteorikProds = sorted([prod for prod in prods if 'meteorik-year' in prod], key = lambda x: (x['meteorik-year'], x['meteorik-type']), reverse=True)
with open('meteoriks.mustache', 'r') as f:
	with open('gen/meteoriks.html', 'w') as fout:
		fout.write(chevron.render(f, { 'page-meteoriks': True, 'entries': meteorikProds }))

with open('about.mustache', 'r') as f:
	with open('gen/about.html', 'w') as fout:
		fout.write(chevron.render(f, { 'page-about': True }))
