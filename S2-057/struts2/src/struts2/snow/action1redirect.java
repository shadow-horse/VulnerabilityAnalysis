package struts2.snow;

import com.opensymphony.xwork2.ActionSupport;

public class action1redirect extends ActionSupport{
	
	private String username;
	private String password;
	
    @Override
    public String execute() throws Exception {
        // TODO Auto-generated method stub
    	System.out.println("action1redirect execute.......");
    	if(username !=null && password !=null && username.length()>0 &&password.length()>0)
    	{
    		return "success";
    	}
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
