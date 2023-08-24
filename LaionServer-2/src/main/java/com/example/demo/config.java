package com.example.demo;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class config implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
    	   registry.addMapping("/**")
           .allowedOrigins("https://4614-203-252-223-253.ngrok.io", "http://localhost:8070");
    }
}