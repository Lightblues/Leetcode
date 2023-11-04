from 廖雪峰 [Maven基础](https://www.liaoxuefeng.com/wiki/1252599548343744/1255945359327200)


- 官网: https://maven.apache.org/
- 搜索包: https://central.sonatype.com/

## maven 基础使用

### 依赖类型

- 默认的`compile`是最常用的，Maven会把这种类型的依赖直接放入classpath
- `test`依赖表示仅在测试时使用，正常运行时并不需要。最常用的`test`依赖就是JUnit
- `runtime`依赖表示编译时不需要，但运行时需要。最典型的`runtime`依赖是 JDBC驱动，例如MySQL驱动
- `provided`依赖表示编译时需要，但运行时不需要。最典型的`provided`依赖是Servlet API，编译的时候需要，但是运行时，Servlet服务器内置了相关的jar，所以运行期不需要

### ID

唯一ID: 由三部分组成

*   groupId：属于组织的名称，类似Java的包名；
*   artifactId：该jar包自身的名称，类似Java的类名；
*   version：该jar包的版本。

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.48</version>
    <scope>runtime</scope>
</dependency>
```

### 构建流程: 生命周期, 指令

maven 运行指令

*   clean：清理
*   compile：编译
*   test：运行测试
*   package：打包


### 使用插件

实际上，执行每个phase，都是通过某个插件（plugin）来执行的，Maven本身其实并不知道如何执行`compile`，它只是负责找到对应的`compiler`插件，然后执行默认的`compiler:compile`这个goal来完成编译。


插件名称	对应执行的phase
clean	clean
compiler	compile
surefire	test
jar	package


自定义插件

```xml
<project>
    ...
	<build>
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-shade-plugin</artifactId>
                <version>3.2.1</version>
				<executions>
					<execution>
						<phase>package</phase>
						<goals>
							<goal>shade</goal>
						</goals>
						<configuration>
                            ...
						</configuration>
					</execution>
				</executions>
			</plugin>
		</plugins>
	</build>
</project>

<!-- 配置 
maven-shade-plugin需要指定Java程序的入口, 配置如下
-->
<configuration>
    <transformers>
        <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
            <mainClass>com.itranswarp.learnjava.Main</mainClass>
        </transformer>
    </transformers>
</configuration>
```

