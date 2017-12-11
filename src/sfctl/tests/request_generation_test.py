# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Tests that the HTTP request generated is correct. This requires a cluster connection."""

from unittest import skipUnless
from mock import patch
from knack.testsdk import (ScenarioTest, JMESPathCheck, NoneCheck)
from sfctl.entry import cli
from jsonpickle import decode
from vcr import (VCR, use_cassette)
from sys import stderr

from sfctl.tests.helpers import (MOCK_CONFIG, ENDPOINT)

class ServiceFabricRequestTests(ScenarioTest):
    """HTTP request generation tests for Service Fabric commands.
    This test requires a live connection to a cluster. This is so we generate commands in the way that the users will.
    The purpose of this test is to generate the commands and read the HTTP request to ensure correctness.
    The expected values are hardcoded.
    The VCR library records all HTTP requests into a file. For the sake of clarity, each test to write to its own file.
    The tests should then read the file to validate correctness.
    For on the fly debugging, printing to stdout does not print to the terminal/command line. Please use other output, such as stderr."""

    def __init__(self, method_name):
        cli_env = cli()
        super(ServiceFabricRequestTests, self).__init__(cli_env, method_name)

    @skipUnless(ENDPOINT, 'Requires live cluster')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def provision_app_type_test(self):
        """Tests that a basic call to provision app type generates the correct HTTP request"""

        generated_file_path = 'HTTP_request_testing/provision_app_type.json'

        # To force new recordings, and to keep tests clean, remove old test files
        try:
            os.remove(generated_file_path)
        except FileNotFoundError:
            # if the file doesn't exist, then there's nothing for us to do
            pass

        my_vcr = VCR(serializer='json')

        # Record the HTTP request
        with my_vcr.use_cassette(generated_file_path):
            try:
                response = self.cmd('application provision --provision-kind=ImageStorePath --application-type-build-path=test_path')
            except AssertionError:
                print('Caught exception. See {0} - first item - for details.'.format(generated_file_path), file=stderr)

            try:
                response = self.cmd('application provision --provision-kind=ExternalStore \
                    --application-package-download-uri=test_path --application-type-name=name \
                    --application-type-version=version')
            except AssertionError:
                print('Caught exception. See {0} - second item - for details.'.format(generated_file_path), file=stderr)

        # Read recorded JSON file
        with open(generated_file_path, 'r') as f:
            json_str = f.read()
            vcr_recording = decode(json_str)
            print('', file=stderr)
            print('', file=stderr)
            print(vcr_recording, file=stderr)
            print('', file=stderr)
            print('', file=stderr)
            print(vcr_recording['interactions'][0]['request'], file=stderr)

