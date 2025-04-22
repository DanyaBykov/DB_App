USE Medical_Screening;

SELECT * FROM Patient WHERE Last_Name = 'Doe';

DELETE FROM Patient
WHERE Last_Name = 'Doe';

DELETE FROM Hospital
WHERE Hospital_Name = 'General Hospital 2';