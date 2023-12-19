---
---
# Preface

## About this book

This book is the result of research performed in the field of file
formats I started during the development of my Ph.D. Thesis in computational
chemistry. The problem at that time was (and still is) to store information
relative to mathematical entities describing physical properties of the
molecules, in general quite bulky in terms of space occupation.
During this time, I realized how important is the role of file
formats and, in particular, of the API for accessing the file format.
Notable requirements for this project were an easy and self descriptive
API, extensibility of the file format, platform independence, metadata
association.
After my Ph.D., I started working for a nanotechnology company, when
again I was faced with file format issues, this time relatively to backward
compatibility and a rigorous data-preserving policy. Most of all, I felt the
urgence of specialization in the field, and I started doing research on the
available solutions to well-known problems in data storage. The result is
this book, which has been written four hands between me and Simone.
Together, we collect the experience of both the scientific and enterprise
environments.



## Why file format design?

File format design is a complex issue. Nevertheless, very few books
exist on the argument, and the few that do normally report the
specifications of standard file formats, without going into the details on
how to design a format.
Why should you design a file format? The answer is pretty simple:
every time you are creating an application which has to read or store
information, then you need a file format. Of course, some specific software
categories do not need a file format: simple applets like a calculator, for
example... anything else? We realize that even the most basic application
like a notepad need a file format. Still, when software is designed, a lot
of investment is done for describing how the software should behave, how it
should be designed, and hopefully how it should be cleaned up after
implementation, but little time is actually spent for two really important
aspects of a software product: user interface and file format.
This is quite surprising, because both the user interface and the file
format are the most important aspects that the user will appreciate of your
product. The customer won't really care if you implemented the Command
pattern for providing undo, but he will not like your product if you do not
provide undo, regardless of how you design and implement it. A clumsy
interface with a perfect internal design will have a very bad time on the
market, because the interface is what the user sees of your product, how it
appears and behaves. Also important, users do not like changes, and in
general a radical change in the interface interaction will not be
appreciated.
However, your software product has another important user-accessible
entity: the file format. Your user call it "document" or "song" or
"drawing". For them, it is absolutely valuable. They could have a bad time
if you change the interface (and your customer support also will), but they
will panic and scream in terror if they cannot access their documents, and
your product will be dumped in seconds.
As you can see, there's a great degree of importance in what you
deploy on your customer hard disk, and youu should not consider a file
format as a low or even medium priority task. What you are writing on user's
hard disks is going to stay forever. Any choice you make, any mistake you do
must be supported by future releases of your application, no exceptions.

## Do I need a file format?

The first question you should ask yourself is: do I need to develop a new
file format? Most often, the answer is no. A lot of existent file formats
already deal with categories of data, grasping all the needs and sometimes
providing an API you can use in your application. If you are developing a
Picture editor, probably a new proprietary graphic file format is the last
thing your customer wants. More probably, they want to use well known file
formats like JPG, of TIFF. If you are producing a music editor, your user
probably needs to produce a MIDI file, a WAV or a MP3. In these cases, the
answer to the previous question is no.
If your application is a converter, then again you don't need your own
file format, but instead you have to provide a large number of available
file formats which can be read and written by your application. Again, the
answer is no.
So when do you need your own file format? Intuitively, the answer is
"when the already available file formats do not provide the features I need"


# How this book is structured

This book has been structured keeping into account important issues
raising during file format design. These issues normally come in form of a
specific question like "how can I guarantee corruption detection?" or "how
can I organize my data?". This book has been structured with the same idea.
Each chapter will introduce a specific question about file format design,
present already established file formats which answer the question, and
devise a general stylistic guideline for your implementation. More
specifically, we will answer these questions

 How can I guarantee sanity check for my data?
 How can I prevent more than one instance of an application to use my file?
 How can I rationalize the information to be stored, and
 correctly map it on the file format?
 How can I manage consistency between the stored information
 How can I deal with versioning of the file format?
 How can I handle optional information?
 How can I implement ACID behavior in my library?
 How can I deal with huge files?
 How can I compress data?
 How can I achieve platform independence?
 How can I search for information in a quick and efficient way?
 How can I make my file format well known and standardized?

We are going to explore a wide range of algorithms, techniques and best
practices, bringing real world cases and descrbing their solutions,
limitations and how to eventually improve them.


