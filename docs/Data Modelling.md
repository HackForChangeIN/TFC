TFC Modelling
------------------------------------------------------------------------------------------------------

## Organization | organizations (Governmental/ Non-Governmental organization)
    Name | String | name | required | Ex:factly
    Website |String  | website | required |  Ex: http://www.factly.in/  
    Organization Brief | Text| organization_brief| required |  Ex: Factly is a Hyderabad based fact checking organization focused on fake news detection and educaition
    Contact Phone Number | String | phone_number | required 
    Contact Email | String | email | required
    Logo | Image | logo | required
    City | String | city | required
    Focus Area | String | focus_area | required | EX:"open gov","democracy"   
    
    * Not asked during signup
    State | String | state | required
    subdomain | String | subdomain | Automatically generated based on organization abbreviation, which can changed by the admin later.
    thankyou_template | String | thankyou_template | Automatically generated the first time, the organization will have option to edit it later.
    UPI Identifier | String | upi_id | Ex: factly@okhdfcbank
    
## Member (Team Members) | members
    Name | String | member_name | required | Ex: Rakesh Dubbudu
    Email | String | member_email | required
    Phone Number | String | member_phone_number| required |Ex: +91 8888, We should be able to accept international numbers as well
    Password | String | password | required
    Invitation Auth Token | String | auth token | Created and sent in the email link, On password setup, auth token is cleared, if the auth token is nil, the email link will expire.
    *role | String | role | Possible: "Primary Contact(Admin) / Member"

## Volunteer Information | volunteers (This is a subclass of the candidate model)
    *This can be any kind of profession (other than tech, desing, project mangament) 
    Current Occupation | String | current_occupation | required | Ex: Student, Working Professional, Govenment Official
    Availability | String | availability | required | Ex: 0 - 10hours, 10 - 20hours, 20 - 30hours, 30 - 40hours per week  Based on this we are populating the level of expertise.  
    Years Of Experience | String | years_of_experience | required | "No Experience, 1+ years, 2+ years, 3+ years, 5+ years, 10+years, 15+years, 20+ years"
    Organization Mapping | integer | organization_id | This essentially means a volunteer is tied to a particular organization as an applicant

## Donation Intents | donation_intents
    Organization Association | integer| organization_id | 
    Intent Amount | float | intent_amount | Ex: 100.00, 500.00, 1000.00
    Intent Frequency | string | intent_frequency | Ex: One Time, Monthly, Quarterly, Annually
    Donor First Name | string | first_name
    Donor Last Name | string | last_name 
    Donor Email | string | donor_email
    Donor Phone Number | string | donor_mobile
    Donor Comment | text | comments
    Donor Anonymity | string | donor_anonymity | Ex: Yes / No    
    Subscription

## Platform Donation Requests (Jobs)
    Donor Full Name | string | donor_fullname
    Donor Phone Number | string | donor_mobile
    Donation Request Amount | float | request_amount
    Status | string | status | Ex: Open, Raised, Full-filled
    
------------------------------------------------------------------------------------------------------
Screening App Models (Should be usable by volunteers/non-volunteers as well)
------------------------------------------------------------------------------------------------------

## Candidate | candidates
    Name | String | name | required
    Email | String | email | required  
    Contact Number | String | contact_number | required  
    Gender | String | gender | not required  
    D.0.B | Datefield | dob |  not required 
    Highest Education | String | highest_education | Possible Values: "Intermediate, Bachelors, Masters" |required  
    Profession | String | profession | Ex: Design, Engineering, Management, Operations, HR,  etc. (This should be populated form area of category from category table)  
    Area of Expertise (Skills) | String | area_of_expertise | Ex: For Contributer "Python, CSS, HTML, Databases", For Mentor "Project Management| required  
    Level of Expertise | String | level_of _expertise | Possible Values: "Entry Level, Intermediate, Advanced, Expert" | required  
    
## Expertise Areas | expertise_areas
    Expertise Area Id | Integer | expertise_area_id
    Area Of Expertise (Profession) | String | area_of_expertise | Ex: Design, Engineering
    
## Expertise | expertise     
    Expertise Id | Integer | expertise_id
    Expertise Name | String | expertise | required | Ex: Python, Ruby, HTML, CSS, Java,
    Expertise Area Mapping | integer | expertise_area_id  
    is published | Boolean | is_published 
    
## Question Bank | questions
    Question | Text | question | required 
    type | String | qtype | Possible Values: "Multiple Choice, Yes/No"
    Option 1 | Text | option_1 | required when type is multiple choice
    Option 2 | Text | option_2 | required when type is multiple choice
    Option 3 | Text | option_3 | required when type is multiple choice
    Option 4 | Text | option_4 | required when type is multiple choice
    yes / no | String | yes_no | Possiblie Valaues: "YES, NO"
    Answer | String | answer | required  
    Question Image | Image | question_image | not required  
    Area Of Expertise Mapping | integer | expertise_area_id | required  (Is mapped with candidate/volunteers profession)  
    Expertise Mapping | integer | expertise_id | required (Is mapped with candidate/volunteers area of expertise) 
    Question Level Mapping | integer | level | entry, intermediate, advanced, expert | required (Is mapped with candidate/volunteers level_of_expertise)   
    Topic | String | topic | required | Ex: ORM, DOM Model, CSS Animations etc.  

## Screening with lots of questions | screenings_questions
    Screening Association | integer | screening_id | required  
    Question Association | integer | question_id | required  
    Candidates Answer | String | candidates_answer 
    Correct Answer | String | correct_ans | required  
    Answers Correctness | Boolean | answer_correctness | Ex: True, False

## Many to Many Screening | screenings
    
    Screening UUID | String | screening_uuid | Ex: SCRNGSMTY01, SCRNGSMTY02 so on which is auto generated whenever you create the record
    Candidate association | integer | candidate_id
    Screening association | id | screening_id
    Status | String | Possible Values: "New, Closed, Passed, Failed" 
    Screening Result | String | screening_result | Possible Values:60%,50%,  
    Created On | Date | created_on | not required 
    First Reminder Date | Date | first_reminder_date | not required 
    Second Reminder Date | Date | second_reminder_date | not required 
    Third Reminder Date | Date | third_reminder_date | not required  

