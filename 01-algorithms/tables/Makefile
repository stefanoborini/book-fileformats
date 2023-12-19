
TABLES=table_move_to_front_encoding.xml table_move_to_front_decoding.xml

.SUFFIXES: .tbl .xml
alltables: $(TABLES)

.tbl.xml:
	python ../../../utils/tbl2xml.py $< > $@

clean:
	rm -f $(TABLES)
