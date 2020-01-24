#!/usr/bin/python3
# Simple script to get your private/public or both programs ussing HackerOne graphQL.
# you may grab your Hackerone graphQL token from : https://hackerone.com/current_user/graphql_token.json
# @m3dsec @b10ta

import json
import requests
import sys
import time

# GET YOUR TOKEN FROM HERE >> https://hackerone.com/current_user/graphql_token.json
token = "KDFJDKFJDKFJKDJFKDJFKDJFKFJD.DFLKDFLDKFLKDLFKDLFK.erYw-DLFKDFLKDLFKDLFKLDKFLDKLFKDLFK----23232323"

sw = "Something Went Wrong..\ncheck ur token, it may be dead or something.."
usage = """[~] Usage : python3 h1getPrograms.py private      to print only private programs
            python3 getPrograms.py public       to print only public programs
            python3 getPrograms.py all          to print all your programs
"""

if len(sys.argv) != 2:
    print(usage)
    exit()

method = sys.argv[1]

if method.lower() == "private":
	print("Getting private Programs and they'r Scoops...\n")
	queryPrivatePrograms = "{\"operationName\":\"MyProgramsQuery\",\"variables\":{\"where\":{\"_and\":[{\"_or\":[{\"submission_state\":{\"_eq\":\"open\"}},{\"submission_state\":{\"_eq\":\"api_only\"}},{\"submission_state\":{\"_is_null\":true}}]},{\"_and\":[{\"_or\":[{\"bookmarked_team_users\":{\"is_me\":true}},{\"whitelisted_hackers\":{\"is_me\":true}}]},{\"state\":{\"_eq\":\"soft_launched\"}}]}]},\"count\":25,\"orderBy\":null,\"secureOrderBy\":{\"started_accepting_at\":{\"_direction\":\"DESC\"}}},\"query\":\"query MyProgramsQuery($cursor: String, $count: Int, $where: FiltersTeamFilterInput, $orderBy: TeamOrderInput, $secureOrderBy: FiltersTeamFilterOrder) {\\n  me {\\n    id\\n    ...MyHackerOneSubHeader\\n    __typename\\n  }\\n  teams(first: $count, after: $cursor, order_by: $orderBy, secure_order_by: $secureOrderBy, where: $where) {\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n      __typename\\n    }\\n    edges {\\n      cursor\\n      node {\\n        id\\n        handle\\n        name\\n        currency\\n        team_profile_picture: profile_picture(size: medium)\\n        submission_state\\n        triage_active\\n        state\\n        started_accepting_at\\n        number_of_reports_for_user\\n        number_of_valid_reports_for_user\\n        bounty_earned_for_user\\n        last_invitation_accepted_at_for_user\\n        bookmarked\\n        external_program {\\n          id\\n          __typename\\n        }\\n        ...TeamLinkWithMiniProfile\\n        ...TeamTableAverageBounty\\n        ...TeamTableMinimumBounty\\n        ...TeamTableResolvedReports\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment TeamLinkWithMiniProfile on Team {\\n  id\\n  handle\\n  name\\n  __typename\\n}\\n\\nfragment TeamTableAverageBounty on Team {\\n  id\\n  currency\\n  average_bounty_lower_amount\\n  average_bounty_upper_amount\\n  __typename\\n}\\n\\nfragment TeamTableMinimumBounty on Team {\\n  id\\n  currency\\n  base_bounty\\n  __typename\\n}\\n\\nfragment TeamTableResolvedReports on Team {\\n  id\\n  resolved_report_count\\n  __typename\\n}\\n\\nfragment MyHackerOneSubHeader on User {\\n  id\\n  has_checklist_check_responses\\n  soft_launch_invitations(state: open) {\\n    total_count\\n    __typename\\n  }\\n  __typename\\n}\\n\"}"
	r = requests.post('https://hackerone.com/graphql', data=queryPrivatePrograms, headers={'content-type': 'application/json', 'X-Auth-Token': '%s' % token})
	if r.status_code == 200:	
		scope_resp = json.loads(r.text)
		# L3Z LHAD KHOUNA HNA https://stackoverflow.com/questions/12788217/how-to-extract-a-single-value-from-json-response
		# GET TARGETS NAMES AND THE PROGRAMS URLs
		target = ""
		for e in scope_resp['data']['teams']['edges']:
			target = str(e['node']['handle'])
			programURL = "http://hackerone.com/%s" % target
			print("[!] %s  ==>  %s " % (target.upper(),programURL))
			# GET SCOP URLs FROM API
			queryDomains = "{\"query\":\"query Team_assets($first_0:Int!) {query {id,...F0}} fragment F0 on Query {me {_membership3rWriM:membership(team_handle:\\\"%s\\\") {permissions,id},id},_team2qdS8K:team(handle:\\\"%s\\\") {handle,_structured_scope_versions2ZWKHQ:structured_scope_versions(archived:false) {max_updated_at},_structured_scopes2qeKP8:structured_scopes(first:$first_0,archived:false,eligible_for_submission:true) {edges {node {id,asset_type,asset_identifier,rendered_instruction,max_severity,eligible_for_bounty},cursor},pageInfo {hasNextPage,hasPreviousPage}},_structured_scopes1wWN6h:structured_scopes(first:$first_0,archived:false,eligible_for_submission:false) {edges {node {id,asset_type,asset_identifier,rendered_instruction},cursor},pageInfo {hasNextPage,hasPreviousPage}},id},id}\",\"variables\":{\"first_0\":500}}" % (target, target)
			r2 = requests.post('https://hackerone.com/graphql', data=queryDomains, headers={'content-type': 'application/json', 'X-Auth-Token': '%s' % token})
			scopeDomainsJsonResp = json.loads(r2.text)
			for u in scopeDomainsJsonResp['data']['query']['_team2qdS8K']['_structured_scopes2qeKP8']['edges']:
				fuckingTURL = u['node']['asset_identifier']
				if u['node']['eligible_for_bounty']:
					print('[*.*] ' + str(fuckingTURL))
				else:
					print('[-_-] ' + str(fuckingTURL))
			print()
	else:
		print(sw)
		exit()

