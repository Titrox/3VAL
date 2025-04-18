package com.example.demo.controller;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
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


    @PostMapping("/reset-evaluation-factors")
    public String resetEvaluationFactors(@RequestBody String currentBoardState) {


        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response;


        try {
            HttpHeaders header = new HttpHeaders();
            header.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> requestEntity = new HttpEntity<>(currentBoardState, header);

            response = restTemplate.postForEntity(String.format("%s/reset-evaluation-factors", flaskUrl), requestEntity, String.class);

            return response.getBody();

        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
        return null;
    }


    @GetMapping("/get-evaluation-factors")
    public String getEvaluationFactors() {
        try {
            RestTemplate restTemplate = new RestTemplate();
            ResponseEntity<String> response = restTemplate.getForEntity(
                    String.format("%s/get-evaluation-factors", flaskUrl),
                    String.class
            );
            return response.getBody();
        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
        return null;
    }


    @PutMapping("/put-evaluation-factors")
    public String postEvaluationFactors(@RequestBody String factors) {

        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> response;


        try {
            HttpHeaders header = new HttpHeaders();
            header.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> requestEntity = new HttpEntity<>(factors, header);

            response = restTemplate.exchange(
                    String.format("%s/put-evaluation-factors", flaskUrl),
                    HttpMethod.PUT,
                    requestEntity,
                    String.class
            );

            return response.getBody();

        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
        return null;
    }

}
