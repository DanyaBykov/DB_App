USE Medical_Screening;

UPDATE Patient
SET Address_ID = 22
WHERE Patient_ID = 1;

UPDATE Patient
SET Address_ID = 21
WHERE Patient_ID = 2;

UPDATE Hospital
SET Capacity = 143
WHERE Hospital_ID = 7;

UPDATE Appointment
SET Status = 'Completed'
WHERE Appointment_ID = 1;

UPDATE Medical_History
SET Chronic_Conditions = 'Hypertension, Diabetes'
WHERE Patient_ID = 2;

UPDATE Medical_Screening_Test
SET Test_ID = 11
WHERE Test_ID = 10;