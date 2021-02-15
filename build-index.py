#!/usr/local/bin/python3
##!/usr/bin/python3

import chevron
import psycopg2

collection = [
	284903,	# containment
#	284906,	# Twigs
#	284907,	# The Stars Are Fcked
#	284905,	# Forgotten Artifact
#	284904,	# Backlight
#	282288,	# Suicidal Thoughts
	281254,	# Reconstruction
	280518,	# Enamel Pin
	280519,	# The Engineer
#	280517,	# End of an Era
#	280514,	# Eternal Forest
#	280515,	# Clowning Around
	280516,	# Siaphalis
#	279417,	# Storage Room
	279419,	# Phyllotaxes
#	279420,	# Cloth!!!
#	279421,	# Convergence
#	279418,	# Dungeon HMM3
#	279416,	# competition
#	279206,	# hunter
#	279211,	# orange in border
#	279205,	# Cable Tangle
#	279207,	# Dark Forest
	279174,	# Orange on a Table
#	278502,	# Ice core
#	278495,	# Octree
#	278498,	# Danmarksfärjan
	278496,	# Sunakai
#	277149,	# The Narrow Door
#	277150,	# Kunimitsu
#	277154,	# The Night Shift
	277158,	# Mathketball
	277156,	# Narcissus
#	277155,	# n-scape
#	277159,	# Mission Accomplished
#	277151,	# Access Control
#	277166,	# undefined symbol
	277152,	# Backbone
	277153,	# District 581c
	277165,	# Hoody
	277164,	# The Real Party is in Your Pocket
	277163,	# Waterfall
	277162,	# Primitive Portrait
#	277160,	# O'Hare
#	275127,	# Kuu
	273891,	# Long Way From Home
#	273936,	# Novae Terrae
#	273086,	# Forbidden Path
#	272690,	# Mach
#	272692,	# Meromorph
#	272691,	# Cozy
#	272689,	# Gummiklump
#	272688,	# Rauschabstand
#	272687,	# Apfelstrudel
#	272686,	# Foto von der Halle
#	270099,	# Brutal Knowledge
#	269426,	# Fakir
#	269425,	# test
#	266503,	# sler.py
#	205206,	# thinktank
#	205203,	# Spring Has Sprung
#	205204,	# Light at the end of the tunnel
#	205205,	# Snowoman
#	205005,	# M.M.W.
#	205003,	# teaser 02
#	205004,	# GhostTown
	202724,	# information network
#	202716,	# Jumacon 2019b
#	202715,	# Entrydisk
#	202717,	# The spice is vital
#	202718,	# 4kb
#	202719,	# Something blue
	202731,	# International Shipping
	202730,	# A Fish Best Served Cold
#	202720,	# 4k-nak indult, de 1.3k-nál meguntam.
#	202729,	# Is that It?
#	202728,	# 0DAY Cove
#	202721,	# ᴇ  s  ᴄ  ʜ  ᴇ  ʀ  ᴡ  ᴀ  ᴠ  ᴇ
#	202727,	# Pit Stop
#	202726,	# Penrose Pathtraced
#	173387,	# Riftonia by Rail
#	202722,	# Domo arigato, Mr. Roboto
	202723,	# Leap of Faith
	202725,	# Devour
#	201104,	# Meow
#	199014,	# Decrunch promo1
#	197936,	# loki mask
#	197934,	# Dithered XOR pattern
#	197726,	# Arca
#	197728,	# Blökchain
#	197727,	# Pavo
#	197725,	# Luminol
#	192514,	# Wonder Gal
#	192004,	# Jarig
#	188674,	# Postcard
#	187934,	# Step Inside and Bask in Luxury
#	185518,	# ÖÖÖstern
#	185522,	# Cenotaph for Soda
##	185523,	# Raumschiff Hunderprise
#	185521,	# Kyoto Temple
	185520,	# Unmortem
#	185519,	# No cube. Just panda.
#	185011,	# Decrunch 2048 Teaser
#	182548,	# Portrait
#	181800,	# Load "xmas",8,1
#	181847,	# Alkahest
#	181848,	# Spongeblob
#	274017,	# Face
#	178915,	# Rusty (Rust 2.0)
#	178204,	# Sunset
#	177769,	# Serenity
#	177060,	# Cityscape
#	176878,	# cornell box
#	176361,	# lena
#	174124,	# Menger
#	172760,	# simulacrum
#	172438,	# Postcard
#	170815,	# BuddhaBar
#	170817,	# Hubertus
#	170816,	# Curred Depression
#	170818,	# Urban Woods
#	170814,	# Ostehasi
	168486,	# Takochu Kiss
#	166664,	# Panacea
#	163769,	# Postcard
#	161850,	# Kellerkugel
#	160397,	# Playground Punk
#	160394,	# Postcard
#	160405,	# Norwegian Flower
#	160396,	# Last Sundown
#	160395,	# Coming Up?
#	158233,	# C64POWER
#	158232,	# Ghostland
#	158231,	# Rust
#	156956,	# Nummer 14
#	155138,	# Landing
#	155139,	# Evil Go
#	155136,	# Obey
#	155137,	# Human Flesh
#	155140,	# TRSI Temple
#	155141,	# Night Time
#	168570,	# Esperanta
#	152103,	# In den Hund!
#	152101,	# Kryptonite
#	152102,	# FRAME ZERO
	152100,	# daisy
#	141376,	# Come Play Our Organ
#	138433,	# HelloBoing
#	136280,	# Lotus
#	136278,	# Reactor
#	136277,	# Bat
#	136281,	# Lanchid
#	136275,	# Puskamma
#	136279,	# Biollante
#	136283,	# I must go, my planet needs me
#	136276,	# Nebula
#	136284,	# Who left that shit in our engine room?
	136347,	# Binah
#	135216,	# Late
#	135213,	# Kessler Syndrome
#	135214,	# Kiss The Floor, LOL
#	135215,	# The Nvengers
#	133232,	# 2-A
#	130082,	# Ferrofluid
#	130081,	# Technomimicry
#	130080,	# High Quality Cloud
#	130079,	# Heuschnecke
	201654,	# Decay
	124373,	# Future Decay
#	120274,	# Corrupted Jpeg
#	120273,	# Platypus is watching you
#	120243,	# Escher's Lucid Dream
#	120242,	# Forgiveness
#	116745,	# Pop Art
#	116744,	# Play It Again
#	116743,	# Stald
#	109155,	# M.o.o.n.
#	109154,	# Golden Age of Attentionwhore
#	109153,	# Drowning Forest
#	109156,	# Connossieur
#	109152,	# Elomen
#	109157,	# Painter's Teaser
#	104127,	# Dragon Obscura
#	104125,	# Lego Tutorial
#	104126,	# There
#	104124,	# Leggy
#	164540,	# Glow Effects
#	98187,	# Momentum
#	96460,	# Frohe Schreinachten
#	96459,	# Pingu
#	96461,	# The Gates of Hell
#	96462,	# In Soviet Russia...
#	87899,	# Mindpattern I
#	87901,	# Köttbullar mit Käseschmeck(TM)
#	87905,	# Random Something
#	87906,	# Grumpy
#	87907,	# Structured Lameness
#	87903,	# 31 Byte Sierpinski
	87897,	# 8 Ball
	87898,	# Milkdrop
#	87900,	# Flower
#	87902,	# Ein Penis macht noch keinen Sommer
#	87904,	# Little Owl
#	82879,	# Deadline
#	60079,	# WAS Poster
	60078,	# Brain Control
#	60084,	# The Ugly Truth
#	60085,	# Happy Happy Joy Joy Joy
#	60081,	# Magique
#	60080,	# Kacce
#	60082,	# PenRoseWhore
#	60083,	# Gæt en autonom (guess an autonomous)
#	47342,	# Weihnachtswurst
#	47341,	# The Careless Wizard
	43990,	# Fruxis
#	40781,	# Permutation 23
#	40780,	# Virus
#	40779,	# Perlin vor die Säule
#	69885,	# Pussy Riot
#	36762,	# Dawn In The Dead Sponge
#	36763,	# LIKE A SIR
#	36681,	# suiren
	266228,	# Strawberry
#	98010,	# Self Portrait
#	31739,	# Night Air
#	31735,	# Maybe The Real Party Is Outside
#	31740,	# Piggy
	31736,	# Megaherz
	31737,	# Sloppy Sketch of an Autumnal Afternoon
#	31738,	# Lobstervision
#	274161,	# Bubblez
#	23398,	# STH
#	54447,	# Menger search patrol
#	26846,	# Schweizer Verkehrsfuehrung
#	26844,	# Lost Marbles
#	26845,	# Massageball
#	269057,	# Forest of Life
	30004,	# Guideline Daily Amount?
#	279987,	# Marching Embryos
#	1148,	# Tummelplatz
#	1149,	# BITS5015 TUM Christmas
#	51469,	# Eyes
#	61119,	# vordhosbn
#	61121,	# Technologic
#	61120,	# Sunrise
#	38310,	# Code Recycling
#	70797,	# Novus vita
#	70798,	# Come play with us
#	266224,	# Army
#	266226,	# Flying Castle
#	925,	# Bloodsucker
#	922,	# Particle Physics
#	928,	# Back Off!
#	927,	# The King Is Dead... Long Live The King!
#	921,	# Spacepigs Are Forever
#	924,	# Naulos
#	923,	# Lighthouse
#	919,	# Burj Babil
#	920,	# Demoish Object
#	926,	# 8-bit Affection
#	70379,	# Mittagspause
#	70377,	# The Bridge
#	70378,	# Unfall beim Bügeln
#	98185,	# 64:1
#	51555,	# The Jam Factory
#	51556,	# Europa
#	51358,	# Hitachi compo
#	51356,	# Hedgehog
#	51355,	# Orange Dream
#	51354,	# Spilled
#	51357,	# My Garage
#	49972,	# LionRo4r
#	55045,	# Carry
#	55046,	# Cyku CC
#	55044,	# Life is good
#	55043,	# Jinn
#	55042,	# I felt the earth breathing
#	86749,	# Pandemic
#	86751,	# Rosone
#	86750,	# Ancient Secret
#	71454,	# Solitary Confinement
#	71460,	# Magical Checkers
#	1697,	# Patter
#	162891,	# jävla SIDfitta
#	1698,	# Smoking Kill
#	4990,	# CMath11gfx:wired
#	4989,	# Sollbruchstelle
#	4992,	# Woman
#	4991,	# Brix
#	70279,	# Gateway to Hell
#	70280,	# House at the Mountains
#	70278,	# Let Me Think
#	86370,	# Diffuse Dogfight
#	86371,	# Sælen på patrulje i Irak
#	51300,	# Red Planet
#	51301,	# Apfelmann
#	51298,	# bács-kiskun
##	51295,	# Organix
#	51297,	# Smart weapon
#	51296,	# last night a dj killed my demoskene
#	51299,	# Starting Grid
#	54346,	# 4d Quaternion Butterbrot Set
#	54345,	# klava
#	54347,	# opengl_render_test
#	54349,	# Oil trader's nightmare
#	54348,	# One Way Road
#	59055,	# Photon Race
#	59057,	# Donut Duck in Danger
#	59056,	# Stacheldraht
#	59054,	# Godspeed
#	75396,	# spAre
#	75397,	# True Lies
#	75394,	# Good morning, city!
#	75395,	# Ray Attack
#	75388,	# Still sucking PC
#	75389,	# 74
#	75391,	# Karkkimaa
##	54123,	# Slisesix
#	54124,	# Bubble
#	54125,	# LOLscape
#	1672,	# Ain't No Fool, Went To Clown School
#	1673,	# Raah
	4767,	# Ixaleno
#	4776,	# mPT
#	4769,	# b-meise
#	4775,	# CMath gfx
#	4772,	# lunreal
#	4768,	# Off The Shelf
#	4777,	# Blob bug wearing fedora and foliba!
#	4770,	# Yeeeees Yes!
#	4778,	# Girlie
#	4773,	# Couldn't come up with anything more cheesy
#	4774,	# Headfunk
#	4771,	# Versus
#	57055,	# Lonely Boat
#	57056,	# Think inside the box
#	57057,	# Minimalism
#	57058,	# inslexia
#	57059,	# The Mask
#	58999,	# Xdivzero
#	59002,	# Donut
#	59001,	# Abstract shit
	58998,	# Black Lines
#	59003,	# 3000 pixels (structered in some squares)
#	59000,	# Acid
#	59004,	# Black Square (no copy)
#	54268,	# Blubb
#	54269,	# Sky's The Limit
#	54265,	# Tiphareth
#	54270,	# tum
#	54267,	# v.o.x.e.L.
#	54266,	# 3 Minutes
#	58905,	# Der Wald Stirbt
#	58910,	# Kill all audio and lights
#	58909,	# Huhn
#	58906,	# Steintal
#	8204,	# Maybe The background should have been white
#	58907,	# Microcosm
#	10201,	# 2-million-Polys-and-some-Moonlight
#	10221,	# Jacubus the Serious Cube
#	10220,	# Der Thorax
#	58959,	# Carnegiea Gigantea
]



conn = psycopg2.connect(host="localhost", database="demozoo")
cur = conn.cursor()

availableprods = []

for demozoo_id in collection:
	cur.execute(
		'''
		SELECT productions_production.id, productions_production.release_date_date, productions_production.title
		FROM productions_production
		WHERE productions_production.id=%s
		ORDER BY productions_production.release_date_date DESC;
		''',
		(demozoo_id,))
	for row in cur.fetchall():
		availableprods.append({
			'id': row[0],
			'release_date': row[1],
			'title': row[2],
			'demozoo_url': f"https://demozoo.org/graphics/{row[0]}/"
		})


# get party name via competition placing
for prod in availableprods:
	cur.execute(
		'''
		SELECT parties_party.name
		FROM parties_party
		INNER JOIN parties_competition
		ON parties_party.id=parties_competition.party_id
		INNER JOIN parties_competitionplacing
		ON parties_competitionplacing.competition_id=parties_competition.id
		AND parties_competitionplacing.production_id=%s;
		''',
		(prod['id'],))
	partiesByCompetition = cur.fetchall()

	cur.execute(
		'''
		SELECT parties_party.name
		FROM parties_party
		INNER JOIN parties_party_releases
		ON parties_party.id=parties_party_releases.party_id
		AND parties_party_releases.production_id=%s;
		''',
		(prod['id'],))
	partiesByReleaseParty = cur.fetchall()

	if len(partiesByCompetition) > 0:
		prod['party'] = partiesByCompetition[0][0]
	elif len(partiesByReleaseParty) > 0:
		prod['party'] = partiesByReleaseParty[0][0]
	else:
		prod['party'] = f"{prod['release_date']:%B %Y}"


