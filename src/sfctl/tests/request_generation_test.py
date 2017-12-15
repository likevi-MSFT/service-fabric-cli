# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Tests that the HTTP request generated is correct.
This requires a cluster connection."""

from unittest import skipUnless
from sys import stderr
from os import remove
from mock import patch
from knack.testsdk import ScenarioTest
from sfctl.entry import cli
from sfctl.tests.helpers import (MOCK_CONFIG, ENDPOINT)
from jsonpickle import decode
from vcr import VCR

class ServiceFabricRequestTests(ScenarioTest):
    """HTTP request generation tests for Service Fabric commands.
    This test requires a live connection to a cluster.
    This is so we generate commands in the way that the users will.
    The purpose of this test is to generate the commands and
    read the HTTP request to ensure correctness.
    The expected values are hard-coded.
    The VCR library records all HTTP requests into
    a file. For the sake of clarity,
    each test to write to its own file.
    The tests should then read the file to validate correctness.
    For on the fly debugging,
    printing to stdout does not print to the terminal/command line.
    Please use other output, such as stderr."""

    def __init__(self, method_name):
        cli_env = cli()
        super(ServiceFabricRequestTests, self).__init__(cli_env, method_name)

    @skipUnless(ENDPOINT, 'Requires live cluster')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def provision_app_type_test(self): # pylint: disable=too-many-locals
        """Tests that a basic call to provision app type generates
        the correct HTTP request"""

        generated_file_path = 'HTTP_request_testing/provision_app_type.json'

        # To force new recordings, and to keep tests clean,
        # remove old test files
        try:
            remove(generated_file_path)
        except FileNotFoundError:
            # if the file doesn't exist, then there's nothing for us to do
            pass

        my_vcr = VCR(serializer='json', record_mode='all',
                     match_on=['uri', 'method'])

        # Record the HTTP request;
        # this writes the recodings to generated_file_path
        # Run async-operation as false tests for simplicity
        with my_vcr.use_cassette(generated_file_path):
            try:
                self.cmd('application provision --image-store-provision \
                --application-type-build-path=test_path')
            except AssertionError:
                print('This does not indicate error. Caught exception. \
                    See {0} - first item - \
                    for details.'.format(generated_file_path),
                      file=stderr)

            try:
                self.cmd('application provision --external-store-provision \
                    --application-package-download-uri=test_path --application-type-name=name \
                    --application-type-version=version')
            except AssertionError:
                print('This does not indicate an error. Caught exception. \
                    See {0} - second item - \
                    for details.'.format(generated_file_path),
                      file=stderr)

        # Read recorded JSON file
        with open(generated_file_path, 'r') as http_recording_file:
            json_str = http_recording_file.read()
            vcr_recording = decode(json_str)

            # The responses create an array of request and other objects
            # the numbers (for indexing) represent which request was made first
            # the ordering is determined by the ordering of calls to self.cmd
            # see outputted JSON file at generated_file_path for more details
            image_store_recording = vcr_recording['interactions'][0]['request']
            external_store_recording = \
                vcr_recording['interactions'][1]['request']

            # Get HTTP Body
            image_store_recording_body = decode(image_store_recording['body'])

            # Content inside HTTP body
            kind = image_store_recording_body['Kind']
            self.assertEqual(kind, 'ImageStorePath')

            async_operation = image_store_recording_body['Async']
            self.assertEqual(async_operation, False)

            application_type_build_path = \
                image_store_recording_body['ApplicationTypeBuildPath']
            self.assertEqual(application_type_build_path, 'test_path')

            # Get HTTP Body
            external_store_recording_body = \
                decode(external_store_recording['body'])

            # Content inside HTTP body
            kind = external_store_recording_body['Kind']
            self.assertEqual(kind, 'ExternalStore')

            async_operation = external_store_recording_body['Async']
            self.assertEqual(async_operation, False)

            download_uri = \
                external_store_recording_body['ApplicationPackageDownloadUri']
            self.assertEqual(download_uri, 'test_path')

            application_type_name = \
                external_store_recording_body['ApplicationTypeName']
            self.assertEqual(application_type_name, 'name')

            application_type_version = \
                external_store_recording_body['ApplicationTypeVersion']
            self.assertEqual(application_type_version, 'version')

            # Get HTTP Method type (Get vs Post)
            image_store_recording_method = image_store_recording['method']
            self.assertEqual(image_store_recording_method, 'POST')

            external_store_recording_method = \
                external_store_recording['method']
            self.assertEqual(external_store_recording_method, 'POST')

            # Get HTTP URI
            image_store_recording_uri = image_store_recording['uri']
            # assert '/ApplicationTypes/$/Provision?api-version=6.1&timeout=60'
            # in image_store_recording_uri
            self.assertIn(
                '/ApplicationTypes/$/Provision?api-version=6.1&timeout=60',
                image_store_recording_uri)

            external_store_recording_uri = external_store_recording['uri']
            self.assertIn(
                '/ApplicationTypes/$/Provision?api-version=6.1&timeout=60',
                external_store_recording_uri)

        # If this test reaches here, then this test is successful.
