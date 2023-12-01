package main

import (
	"bytes"
	"fmt"
	"net/http"
	"os"
)

func main() {
	arg := os.Args[1]
	
	body := []byte(fmt.Sprintf(`{
		"state": "%s"
	}`, arg))

	
	req, err := http.NewRequest("POST", "http://localhost:3000/update_state", bytes.NewBuffer(body))
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Content-Length", fmt.Sprintf("%d", len(body)))
	
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	defer resp.Body.Close()

	fmt.Printf("Response: %v\n", resp.Status)
}