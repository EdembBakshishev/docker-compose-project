from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import psycopg2
import bcrypt
import logging

# Налаштування логування
logging.basicConfig(level=logging.DEBUG)

# Параметри підключення до бази
DB_PARAMS = {
    "dbname": "smmhub",
    "user": "user",
    "password": "password",
    "host": "db"
}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/register":
            with open("public/register.html", "r") as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(file.read().encode())
        elif self.path == "/login":
            with open("public/login.html", "r") as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(file.read().encode())
        else:
            self.send_error(404, "Not Found")

    ###########################################################################
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        data = parse_qs(post_data)

        if self.path == "/register":
            username = data.get("username", [""])[0]
            email = data.get("email", [""])[0]
            password = data.get("password", [""])[0]

            if username and email and password:
                conn = psycopg2.connect(**DB_PARAMS)
                cursor = conn.cursor()
                hashed_password = password  # тут можна додати bcrypt пізніше

                try:
                    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                                   (username, email, hashed_password))
                    conn.commit()
                    self.send_response(302)
                    self.send_header("Location", "/register")
                    self.end_headers()
                    logging.info(f"User {username} registered successfully")
                except Exception as e:
                    logging.error(f"Error saving user: {e}")
                    self.send_error(400, "Error saving user")
                finally:
                    cursor.close()
                    conn.close()
            else:
                logging.warning("Invalid data received")
                self.send_error(400, "Invalid data")

        elif self.path == "/login":
            email = data.get("email", [""])[0]
            password = data.get("password", [""])[0]

            if email and password:
                conn = psycopg2.connect(**DB_PARAMS)
                cursor = conn.cursor()

                try:
                    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
                    result = cursor.fetchone()

                    if result:
                        stored_password = result[0]
                        # Тут можеш розкоментувати, якщо будеш використовувати bcrypt
                        # if bcrypt.checkpw(password.encode(), stored_password.encode()):
                        if password == stored_password:
                            self.send_response(302)
                            self.send_header("Location", "/dashboard")
                            self.end_headers()
                            logging.info(f"User {email} logged in")
                        else:
                            logging.warning("Incorrect password")
                            self.send_error(401, "Incorrect email or password")
                    else:
                        logging.warning("Email not found")
                        self.send_error(401, "Incorrect email or password")
                except Exception as e:
                    logging.error(f"Login error: {e}")
                    self.send_error(500, "Server error")
                finally:
                    cursor.close()
                    conn.close()
            else:
                logging.warning("Email or password not provided")
                self.send_error(400, "Missing email or password")

    # def do_POST(self):
    #     if self.path == "/register":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length).decode()
    #         data = parse_qs(post_data)

    #         username = data.get("username", [""])[0]
    #         email = data.get("email", [""])[0]
    #         password = data.get("password", [""])[0]

    #         if username and email and password:
    #             conn = psycopg2.connect(**DB_PARAMS)
    #             cursor = conn.cursor()

    #             # hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    #             hashed_password = password

    #             try:
    #                 cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
    #                                (username, email, hashed_password))
    #                 conn.commit()
    #                 self.send_response(302)
    #                 self.send_header("Location", "/register")
    #                 self.end_headers()
    #                 logging.info(f"User {username} registered successfully")
    #             except Exception as e:
    #                 logging.error(f"Error saving user: {e}")
    #                 self.send_error(400, "Error saving user")
    #             finally:
    #                 cursor.close()
    #                 conn.close()
    #         else:
    #             logging.warning("Invalid data received")
    #             self.send_error(400, "Invalid data")

def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logging.info("Server running on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
