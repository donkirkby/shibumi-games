# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 5.15.0
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore

qt_resource_data = b"\
\x00\x00\x02\x02\
-\
--\x0atitle: Spline\
 Rules\x0a\x0a---\x0a\x0a* d\
esigned by N\xc3\xa9st\
or Romeral Andr\xc3\
\xa9s\x0a* 2 players\x0a\x0a\
### Start\x0aThe bo\
ard starts empty\
.\x0a\x0a### Play\x0aPlay\
ers take turns a\
dding a piece of\
 their colour to\
 any\x0aplayable po\
int (empty hole \
or platform).\x0a\x0a#\
## End\x0aA player \
wins by making a\
 flat line of th\
eir colour spann\
ing\x0aside to side\
, or corner to c\
orner, on any le\
vel.\x0a\x0a### Strate\
gy\x0aMost wins wil\
l occur on the 2\
\xc3\x972 level, by th\
e first player t\
o reach that hig\
h.\x0a\x0aEvery game i\
s guaranteed to \
produce a winner\
 before the last\
 ball is played.\
\x0a\
\x00\x00\x00\x95\
<\
!DOCTYPE RCC><RC\
C version=\x221.0\x22>\
\x0a<qresource>\x0a<fi\
le>./shibumi_rul\
es.qrc</file>\x0a<f\
ile>./spargo.md<\
/file>\x0a<file>./s\
pline.md</file>\x0a\
</qresource>\x0a</R\
CC>\x0a\
\x00\x00\x03\xc8\
-\
--\x0atitle: Spargo\
 Rules\x0a\x0a---\x0a\x0a* d\
esigned by Camer\
on Browne\x0a* 2 pl\
ayers\x0a\x0aSpargo is\
 a 3D extension \
of Go, in which \
pinned pieces re\
main active in t\
he game\x0afollowin\
g capture.\x0a\x0a### \
Start\x0aThe board \
starts empty.\x0a\x0a#\
## Play\x0aPlayers \
take turns addin\
g a ball of thei\
r colour to a pl\
ayable\x0apoint. Th\
e ball must have\
 freedom (i.e. i\
t must be visibl\
y connected\x0ato a\
t least one empt\
y board hole by \
a chain of visib\
ly touching\x0afrie\
ndly balls) foll\
owing the move.\x0a\
\x0aEnemy groups wi\
th no freedom ar\
e captured after\
 each move,\x0aexce\
pt that balls su\
pporting one or \
more enemy piece\
s are not\x0aremove\
d. Such balls su\
rvive capture an\
d remain active \
in the\x0agame as z\
ombies.\x0a\x0aPassing\
 is not allowed.\
\x0a\x0aOverpasses cut\
 underpasses.\x0a\x0aT\
he superko rule \
applies: it is n\
ot allowed to re\
peat the board p\
osition of\x0aany p\
revious turn wit\
h the same playe\
r to move.\x0a\x0a### \
End\x0aThe game end\
s when the curre\
nt player has no\
 legal moves,\x0aan\
d is won by the \
player with the \
most balls in pl\
ay (counting zom\
bies).\x0a\
"

qt_resource_name = b"\
\x00\x0d\
\x0c\xb6\xbbC\
\x00s\
\x00h\x00i\x00b\x00u\x00m\x00i\x00_\x00r\x00u\x00l\x00e\x00s\
\x00\x09\
\x03\x04\xb1\xd4\
\x00s\
\x00p\x00l\x00i\x00n\x00e\x00.\x00m\x00d\
\x00\x11\
\x0b_5\xe3\
\x00s\
\x00h\x00i\x00b\x00u\x00m\x00i\x00_\x00r\x00u\x00l\x00e\x00s\x00.\x00q\x00r\x00c\
\
\x00\x09\
\x08\x8f\x11\xf4\
\x00s\
\x00p\x00a\x00r\x00g\x00o\x00.\x00m\x00d\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00 \x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01t\x95i\x8e\x9e\
\x00\x00\x00`\x00\x00\x00\x00\x00\x01\x00\x00\x02\x9f\
\x00\x00\x01t\x95fE\x83\
\x00\x00\x008\x00\x00\x00\x00\x00\x01\x00\x00\x02\x06\
\x00\x00\x01t\x99S\xea\xe7\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
