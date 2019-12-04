import pytest
import koji_tag


class FakeSession(object):
    def __init__(self):
        self.repos = []

    def getTagExternalRepos(self, tag_info=None, repo_info=None):
        return self.repos

    def addExternalRepoToTag(self, tag_info, repo_info, priority,
                             merge_mode='koji'):
        pass

    def removeExternalRepoFromTag(self, tag_info, repo_info):
        pass

    def ensure_logged_in(self, session):
        return session

    def logged_in(self, session):
        return True


class TestValidateRepos(object):

    def test_simple(self):
        repos = [{'repo': 'epel-7', 'priority': 10}]
        koji_tag.validate_repos(repos)

    def test_empty(self):
        repos = []
        koji_tag.validate_repos(repos)

    def test_duplicate_name(self):
        repos = [
            {'repo': 'epel-7', 'priority': 10},
            {'repo': 'epel-7', 'priority': 20},
        ]
        with pytest.raises(koji_tag.DuplicateNameError):
            koji_tag.validate_repos(repos)

    def test_duplicate_priority(self):
        repos = [
            {'repo': 'centos', 'priority': 10},
            {'repo': 'epel-7', 'priority': 10},
        ]
        with pytest.raises(koji_tag.DuplicatePriorityError):
            koji_tag.validate_repos(repos)


class TestAddExternalRepos(object):

    def test_simple(self):
        session = FakeSession()
        tag_name = 'my-centos-7'
        repos_to_add = [{'repo_info': 'centos-7-cr', 'priority': 10}]
        koji_tag.add_external_repos(session, tag_name, repos_to_add)


class TestRemoveExternalRepos(object):

    def test_simple(self):
        session = FakeSession()
        tag_name = 'my-centos-7'
        repos_to_remove = ['centos-7-cr', 'epel-7']
        koji_tag.remove_external_repos(session, tag_name, repos_to_remove)


class TestEnsureExternalRepos(object):

    def test_from_no_repos(self):
        session = FakeSession()
        tag_name = 'my-centos-7'
        check_mode = False
        repos = [{'repo': 'centos-7-cr',
                  'priority': 10},
                 {'repo': 'epel-7-cr',
                  'priority': 20},
                 ]
        koji_tag.ensure_external_repos(session, tag_name, check_mode, repos)

    def test_add_one_repo(self):
        session = FakeSession()
        session.repos = [{'external_repo_name': 'centos-7-cr',
                          'priority': 10}]
        tag_name = 'my-centos-7'
        check_mode = False
        repos = [{'repo': 'centos-7-cr',
                  'priority': 10},
                 {'repo': 'epel-7-cr',
                  'priority': 20},
                 ]
        koji_tag.ensure_external_repos(session, tag_name, check_mode, repos)
