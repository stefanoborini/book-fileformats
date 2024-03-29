Burrows Wheeler transformation
The Burrows Wheeler transformation is a lossless reversible
transformation used in the bzip2 compression program. It does not
reduce the data size, but rearranges data in order to achieve a higher
efficiency for subsequent compression schemes like RLE, move-to-front or
Lempel-Ziv.
The main concept behind Burrows Wheeler is to process a block of data of
size N to form a matrix NxN whose rows are the cyclic rotation of the block.
The resulting rows are then sorted, and the last column of the matrix is
extracted together with the row index where the original data appears. For
example, encoding the word "recurrence" leads to




recurrence          cerecurren  
ecurrencer          currencere
currencere          ecurrencer
urrencerec          encerecurr
rrencerecu    ->    erecurrenc   ->   nerrceeruc, 6
rencerecur          ncerecurre
encerecurr          recurrence  
ncerecurre          rencerecur
cerecurren          rrencerecu
erecurrenc          urrencerec

  initial             after           Burrows Wheeler
  matrix             sorting             result 




As we can see, the algorithm tends to aggregate similar characters,
leading to a better layout for compression. The effect is particularly strong
with text: in large blocks of english text, for example, is quite frequent to
have words like "the". During the encoding transformation, the cyclic rotation
split the entries so that the "he" part is at the beginning of the line, and
the "t" at the end. Occasionally, entries for "The" or "she" will also be
present, but in general the net effect of Burrows Wheeler will be to pack "t"
letters together thanks to the sort performed on the "he" part.
To perform the decoding, the matrix is recreated by an alternated add +
sort scheme:

 add    sort    add     sort    add      sort     add       sort  
                                                            
 n       c      nc      ce      nce      cer      ncer      cere
 e       c      ec      cu      ecu      cur      ecur      curr
 r       e      re      ec      rec      ecu      recu      ecur
 r       e      re      en      ren      enc      renc      ence
 c  ->   e  ->  ce  ->  er  ->  cer  ->  ere  ->  cere  ->  erec -> ...
 e       n      en      nc      enc      nce      ence      ncer
 e       r      er      re      ere      rec      erec      recu
 r       r      rr      re      rre      ren      rren      renc
 u       r      ur      rr      urr      rre      urre      rren
 c       u      cu      ur      cur      urr      curr      urre


        add            sort            add            sort
      
      ncerecurr      cerecurre      ncerecurre      cerecurren  
      ecurrence      currencer      ecurrencer      currencere
      recurrenc      ecurrence      recurrence      ecurrencer
      rencerecu      encerecur      rencerecur      encerecurr
...   cerecurre  ->  erecurren  ->  cerecurren  ->  erecurrenc
      encerecur      ncerecurr      encerecurr      ncerecurre
      erecurren      recurrenc      erecurrenc      recurrence  -- row 6
      rrencerec      rencerecu      rrencerecu      rencerecur
      urrencere      rrencerec      urrencerec      rrencerecu
      currencer      urrencere      currencere      urrencerec


which recreates the M matrix. We can now extract the row with index
number 6, reobtaining the original data.

