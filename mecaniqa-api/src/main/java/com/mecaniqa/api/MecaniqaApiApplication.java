package com.mecaniqa.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController

public class MecaniqaApiApplication {

    @GetMapping("/")
    public String home() {
        return "MecâniQA API está funcionando!";
    }

    public static void main(String[] args) {
		SpringApplication.run(MecaniqaApiApplication.class, args);
	}

}
