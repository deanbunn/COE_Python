#!/usr/bin/env python3

import sys
import json
import urllib
import urllib.request

# Var for Headers
coe_headers = {"coe-key":"your_api_key"}

# Var for Base API URL
coe_base_url = "https://xxxxxxxxxxxxxx.coe.ucdavis.edu/api/"

# Class for AD3 User
class AD3User:
	def __init__(self):
		self.account_status = ""
		self.sam = ""
		self.cn = ""
		self.upn = ""
		self.display_name = ""
		self.first_name = ""
		self.last_name = ""
		self.last_password_change = ""
		self.last_login = ""
		self.exchange_status = ""
		self.email_primary = ""
		self.email_addresses = []
		self.group_membership = []



# End of AD3User Class

# Class for AD3 User Group Membership
class AD3UserGM:
	def __init__(self):
		self.grp_guid = ""
		self.grp_name = ""



# End of AD3UserGM Class

# Class for OU Group
class OUGroup:
	def __init__(self):
		self.grp_guid = ""
		self.grp_name = ""
		self.grp_type = ""
		self.grp_email = ""
		self.grp_dn = ""
		self.grp_members = []


# End of OUGroup Class

# Class for OU Group Member
class OUGroupMember:
	def __init__(self):
		self.upn = ""
		self.domain = ""
		self.sam = ""
		self.display_name = ""
		self.email_address = ""


# End of OUGroupMember

# Function for uGroup
def ugroup(srch_term):

	# Set API URL
	coe_url = coe_base_url + "ugroup/" + urllib.parse.quote(srch_term)

	# Set Up Request
	coe_request = urllib.request.Request(coe_url,None,coe_headers)
	
	# Call API
	coe_response = urllib.request.urlopen(coe_request)
	
	# Pull Returned Json
	dct_ugroup = json.loads(str(coe_response.read(),'utf-8'))
	
	# Initiate OUGroup
	ouGrp = OUGroup() 
	ouGrp.grp_guid = dct_ugroup["grp_guid"]
	ouGrp.grp_name = dct_ugroup["grp_name"]
	ouGrp.grp_type = dct_ugroup["grp_type"]
	ouGrp.grp_email = dct_ugroup["grp_email"]
	ouGrp.grp_dn = dct_ugroup["grp_dn"]
	
	#Check Membership
	if(dct_ugroup["grp_members"] and len(dct_ugroup["grp_members"]) > 0):
		
		for grpmbr in dct_ugroup["grp_members"]:
			
			#Initiate OU Group Member
			ouGrpMbr = OUGroupMember()
			ouGrpMbr.upn = grpmbr["upn"]
			ouGrpMbr.domain = grpmbr["domain"]
			ouGrpMbr.sam = grpmbr["sam"]
			ouGrpMbr.display_name = grpmbr["display_name"]
			ouGrpMbr.email_address = grpmbr["email_address"]
			
			# Add Group Member to Members Listing
			ouGrp.grp_members.append(ouGrpMbr)
		

	return ouGrp


# Function for uUser
def uuser(srch_term):

	# Set API URL
	coe_url = coe_base_url + "uuser/"  +  srch_term

        # Set Up Request
	coe_request = urllib.request.Request(coe_url,None,coe_headers)

	# Call API
	coe_response = urllib.request.urlopen(coe_request)

	# Pull Returned Json
	dct_uuser = json.loads(str(coe_response.read(),'utf-8'))

	#Initiate AD3User
	ad3Usr = AD3User()
	ad3Usr.account_status = dct_uuser["account_status"]
	ad3Usr.sam = dct_uuser["sam"]
	ad3Usr.cn = dct_uuser["cn"]
	ad3Usr.upn = dct_uuser["upn"]
	ad3Usr.display_name = dct_uuser["display_name"]
	ad3Usr.first_name = dct_uuser["first_name"]
	ad3Usr.last_name = dct_uuser["last_name"]
	ad3Usr.last_password_change = dct_uuser["last_password_change"]
	ad3Usr.last_login = dct_uuser["last_login"]
	ad3Usr.exchange_status = dct_uuser["exchange_status"]
	ad3Usr.email_primary = dct_uuser["email_primary"]
	
	#Check for Email Addresses
	if(len(dct_uuser["email_addresses"]) > 0):
		for emladdr in dct_uuser["email_addresses"]:
			ad3Usr.email_addresses.append(emladdr)

	
	#Check for Group Membership
	if(len(dct_uuser["group_membership"]) > 0):
		for grpmbrshp in dct_uuser["group_membership"]:
			ad3Usr.group_membership.append(grpmbrshp["grp_name"])


		
	return ad3Usr


