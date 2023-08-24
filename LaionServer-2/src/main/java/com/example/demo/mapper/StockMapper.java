package com.example.demo.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import com.example.demo.model.Machine;
import com.example.demo.model.Stock;


@Mapper
public interface StockMapper {
	
	@Select("SELECT * FROM stock WHERE item_id=#{item_id}")
	Stock getStock(@Param("item_id") String item_id);
	
	@Select("SELECT * FROM user")
	List<Stock> getStockList();
	
	@Select("SELECT machine_using FROM machine WHERE machine_id=#{machine_id}")
	int getMachine_rest(@Param("machine_id") int machine_id);
	
	@Insert("INSERT INTO user VALUES (#{user_id},#{user_name},#{user_val},#{user_pswd},#{user_email})")
	int setStockList(@Param("user_id") int user_id,@Param("user_name") int user_name,@Param("user_val") int user_val, @Param("user_pswd") String user_pswd, @Param("user_email") String user_email);

	

	@Select("SELECT user_pswd FROM user WHERE user_id=#{user_id}")
	String Login(@Param("user_id") int user_id);
	
	
    @Update("UPDATE machine SET machine_using=#{machine_using} WHERE machine_id =#{machine_id}")
    int updateMachineUsing(@Param("machine_id")int machine_id, int machine_using);
    /*
    @Insert("INSERT INTO mypage VALUES (#{user_id},#{user_name},#{user_val},#{user_pswd},#{user_email})")
	void setMyPage(int user_id, int user_name, int user_val, String user_pswd, String user_email);
    */
    @Insert("INSERT INTO mypage VALUES (#{user_id},0,0,0,0,0,0,0,0,0,0,0,0)")
	void setMyPage(@Param("user_id") int user_id);
    
    
    @Update("UPDATE mypage SET ma=#{ma} WHERE user_id=1")
    int updateMa(@Param("ma")int ma);
    
    
    //순위 정하기
    @Select("SELECT COUNT(user_id) FROM mypage WHERE ma>0")
    int rank();
 

}