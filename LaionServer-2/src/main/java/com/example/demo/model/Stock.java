package com.example.demo.model;


public class Stock {
	
	private int user_id;
	
	private int user_name;
	private int user_val;
	private String user_pswd;
	private String user_email;
	
	
	
	
	public Stock(int user_id, int user_name, int user_val, String user_pswd, String user_email) {
		super();
		this.setUser_id(user_id);
		this.setUser_name(user_name);
		this.setUser_val(user_val);
		this.setUser_pswd(user_pswd);
		this.setUser_email(user_email);
	}
	//private List Stock;
	
	

	public int getUser_name() {
		return user_name;
	}

	public void setUser_name(int user_name) {
		this.user_name = user_name;
	}



	public int getUser_id() {
		return user_id;
	}



	public void setUser_id(int user_id) {
		this.user_id = user_id;
	}



	public int getUser_val() {
		return user_val;
	}



	public void setUser_val(int user_val) {
		this.user_val = user_val;
	}



	public String getUser_pswd() {
		return user_pswd;
	}



	public void setUser_pswd(String user_pswd) {
		this.user_pswd = user_pswd;
	}



	public String getUser_email() {
		return user_email;
	}



	public void setUser_email(String user_email) {
		this.user_email = user_email;
	}
		
}