# Function for Displaying AD3 User Values
def displayAD3User(ad3User):
	print(" ")
	print("###################################################")
	print(" ")
	print("Account Status: " + ad3User.account_status) 
	print(" ")
	print("sAMAccountName: " + ad3User.sam)
	print(" ")
	print("CN: " + ad3User.cn)
	print(" ")
	print("UPN: " + ad3User.upn)
	print(" ")
	print("Display Name: " + ad3User.display_name)
	print(" ")
	print("First Name: " + ad3User.first_name)
	print(" ")
	print("Last Name: " + ad3User.last_name)
	print(" ")
	print("Last Password Change: " + ad3User.last_password_change)
	print(" ")
	print("Last Login: " + ad3User.last_login)
	print(" ")
	print("Exchange Status: " + ad3User.exchange_status)
	print(" ")
	print("Email Primary: " + ad3User.email_primary)
	print(" ")
	print("Email Addresses: ")
	
	if(len(ad3User.email_addresses) > 0):
		for emladr in ad3User.email_addresses:
			print("\t" + emladr)


	
	print(" ")
	print("Group Membership: ")
	if(len(ad3User.group_membership) > 0):
		for grpmbrshp in ad3User.group_membership:
			print("\t" + grpmbrshp)


	print(" ")
	print("###################################################")
	print(" ")

	return

# End of displayAD3User Function

# Function for Pulling and Displaying All COE OU Users
def displayOUUsers():
	
	# Set API URL
	coe_url = coe_base_url + "uuser"

	# Set Up Request
	coe_request = urllib.request.Request(coe_url,None,coe_headers)

	# Call API
	coe_response = urllib.request.urlopen(coe_request)

	# Pull Returned Json
	dct_ou_users = json.loads(str(coe_response.read(),'utf-8'))

	# Null\Empty Check on Returned OU Users
	if(dct_ou_users and len(dct_ou_users) > 0):
		
		print(" ")
		coePrintTabSpaced("UPN","Common Name")
		coePrintTabSpaced("-----------","------------")	
	
		for ouusr in dct_ou_users:
			coePrintTabSpaced(ouusr["upn"],ouusr["cn"])

				
		print(" ")
		

	return

# End of displayOUUsers Function

# Function for Displaying OU Computers
def displayOUComputers():
	
	# Set API URL
	coe_url = coe_base_url + "ucomputer"

	# Set Up Request
	coe_request = urllib.request.Request(coe_url,None,coe_headers)
	
	# Call API
	coe_response = urllib.request.urlopen(coe_request)

	# Pull Returned Json
	dct_ou_computers = json.loads(str(coe_response.read(),'utf-8'))

	# Null\Empty Check on Returned OU Computers
	if(dct_ou_computers and len(dct_ou_computers) > 0):
		print(" ")
		coePrintTabSpaced("Computer Name","Operating System")
		coePrintTabSpaced("--------------","----------------")		

		for oucmp in dct_ou_computers:

			coePrintTabSpaced(oucmp["cmp_name"], oucmp["os"])


		print(" ")	


	return

# End of displayOUComputers Function

# Function for OU Computer
def displayOUComputer(srch_term):
	
	# Set API URL
	coe_url = coe_base_url + "ucomputer/" + srch_term

	# Set Up Request
	coe_request = urllib.request.Request(coe_url,None,coe_headers)

	# Call API
	coe_response = urllib.request.urlopen(coe_request)
	
	# Pull Returned Json
	dct_ou_cmptr = json.loads(str(coe_response.read(),'utf-8'))

	# Null\Empty Check on Returned OU Computer
	if(dct_ou_cmptr):
		print(" ")
		print("#############################################")
		print(" ")
		print("Computer Name: " + dct_ou_cmptr["cmp_name"])
		print(" ")
		print("Operating System: " + dct_ou_cmptr["os"])
		print(" ")
		print("When Created: " + dct_ou_cmptr["when_created"])
		print(" ")
		print("Last System Auth: " + dct_ou_cmptr["last_auth"])
		print(" ")
		print("Distinguished Name: " + dct_ou_cmptr["dn"])
		print(" ")
		print("##############################################")
		print(" ")


	return

