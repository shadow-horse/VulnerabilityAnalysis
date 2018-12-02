## Web代码片段导致iPhone和iPads内核pannic和reboot

该漏洞通过加载专门制作的CSS代码的HTML页面来利用，CSS代码并不复杂，它试图将一种称为背景筛选的CSS效果应用到一些列嵌套页面DIV中。  

背景过滤器是一个相对新的CSS属性，它通过模糊或颜色转移到元素后面的区域来工作，研究人员猜测，这种效果的渲染对IOS图形处理库造成了影响，最终导致OS完全崩溃。  

攻击者利用Webkit filter CSS属性的一个弱点，该属性使用3D加速来处理器背后的元素，通过使用嵌套的DIV，我们可以快速的消耗所有图形资源，并冻结内核操作系统。  

该漏洞也影响MacOS，它需要一个包含JavaScript的修改版本，Safari在强制重启之后仍然存在，并且浏览器会再次启动，因此再次执行恶意代码阻塞用户。  

该漏洞影响范围可能更广，因为苹果强迫Appstore上列出的所有浏览器和能够进行HTML的应用程序使用Webkit渲染引擎，意味着这个问题可能是任何加载网页的应用程序崩溃。  

漏洞发现者Twwiter: https://twitter.com/pwnsdx  
Github: https://gist.github.com/pwnsdx/ce64de2760996a6c432f06d612e33aea