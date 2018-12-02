package struts2.snow;

import com.opensymphony.xwork2.ActionSupport;

public class action1chain extends ActionSupport{
	
	@Override
    public String execute() throws Exception {
        // TODO Auto-generated method stub
    	System.out.println("action1chain execute.......");
    	return "success";
	}
}
