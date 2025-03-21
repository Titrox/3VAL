package com.example.demo.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class ChessMoveController {

    String flask_url = "http://localhost:5000/best-move";

    /**
     * Returns best possible move found by validation function
     *
     * @param currentBoardState current board state in FEN
     */
    @PostMapping("/best-move")
    public String getBestMove(@RequestBody String currentBoardState) {

        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response;

        try {
            response = restTemplate.postForEntity(flask_url, currentBoardState, String.class);
            return response.getBody();
        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
        return null;
    }
}
