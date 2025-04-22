USE Medical_Screening;

# Union
SELECT First_Name FROM Patient
UNION
SELECT First_Name FROM Doctor;

# Intersection
SELECT First_Name FROM Patient
INTERSECT
SELECT First_Name FROM Doctor;

# Difference
SELECT First_Name FROM Patient
EXCEPT
SELECT First_Name FROM Doctor;

# Cartesian Product
SELECT
    Patient.First_Name AS Patient_First_Name,
    Patient.Last_Name AS Patient_Last_Name,
    Doctor.First_Name AS Doctor_First_Name,
    Doctor.Last_Name AS Doctor_Last_Name
FROM
    Patient
CROSS JOIN
    Doctor;

# Selection
SELECT * FROM Patient WHERE Age > 30;

# Projection
SELECT DISTINCT First_Name, Last_Name, Gender, Age FROM Patient;

# Theta Join
SELECT
    Patient.First_Name AS Patient_First_Name,
    Doctor.First_Name AS Doctor_First_Name,
    Patient.Age AS Patient_Age,
    Doctor.Age AS Doctor_Age
FROM
    Patient JOIN Doctor
ON
    Patient.Age = Doctor.Age;