Tools For Change (TFC)
------------------------------------------------------------------------------------------------------

# Summary
TFC in a generic application, which can be used by any organization (for-profit or non-profit) to engage the community and also raise money for their cause. This becomes a placeholder for adding any common tools that can be used by organizations like CTSC.

# Goal(s)
	- A way for orgnizations to seek volunteers and screen them
	- Raise donation requests on organizations behalf
    - A way to show case their mission vision and their story.

# Domain Overview
	# Organization
	Organization is any governmental or non-governmental organization that can signup for an account on our platform and use our tools for change for their cause.

	# Volunteer
	Volunteer is any individual who is willing to contribute their time and skills towards their cause of choice by working closely with any organization

	# Donation
	Donation is money contribution towards any particular organizations cause or for core operations.

# Feature Overview
	- Organizations should be able to signup and login
	- Organizations should be able to manage their own volunteer requrirements and volunteer registrations
	- Organizations should be able to accept donations and review the same across their own specific needs
	- That means organiztion(s) should be able to specify their needs, and people can select a need and select a comfortable amount that they can donate	
	- We end our process by taking them to a page, where we are sending a request to the user for the donatoin amount on their upi app.

# Application Overview
	## Global Static Pages
		- Home Page 
			https://www.forchange.in/

	## Gloabal Dynamic Pages
		- Org List
			https://www.forchange.in/orginizations
			
			- By cause etc. (Somethign like a Filter or a tag or a label) 
				https://www.forchange.in/orginizations/{label}
		
		- Organization Registration
			https://www.forchange.in/organizations/signup (Admin Member Details as well here)

	# Organization Pages (Subdomain level)
		- Org Home Page
			https://factly.forchange.in

		- Org Donation Request Page
			https://factly.forchange.in/donate
            https://factly.forchange.in/donate/thankyou

		- Organization Login
			https://factly.forchange.in/login

		- Organization Volunteer Signup
			https://factly.forchange.in/volunteer

		- Volunteer Screning
			https://factly.forchange.in/volunteer/screening/:screning_id

	## Organization Dashboard (Private, Only when somebody is logged in)
		- Org Dashboard
			https://factly.forchangein/dashboard

		- Org profile management
			- Basic Profile
			- UPI Details

		- Team Management
			- Member List page
				https://factly.forchange.in/members
			
			- Organization Member Magement
				https://factly.forchange.in/members/new
				https://factly.forchange.in/members/:member_id/edit
				
				- Activate a member
				https://factly.forchange.in/members/activate/:invitation_token
					After activation we clear the invitation_token
				
				- Set password first time after activation, secon	
				https://factly.forchange.in/members/:member_id/set_password

		- Volunteer Management (Applications)
			- List / Detail
		
		- Donation Intent Management (Donations)
			- List / Detail / Metrics etc

		- Donation Requests Raised
		    - Mark it as full filled
		    - Request to raise again

	## Admin Panel
		https://www.forchange.in/admin

		- Organization Management
			- Create an organization manually
			- Metrics

		- Member Management at orginzation level
			List members
				Members, activation status
		
		- Volunteer Management
			- Metrics

		- Donation Management
			- Metrics

------------------------------------------------------------------------------------------------------
Screening App
------------------------------------------------------------------------------------------------------

# Summary
	 A rootless screening app that can be used be anybody for screening people  

# Goal(s)
	Goal is to abstract out the screening functionality that can be used by any body in the future, to screen their candidates.

# Domain
	# Candidate
	Candidate is any individual who can be evaluated based on his own interests and skillset.

	# Expertise Areas 
		These are the categories to which a candidate belongs.   
		Ex:Design,Engineering,Management,Marketing  

	# Expertise  
		These are the sub categories for particular categories.  
		Ex:Python,Django comes under the Engineering  
		Digital marketing comes under Marketing  
		Project management comes under Management  

	# Questions  
		All the questions are multiple choice having 4 options from which only one is correct answer.  

	# Question Type	
		Question type are multiple choice.    

# Feature Overview
	- Candidate screening workflow
		- Create a screening
		- Create a screening page where some is actually screened
		- On succeful submittee, say say thankyou

	- Screening should change based on level of expertise a person has
		- Entry level is for 0 to 2+ years of experience  
		- Intermediate is for 3+ to 5+ years of experience people
		- Advanded  is for 10+ to 15+ years of experience  
		- Experty is for 20+ years of exp.

	- Randomized so that not everyone is seeing the same test
	- every screening can be given a passing criteria
	- Admin Panel to manage the questions and the question bank
	- Admin Panel to mange the screenings

# Screening Criteria  
	- Screening is based on the level of expertise  and area of expertise  
	- Every screening consist of 10 questions from the area of expertise 
	- All the questions from different topics under the area of expertise  
	- Qualifying criteria of  screening is 70%   
	- Once screening completes the status of the candidate automatically change from "New" to "Passed" or "Failed" on organization dashboard.  
	- Until the candidate has not attempted the screening the status of screening is "Open".
	- After completion of screening its result will display in the screening result pages. 

# Application Overview
	## Screening 		
		- Screening Page
		- Thank you Page

	## Admin Pages
		- Screenings List
		- Question Types List
		- Question Bank
		- Question Categories
			- Areas
		- Question Sub Categories
