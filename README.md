# Custom HTTP Server with Image Gallery Support

This tool is a custom HTTP server built using Flask that allows you to serve a folder of image files as a gallery. The directory listing is sorted by file modification time (latest first), and images can be viewed one at a time with navigation.

## Features

- Dynamically set the base directory to serve images via a command-line parameter.
- Displays a directory listing sorted by file modification date (newest first).
- Supports viewing images with navigation to the next or previous image.
- Lightweight and easy to use with Flask.

## Requirements

- **Python 3.7+** installed on your system.
- **Flask** installed (`pip install flask`).

## Installation

1. **Clone or download the script**:
   Download the `app.py` file from this repository.

2. **Install Python (if not installed)**:
   - Download and install Python from [python.org](https://www.python.org/).
   - Ensure that `python` and `pip` are added to your system's PATH.

3. **Install Dependencies**:
   Install Flask (and other dependencies if needed):
   ```bash
   pip install flask
   ```

## Usage

1. **Set the Base Directory**:
   Specify the folder containing images using the `--base_dir` parameter when running the script. For example:
   ```bash
   python app.py --base_dir "C:\your\output\path"
   ```
   Replace `"C:\your\output\path"` with the path to the folder you want to serve.

2. **Run the Server**:
   Execute the script as shown above. The server will start and display a message like this:
   ```
   * Running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   ```

3. **Access the Server**:
   Open a web browser and go to:
   ```
   http://localhost:8000
   ```
   You will see a gallery interface for browsing and viewing the images in the specified directory.

## Example Command

To serve a folder of images located at `C:\Images`, run:
```bash
python app.py --base_dir "C:\Images"
```

### Command-Line Parameters

| Parameter    | Required | Description                                  |
|--------------|----------|----------------------------------------------|
| `--base_dir` | Yes      | Path to the directory containing the images. |

## Example Output

- **Directory Listing**:
  ```
  Directory listing for C:\Images
  - image1.jpg - 2024-12-13 10:00:00
  - image2.png - 2024-12-12 15:45:30
  ```

- **Image URLs**:
  ```
  http://localhost:8000/image/image1.jpg
  ```

## Troubleshooting

- **Invalid Directory**:
  If the specified directory does not exist, the script will exit with an error:
  ```
  FileNotFoundError: The specified base directory does not exist: <path>
  ```

- **Missing Flask**:
  If Flask is not installed, install it using:
  ```bash
  pip install flask
  ```

- **Port Already in Use**:
  By default, Flask uses port `8000`. If this port is already in use, Flask will try another port or provide instructions to specify a different one.

## License

This tool is released under the [MIT License](LICENSE).
