#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs) 2>/dev/null || true
streamlit run streamlit_app.py 