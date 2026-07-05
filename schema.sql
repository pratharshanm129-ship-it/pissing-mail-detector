-- ==========================================================
-- AI Phishing Email Detector - Database Schema
-- SQLite Database Creation Script
-- ==========================================================

-- Drop tables if they already exist (useful for a clean re-run)
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS users;

-- ----------------------------------------------------------
-- Table: users
-- Stores registered user account information
-- ----------------------------------------------------------
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------
-- Table: predictions
-- Stores the history of every email checked by every user
-- ----------------------------------------------------------
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    email_text TEXT NOT NULL,
    prediction TEXT NOT NULL,
    confidence INTEGER NOT NULL,
    risk_level TEXT NOT NULL,
    keywords_found TEXT,
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Helpful index for fetching a user's history quickly
CREATE INDEX idx_predictions_user_id ON predictions (user_id);
