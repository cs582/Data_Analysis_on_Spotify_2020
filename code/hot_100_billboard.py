import billboard
chart = billboard.ChartData('hot-100')

for song in chart[:10]:
	print(song.title)
	print(song.artist)