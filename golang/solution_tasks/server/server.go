/*
Пакет main реализует HTTP-сервер с цепочкой middleware 
для аутентификации и логирования запросов.
*/

package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

// Middleware - тип функции-обертки для обработчиков HTTP.
type Middleware func(http.HandlerFunc) http.HandlerFunc

func main() {
	http.HandleFunc("/public", Chain(publicHandler, Logging()))
	http.HandleFunc("/private", Chain(privateHandler, Logging(), Auth()))
	
	fmt.Println("Server started at :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// Logging создает middleware для логирования времени выполнения запроса.
func Logging() Middleware {
	return func(next http.HandlerFunc) http.HandlerFunc {
		return func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()
			defer func() {
				log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
			}()
			next(w, r)
		}
	}
}

// Auth создает middleware для проверки токена в заголовке Authorization.
func Auth() Middleware {
	return func(next http.HandlerFunc) http.HandlerFunc {
		return func(w http.ResponseWriter, r *http.Request) {
			token := r.Header.Get("Authorization")
			if token != "Bearer 123" {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
			next(w, r)
		}
	}
}

// Chain связывает middleware в цепочку для последовательного выполнения.
func Chain(f http.HandlerFunc, middlewares ...Middleware) http.HandlerFunc {
	for _, m := range middlewares {
		f = m(f)
	}
	return f
}

// publicHandler обрабатывает публичный маршрут /public.
func publicHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Public endpoint")
}

// privateHandler обрабатывает приватный маршрут /private.
func privateHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Private endpoint")
}