# End of displayOUComputer Function

# Function for OU Group
def displayOUGroup(ouGroup):
	print(" ")
	print("################################################")	
	print(" ")
	print("Group Name: " + ouGroup.grp_name)
	print(" ")
	print("Group Guid: " + ouGroup.grp_guid)
	print(" ")
	print("Group Type: " + ouGroup.grp_type)
	print(" ")
	print("Group Email: " + ouGroup.grp_email)
	print(" ")
	print("Group DN: " + ouGroup.grp_dn)
	print(" ")
	print("Group Membership: ")
	print(" ")
	#Check Group Membership
	if(len(ouGroup.grp_members) > 0):
		for grpMbr in ouGroup.grp_members:
			coePrintIndentedTabSpaced(grpMbr.upn,grpMbr.display_name)	



	print(" ")
	print("##################################################")
	print(" ")


	return

# End of displayOUGroup Function

# Function for Displaying OU Groups
def displayOUGroups():

	# Set API URL
	coe_url = coe_base_url + "ugroup"

	# Set Up Request
	coe_request = urllib.request.Request(coe_url,None,coe_headers)
	
	# Call API
	coe_response = urllib.request.urlopen(coe_request)	

	# Pull Returned Json
	dct_ou_groups = json.loads(str(coe_response.read(),'utf-8'))

	# Null\Empty Check on Returned OU Groups
	if(dct_ou_groups and len(dct_ou_groups) > 0):

		print(" ")
		coePrintTabSpaced("Group Guid","Group Name")
		coePrintTabSpaced("-----------","-----------")

		for ougrp in dct_ou_groups:
			coePrintTabSpaced(ougrp["grp_guid"],ougrp["grp_name"])

                
		print(" ")

	return

# End of displayOUGroups Function

# Function for Displaying uCampus
def displayuCampus(srch_term):
	
	# Set API URL
	coe_url = coe_base_url + "ucampus/" + srch_term

	# Set Up Request
	coe_request = urllib.request.Request(coe_url,None,coe_headers)
	
	# Call API
	coe_response = urllib.request.urlopen(coe_request)

	# Pull Returned Json
	dct_campus_usr = json.loads(str(coe_response.read(),'utf-8'))

	# Null\Empty Check on Returned Campus User
	if(dct_campus_usr and len(dct_campus_usr) > 0):
		
		print(" ")
		print("###########################################")
		print(" ")
		print("Campus UID: " + dct_campus_usr["kerb_id"])
		print(" ")
		print("UCD UUID: " + dct_campus_usr["ucduuid"])
		print(" ")
		print("Common Name: " + dct_campus_usr["common_name"])
		print(" ")
		print("First Name: " + dct_campus_usr["first_name"])
		print(" ")
		print("Last Name: " + dct_campus_usr["last_name"])
		print(" ")
		print("Display Name: " + dct_campus_usr["display_name"])
		print(" ")
		print("Mail: " + dct_campus_usr["mail"])
		print(" ")
		print("UCD Affiliation: " + dct_campus_usr["ucd_affiliation"])
		print(" ")
		print("Title: " + dct_campus_usr["title"])
		print(" ")
		print("Department: " + dct_campus_usr["department_name"])
		print(" ")
		print("Department Code: " + dct_campus_usr["department_code"])
		print(" ")
		print("Address: " + dct_campus_usr["postal_address"])
		print(" ")
		print("Telephone: " + dct_campus_usr["telephone_number"])
		print(" ")
		print("Student Level: " + dct_campus_usr["student_level"])
		print(" ")
		print("Student Major: " + dct_campus_usr["student_major"])
		print(" ")
		print("###########################################")
		print(" ")


	return

#End of displayuCampus

