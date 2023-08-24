package com.example.demo.model;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Param;

public class MyPage {
	private int user_id;
	private int ma;
	private int mb;
	private int mc;
	private int md;
	private int me;
	private int mf;
	private int mat;
	private int mbt;
	private int mct;
	private int mdt;
	private int met;
	private int mft;
	public int getUser_id() {
		return user_id;
	}
	public void setUser_id(int user_id) {
		this.user_id = user_id;
	}
	public int getMa() {
		return ma;
	}
	public void setMa(int ma) {
		this.ma = ma;
	}
	public int getMb() {
		return mb;
	}
	public void setMb(int mb) {
		this.mb = mb;
	}
	public int getMc() {
		return mc;
	}
	public void setMc(int mc) {
		this.mc = mc;
	}
	public int getMft() {
		return mft;
	}
	public void setMft(int mft) {
		this.mft = mft;
	}
	public int getMet() {
		return met;
	}
	public void setMet(int met) {
		this.met = met;
	}
	public int getMdt() {
		return mdt;
	}
	public void setMdt(int mdt) {
		this.mdt = mdt;
	}
	public int getMct() {
		return mct;
	}
	public void setMct(int mct) {
		this.mct = mct;
	}
	public int getMbt() {
		return mbt;
	}
	public void setMbt(int mbt) {
		this.mbt = mbt;
	}
	public int getMat() {
		return mat;
	}
	public void setMat(int mat) {
		this.mat = mat;
	}
	public int getMf() {
		return mf;
	}
	public void setMf(int mf) {
		this.mf = mf;
	}
	public int getMe() {
		return me;
	}
	public void setMe(int me) {
		this.me = me;
	}
	public int getMd() {
		return md;
	}
	public void setMd(int md) {
		this.md = md;
	}
	
	
	public MyPage(int user_id,int ma,int mb,int mc,int md,int me,int mf,int mat, int mbt, int mct, int mdt, int met, int mft ) {
		super();
		this.setUser_id(user_id);
		this.setMa(ma);
		this.setMb(mb);
		this.setMc(mc);
		this.setMd(md);
		this.setMe(me);
		this.setMf(mf);
		this.setMf(mat);
		this.setMf(mbt);
		this.setMf(mct);
		this.setMf(mdt);
		this.setMf(met);
		
	}
	
	

}
