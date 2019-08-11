## 基于Apache Solr 6.6创建core实例  

19年Apache Solr报出了2个严重、高危的漏洞，因此学习验证下cve-2019-0192和cve-2019-0193，鉴于之前未接触过Solr搜索服务器，需要先学习搭建Solr服务器，将搭建学习内容整理如下。  

### 1. Apache Solr文件搜索服务器

Solr是一个独立的企业级搜索应用服务器，它对外提供类似Web-service的api接口，用户通过http请求向搜索引擎服务器提交一定格式的XML文件，生成索引；也可以通过http get操作提出查找请求，并得到XML格式的返回结果。  

Solr是一个基于Lucene的java搜索服务器，支持多种格式（XML、JSON等格式），并且附带一个管理界面。  

### 2. 环境搭建 

JDK: jdk 1.8.0_171   
Solr: solr 6.6.0  (5版本可以基于jdk1.7)

在solr 5版本之后，安装包默认继承了jetty服务器，可以直接通过运行bin目录下的脚本运行启动solr，无需在Tomcat中进行配置； 

#### 1）目录结构 

	bin      Solr的脚本目录，启动，关闭，操作命令  
	contrib    存放关于solr的扩展  
	dist     Solr的核心jar包和扩展jar包  
	docs     文档中心
	example  Solr的webapp示例 
	licenses  协议  
	server   在本地运行solr服务运行的必要文件存放在这里，例如core  
	
	
#### 2)直接通过脚本启动  

进入solr-6.6.0/bin目录下，运行：  

	bogon:bin snow$ ./solr start
	Waiting up to 180 seconds to see Solr running on port 8983 [/]
	Started Solr server on port 8983 (pid=3177). Happy searching!

	bogon:bin snow$
	
./solr stop  
./solr create -c new_core  
./solr delete -c new_core  
	
#### 3）访问页面  
http://127.0.0.1:8983/solr/index.html#/  

![](www.baidu.com)


### 3. 创建示例  

网上教程比较多的是，直接通过admin 管理界面的Core Admin进行创建，点击add_core，创建new_core。但是在实际操作过程中，会报错，找不到配置文件：   

	
	Error CREATEing SolrCore 'my_core': Unable to create core [my_core] Caused by: Can't find resource 'solrconfig.xml' in classpath 
	
	网上简单查了下可能是因为没有配置环境变量或哪有问题；

最后通过手工创建new_core工程，首先在solr-6.6.0/server/solr目录下创建new_core目录，并将solr-6.6.0/example/example-DIH/solr/solr/conf目录复制进新建的new_core目录；然后再点击创建core按钮，即可创建成功。    

在admin管理界面，选择创建的new_core工程。   

![](www.baidu.com)

### 4. 基于Tomcat部署Solr

基于Eclipse Tomcat部署，有利于反编译跟进代码异常，进行代码分析。   

1. Eclipse中新建 web工程   
2. 将server\solr-webapp文件夹的内容，复制至工程的webapps目录中  
3. 复制需要的核心jar包  

	将solr-6.6.0\server\lib\ext的jar包复制到apache-tomcat-8.0.32\webapps\solr\WEB-INF\lib目录下

	将solr-6.6.0\dist下的solr-dataimporthandler-6.6.0.jar和solr-dataimporthandler-extras-6.6.0.jar复制到apache-tomcat-8.0.32\webapps\solr\WEB-INF\lib目录下

	将solr-6.6.0\server\lib下的以metrics开头的5个jar包复制到apache-tomcat-8.0.32\webapps\solr\WEB-INF\lib目录下
	
4. 创建solrhome文件夹，将server/solr下的文件都复制到solrhome文件夹内  
5. 在web.xml中配置路径，40行  

		修改<env-entry-value>值为solrhome文件夹路径
6. 复制其它配置文件

	web工程的WEB-INF目录下创建classes文件夹，将solr-6.6.0\server\resources下的log4j.properties复制过去  
	此处需要修改log4j指定的log路径，配置为当前路径./logs即可 
7. 启动web应用  

		http://localhost:8080/solr/index.html

	