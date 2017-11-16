import json
from subprocess import run, PIPE
from unittest import TestCase


class TestBuyWait(TestCase):
    add_hook = 'src/on-add.buy_wait.rb'
    modify_hook = 'src/on-modify.buy_wait.rb'

    @staticmethod
    def _getInitialRecord():
        return {
            "description": "Buy hard drive for Mac backuping",
            "entry": "20171114T115807Z",
            "modified": "20171115T132022Z",
            "project": "Buy",
            "status": "pending",
            "tags": ["buy"],
            "uuid": "7d3951dc-d17d-4495-a094-0694a4de93c1"
        }

    @staticmethod
    def _getModifiedRecord():
        return {
            "description": "Buy hard drive for Mac backuping",
            "entry": "20171114T115807Z",
            "modified": "20171115T132022Z",
            "project": "Buy",
            "status": "pending",
            "tags": ["buy", "pc"],
            "uuid": "7d3951dc-d17d-4495-a094-0694a4de93c1"
        }

    @staticmethod
    def _getRecordWithAnotherProject():
        return {
            "description": "Buy hard drive for Mac backuping",
            "entry": "20171114T115807Z",
            "modified": "20171115T132022Z",
            "project": "Another",
            "status": "pending",
            "tags": ["buy", "pc"],
            "uuid": "7d3951dc-d17d-4495-a094-0694a4de93c1"
        }

    @staticmethod
    def _getRecordWithEmptyProject():
        return {
            "description": "Buy hard drive for Mac backuping",
            "entry": "20171114T115807Z",
            "modified": "20171115T132022Z",
            "project": "",
            "status": "pending",
            "tags": ["buy", "pc"],
            "uuid": "7d3951dc-d17d-4495-a094-0694a4de93c1"
        }

    @staticmethod
    def _getRecordWithDetailedProject():
        return {
            "description": "Buy hard drive for Mac backuping",
            "entry": "20171114T115807Z",
            "modified": "20171115T132022Z",
            "project": "Buy.Stuff",
            "status": "pending",
            "tags": ["buy", "pc"],
            "uuid": "7d3951dc-d17d-4495-a094-0694a4de93c1"
        }

    @staticmethod
    def run_hook(hook_path, input_string='', arguments=[]):
        cmd = [hook_path]
        cmd.extend(arguments)
        return run(
            cmd,
            stdout=PIPE,
            input=input_string,
            encoding='utf-8'
        ).stdout.split("\n")[0]

    def test_new_record(self):
        initial = self._getInitialRecord()
        result = json.loads(self.run_hook(self.add_hook, json.dumps(initial)))
        assert result['wait'] == 'someday'
        for key in initial:
            assert initial[key] == result[key]

    def test_another_project(self):
        initial = self._getRecordWithAnotherProject()
        result = json.loads(self.run_hook(self.add_hook, json.dumps(initial)))
        assert initial == result

    def test_empty_project(self):
        initial = self._getRecordWithEmptyProject()
        result = json.loads(self.run_hook(self.add_hook, json.dumps(initial)))
        assert initial == result

    def test_detailed_project(self):
        initial = self._getRecordWithDetailedProject()
        result = json.loads(self.run_hook(self.add_hook, json.dumps(initial)))
        assert result['wait'] == 'someday'
        for key in initial:
            assert initial[key] == result[key]

    def test_modified_record(self):
        initial = self._getInitialRecord()
        modified = self._getModifiedRecord()
        input_string = json.dumps(initial) + "\n" + json.dumps(modified)
        result_string = self.run_hook(self.modify_hook, input_string)
        result = json.loads(result_string)
        assert result['wait'] == 'someday'
        for key in modified:
            assert modified[key] == result[key]
