import requests


class TestApi:
    """
    Test GUIG api
    """

    def test_get_branches(self, api_url: str):
        """
        Get /branches
        - Response must be success with code 200
        - Response body must be of type list
        - Body element (branch) must have: name, commit and datetime elements
        (Test repo must have at least one branch)
        """
        response = requests.get(f'{api_url}/branches')
        response_body = response.json()
        # validate success response
        assert response.status_code == 200
        # validate response object type (a list of branches)
        assert isinstance(response_body, list)
        # validate response branch structure
        filds_must_have = ['name', 'commit', 'datetime']
        assert all(field in response_body[0] for field in filds_must_have)

    def test_get_branch(self, api_url: str):
        """
        Get /branches/:branch_name:
        - Response must be success with code 200
        - Response must be of type dict
        - Response must have: name, commit and datetime elements
        - Elements name, commit and datetime must be of type str
        (Test repo must have at least one branch named master)
        """
        response = requests.get(f'{api_url}/branches/master')
        # validate success response
        assert response.status_code == 200
        # validate response objetc type dict
        branch = response.json()
        assert isinstance(branch, dict)
        # validate response objet elements
        filds_must_have = ['name', 'commit', 'datetime']
        assert all(field in branch for field in filds_must_have)
        assert all(isinstance(branch[field], str) for field in filds_must_have)

    def test_not_existing_branch(self, api_url: str):
        """
        Get /branches/:branch_name:
        test fail request
        - Response must be fail with code 404
        - Response must be dict
        - Response must have one element message of type str
        """
        response = requests.get(f'{api_url}/branches/this_branch_dont_exists')
        # validate not found response
        assert response.status_code == 404
        # validate response objetc type dict
        response_body = response.json()
        assert isinstance(response_body, dict)
        # validate error response element
        assert 'message' in response_body
        assert isinstance(response_body['message'], str)

    def test_get_commits(self, api_url: str):
        """
        Get /branches/:branch_name:/commits
        - Response must be success with code 200
        - Response must be of type list
        - Body element must have: commit, datetime, author, author_email, files
        (Test repo must have at least one branch with one commit)
        """
        response = requests.get(f'{api_url}/branches/master/commits')
        # validate success response
        assert response.status_code == 200
        # validate response type list
        response_body = response.json()
        assert isinstance(response_body, list)
        # validate response commit element
        commit = response_body[0]
        assert isinstance(commit, dict)
        filds_must_have = ['commit', 'author', 'email', 'files', 'datetime']
        assert all(field in commit for field in filds_must_have)

    def test_get_commit(self, api_url: str):
        """
        Get /branches/:branch_name:/commits/:commit:
        - Response must be success with code 200
        - Response must be dict
        - Body element must have: commit, datetime, author, author_email, files
        (The test repo has a initial commit for testing
         94181465ecc02fbc9f3d0ad25d9f6c59e166a3e1)
        """
        test_commit = '94181465ecc02fbc9f3d0ad25d9f6c59e166a3e1'
        response = requests.get(f'{api_url}/branches/master/commits/{test_commit}')
        # validate success response
        assert response.status_code == 200
        # validate response fields
        commit = response.json()
        assert isinstance(commit, dict)
        filds_must_have = ['commit', 'author', 'email', 'files', 'datetime']
        assert all(field in commit for field in filds_must_have)

    def test_not_existing_commit(self, api_url: str):
        """
        Get /branches/:branch_name:/commits/:commit_sha:
        test fail request
        - Response must be fail with code 404
        - Response must be dict
        - Response must have one element message of type str
        """
        commit_sha = 'thisisawrongshahex'
        response = requests.get(f'{api_url}/branches/master/commits/{commit_sha}')
        # validate not found response
        assert response.status_code == 404
        # validate response objetc type dict
        response_body = response.json()
        assert isinstance(response_body, dict)
        # validate error response element
        assert 'message' in response_body
        assert isinstance(response_body['message'], str)

    def test_post_pull_requests(self, api_url: str, mock_pull_request: dict):
        """
        Post /pull-requests
        - Response must be success with code 201
        - Response must be of type dict
        - Body must have: id, title, description, status, author, created_at
          source_branch, destiny_branch
        (Repository must have master and dev branches)
        """
        response = requests.post(f'{api_url}/pull-requests', mock_pull_request)
        # validate response success
        assert response.status_code == 201
        # validate response data
        pull_request = response.json()
        assert isinstance(pull_request, dict)
        filds_must_have = ['id', 'title', 'description', 'status', 'author',
                           'source_branch', 'destiny_branch', 'commit',
                           'created_at']
        assert all(field in pull_request for field in filds_must_have)

    def test_get_pull_requests(self, api_url: str, mock_pull_request: dict):
        """
        Get /pull-requests
        - Response must be success with code 200
        - Response must be of type list
        - Body must have: id, title, description, status, author, created_at
          source_branch, destiny_branch
        """
        # One pull request is created in order to have at least one result
        post_response = requests.post(f'{api_url}/pull-requests',
                                      mock_pull_request)
        # validate resource created
        assert post_response.status_code == 201
        # validate GET
        response = requests.get(f'{api_url}/pull-requests')
        assert response.status_code == 200
        # validate response data
        pull_request_collection = response.json()
        assert isinstance(pull_request_collection, list)

        pull_request = pull_request_collection[0]
        assert isinstance(pull_request, dict)
        filds_must_have = ['id', 'title', 'description', 'status', 'author',
                           'source_branch', 'destiny_branch', 'commit',
                           'created_at']
        assert all(field in pull_request for field in filds_must_have)

    def test_merge_pull_request(self, api_url: str, mock_pull_request: dict):
        """
        Post /pull-requests/:pull_request_id:/merge
        Test pull request merging
        - Response must be success with code 200
        - Response must be dict
        - Pull requests merged cannot be merged again
            * Validate merge response code for merged PR is 400
        """
        # One pull request is created for test
        post_response = requests.post(f'{api_url}/pull-requests',
                                      mock_pull_request)
        # validate resource created
        assert post_response.status_code == 201

        pull_request = post_response.json()

        merge_response = requests.post(
            f'{api_url}/pull-requests/{pull_request["id"]}/merge'
        )
        # validate merge success
        assert merge_response.status_code == 200
        merge_result = merge_response.json()
        assert isinstance(merge_result, dict)

        # validate that a merged pull request cannot be merged again
        merge_try_2_response = requests.post(
            f'{api_url}/pull-requests/{pull_request["id"]}/merge'
        )
        assert merge_try_2_response.status_code == 400

    def test_close_pull_request(self, api_url: str, mock_pull_request: dict):
        """
        Post /pull-requests/:pull_request_id:/close
        Test pull request closing
        - Response must be success with code 200
        - Response must be dict
        - Only open PR can be closed
            * Validate close response code for closed PR is 400
        """
        # One pull request is created for test
        post_response = requests.post(f'{api_url}/pull-requests',
                                      mock_pull_request)
        # validate resource created
        assert post_response.status_code == 201

        pull_request = post_response.json()

        close_response = requests.post(
            f'{api_url}/pull-requests/{pull_request["id"]}/close'
        )
        # validate close success
        assert close_response.status_code == 200

        # close the same pull request again must fail
        close_try_2_response = requests.post(
            f'{api_url}/pull-requests/{pull_request["id"]}/close'
        )
        assert close_try_2_response.status_code == 400
