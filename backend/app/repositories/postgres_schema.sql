-- ==============================================================================
-- LocalJobs Production Database Schema (PostgreSQL DDL)
-- Compatible with: Supabase, Neon, AWS RDS, GCP Cloud SQL, and Docker PostgreSQL
-- ==============================================================================

-- 1. Employers Table
CREATE TABLE IF NOT EXISTS employers (
    employer_id VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    location VARCHAR(255) NOT NULL,
    verified VARCHAR(50) NOT NULL DEFAULT 'Pending',
    created_at VARCHAR(50) NOT NULL
);

-- 2. Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR(50) PRIMARY KEY,
    employer_id VARCHAR(50) NOT NULL REFERENCES employers(employer_id) ON DELETE CASCADE,
    job_type VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL DEFAULT 'Hyderabad',
    locality VARCHAR(255) NOT NULL,
    district VARCHAR(255) NOT NULL DEFAULT 'Medchal-Malkajgiri',
    state VARCHAR(255) NOT NULL DEFAULT 'Telangana',
    salary INTEGER NOT NULL DEFAULT 0,
    salary_type VARCHAR(50) NOT NULL DEFAULT 'Month',
    hours VARCHAR(100) NOT NULL DEFAULT '8 hours',
    required_experience VARCHAR(100) NOT NULL DEFAULT 'Fresher',
    vacancies INTEGER NOT NULL DEFAULT 1,
    description TEXT NOT NULL DEFAULT '',
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    verified VARCHAR(50) NOT NULL DEFAULT 'Pending',
    created_at VARCHAR(50) NOT NULL,
    expiry_date VARCHAR(50) NOT NULL DEFAULT '2026-12-31'
);

-- 3. Workers Table
CREATE TABLE IF NOT EXISTS workers (
    worker_id VARCHAR(50) PRIMARY KEY,
    phone VARCHAR(50) UNIQUE NOT NULL,
    language VARCHAR(10) NOT NULL DEFAULT 'te',
    location VARCHAR(255) NOT NULL DEFAULT 'Hyderabad',
    locality VARCHAR(255) NOT NULL DEFAULT 'Uppal',
    preferred_job_type VARCHAR(100) NOT NULL DEFAULT 'Driver',
    experience VARCHAR(100) NOT NULL DEFAULT 'Fresher',
    created_at VARCHAR(50) NOT NULL
);

-- 4. Applications Table
CREATE TABLE IF NOT EXISTS applications (
    application_id VARCHAR(50) PRIMARY KEY,
    worker_id VARCHAR(50) REFERENCES workers(worker_id) ON DELETE SET NULL,
    worker_phone VARCHAR(50) NOT NULL,
    job_id VARCHAR(50) NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    applied_at VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Interested',
    CONSTRAINT uq_worker_job_application UNIQUE (worker_phone, job_id)
);

-- 5. Categories Table
CREATE TABLE IF NOT EXISTS categories (
    category_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    telugu_name VARCHAR(100) NOT NULL,
    hindi_name VARCHAR(100) NOT NULL,
    english_name VARCHAR(100) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_jobs_search_active ON jobs(status, verified, expiry_date);
CREATE INDEX IF NOT EXISTS idx_jobs_type_locality ON jobs(job_type, locality);
CREATE INDEX IF NOT EXISTS idx_jobs_employer ON jobs(employer_id);
CREATE INDEX IF NOT EXISTS idx_workers_phone ON workers(phone);
CREATE INDEX IF NOT EXISTS idx_applications_phone ON applications(worker_phone);
CREATE INDEX IF NOT EXISTS idx_applications_job ON applications(job_id);
