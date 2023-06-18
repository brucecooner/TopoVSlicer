#	TODO:
#	* added elevation below minimum
# TODO: style options


# seemingly arbitrary scale I got from looking at an SVG generated by inkscape

#  -----------------------------------------------------------------
def inches_to_pixels(coord):
	inches_to_pixels_scale = 25.4
	return coord * inches_to_pixels_scale

# ------------------------------------------------------------------
def snakeCase(s):
	from re import sub
	return '_'.join(
		sub('([A-Z][a-z]+)', r' \1',
		sub('([A-Z]+)', r' \1',
		s.replace('-', ' '))).split()).lower()

#  -----------------------------------------------------------------
# doesn't speak horizontal or vertical line (yet)
# TODO: style options
class InkscapePath:
	# must supply starting coordinates
	def __init__(self, start_x, start_y) -> None:
		self.path_text = f"M {inches_to_pixels(start_x)},{inches_to_pixels(start_y)}"

		# hex
		self.color_string = "000000" # black

	def setColor(self, color_string):
		self.color_string = color_string

	def draw(self, x,y):
		self.path_text += f" {inches_to_pixels(x)},{inches_to_pixels(y)}"

	def Ldraw(self, x,y):
		self.path_text += f"L {inches_to_pixels(x)},{inches_to_pixels(y)}"

	def Qdraw(self, x,y, cx, cy):
		self.path_text += f" Q{inches_to_pixels(cx)},{inches_to_pixels(cy)} {inches_to_pixels(x)},{inches_to_pixels(y)}"

	def Tdraw(self, x,y):
		self.path_text += f" T{inches_to_pixels(x)},{inches_to_pixels(y)}"

	def Cdraw(self, c1x, c1y, c2x, c2y, x,y):
		self.path_text += f" C{inches_to_pixels(c1x)},{inches_to_pixels(c1y)} {inches_to_pixels(c2x)},{inches_to_pixels(c2y)} {inches_to_pixels(x)},{inches_to_pixels(y)}"

	def Sdraw(self, x,y, cx, cy):
		self.path_text += f" Q{inches_to_pixels(cx)},{inches_to_pixels(cy)} {inches_to_pixels(x)},{inches_to_pixels(y)}"

	def move(self, x,y):
		self.path_text += f" M {inches_to_pixels(x)},{inches_to_pixels(y)}"

	def close(self):
		self.path_text += " Z"

	def style_text(self):
		return f'style="opacity:0.981447;fill:none;fill-opacity:0.992157;stroke:#{self.color_string};stroke-width:0.5"'

	#  -----------------------------
	def write(self, file_obj):
		node_text = f'<path\n\
       {self.style_text()}\n\
       d="{self.path_text}"/>\n'	# note the " Z" was removed here, so paths don't close!
		
		file_obj.write(node_text)

#  -----------------------------------------------------------------
class InkscapeLayer:
	def __init__(self, layer_name) -> None:
		self.name = layer_name
		self.nodes = []

	#  -----------------------------
	def add_node(self, new_node):
		self.nodes.append(new_node)

	#  -----------------------------
	def write(self, file_obj):
		file_obj.write(f'<g\n\
inkscape:label="{self.name}"\n\
inkscape:groupmode="layer"\n\
id="{snakeCase(self.name)}">\n')

		# write nodes
		for cur_node in self.nodes:
			cur_node.write(file_obj)

		file_obj.write('</g>\n')

#  -----------------------------------------------------------------
class InkscapeSVG:
	def __init__(self) -> None:
		self.nodes = []

	#  ------------------------------------
	@staticmethod
	def XMLTag():
		return f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n'

	#  -----------------------------------------------------------------
	@staticmethod
	def namedViewNode():
		return f'<sodipodi:namedview\n\
id="namedview7"\n\
pagecolor="#ffffff"\n\
bordercolor="#cccccc"\n\
borderopacity="1"\n\
inkscape:pageshadow="0"\n\
inkscape:pageopacity="1"\n\
inkscape:pagecheckerboard="0"\n\
inkscape:document-units="in"\n\
showgrid="false"\n\
units="in"/>\n'

	#  -----------------------------
	def addNode(self, new_node):
		self.nodes.append(new_node)

	#  -----------------------------
	def open_tag(self, file_name):
		# the viewBox dimensions are some sort of magic that fixes everything
		node_text = f'<svg\n\
width="20in"\n\
height="12in"\n\
viewBox="0 0 508.00001 304.8"\n\
version="1.1"\n\
id="svg5"\n\
inkscape:version="1.1 (c68e22c387, 2021-05-23)"\n\
sodipodi:docname="{file_name}"\n\
xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n\
xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"\n\
xmlns="http://www.w3.org/2000/svg"\n\
xmlns:svg="http://www.w3.org/2000/svg">\n'

		return node_text

	#  -----------------------------
	def close_tag(self):
		return '</svg>'

	#  -----------------------------
	def write(self, filename):
		full_filename = filename + ".svg"
		with open(filename + ".svg", "w") as file_obj:
			file_obj.write(self.XMLTag())

			# opening tag
			file_obj.write(self.open_tag(full_filename))
			file_obj.write(self.namedViewNode())
			# write nodes
			for cur_node in self.nodes:
				cur_node.write(file_obj)

			# closing tag
			file_obj.write(self.close_tag())


