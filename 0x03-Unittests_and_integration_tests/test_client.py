#!/usr/bin/env python3
"""
Module for testing GithubOrgClient class
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for GithubOrgClient
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        """
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the correct value
        """
        mock_org.return_value = {"repos_url": "http://some_url.com/repos"}
        client = GithubOrgClient("test_org")
        self.assertEqual(client._public_repos_url, "http://some_url.com/repos")

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test that public_repos returns the correct value
        """
        mock_public_repos_url.return_value = "http://some_url.com/repos"
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        mock_get_json.assert_called_once_with("http://some_url.com/repos")
        mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns the correct value
        """
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), [
    (org_payload, repos_payload, expected_repos, apache2_repos)
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class by patching requests.get
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            Mock(**{"json.return_value": cls.org_payload}),
            Mock(**{"json.return_value": cls.repos_payload})
        ]

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the class by stopping the patcher
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test the public_repos method
        """
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test the public_repos method with license filter
        """
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
