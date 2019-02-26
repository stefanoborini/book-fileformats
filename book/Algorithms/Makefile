DIRS=tables

SECTIONS=main.xml arithmetic.xml crc.xml deflate.xml huffman.xml lempelziv.xml \
	packbits.xml rle.xml move_to_front.xml burrows_wheeler.xml

chapter.xml: $(SECTIONS)
	for d in $(DIRS); do make -C $$d; done
	xmllint --xinclude --output chapter.xml main.xml

clean: 
	for d in $(DIRS); do make -C $$d clean; done
	rm -f chapter.xml
