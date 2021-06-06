## Test procedure for verifying site administrators can update vehicle model information.

The purpose of this test is to verify that a site administrator can use the built-in Django admin interface to perform CRUD (create, read, update, delete) operations on the vehicle data model entries. This capability allows site administrators to update BottomLine on the fly with current vehicle information if needed.

###### Preconditions:
- Tester has access to the admin console credentials in LastPass
- BottomLine has been deployed locally (refer to BottomLine Deployment Guide)
- All data model migrations have been applied
- The Django test server is up and running on port 8000

###### Procedure:
1. Open a browser and navigate to: http://127.0.0.1:8000/admin
2. Retrieve the admin credentials (username and password) from the LastPass vault
3. Enter the credentials in the username and password fields and click "Log in"
4. The Django administration site is presented. Locate the BLWEB block on the left side of the page.
5. Verify the presence of BLWEB title block and the following data models:
    - Vehicle makes
    - Vehicle models
    - Vehicle options
6. Click on Vehicle makes
7. In the top-right of the page, click on "ADD VEHICLE MAKE"
8. Verify the following two fields are presented:
    - Name
    - Website
9. Enter the information in quotes below into each field:
    - Name: "Ford"
    - Website: "www.ford.com"
10. Click SAVE
11. Verify the site displays the following information:
    - 'The vehicle make "Ford" was added successfully' is displayed at the top of the screen
    - "Ford" is shown in the table under VEHICLE MAKE
12. Click on "Vehicle models" using the link on the left pane of the site
13. In the top-right of the page, click on "ADD VEHICLE MODEL"
14. Verify the following two fields are presented:
    - Name
    - Year
    - Make
15. Enter the information in quotes below into each field:
    - Name: "Mustang"
    - Year: "2021"
    - Make: "Ford" (Use the picklist to select this option)
16. Click SAVE
17. Verify the site displays the following information:
    - 'The vehicle model "Mustang" was added successfully' is displayed at the top of the screen
    - "Mustang" is shown in the table under VEHICLE MODEL
18. Click on the "Mustang" entry in the list
19. The "Change vehicle model" page is displayed.
20. Change the Year field from 2021 to 2020. Click SAVE.
21. Verify the page displays the "The vehicle model "Mustang" was changed successfully" message.
22. Click on the "Mustang" entry. 
23. Verify the Year is now shown as 2020.
24. Click "Delete". Click "Yes, I'm sure"
25. Verify the "The vehicle model "Mustang" was deleted successfully" message is displayed
26. Click on "Vehicle makes"
27. Click on "Ford"
28. Click "Delete". Click "Yes, I am sure"
29. Verify the "The vehicle make "Ford" was deleted succesfully" message is displayed.
30. Log out of the application by selecting the "LOG OUT" link from the top right of the page.

This concludes the test procedures for this test. If all "verify" steps indicate a pass, this test has passed.

###### Post-conditions / Test Results:
 - The tester is logged out of the application
 - The test results are as follows:
    - All "verify" steps in the procedure indicate a pass: This test passes 
    - ANY "verify" step in the procedure fails: This test fails.