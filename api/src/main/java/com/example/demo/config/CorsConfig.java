package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig {

    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/**") // Erlaubt alle Endpunkte
                        .allowedOrigins("http://localhost:5173") // Vue-Entwicklungsserver
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS") // Erlaubte Methoden
                        .allowedHeaders("*")
                        .allowCredentials(true);
            }
        };
    }
}
