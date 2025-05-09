\# Wisecow Kubernetes Deployment

This repository contains a complete production-style setup for deploying the Wisecow application using Docker and Kubernetes. The goal of this project was to containerize the original shell-based Wisecow app and deploy it securely on a Kubernetes cluster with TLS encryption, leveraging modern DevOps practices including GitHub-based CI/CD.

The application logic was provided in a shell script (`wisecow.sh`), which listens on a TCP port and responds to HTTP requests with a randomly selected fortune wrapped using `cowsay`. Due to constraints of the challenge, the script itself was not modified, and all deployment work had to be built around it.


## Dockerization

To containerize the application, we created a Dockerfile based on an Ubuntu base image. All required dependencies like `cowsay`, `fortune-mod`, and `netcat` were installed within the image. Because the original application expects to use `nc` with flags not available in Alpine Linux, an Ubuntu-based image was chosen for compatibility. Symlinks were created to ensure the cowsay and fortune binaries were accessible via the system's `PATH`.

A custom wrapper ensured that netcat bound correctly to the specified port, working within containerized environments where behavior can differ from a bare-metal shell.


## Kubernetes Deployment

The application was deployed as a Kubernetes Deployment object, with a corresponding Service of type `NodePort` to make the container accessible within the cluster.

The Deployment YAML ensures the container runs on port 4499, and the Service exposes this on port 80 within the cluster and via a random high port on the host. Proper labels were added to tie the pods to the Service and to enable Ingress routing later.


## Ingress and TLS with cert-manager

To securely expose the application over HTTPS, an NGINX Ingress controller was deployed using official manifests. The Ingress routes incoming requests for `https://wisecow.local` to the backend service.

For TLS encryption, `cert-manager` was installed and configured with a self-signed issuer. A certificate resource was defined to generate and manage a TLS certificate for the `wisecow.local` domain, which is then referenced in the Ingress definition.

This setup simulates a production-grade HTTPS deployment, even though the certificate is self-signed. The local `/etc/hosts` file can be edited to route `wisecow.local` to `127.0.0.1` for browser-based testing.


## CI/CD Pipeline with GitHub Actions

A GitHub Actions workflow was added to automate Docker builds and push them to Docker Hub whenever code is pushed to the main branch. The workflow ensures consistency in the image building process and avoids manual intervention.

While automated deployment to Kubernetes was marked as an optional challenge, the workflow is designed to be easily extended to perform `kubectl apply` commands using GitHub secrets, allowing continuous delivery in real-world scenarios.


## Running the Application

After deployment, the application can be accessed in several ways depending on your local Kubernetes setup

For Ingress-based access, ensure this line is added to `/etc/hosts`:

