package com.example.demo.model;

public class Machine {
	
	private int machine_id;
	private String machine_name;
	private int machine_total;
	private int machine_using; 
	private int machine_rest;
	
	
	public int getMachine_id() {
		return machine_id;
	}
	public void setMachine_id(int machine_id) {
		this.machine_id = machine_id;
	}
	public String getMachine_name() {
		return machine_name;
	}
	public void setMachine_name(String machine_name) {
		this.machine_name = machine_name;
	}
	public int getMachine_using() {
		return machine_using;
	}
	public void setMachine_using(int machine_using) {
		this.machine_using = machine_using;
	}
	public int getMachine_total() {
		return machine_total;
	}
	public void setMachine_total(int machine_total) {
		this.machine_total = machine_total;
	}
	public int getMachine_rest() {
		return machine_rest;
	}
	public void setMachine_rest(int machine_rest) {
		this.machine_rest = machine_rest;
	}
	
	

}
