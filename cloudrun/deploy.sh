#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID="${1:-your-gcp-project-id}"
REGION="${2:-us-central1}"
SERVICE="${3:-openshell-nemoclaw-demo}"

gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

gcloud builds submit --tag "gcr.io/$PROJECT_ID/$SERVICE"

gcloud run deploy "$SERVICE" \
  --image "gcr.io/$PROJECT_ID/$SERVICE" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated
