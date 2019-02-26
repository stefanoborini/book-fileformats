DIRS=tables

SECTIONS=main.xml 7zip.xml arj.xml bzip2.xml cpio.xml jar.xml \
	tar.xml ace.xml autopackage.xml compress.xml gzip.xml \
	lha.xml rpm.xml zip.xml

chapter.xml: $(SECTIONS)
	for d in $(DIRS); do make -C $$d; done
	xmllint --xinclude --output chapter.xml main.xml

clean: 
	for d in $(DIRS); do make -C $$d clean; done
	rm -f chapter.xml
