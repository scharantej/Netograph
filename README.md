## Flask Application Design: GCP Project Network Architecture Diagram Generator

### HTML Files

- **index.html**: This file defines the landing page of the application. It provides a user interface for uploading a GCP project ID and submitting it for analysis.
- **results.html**: This file displays the generated network architecture diagram. It includes a header with the project ID and an image of the diagram.

### Routes

- **home route ('/')**: This route renders the `index.html` file and presents the user interface for uploading a GCP project ID.
- **submit route ('/submit')**: This route receives the GCP project ID and initiates the analysis process. It fetches the project details using the Google Cloud Platform API and generates the network architecture diagram.
- **result route ('/result')**: This route renders the `results.html` file, displaying the generated network architecture diagram.