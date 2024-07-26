# FaceAPI

![FaceAPI Logo](https://via.placeholder.com/150)

## Overview

FaceAPI is a robust and versatile API designed to handle face and NSFW (Not Safe For Work) content detection. It provides various functionalities including human detection, face detection, and content moderation using state-of-the-art machine learning models.

## Features

### HumanDetectionAPI
- **Face Detection**: Detects faces in images with high accuracy.
- **Facial Landmark Detection**: Identifies key facial features such as eyes.
- **Eye State Detection**: Determines if eyes are open or closed.
- **Face Coverage Analysis**: Assesses the coverage of the face in the image to ensure it's suitable for processing.

### NSFWDetectionAPI
- **NSFW Content Detection**: Classifies images into categories like drawings, hentai, neutral, porn, and sexy.

## Repository Structure

```plaintext
FaceAPI/
├── HumanDetectionAPI/
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── images/
│   ├── mask_detector.model
│   └── routes.py
└── NSFWDetectionAPI/
    ├── api/
    ├── config.py
    ├── nsfw_detector/
    │   ├── __init__.py
    │   ├── nsfw_model.h5
    │   ├── predict.py
    │   └── __pycache__/
    ├── __pycache__/
    └── requirements.txt
```

## Installation

### Prerequisites

- Python 3.6 or higher
- Required Python libraries (listed in `requirements.txt` of each API)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/AbhishekKumar1602/FaceAPI.git
    cd FaceAPI
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies for each API:

    ```bash
    cd HumanDetectionAPI
    pip install -r requirements.txt
    cd ../NSFWDetectionAPI
    pip install -r requirements.txt
    ```

## Usage

### Running the Human Detection API Server

1. Navigate to the HumanDetectionAPI directory:

    ```bash
    cd HumanDetectionAPI
    ```

2. Start the server:

    ```bash
    uvicorn main:app --reload
    ```

3. The API server will be running at `http://localhost:8000`.

### Human Detection API Endpoints

- **Detect Human**: `POST /human-detection/`
  
  **Request**: JSON with an image file.

  **Response**: JSON indicating whether a human is detected.

### Running the NSFW Detection API Server

1. Navigate to the NSFWDetectionAPI directory:

    ```bash
    cd NSFWDetectionAPI
    ```

2. Start the server:

    ```bash
    uvicorn api.main:app --reload
    ```

3. The API server will be running at `http://localhost:5009`.

### NSFW Detection API Endpoints

- **Classify Image**: `POST /classify/`
  
  **Request**: JSON with an image URL or base64-encoded image.

  **Response**: JSON with the classification of the image into various NSFW categories.

## Example Requests

### Human Detection Example

Here’s a sample request to detect a human in an image:

```bash
curl -X POST http://localhost:8000/human-detection/ -H "Content-Type: application/json" -H "api-key: STFAPIEXP0001" -d '{"file": "<base64-encoded-image>"}'
```

### NSFW Detection Example

Here’s a sample request to classify an image for NSFW content:

```bash
curl -X POST http://localhost:5009/classify/ -H "Content-Type: application/json" -d '{"image_url": "http://example.com/image.jpg"}'
```

## Contributing

We welcome contributions to improve FaceAPI. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenCV](https://opencv.org/) for image processing functionalities.
- [TensorFlow](https://www.tensorflow.org/) for deep learning models.
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework.

## Contact

For any queries or support, please contact