elif method.lower() == "public":
	print("Getting Public Programs and they'r Scoops...")
	queryPublicPrograms = "{\"operationName\":\"MyProgramsQuery\",\"variables\":{\"where\":{\"_and\":[{\"_or\":[{\"submission_state\":{\"_eq\":\"open\"}},{\"submission_state\":{\"_eq\":\"api_only\"}},{\"submission_state\":{\"_is_null\":true}}]},{\"_and\":[{\"_or\":[{\"bookmarked_team_users\":{\"is_me\":true}},{\"reporters\":{\"is_me\":true}}]},{\"_or\":[{\"state\":{\"_eq\":\"public_mode\"}},{\"external_program\":{\"id\":{\"_is_null\":false}}}]}]}]},\"count\":25,\"orderBy\":null,\"secureOrderBy\":{\"started_accepting_at\":{\"_direction\":\"DESC\"}}},\"query\":\"query MyProgramsQuery($cursor: String, $count: Int, $where: FiltersTeamFilterInput, $orderBy: TeamOrderInput, $secureOrderBy: FiltersTeamFilterOrder) {\\n  me {\\n    id\\n    ...MyHackerOneSubHeader\\n    __typename\\n  }\\n  teams(first: $count, after: $cursor, order_by: $orderBy, secure_order_by: $secureOrderBy, where: $where) {\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n      __typename\\n    }\\n    edges {\\n      cursor\\n      node {\\n        id\\n        handle\\n        name\\n        currency\\n        team_profile_picture: profile_picture(size: medium)\\n        submission_state\\n        triage_active\\n        state\\n        started_accepting_at\\n        number_of_reports_for_user\\n        number_of_valid_reports_for_user\\n        bounty_earned_for_user\\n        last_invitation_accepted_at_for_user\\n        bookmarked\\n        external_program {\\n          id\\n          __typename\\n        }\\n        ...TeamLinkWithMiniProfile\\n        ...TeamTableAverageBounty\\n        ...TeamTableMinimumBounty\\n        ...TeamTableResolvedReports\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment TeamLinkWithMiniProfile on Team {\\n  id\\n  handle\\n  name\\n  __typename\\n}\\n\\nfragment TeamTableAverageBounty on Team {\\n  id\\n  currency\\n  average_bounty_lower_amount\\n  average_bounty_upper_amount\\n  __typename\\n}\\n\\nfragment TeamTableMinimumBounty on Team {\\n  id\\n  currency\\n  base_bounty\\n  __typename\\n}\\n\\nfragment TeamTableResolvedReports on Team {\\n  id\\n  resolved_report_count\\n  __typename\\n}\\n\\nfragment MyHackerOneSubHeader on User {\\n  id\\n  has_checklist_check_responses\\n  soft_launch_invitations(state: open) {\\n    total_count\\n    __typename\\n  }\\n  __typename\\n}\\n\"}"
	r = requests.post('https://hackerone.com/graphql', data=queryPublicPrograms, headers={'content-type': 'application/json', 'X-Auth-Token': '%s' % token})
	if r.status_code == 200:	
		scope_resp = json.loads(r.text)
		target = ""
		for e in scope_resp['data']['teams']['edges']:
			target = str(e['node']['handle'])
			programURL = "http://hackerone.com/%s" % target
			print("[!] %s  ==>  %s " % (target.upper(),programURL))
			queryDomains = "{\"query\":\"query Team_assets($first_0:Int!) {query {id,...F0}} fragment F0 on Query {me {_membership3rWriM:membership(team_handle:\\\"%s\\\") {permissions,id},id},_team2qdS8K:team(handle:\\\"%s\\\") {handle,_structured_scope_versions2ZWKHQ:structured_scope_versions(archived:false) {max_updated_at},_structured_scopes2qeKP8:structured_scopes(first:$first_0,archived:false,eligible_for_submission:true) {edges {node {id,asset_type,asset_identifier,rendered_instruction,max_severity,eligible_for_bounty},cursor},pageInfo {hasNextPage,hasPreviousPage}},_structured_scopes1wWN6h:structured_scopes(first:$first_0,archived:false,eligible_for_submission:false) {edges {node {id,asset_type,asset_identifier,rendered_instruction},cursor},pageInfo {hasNextPage,hasPreviousPage}},id},id}\",\"variables\":{\"first_0\":500}}" % (target, target)
			r2 = requests.post('https://hackerone.com/graphql', data=queryDomains, headers={'content-type': 'application/json', 'X-Auth-Token': '%s' % token})
			scopeDomainsJsonResp = json.loads(r2.text)
			for u in scopeDomainsJsonResp['data']['query']['_team2qdS8K']['_structured_scopes2qeKP8']['edges']:
				fuckingTURL = u['node']['asset_identifier']
				if u['node']['eligible_for_bounty']:
					print('[*.*] ' + str(fuckingTURL))
				else:
					print('[-_-] ' + str(fuckingTURL))
			print("\n")
	else:
		print(sw)
		exit()