# get platform
for prod in availableprods:
	cur.execute(
		'''
		SELECT platforms_platform.name
		FROM platforms_platform
		INNER JOIN productions_production_platforms
		ON platforms_platform.id=productions_production_platforms.platform_id
		AND productions_production_platforms.production_id=%s;
		''',
		(prod['id'],))
	platformsForProd = cur.fetchall()
	if len(platformsForProd) > 1:
		prod['platform'] = '/'.join([platform[0] for platform in platformsForProd])
	elif len(platformsForProd) > 0:
		prod['platform'] = platformsForProd[0][0]
	else:
		prod['platform'] = 'NO ASSOCIATED PLATFORM(S)'

	prod['platform'] = prod['platform'].replace('Mac OS X', 'macOS')


# get screenshot
for prod in availableprods:
	cur.execute(
		'''
		SELECT productions_screenshot.original_url, productions_screenshot.original_width, productions_screenshot.original_height
		FROM productions_screenshot
		WHERE productions_screenshot.production_id=%s
		ORDER BY original_width DESC
		LIMIT 1;
		''',
		(prod['id'],))
	screenshotsForProd = cur.fetchall()
	if len(screenshotsForProd) > 0:
		prod['thumb_url'] = screenshotsForProd[0][0]
	else:
		prod['thumb_url'] = 'NO SCREENSHOT(S)'


