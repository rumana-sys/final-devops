# Wild Rydes Infrastructure as Code (IaC)

This repository contains CloudFormation templates to deploy a scalable, highly redundant website for Wild Rydes, hosted on AWS.

## Infrastructure Overview

The CloudFormation template deploys the following AWS resources:

- VPC with two public subnets across different Availability Zones
- Internet Gateway and Route Tables for public access
- Application Load Balancer (ALB) with proper security groups
- ECS Cluster using Fargate launch type
- ECR Repository for Docker images
- CI/CD Pipeline using AWS CodePipeline, CodeBuild
- CloudWatch Alarms for monitoring build and deployment failures

## Architecture

The application architecture follows these principles:

1. **Containerized Application**: The application runs in Docker containers managed by ECS Fargate.
2. **High Availability**: The application runs across two subnets in different Availability Zones.
3. **Auto Scaling**: ECS service can be configured to scale based on load.
4. **CI/CD Pipeline**: Automated deployment pipeline that pulls from GitHub, builds Docker images, and deploys to ECS.
5. **Monitoring**: CloudWatch alarms to detect and notify on failures.

## Deployment Instructions

### Prerequisites

1. AWS CLI installed and configured with appropriate credentials
2. GitHub personal access token with repo permissions

### Steps to Deploy

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Deploy the CloudFormation stack:
   ```
   aws cloudformation create-stack \
     --stack-name wild-rydes-infrastructure \
     --template-body file://cloudformation.yaml \
     --parameters \
       ParameterKey=GitHubOwner,ParameterValue=<your-github-username> \
       ParameterKey=GitHubRepo,ParameterValue=<your-github-repo> \
       ParameterKey=GitHubBranch,ParameterValue=main \
       ParameterKey=GitHubToken,ParameterValue=<your-github-token> \
     --capabilities CAPABILITY_IAM
   ```

3. Monitor the stack creation:
   ```
   aws cloudformation describe-stacks --stack-name wild-rydes-infrastructure
   ```

4. Once deployment is complete, you can access the application using the LoadBalancerURL from the stack outputs:
   ```
   aws cloudformation describe-stacks \
     --stack-name wild-rydes-infrastructure \
     --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerURL'].OutputValue" \
     --output text
   ```

## CI/CD Pipeline

The CI/CD pipeline automatically:

1. Pulls code from the GitHub repository when changes are pushed
2. Builds a Docker image using the Dockerfile in the repository
3. Pushes the image to the ECR repository
4. Deploys the updated image to the ECS service

## Monitoring and Alarms

CloudWatch alarms are configured to monitor:
- CodeBuild failures
- ECS deployment failures

Alarms are sent to an SNS topic which can be subscribed to receive notifications. 