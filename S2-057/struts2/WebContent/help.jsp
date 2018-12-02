<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    <%@ taglib prefix="s" uri="/struts-tags" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
	I am help.<br/>
	<s:url includeParams="get">
		<s:param name="id" value="%{'22'}"/>
	</s:url>
</body>
</html>