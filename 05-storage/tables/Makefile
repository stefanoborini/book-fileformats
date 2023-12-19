
TABLES=table_cpio_ascii_hdr.xml \
	table_cpio_binary_hdr.xml \
	table_cpio_new_hdr.xml \
	table_tar_v7_hdr.xml \
	table_ustar_hdr.xml \
	table_gnu_tar_hdr.xml \
	table_cpio_filemode_flags.xml \
	table_zip_orig_local_file_hdr.xml \
	table_zip_orig_central_file_hdr.xml \
	table_zip_os_values.xml \
	table_bzip2_format.xml

.SUFFIXES: .tbl .xml
alltables: $(TABLES)

.tbl.xml:
	python ../../../utils/tbl2xml.py $< > $@

clean:
	rm -f $(TABLES)
