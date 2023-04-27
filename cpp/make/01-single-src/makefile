# 变量定义
app_name = app
clean_cmd = rm app *.o
COPTIONS = -c -o

# 使用变量: ${variable name}
all: ${app_name}

app: app.o
	gcc -o $@ $<

app.o: main.c
	gcc $(COPTIONS) $@ $^

# 2. 使用变量: $(variable name)
clean:
	$(clean_cmd)

run:
	./app