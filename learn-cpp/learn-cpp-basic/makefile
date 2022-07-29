CC	= g++
CPPFLAGS= -Wno-deprecated -std=c++11 -O3 -m64 -c -w #-Wall
LDFLAGS	= -O3 -m64 
SOURCES	= tmp.cpp
OBJECTS	= $(SOURCES:.cpp=.o)
EXECUTABLE=a.out

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE) : $(OBJECTS)
	$(CC) $(LDFLAGS) $^ -o $@

.cpp.o : 
	$(CC) $(CPPFLAGS) $< -o $@

clean:
	rm -f *.o
