#!/usr/bin/env python
#DJANGO_SETTINGS_MODULE=d0018e_project.settings python populatedb.py
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'd0018e_project.settings'

from shopping.models import Customer, Category, Asset, Basket

categories = [
		('socks', 'Items to put on your feet'),
		('shoes', 'Items to put on your socks'),
		('fruit', "Eat this, it's good for you"),
		('telephones', 'Put one end against your ear and shout in the other'),
		]

for n, d in categories:
	c = Category(name=n, description=d)
	c.save()

sockCat = Category.objects.get(name='socks')
shoeCat = Category.objects.get(name='shoes')
fruitCat = Category.objects.get(name='fruit')
telCat = Category.objects.get(name='telephones')
products = [
		# (name, tagline, description, category, price, stock)
		('blue sock', 'An exquisite blue sock, fit for kings and queens alike', 
"""A sock is an item of clothing worn on the feet. This particular specimen is blue. 
The foot is among the heaviest producers of sweat in the body, as it is able to produce over 1 US pint (0.47 l) of perspiration per day. Socks help to absorb this sweat and draw it to areas where air can evaporate the perspiration. In cold environments, socks decrease the risk of frostbite. Its name is derived from the loose-fitting slipper, called a soccus in Latin, worn by Roman comic actors.""",
			sockCat, 10, 100),
		('green sock', 'A sock of the green persuasion', 
"""Green socks have evolved over the centuries from the earliest models which were made from animal skins gathered up and tied around the ankles. In the 8th century BC, the Ancient Greeks wore socks from matted animal hair for warmth. The Romans also wrapped their feet with leather or woven fabrics. By the 5th century AD, socks called "puttees" were worn by holy people in Europe to symbolise purity. By 1000 AD, socks became a symbol of wealth among the nobility. From the 16th century onwards, an ornamental design on the ankle or side of a sock has been called a clock.""",
			sockCat, 10, 100),
		('gray sock', 'This sock lacks color', 
"""Gray socks can be created from a wide variety of materials. Some of these materials are cotton, wool, nylon, acrylic, polyester, olefins, (such as polypropylene), or spandex. To get an increased level of softness other materials that might be used during the process can be silk, bamboo, linen, cashmere, or mohair. The color variety of sock choices can be any color that the designers intend to make the sock upon its creation. Sock 'coloring' can come in a wide range of colors. Sometimes art is also put onto socks to increase their appearance. Colored socks may be a key part of the uniforms for sports, allowing players teams to be distinguished when only their legs are clearly visible.""",
			sockCat, 10, 75),

		('boot', 'A boot (or two boots to be specific)', 
"""A boot is a type of footwear and a specific type of shoe. Most boots mainly cover the foot and the ankle and extend up the leg, sometimes as far as the knee or even the hip. Most boots have a heel that is clearly distinguishable from the rest of the sole, even if the two are made of one piece. Traditionally made of leather or rubber, modern boots are made from a variety of materials. Boots are worn both for their functionality - protecting the foot and leg from water, snow, mud or hazards or providing additional ankle support for strenuous activities - and for reasons of style and fashion. High-top athletic shoes are generally not considered boots, even though they do cover the ankle, primarily due to the absence of a distinct heel.""",
			shoeCat, 25, 100),
		('loafer', 'A loafer, slip it on and forget all about it', 
"""Slip-ons are typically low, lace-less shoes. The style most commonly seen, known as a loafer or slippers in American culture, has a moccasin construction. First appearing in the mid-1930s from Norway, Aurlandskoen (Aurland Shoe), they began as casual shoes, but have increased in popularity to the point of being worn in America with city lounge suits. They are worn in many situations in a wide variety of colours and designs, often featuring tassels on the front, or metal decorations (the 'Gucci' loafer).""",
			shoeCat, 20, 100),
		
		('banana', 'A yellow fruit, not very round at all', 
"""Banana is the common name for an edible fruit produced by several kinds of large herbaceous flowering plants of the genus Musa. The fruit is variable in size, color and firmness, but is usually elongated and curved, with soft flesh rich in starch covered with a rind which may be yellow, purple or red when ripe. The fruits grow in clusters hanging from the top of the plant. Almost all modern edible parthenocarpic (seedless) bananas come from two wild species - Musa acuminata and Musa balbisiana.""",
			fruitCat, 8, 200),
		('pear', 'This fruit is a bit more round than the banana', 
"""The pear is any of several tree and shrub species of genus Pyrus, in the family Rosaceae. It is also the name of the pomaceous fruit of these trees. Several species of pear are valued by humans for their edible fruit, while others are cultivated as ornamental trees. The genus Pyrus is classified in subtribe Pyrinae within tribe Pyreae.""",
			fruitCat, 7, 150),
		('apple', "Currently this is the roundest fruit we've got!", 
"""The apple is the pomaceous fruit of the apple tree, species Malus domestica in the rose family (Rosaceae). It is one of the most widely cultivated tree fruits, and the most widely known of the many members of genus Malus that are used by humans. Apples grow on small, deciduous trees. The tree originated in Western Asia, where its wild ancestor, Malus sieversii, is still found today. Apples have been grown for thousands of years in Asia and Europe, and were brought to North America by European colonists. Apples have been present in the mythology and religions of many cultures, including Norse, Greek and Christian traditions. In 2010, the fruit's genome was decoded, leading to new understandings of disease control and selective breeding in apple production.""",
			fruitCat, 6, 200),

		('fixed phone', "This is where it's at", 
"""The telephone, or phone, is a telecommunications device that transmits and receives sounds, usually the human voice. Telephones are a point-to-point communication system whose most basic function is to allow two people separated by large distances to talk to each other. Developed in the mid-1870s by Alexander Graham Bell and others, the telephone has long been considered indispensable to businesses, households and governments, is now one of the most common appliances in the developed world. The word "telephone" has been adapted to many languages and is now recognized around the world.""",
			telCat, 100, 50),
		('mobile phone', "Everywhere is where it's at", 
"""A mobile phone (also known as a cellular phone, cell phone and a hand phone) is a device that can make and receive telephone calls over a radio link while moving around a wide geographic area. It does so by connecting to a cellular network provided by a mobile phone operator, allowing access to the public telephone network. By contrast, a cordless telephone is used only within the short range of a single, private base station.""",
				telCat, 200, 300)
		]

# (name, tagline, description, category, price, stock)
for n, t, d, c, p, s in products:
	a = Asset(name=n, tagline=t, description=d, category=c, price=p, stock=s)
	a.save()


