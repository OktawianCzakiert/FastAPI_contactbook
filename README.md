# Command to run PostgreSQL in Docker:

docker run --name fastapi-postgres -p 5432:5432 -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=fastapi_db -d postgres


Jeśli podczas rejestracji użytkownik z podanym adresem email już istnieje, serwer zwróci błąd HTTP 409 Conflict;
Serwer haszuje hasło i nie przechowuje je w bazie danych w postaci zwykłego tekstu;
W przypadku udanej rejestracji użytkownika serwer powinien zwrócić status odpowiedzi HTTP 201 Created oraz dane nowego użytkownika;
W przypadku udanych żądań metodą POST służących do tworzenia nowych zasobów serwer zwraca status 201 Created;
W przypadku żądań metodą POST służących do uwierzytelnienia użytkownika serwer akceptuje żądania z danymi użytkownika (email, hasło) w treści żądania;
Jeśli użytkownik nie istnieje lub hasło jest niepoprawne, system zwraca błąd HTTP 401 Unauthorised;
Mechanizm autoryzacji jest zaimplementowany przy użyciu pary tokenów JWT: tokena dostępu access_token i tokena odświeżania refresh_token.