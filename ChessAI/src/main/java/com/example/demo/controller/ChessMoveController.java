package com.example.demo.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChessMoveController {


    /**
     * Returns best possible move found by validation function
     *
     * @param currentBoardState current board state in FEN
     */
    @PostMapping("/bestMove")
    public String getBestMove(@RequestBody String currentBoardState) {

        return "test";
    }
}
