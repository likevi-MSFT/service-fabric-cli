# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from .application_event import ApplicationEvent


class ApplicationUpgradeDomainCompleteEvent(ApplicationEvent):
    """Application Upgrade Domain Complete event.

    :param event_instance_id: The identifier for the FabricEvent instance.
    :type event_instance_id: str
    :param time_stamp: The time event was logged.
    :type time_stamp: datetime
    :param has_correlated_events: Shows there is existing related events
     available.
    :type has_correlated_events: bool
    :param kind: Constant filled by server.
    :type kind: str
    :param application_id: The identity of the application. This is an encoded
     representation of the application name. This is used in the REST APIs to
     identify the application resource.
     Starting in version 6.0, hierarchical names are delimited with the "\\~"
     character. For example, if the application name is "fabric:/myapp/app1",
     the application identity would be "myapp\\~app1" in 6.0+ and "myapp/app1"
     in previous versions.
    :type application_id: str
    :param application_type_name: Application type name.
    :type application_type_name: str
    :param current_application_type_version: Current Application type version.
    :type current_application_type_version: str
    :param application_type_version: Target Application type version.
    :type application_type_version: str
    :param upgrade_state: State of upgrade.
    :type upgrade_state: str
    :param upgrade_domains: Upgrade domains.
    :type upgrade_domains: str
    :param upgrade_domain_elapsed_time_in_ms: Upgrade time of domain in
     milli-seconds.
    :type upgrade_domain_elapsed_time_in_ms: float
    """

    _validation = {
        'event_instance_id': {'required': True},
        'time_stamp': {'required': True},
        'kind': {'required': True},
        'application_id': {'required': True},
        'application_type_name': {'required': True},
        'current_application_type_version': {'required': True},
        'application_type_version': {'required': True},
        'upgrade_state': {'required': True},
        'upgrade_domains': {'required': True},
        'upgrade_domain_elapsed_time_in_ms': {'required': True},
    }

    _attribute_map = {
        'event_instance_id': {'key': 'EventInstanceId', 'type': 'str'},
        'time_stamp': {'key': 'TimeStamp', 'type': 'iso-8601'},
        'has_correlated_events': {'key': 'HasCorrelatedEvents', 'type': 'bool'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'application_id': {'key': 'ApplicationId', 'type': 'str'},
        'application_type_name': {'key': 'ApplicationTypeName', 'type': 'str'},
        'current_application_type_version': {'key': 'CurrentApplicationTypeVersion', 'type': 'str'},
        'application_type_version': {'key': 'ApplicationTypeVersion', 'type': 'str'},
        'upgrade_state': {'key': 'UpgradeState', 'type': 'str'},
        'upgrade_domains': {'key': 'UpgradeDomains', 'type': 'str'},
        'upgrade_domain_elapsed_time_in_ms': {'key': 'UpgradeDomainElapsedTimeInMs', 'type': 'float'},
    }

    def __init__(self, event_instance_id, time_stamp, application_id, application_type_name, current_application_type_version, application_type_version, upgrade_state, upgrade_domains, upgrade_domain_elapsed_time_in_ms, has_correlated_events=None):
        super(ApplicationUpgradeDomainCompleteEvent, self).__init__(event_instance_id=event_instance_id, time_stamp=time_stamp, has_correlated_events=has_correlated_events, application_id=application_id)
        self.application_type_name = application_type_name
        self.current_application_type_version = current_application_type_version
        self.application_type_version = application_type_version
        self.upgrade_state = upgrade_state
        self.upgrade_domains = upgrade_domains
        self.upgrade_domain_elapsed_time_in_ms = upgrade_domain_elapsed_time_in_ms
        self.kind = 'ApplicationUpgradeDomainComplete'