# get screenshot
for prod in availableprods:
	cur.execute(
		'''
		SELECT productions_screenshot.original_url, productions_screenshot.original_width, productions_screenshot.original_height
		FROM productions_screenshot
		WHERE productions_screenshot.production_id=%s
		ORDER BY original_width DESC
		LIMIT 1;
		''',
		(prod['id'],))
	screenshotsForProd = cur.fetchall()
	if len(screenshotsForProd) > 0:
		prod['thumb_url'] = screenshotsForProd[0][0]
	else:
		prod['thumb_url'] = 'NO SCREENSHOT(S)'


# get authors
for prod in availableprods:
	authors = []

	cur.execute(
		'''
		SELECT demoscene_nick.name
		FROM demoscene_nick
		INNER JOIN productions_production_author_nicks
		ON demoscene_nick.id=productions_production_author_nicks.nick_id
		AND productions_production_author_nicks.production_id=%s;
		''',
		(prod['id'],))
	authorsForProd = cur.fetchall()
	if len(authorsForProd) > 0:
		authors.append(' + '.join([author[0] for author in authorsForProd]))

	cur.execute(
		'''
		SELECT demoscene_nick.name
		FROM demoscene_nick
		INNER JOIN productions_production_author_affiliation_nicks
		ON demoscene_nick.id=productions_production_author_affiliation_nicks.nick_id
		AND productions_production_author_affiliation_nicks.production_id=%s;
		''',
		(prod['id'],))
	groupsForProd = cur.fetchall()
	if len(groupsForProd) > 0:
		authors.append(' ^ '.join([group[0] for group in groupsForProd]))

	if len(authors) > 0:
		prod['author'] = ' / '.join(authors)
	else:
		prod['author'] = 'NO ASSOCIATED AUTHOR'


template_data = { 'entries': availableprods }

with open('index.mustache', 'r') as f:
	with open('index.html', 'w') as fout:
		fout.write(chevron.render(f, template_data))
