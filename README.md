HLS Adaptive Bitrate Streaming Documentation
============================================

Technologies Used
-----------------

* FFmpeg: A powerful, open-source multimedia processing tool.
* Node.js: A JavaScript runtime environment for building scalable and high-performance server-side applications.
* Express.js: A popular Node.js web framework for building web applications and APIs.
* HLS (HTTP Live Streaming): A protocol developed by Apple for streaming live and on-demand content over HTTP.

Requirements
------------

* FFmpeg installed on the system.
* Node.js and Express.js installed.
* A video file to be streamed.

Installation Instructions
-------------------------

1. Clone the repository using the following command:
`git clone (link unavailable)`
3. Navigate to the project directory:
`cd HLS-Adaptive_Bitrate_Streaming`
5. Install the required dependencies:
`npm install`

Usage Instructions
------------------

1. Start the server using the following command:
`node server.js`
3. Open a web browser and navigate to <http://localhost:3000>.
4. Select a video file to be streamed.
5. The video will be streamed using HLS adaptive bitrate streaming.

Documentation
-------------

This project uses FFmpeg to segment the video file into smaller chunks, and then uses Node.js and Express.js to create an HLS manifest file. The manifest file is used to stream the video content using HLS adaptive bitrate streaming.

The project consists of the following components:

* `server.js`: The main server file that creates the HLS manifest file and streams the video content.
* `ffmpeg.js`: A utility file that uses FFmpeg to segment the video file into smaller chunks.
* `public/index.html`: The client-side HTML file that plays the streamed video content.

Visuals
-------

![Project Screenshot]((link unavailable))

Project Status
--------------

This project is currently in the development stage. It has been tested with a few video files, but it may not work with all types of video files.

Contribution Guidelines
-----------------------

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. Please make sure to include a detailed description of your changes.

Acknowledgments
---------------

This project would not have been possible without the help of the following people:

* Nilesh D