# Function for Pulling and Displaying uSearch Results
def displayuSearchResults(srch_term):

	# Set API URL
	coe_url = coe_base_url + "usearch/" + urllib.parse.quote(srch_term)

	# Set Up Request
	coe_request = urllib.request.Request(coe_url,None,coe_headers)

	# Call API
	coe_response = urllib.request.urlopen(coe_request)

	# Pull Returned Json
	dct_srch_rslts = json.loads(str(coe_response.read(),'utf-8'))

	if(dct_srch_rslts and len(dct_srch_rslts) > 0):
	
		print(" ")
		coePrintTabSpaced("UPN","Display Name")
		coePrintTabSpaced("-------------","--------------")
		
		for srchrslt in dct_srch_rslts:
			coePrintTabSpaced(srchrslt["upn"],srchrslt["display_name"])

		
		print(" ")

	else:
		print(" ")
		print("No results found for search term.")
		print(" ")

	
	return


# Function for Printing Tab Spaced Values
def coePrintTabSpaced(strv1,strv2):

	if(len(strv1) > 39):
		print(strv1 + "\t" + strv2)
	
	elif(len(strv1) > 31):
		print(strv1 + "\t\t" + strv2)

	elif(len(strv1) > 23):
		print(strv1 + "\t\t\t" + strv2)

	elif(len(strv1) > 15):
		print(strv1 + "\t\t\t\t" + strv2)

	elif(len(strv1) > 7):
		print(strv1 + "\t\t\t\t\t" + strv2)

	else:
		print(strv1 + "\t\t\t\t\t\t" + strv2)


	return

# End of coePrintTabSpaced Function

# Function for Printing Indented Tab Spaced Values
def coePrintIndentedTabSpaced(strv1,strv2):
	
	if(len(strv1) > 39):
		print("\t" + strv1 + "\t" + strv2)
	
	elif(len(strv1) > 31):
		print("\t" + strv1 + "\t\t" + strv2)
	
	elif(len(strv1) > 23):
		print("\t" + strv1 + "\t\t\t" + strv2)

	elif(len(strv1) > 15):
		print("\t" + strv1 + "\t\t\t\t" + strv2)

	elif(len(strv1) > 7):
		print("\t" + strv1 + "\t\t\t\t\t" + strv2)

	else:
		print("\t" + strv1 + "\t\t\t\t\t\t" + strv2)
	
	

	return

# Function for Options Information
def displayOptions():
	print(" ")		
	print("################################################")
	print(" ")
	print("Options: ")
	print("\t uuser")
	print("\t ucomputer")
	print("\t ugroup")
	print("\t usearch")
	print("\t ucampus")
	print(" ")
	print("Then space and the identity to look up")
	print(" ")
	print("Examples: ")
	print("\t uuser dbunn")
	print("\t uuser dbunn@ucdavis.edu")
	print("\t ucomputer coe-it-app")
	print("\t ugroup d5a41aad-4420-48a7-bdee-8eca20db42ed")
	print("\t ugroup \"COE Group Name\"")
	print("\t ucampus dbunn@ucdavis.edu")
	print("\t usearch \"Dean Bunn\"")
	print(" ")
	print("#################################################")
	print(" ")


	return

# End of displayOptions Function

# Check for Passed in Script Arguments
if(len(sys.argv) > 1):
	
	# Var for Argument 2 (The Search Term)
	arg2 = " "

	# Check for Argument 2
	if(len(sys.argv) > 2):
		arg2 = sys.argv[2]


	# Check for uUser Option
	if(sys.argv[1].lower() == "uuser"):

		if(arg2 and (not arg2.isspace())):
			displayAD3User(uuser(arg2))
			
		else:
			displayOUUsers()

	# Check for uComputer Option	
	elif(sys.argv[1].lower() == "ucomputer"):
		
		if(arg2 and (not arg2.isspace())):
			displayOUComputer(arg2)
		
		else:
			displayOUComputers()
	
	#Check for uGroup Option
	elif(sys.argv[1].lower() == "ugroup"):
		
		if(arg2 and (not arg2.isspace())):
			displayOUGroup(ugroup(arg2))

		else:
			displayOUGroups()

	# Check for uCampus Option
	elif(sys.argv[1].lower() == "ucampus"):
		
		if(arg2 and (not arg2.isspace())):
			displayuCampus(arg2)

		else:
			print("Needs something to look up")
				
	# Check for uSearch Option
	elif(sys.argv[1].lower() == "usearch"):

		if(arg2 and (not arg2.isspace())):
			displayuSearchResults(arg2)

		else:
			print("Needs something to search")
		

	else:
		displayOptions()
else:

	displayOptions()

#End of Null Check on Passed in Script Arguments

	
#########################
# End of Script
########################
