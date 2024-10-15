# Cover Letter Generator for Job Applications

![Cover Letter Generator](cover_image.png) <!-- Optional: Add an image here -->

## Overview

This **Streamlit-based web application** enables users to generate **personalized cover letters** for job applications. By simply entering a job posting URL and listing the applicant's tech stack, the app extracts job details, matches the required skills with the applicant's projects, and generates a cover letter tailored to the specific role. This tool is designed for tech professionals who want to create targeted cover letters quickly and efficiently.

## Features

- **Job Posting Analysis**: Automatically extracts job descriptions and required skills from a job posting URL.
- **Skill Matching**: Analyzes the skills needed for the role and matches them with the applicant’s tech stack.
- **Project and Link Suggestions**: Recommends relevant projects from the applicant's portfolio, including links to showcase the work.
- **Personalized Cover Letter Generation**: Uses AI to generate a custom cover letter that aligns with the job's requirements.
- **User-Friendly Interface**: The web app is built with Streamlit, making it accessible and easy to use for both technical and non-technical users.

## Technologies Used

- **Streamlit**: Provides the interactive web interface.
- **ChromaDB**: Used as a vector database to store and query tech stack information.
- **LangChain**: Handles job description extraction and natural language generation.
- **Python**: Backend development language for implementing functionality.
- **pandas**: For data processing and manipulation.

## Installation

To get started with the Cover Letter Generator, follow these steps:

### Prerequisites

- **Python** (version 3.7 or higher)
- **pip** (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/yourusername/cover-letter-generator.git
cd cover-letter-generator
