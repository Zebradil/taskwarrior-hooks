import json
from subprocess import run, PIPE
from unittest import TestCase


class TestRemoveNextAndWaitOnDoneOrStart(TestCase):
    modify_hook = 'src/on-modify.remove_next_and_wait_on_done_or_start.rb'

    @staticmethod
    def _getReferenceRecord():
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
    def _getRecordsWithDeletableFields():
        return [{
            "description": "Buy hard drive for Mac backuping",
            "entry": "20171114T115807Z",
            "modified": "20171115T132022Z",
            "project": "Buy",
            "status": "pending",
            "wait": "20171215T132022Z",
            "tags": ["buy", "next"],
            "uuid": "7d3951dc-d17d-4495-a094-0694a4de93c1"
        }, {
            "description": "Buy hard drive for Mac backuping",
            "entry": "20171114T115807Z",
            "modified": "20171115T132022Z",
            "project": "Buy",
            "status": "pending",
            "wait": "20171215T132022Z",
            "tags": ["buy"],
            "uuid": "7d3951dc-d17d-4495-a094-0694a4de93c1"
        }, {
            "description": "Buy hard drive for Mac backuping",
            "entry": "20171114T115807Z",
            "modified": "20171115T132022Z",
            "project": "Buy",
            "status": "pending",
            "tags": ["buy", "next"],
            "uuid": "7d3951dc-d17d-4495-a094-0694a4de93c1"
        }]

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

    def test_removing_on_start_and_done_commands(self):
        records = self._getRecordsWithDeletableFields()
        reference = self._getReferenceRecord()
        for cmd in ['start', 'done']:
            for record in records:
                jsoned_record = json.dumps(record)
                input_string = jsoned_record + "\n" + jsoned_record
                result_string = self.run_hook(
                    self.modify_hook,
                    input_string,
                    ['command:' + cmd]
                )
                result = json.loads(result_string)
                print(result)
                assert 'wait' not in result
                assert 'next' not in result['tags']
                for key in reference:
                    assert reference[key] == result[key]

    def test_preserving_on_other_commands(self):
        records = self._getRecordsWithDeletableFields()
        for cmd in ['modify', 'stop', 'delete']:
            for record in records:
                jsoned_record = json.dumps(record)
                input_string = jsoned_record + "\n" + jsoned_record
                result_string = self.run_hook(
                    self.modify_hook,
                    input_string,
                    ['command:' + cmd]
                )
                result = json.loads(result_string)
                print(result)
                for key in record:
                    assert record[key] == result[key]
