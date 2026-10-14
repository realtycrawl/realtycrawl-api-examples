// One bounded source request. Run after checking capabilities. No automatic retry.
package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

func main() {
	key, idem := os.Getenv("REALTYCRAWL_API_KEY"), os.Getenv("REALTYCRAWL_IDEMPOTENCY_KEY")
	if key == "" || idem == "" {
		fmt.Fprintln(os.Stderr, "Set REALTYCRAWL_API_KEY and REALTYCRAWL_IDEMPOTENCY_KEY")
		os.Exit(1)
	}
	body := []byte(`{"location":{"kind":"bbox","bbox":[-97.82,30.2,-97.65,30.35]},"transaction":"sale","limit":1}`)
	req, err := http.NewRequest("POST", "https://realtycrawl.dev/v1/zillow/listings/search", bytes.NewReader(body))
	if err != nil {
		panic(err)
	}
	req.Header.Set("Authorization", "Bearer "+key)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Max-Credits", "50")
	req.Header.Set("Idempotency-Key", idem)
	client := &http.Client{Timeout: 60 * time.Second, CheckRedirect: func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse }}
	res, err := client.Do(req)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Request failed. No retry made; preserve idempotency key.")
		os.Exit(1)
	}
	defer res.Body.Close()
	data, err := io.ReadAll(io.LimitReader(res.Body, 8*1024*1024+1))
	if err != nil || len(data) > 8*1024*1024 {
		fmt.Fprintln(os.Stderr, "Invalid or oversized response")
		os.Exit(1)
	}
	fmt.Println(string(data))
	if res.StatusCode != 200 {
		os.Exit(1)
	}
}
