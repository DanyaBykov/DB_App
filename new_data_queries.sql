USE Medical_Screening;

# Insert
INSERT INTO Address (Country, City, Street, Zip_Code)
VALUES ('USA', 'New York', '5th Avenue', '10001');

# Complex Insert
INSERT INTO Patient (First_Name, Last_Name, Date_of_Birth, Gender, Phone_Number, Email, Age, Address_ID)
VALUES ('Ivan', 'Sen', '2006-02-02', 'Male',
        '123-456-890', 'ivan.sen@hospital.com', 19, 31);

SET @last_patient_id = LAST_INSERT_ID();

INSERT INTO Medical_History (Patient_ID, Past_Diseases, Past_Surgeries, Chronic_Conditions, Date_of_last_checkup)
VALUES (@last_patient_id, 'Hypertension',
        'Appendectomy', 'Diabetes', '2024-02-15');

# Replace
REPLACE INTO Hospital (Hospital_ID, Hospital_Name, Capacity, Address_ID)
VALUES (1, 'New York Hospital', 1000, 11);