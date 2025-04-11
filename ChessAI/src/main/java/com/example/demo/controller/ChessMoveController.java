package com.example.demo.controller;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class ChessMoveController {

    String flaskUrl = "http://localhost:5000/";

    /**
     * Returns best possible move found by engine
     *
     * @param currentBoardState current board state in FEN
     */
    @PostMapping("/best-move")
    public String getBestMove(@RequestBody String currentBoardState) {


        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response;


        try {
            HttpHeaders header = new HttpHeaders();
            header.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> requestEntity = new HttpEntity<>(currentBoardState, header);

            response = restTemplate.postForEntity(String.format("%s/best-move", flaskUrl), requestEntity, String.class);

            return response.getBody();

        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
        return null;
    }


    @PostMapping("/evaluate-position")
    public String evaluatePosition(@RequestBody String currentBoardState) {


        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response;


        try {
            HttpHeaders header = new HttpHeaders();
            header.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> requestEntity = new HttpEntity<>(currentBoardState, header);

            response = restTemplate.postForEntity(String.format("%s/evaluate-position", flaskUrl), requestEntity, String.class);

            return response.getBody();

        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
        return null;
    }


}
