Introduction
The Facial Recognition Attendance System is a software application designed to automate the process of taking attendance in educational institutions, workplaces, and other settings. By leveraging the capabilities of OpenCV, Python, Pillow, and CSV files, this system captures and identifies faces in real-time, marking attendance with high accuracy and efficiency.

Key Technologies:
OpenCV: A powerful open-source computer vision library that provides tools for face detection and recognition. OpenCV is the backbone of the system, handling the processing and recognition of facial images.

Python: The primary programming language used to build the system. Python's versatility and extensive libraries make it ideal for developing applications that require image processing and data management.

Pillow: A Python Imaging Library (PIL) that adds image processing capabilities to your Python interpreter. It is used in the system for image manipulation tasks, such as resizing and converting images into formats suitable for recognition.

CSV Files: The system uses CSV (Comma-Separated Values) files to store and manage attendance records. Each entry in the CSV file corresponds to a student's or employee's attendance status, providing an easy-to-access and organized record.

Workflow Overview:
Face Detection: The system uses OpenCV to detect faces in live video streams or captured images. This step involves locating the face within the image frame.

Face Recognition: Once a face is detected, the system compares it with a pre-existing database of registered faces. If a match is found, the system identifies the person.

Attendance Marking: After successful recognition, the system automatically logs the attendance of the recognized individual in a CSV file, noting the date and time.

Data Management: The CSV file can be easily exported or integrated into other systems for reporting and analysis, ensuring that attendance records are accurate and up-to-date.


NOTE:Save all to a folder called project in your C drive for smooth running. Required modules are: tkinter,numpy,pillow and opencv-contrib-python
