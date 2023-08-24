package com.example.demo.controller;


import java.util.List;

import org.apache.ibatis.annotations.Param;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;


import com.example.demo.mapper.StockMapper;
import com.example.demo.model.Machine;
import com.example.demo.model.Stock;

@CrossOrigin(origins = "*", allowedHeaders = "*")
@RestController
public class StockController {
	private StockMapper mapper;

	public StockController(StockMapper mapper) {
		
	this.mapper = mapper;
	}
	
	@PutMapping("user/signup")
	
	
	
	@GetMapping("/stock/{item_id}")
	public Stock getStock(@PathVariable("item_id") String item_id) {
		return mapper.getStock(item_id);
	}
	
	@GetMapping("/stock")
	public List<Stock> getStockList(){
		return mapper.getStockList();
	}
	
	
	@PostMapping("/join")
	public int setStockList(@RequestParam("user_id") int user_id,@RequestParam("user_name") int user_name,@RequestParam("user_val") int user_val, @RequestParam("user_pswd") String user_pswd, @RequestParam("user_email") String user_email){
		mapper.setMyPage(user_id);
		mapper.setStockList(user_id,user_name,user_val,user_pswd,user_email);
		return user_id;
		//return mapper.setStockList(user_id,user_name,user_val,user_pswd,user_email);
	
	}
	
	@PostMapping("/database")
	public void setMypage(@RequestParam("user_id") int user_id){
		mapper.setMyPage(user_id);
		
		//return mapper.setStockList(user_id,user_name,user_val,user_pswd,user_email);
	
	}
	
	@GetMapping("/login")
	public int Login(@RequestParam("user_id") int user_id, @RequestParam("user_pswd") String user_pswd){
		
		String pswd = mapper.Login(user_id);
		
		System.out.println(pswd);

		System.out.println(user_pswd);
		
		if (pswd.equals(user_pswd)) {
			return 1;
		}
		else {
			return 0;
		}
	
	}
	
	@PutMapping("/machine/{machine_id}")
    public void updateMachineUsing(@PathVariable("machine_id") int machine_id, @RequestParam int machine_using) {
        // 모델에서 받은 수치로 MySQL의 machine_using 값을 갱신
        mapper.updateMachineUsing(machine_id, machine_using);
    }
	
	
	@PutMapping("/mypage/{user_id}")
    public void updateMa(@PathVariable("user_id") int user_id, @RequestParam int ma) {
        // 모델에서 받은 수치로 MySQL의 machine_using 값을 갱신
        mapper.updateMa(ma);
    }
	
	@GetMapping("/mypage/rank")
	public int rank() {
		return mapper.rank()+1;  
	}
	
	
	
	@GetMapping("/machine/{machine_id}")
	public int getMachine_rest(@PathVariable("machine_id") int machine_id) {
		return mapper.getMachine_rest(machine_id);
		
	}
}