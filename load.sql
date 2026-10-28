SET GLOBAL local_infile = 1;
CREATE DATABASE IF NOT EXISTS credit_risk;
USE credit_risk;
DROP TABLE IF EXISTS loans;

CREATE TABLE loans (
  person_age INT,
  person_income INT,
  person_home_ownership VARCHAR(20),
  person_emp_length DOUBLE NULL,
  loan_intent VARCHAR(30),
  loan_grade VARCHAR(5),
  loan_amnt INT,
  loan_int_rate DOUBLE NULL,
  loan_status INT,
  loan_percent_income DOUBLE,
  cb_person_default_on_file VARCHAR(5),
  cb_person_cred_hist_length INT
);

LOAD DATA LOCAL INFILE 'P:/credit card default/archive/credit_risk_dataset.csv'
INTO TABLE loans
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(person_age, person_income, person_home_ownership, @emp, loan_intent, loan_grade,
 loan_amnt, @rate, loan_status, loan_percent_income, cb_person_default_on_file,
 cb_person_cred_hist_length)
SET person_emp_length = NULLIF(@emp, ''),
    loan_int_rate = NULLIF(@rate, '');

SELECT COUNT(*) FROM loans;