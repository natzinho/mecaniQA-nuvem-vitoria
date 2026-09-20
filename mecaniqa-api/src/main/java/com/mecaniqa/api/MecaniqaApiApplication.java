package com.mecaniqa.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class MecaniqaApiApplication {

    private final JdbcTemplate jdbcTemplate;

    public MecaniqaApiApplication(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @GetMapping("/")
    public String home() {
        return "MecâniQA API está funcionando!";
    }

    @GetMapping("/db")
    public String database() {
        Integer result = jdbcTemplate.queryForObject("SELECT 1", Integer.class);
        return "Conexão com MySQL funcionando! Resultado: " + result;
    }

    public static void main(String[] args) {
        SpringApplication.run(MecaniqaApiApplication.class, args);
    }

}
