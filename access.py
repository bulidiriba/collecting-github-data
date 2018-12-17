import requests
import argparse
import sys
import shlex
import subprocess
import json

class Access():
	def __init__(self):
		self.github = "https://api.github.com/"
		self.user = ''
		self.token = ''
		self.org = 'singnet'
		self.repo = 'atomspace'
		self.event_type = 'issues'
		self.issue_state = 'all'
		self.branch = 'master'
		self.per_page = 50
		self.data_file = open('files/file.txt', "a+")

	def get_arguments(self):
		parser = argparse.ArgumentParser(description="Access Github data")
		parser.add_argument('--user', type=str, default=self.user, help="The name of the user")
		parser.add_argument('--token', type=str, default=self.token, help="The private token of the user")
		parser.add_argument('--org', type=str, default=self.org, help="The name of the Organization")
		parser.add_argument('--repo', type=str, default=self.repo, help="The name of the Repositories")
		parser.add_argument('--event_type', default=self.event_type, type=str, help="The type of the events(e.g issues, commits")
		parser.add_argument('--per_page', default=self.per_page, type=int, help="The number of per_page requests")
		parser.add_argument('--issue_state', default=self.event_type, type=str, help="The state of the issues")
		parser.add_argument('--branch', default=self.branch, type=str, help="The name of the branches")

		return parser.parse_args()


	def validate_arguments(self,args):
		"""Validate arguments entered by user"""
		if args.org == None:
			print('Please specify Organization name. Exiting.')
			sys.exit(0)
		if args.repo == None:
			print('Please specify Repositories name. Exiting.')
			sys.exit(0)
		if args.event_type == None:
			print('Please specify type of the event. Exiting.')
			sys.exit(0)


	def save_to_file(self, data):
		"""To save the data accessed from the github to a file"""
		if self.data_file.write(data):
			print("Data successfully added to file")
		else:
			Print("Problem occured during adding to file")


	def access_event(self, args):
		"""To access any event type with request"""
		issue_request = requests.get(self.github+"repos/"+args.org+"/"+args.repo+"/"+args.event_type, auth=(args.user, args.token))
		issue_dictionary = json.loads(issue_request.text)
		print(len(issue_dictionary))

		issue_url = []

		i = 0
		while i < len(issue_dictionary):
			a = issue_dictionary[i]['url']
			issue_url.append(a)
			i = i + 1

		#print(issue_url)

		for issue in issue_url:
			#r = requests.get(self.github+"repos/"+args.org+"/"+args.repo+"/"+args.event_type+"/"+str(i), auth=(args.user, args.token))
			issue_r = requests.get(issue, auth=(args.user, args.token))
			issue_rdict = json.loads(issue_r.text)
			number = issue_rdict['number']
			# create a specific json file for each issue with corresponding to its issue number 
			with open("singnet/atomspace/issues/issues-"+str(number)+".json", 'wb') as f:
				# store the content of the issue in the created json file
				f.write(issue_r.content)
				
	
		

		#print(r.headers)
		#print(r.headers['Content-Type'])

		#print(r.headers[''])

		#print(r.content)
		'''
		data = r.json()
		with open('commits.json', 'w') as f:
			json.dump(data, f)
		'''
		#print(r.content)
		#print(type(str(r.headers)))
		#self.save_to_file(str(r.headers))

	def main(self):
		args = self.get_arguments()
		valid = self.validate_arguments(args)
		
		self.access_event(args)

"""Initialize the class"""
access = Access()
access.main()
	

