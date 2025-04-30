This server can be tested using Postman:
![req](https://github.com/user-attachments/assets/bdccf748-a80d-4960-9c39-8f281238acaf)

Suppored Requests:
GET, HEAD

Responses:
200 OK, 304 Not Modified, 501 Not Implemeneted

When testing the If-Modified-Since header with my server, the entered date must be in the standard HTTP date format with no extra spaces or characters.
Ex: Mon, 14 Apr 2025 15:37:45 GMT