elif method.lower() == "all":
	queryBothPrograms = "{\"operationName\":\"MyProgramsQuery\",\"variables\":{\"where\":{\"_and\":[{\"_or\":[{\"submission_state\":{\"_eq\":\"open\"}},{\"submission_state\":{\"_eq\":\"api_only\"}},{\"submission_state\":{\"_is_null\":true}}]},{\"_or\":[{\"_and\":[{\"_or\":[{\"bookmarked_team_users\":{\"is_me\":true}},{\"whitelisted_hackers\":{\"is_me\":true}}]},{\"state\":{\"_eq\":\"soft_launched\"}}]},{\"_and\":[{\"_or\":[{\"bookmarked_team_users\":{\"is_me\":true}},{\"reporters\":{\"is_me\":true}}]},{\"_or\":[{\"state\":{\"_eq\":\"public_mode\"}},{\"external_program\":{\"id\":{\"_is_null\":false}}}]}]}]}]},\"count\":25,\"orderBy\":null,\"secureOrderBy\":{\"started_accepting_at\":{\"_direction\":\"DESC\"}}},\"query\":\"query MyProgramsQuery($cursor: String, $count: Int, $where: FiltersTeamFilterInput, $orderBy: TeamOrderInput, $secureOrderBy: FiltersTeamFilterOrder) {\\n  me {\\n    id\\n    ...MyHackerOneSubHeader\\n    __typename\\n  }\\n  teams(first: $count, after: $cursor, order_by: $orderBy, secure_order_by: $secureOrderBy, where: $where) {\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n      __typename\\n    }\\n    edges {\\n      cursor\\n      node {\\n        id\\n        handle\\n        name\\n        currency\\n        team_profile_picture: profile_picture(size: medium)\\n        submission_state\\n        triage_active\\n        state\\n        started_accepting_at\\n        number_of_reports_for_user\\n        number_of_valid_reports_for_user\\n        bounty_earned_for_user\\n        last_invitation_accepted_at_for_user\\n        bookmarked\\n        external_program {\\n          id\\n          __typename\\n        }\\n        ...TeamLinkWithMiniProfile\\n        ...TeamTableAverageBounty\\n        ...TeamTableMinimumBounty\\n        ...TeamTableResolvedReports\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment TeamLinkWithMiniProfile on Team {\\n  id\\n  handle\\n  name\\n  __typename\\n}\\n\\nfragment TeamTableAverageBounty on Team {\\n  id\\n  currency\\n  average_bounty_lower_amount\\n  average_bounty_upper_amount\\n  __typename\\n}\\n\\nfragment TeamTableMinimumBounty on Team {\\n  id\\n  currency\\n  base_bounty\\n  __typename\\n}\\n\\nfragment TeamTableResolvedReports on Team {\\n  id\\n  resolved_report_count\\n  __typename\\n}\\n\\nfragment MyHackerOneSubHeader on User {\\n  id\\n  has_checklist_check_responses\\n  soft_launch_invitations(state: open) {\\n    total_count\\n    __typename\\n  }\\n  __typename\\n}\\n\"}"
	r = requests.post('https://hackerone.com/graphql', data=queryBothPrograms, headers={'content-type': 'application/json', 'X-Auth-Token': '%s' % token})
	if r.status_code == 200:	
		scope_resp = json.loads(r.text)
		target = ""
		for e in scope_resp['data']['teams']['edges']:
			target = str(e['node']['handle'])
			programURL = "http://hackerone.com/%s" % target
			print("[!] %s  ==>  %s " % (target.upper(),programURL))
			queryDomains = "{\"query\":\"query Team_assets($first_0:Int!) {query {id,...F0}} fragment F0 on Query {me {_membership3rWriM:membership(team_handle:\\\"%s\\\") {permissions,id},id},_team2qdS8K:team(handle:\\\"%s\\\") {handle,_structured_scope_versions2ZWKHQ:structured_scope_versions(archived:false) {max_updated_at},_structured_scopes2qeKP8:structured_scopes(first:$first_0,archived:false,eligible_for_submission:true) {edges {node {id,asset_type,asset_identifier,rendered_instruction,max_severity,eligible_for_bounty},cursor},pageInfo {hasNextPage,hasPreviousPage}},_structured_scopes1wWN6h:structured_scopes(first:$first_0,archived:false,eligible_for_submission:false) {edges {node {id,asset_type,asset_identifier,rendered_instruction},cursor},pageInfo {hasNextPage,hasPreviousPage}},id},id}\",\"variables\":{\"first_0\":500}}" % (target, target)
			r2 = requests.post('https://hackerone.com/graphql', data=queryDomains, headers={'content-type': 'application/json', 'X-Auth-Token': '%s' % token})
			scopeDomainsJsonResp = json.loads(r2.text)
			for u in scopeDomainsJsonResp['data']['query']['_team2qdS8K']['_structured_scopes2qeKP8']['edges']:
				fuckingTURL = u['node']['asset_identifier']
				if u['node']['eligible_for_bounty']:
					print('[*.*] ' + str(fuckingTURL))
				else:
					print('[-_-] ' + str(fuckingTURL))
			print("\n")
	else:
		print(sw)
		exit()
else:
	print(usage)
	exit()
