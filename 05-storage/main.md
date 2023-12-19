<?xml version="1.0"?>
<chapter id="storage" xmlns:xi="http://www.w3.org/2001/XInclude">
<title>Storage</title>
<sect1>
<title>Files into files</title>
<para>Here some initial comments on the storage chapter</para>
<remark>
consider the following general points points:

1) solid compression.
2) stream decoding
3) lossless file formats, for obvious reasons 
</remark>

<para>In this section we describe several ways of storing files into files, an
operation usually named <emphasis>archiving</emphasis>.  There can be different
motivations to files inside files, leading to different design decisions:</para>

<itemizedlist>
<listitem><para>grouping together several files, or a whole hierarchy of
directories, in a single easy-to-handle object;</para></listitem>
<listitem><para>applying compression algorithm to obtain a smaller
file;</para></listitem>
<listitem><para>storing file content together with their metadata (e.g.
filename, file attributes, location);</para></listitem>
<listitem><para>adding more metadata and installation instructions (e.g.
packages);</para></listitem>
<listitem><para>adding integrity checks.</para></listitem>
</itemizedlist>

<para>Over time, main goals of archive formats have changed.  Back in the
seventies the main use was to produce tape backups, to be restored in case of
hardware failure or accidental deletion.  Some years later, tapes began to
become an important exchange media as people used to mail tapes back and forth
to exchange data and software.</para>

<para>At some point, with the advent of research networks and bullettin boards
this exchange activity started to be performed over slow network connections
and this made compression a very important feature of archiving.  In the UNIX 
world where tools are normally supposed to do one single thing, compressione
was typically introduced as a two-steps process, meaning that files were
first bundled together with normal tar or cpio, and then compressed with 
compress or gzip.  Out of the UNIX world, new formats combining compression and
bundling in a single step have had more success. They are usually referred as
solid archives.</para>

<para>Nowadays, an important storage concept is the software package, that is a
way to distribute programs and make them nicely auto-install and integrate in a
live operating system.  To make this work, software and data have to be bundled
with descriptions, license info, install and uninstall scripts, information on
how to register/unregister libraries, drivers and components.</para>

</sect1>

<sect1>
<title>Simple storage</title>
<xi:include href="tar.xml"/>
<xi:include href="cpio.xml"/>
</sect1>

<sect1>
<title>Simple compression</title>
<xi:include href="compress.xml"/>
<xi:include href="gzip.xml"/>
<!--xi:include href="bzip2.xml"/-->
</sect1>

<sect1>
<title>Compressed storage</title>
<xi:include href="7zip.xml"/>
<xi:include href="ace.xml"/>
<xi:include href="arj.xml"/>
<xi:include href="lha.xml"/>
<xi:include href="zip.xml"/>
</sect1>

<sect1>
<title>Packaging</title>
<xi:include href="autopackage.xml"/>
<xi:include href="jar.xml"/>
<xi:include href="rpm.xml"/>
</sect1>
</chapter>
