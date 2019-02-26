DBLITE=/usr/local/dblite
DBLATEX=/usr/local/dblatex
DIRS=Storage Algorithms

pdf: book.xml
	$(DBLATEX)/bin/dblatex -T db2latex -t pdf -b pdftex -o book.pdf book.xml
book.xml: 
	for d in $(DIRS); do make -C $$d chapter.xml; done
	xmllint --xinclude --output book.xml --postvalid main.xml

html: book.xml
	$(DBLITE)/bin/db2h book.xml

clean:
	for d in $(DIRS); do make -C $$d clean; done
	rm -f *.aux *.dvi *.log *.blg *.toc *.bbl book.xml book.pdf

valid: book.xml
	$(DBLITE)/bin/xval book.xml

