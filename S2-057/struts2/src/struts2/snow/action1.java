package struts2.snow;

import com.opensymphony.xwork2.ActionSupport;

public class action1 extends ActionSupport{
	
	private String username;
	private String password;
	
    @Override
    public String execute() throws Exception {
        // TODO Auto-generated method stub
    	System.out.println("action1 execute.......");
    	if(username.equals("redirect"))
    		return "success";
    	if(username.equals("chain"))
    		return "chain";
    	if(username.equals("postback"))
    		return "postback";
    	return "error";
    }

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}
}
