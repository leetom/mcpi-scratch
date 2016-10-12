#!/bin/env python
#-*- encoding:gbk -*-
### python 点阵字体
import os

class PixelText:

	def __init__(self, text, font="simsun12.fon"):
		self.text = text.encode('gbk')
		current_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
		self.font = current_path + font

	def getPixelList(self):
		text = self.text
		font_file_name = self.font

		font_width = 12
		font_height = 12
		start_offset = 0


		fp = open(font_file_name, 'rb')

		offset_size = font_width * font_height / 8 #计算出一个字的偏移量

		string_size = font_width * font_height

		bin_array = []
		i = 0
		while i < len(text):
			bin_str = ''
			if ord(text[i]) > 160:
				offset = ((ord(text[i]) - 0xa1) * 94 + ord(text[i + 1]) - 0xa1 ) * offset_size 
				i += 1 
			else:
				offset = (ord(text[i]) + 156 - 1) * offset_size

			fp.seek(start_offset + offset)
			bindot = fp.read(offset_size)

			for j in xrange(offset_size):
				bin_str += "{0:08b}".format(ord(bindot[j]))

			bin_array.append(bin_str)
			i += 1
		fp.close()

		return bin_array

if __name__ == "__main__":
	pt = PixelText(u'中国Abe')

	print "\n".join(pt.getPixelList())
