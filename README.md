# Live Video Streaming with OBS, NGINX, and AWS

**[🎥 Watch Demo Video](https://drive.google.com/file/d/15uZZhSL0pmhI2AiDBGD9Fb6xQnQkIdCJ/view)**  
 

This project demonstrates a live video streaming solution using OBS Studio, NGINX with RTMP module, and AWS services (EC2 and S3). The workflow involves streaming from OBS Studio to an NGINX RTMP server, transcoding the stream, and serving it to clients via AWS S3.

---

## Features

- Live streaming using RTMP.
- Transcoding RTMP streams into HLS format (`.ts` and `index.m3u8`).
- Storage of transcoded files in Amazon S3.
- Stream delivery to clients for real-time playback.

---

## Architecture

![Architecture Diagram](https://github.com/user-attachments/assets/0647f4de-0712-4907-8aeb-1b612068fc67)

### Workflow:

1. **Broadcasting**:  
   OBS Studio sends an RTMP stream to the NGINX RTMP server hosted on an EC2 instance.

2. **Transcoding**:  
   The RTMP stream is transcoded into HLS format using FFMPEG on another EC2 instance.

3. **Storage and Distribution**:  
   Transcoded `.ts` and `index.m3u8` files are stored in Amazon S3 for streaming to clients.

---

## Prerequisites

### 1. **OBS Studio**:
   - Download OBS Studio from [here](https://obsproject.com/).
   - Configure OBS to send RTMP streams to your NGINX server.

### 2. **AWS Services**:
   - **EC2 Instances**: Two EC2 instances are required.
     - One for running the NGINX server with the RTMP module.
     - Another for transcoding the stream using FFMPEG.
   - **S3 Bucket**: Create an S3 bucket for storing the HLS files.

### 3. **NGINX with RTMP Module**:
   - Install and configure NGINX with the RTMP module on EC2 Instance 1.

### 4. **FFMPEG**:
   - Install FFMPEG on EC2 Instance 2 for transcoding the RTMP streams to HLS format.

---

## Setup Instructions

### 1. **NGINX RTMP Server**:
   - SSH into EC2 Instance 1.
   - Install NGINX with the RTMP module:
     ```bash
     sudo apt update
     sudo apt install nginx libnginx-mod-rtmp
     ```
   - Configure `nginx.conf` to enable RTMP:
     
   - Restart NGINX:
     ```bash
     sudo systemctl restart nginx
     ```

### 2. **OBS Studio Configuration**:
   - Open OBS Studio.
   - Go to **Settings > Stream** and set:
     - **Service**: Custom
     - **Server**: `rtmp://<EC2_Instance_1_IP>/live`
     - **Stream Key**: `test` (or any key you prefer)

### 3. **Transcoding with FFMPEG**:
   - SSH into EC2 Instance 2.
   - Install FFMPEG:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
  

### 4. **Amazon S3 Storage**:
   - Upload the `.ts` and `index.m3u8` files to an S3 bucket:
     ```bash
     aws s3 cp /path/to/output s3://<your-bucket-name>/  
     ```
   - Make the bucket publicly accessible for cors

### 5. **Serving the Stream to Clients**:
   - Provide the S3 bucket URL for the `index.m3u8` file to clients.
   - Use a video player like Video.js to play the HLS stream.

---

## Technologies Used

- **OBS Studio**: For live streaming.
- **NGINX with RTMP Module**: To accept RTMP streams.
- **FFMPEG**: For transcoding RTMP streams to HLS.
- **Amazon S3**: For storing and serving HLS files.
- **Amazon EC2**: For hosting the NGINX RTMP server and running FFMPEG.
- **HTNL**: For serving the client side streaming.

---

## Future Improvements

- Use AWS MediaLive for automated transcoding.
- Implement CloudFront for efficient content delivery.

---

 

## Contact

For any questions or feedback, please feel free to open an issue or contact me.

---

## Screenshots
![Screenshot 2024-11-25 154402](https://github.com/user-attachments/assets/f036ff34-e081-4110-9b50-b991ac781553)


![Screenshot 2024-11-25 154252](https://github.com/user-attachments/assets/c3d08dba-9f57-46c9-9228-620b97dc93a3)


![Screenshot 2024-11-25 154223](https://github.com/user-attachments/assets/63826a94-f63d-4fbd-8fec-0b1086460267)


![Screenshot 2024-11-25 154323](https://github.com/user-attachments/assets/3b3d40f2-a0cb-4c8e-a6c3-83996f97a6b8)


