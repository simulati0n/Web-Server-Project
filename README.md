This server can be tested using Postman:
To test the server, run the server.py file then go to Postman and start a new request.

The test request:

![image](https://github.com/user-attachments/assets/36359c6a-2975-4b4d-bbfe-766e32156476)

The test response:

![image](https://github.com/user-attachments/assets/28b68751-8818-4e72-a4e0-5241abb17b33)

Suppored Requests:
GET, HEAD

Responses:
200 OK, 304 Not Modified, 501 Not Implemeneted

When testing the If-Modified-Since header with my server, the entered date must be in the standard HTTP date format with no extra spaces or characters.
I have included testfile.txt for testing my server. It was last modified on Mon, 14 Apr 2025 15:37:45 GMT
