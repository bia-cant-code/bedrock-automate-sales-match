# Using Amazon Bedrock to build a simple automation system 

This repository contains a step-by-step guide and code samples build a simple automataion system powered by Generative AI to match new customers to relevant pricing plans in sales.

## What are we building

## Architecture

The architecture of the solution we are building.

![Architecture Diagram](images/br-sales-agent-arch.png)

1. User input their website URL on the Streamlit app
2. The app triggers the Amazon Bedrock agent
3. The agent forwards the website URL to an Amazon Bedrock Foundational Model such as Claude and determines the industry type
4. Based on the industry type, the agent queries the knowledge base and identifes the most suitable pricing plan
5. Returns pricing plan price and features to the user
6. Users interested in further details provide their email address
7. Upon receiving the email address, the agent sends an email containing the pricing plan details, including price and features, to the user.

## Initial setup

### Step 1: Creating S3 buckets
- In us-east-1 region, create an S3 bucket to store CloudGuardian's product details and features.

![Create S3 bucket](images/create-s3-bucket.png)

- Click on `Upload`
![Upload button](images/upload-on-s3.png)

- Upload sample PDF in s3docs folder to your S3 bucket and keep default settings.

![Upload PDF](images/add-pdf-s3.png)

- Once successfully uploaded, you should be able to view the file in your s3 bucket

![View S3 files](images/view-files-s3.png)

- Navigate to the Amazon Bedrock console, scroll on the left-hand side and click on `Model Access`

![Model Access](images/br-console.png)

- Click on `Manage model access`

![Manage model access](images/manage-model-access.png)

- Select all models

![Select models](images/select-models.png)

- Scroll down and `Save changes`

![Save changes](images/br-save-changes.png)




