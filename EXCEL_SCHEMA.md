# LocalJobs Excel MVP Data Schema

File location: `data/jobs.xlsx`

The Excel workbook serves as the primary data store for the MVP. It contains 5 separate sheets.

---

## 1. Sheet: `Jobs`

Stores all posted job openings.

| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `JobID` | String (PK) | Unique Job Identifier | `JOB-1001` |
| `EmployerID` | String (FK) | Employer posting the job | `EMP-101` |
| `JobType` | String | Standard job category | `Driver` |
| `Location` | String | Major city | `Hyderabad` |
| `Locality` | String | Neighborhood / Locality | `Uppal` |
| `District` | String | Administrative district | `Medchal-Malkajgiri` |
| `State` | String | State | `Telangana` |
| `Salary` | Integer | Pay amount | `18000` |
| `SalaryType` | String | Pay interval (`Month`, `Day`, `Week`) | `Month` |
| `Hours` | String | Shift timing / hours | `9 AM - 6 PM` |
| `RequiredExperience` | String | Experience criteria | `1 year` |
| `Vacancies` | Integer | Number of open positions | `2` |
| `Description` | String | Plain language description | `Commercial car driver needed...` |
| `Status` | String | `Active`, `Closed`, `Expired` | `Active` |
| `Verified` | String | `Verified`, `Pending`, `Rejected` | `Verified` |
| `CreatedAt` | String (Date) | Date posted (`YYYY-MM-DD`) | `2026-10-01` |
| `ExpiryDate` | String (Date) | Date of expiration (`YYYY-MM-DD`) | `2026-12-31` |

> **Critical Rule**: A job is only voiced on the IVR and listed on the worker portal if:
> `Status == 'Active'` AND `Verified == 'Verified'` AND `ExpiryDate >= Today`.

---

## 2. Sheet: `Employers`

Stores registered local businesses and hiring contractors.

| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `EmployerID` | String (PK) | Unique Employer ID | `EMP-101` |
| `CompanyName` | String | Registered business or entity name | `Sri Krishna Logistics` |
| `ContactName` | String | Contact person | `Ramesh Reddy` |
| `Phone` | String | E.164 normalized phone | `+919876543210` |
| `Location` | String | Business address / locality | `Uppal, Hyderabad` |
| `Verified` | String | `Verified`, `Pending` | `Verified` |
| `CreatedAt` | String (Date) | Registration date | `2026-09-15` |

---

## 3. Sheet: `Workers`

Stores profiles of registered job seekers.

| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `WorkerID` | String (PK) | Unique Worker ID | `WRK-501` |
| `Phone` | String (Unique) | E.164 phone number (CLI) | `+919848012345` |
| `Language` | String | Preferred language code (`te`, `hi`, `en`) | `te` |
| `Location` | String | Base city | `Hyderabad` |
| `Locality` | String | Home neighborhood | `Uppal` |
| `PreferredJobType` | String | Category of interest | `Driver` |
| `Experience` | String | Experience summary | `3 years` |
| `CreatedAt` | String (Date) | Registration date | `2026-10-02` |

---

## 4. Sheet: `Applications`

Stores expressions of interest submitted via voice IVR or web.

| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `ApplicationID` | String (PK) | Unique Application ID | `APP-10001` |
| `WorkerID` | String (FK) | Worker profile ID | `WRK-501` |
| `WorkerPhone` | String | Worker telephone number | `+919848012345` |
| `JobID` | String (FK) | Job applied for | `JOB-1001` |
| `AppliedAt` | String (Timestamp)| Timestamp (`YYYY-MM-DD HH:MM:SS`) | `2026-10-20 11:15:00` |
| `Status` | String | `Interested`, `Shortlisted`, `Rejected` | `Interested` |

> **Duplicate Protection**: Before adding a row to `Applications`, the repository verifies whether `WorkerPhone` + `JobID` already exists. Duplicate applications are blocked.

---

## 5. Sheet: `Categories`

Job classification taxonomy.

| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `CategoryID` | String (PK) | Unique category code | `CAT-1` |
| `Name` | String | Standard English key | `Driver` |
| `TeluguName` | String | Telugu label | `డ్రైవర్` |
| `HindiName` | String | Hindi label | `ड्राइवर` |
| `EnglishName` | String | English label | `Driver` |
| `Active` | Boolean | Whether category is enabled | `TRUE` |
