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

from .partition_event import PartitionEvent


class PartitionAnalysisEvent(PartitionEvent):
    """Represents the base for all Partition Analysis Events.

    You probably want to use the sub-classes and not this class directly. Known
    sub-classes are: PartitionPrimaryMoveAnalysisEvent

    :param event_instance_id: The identifier for the FabricEvent instance.
    :type event_instance_id: str
    :param time_stamp: The time event was logged.
    :type time_stamp: datetime
    :param has_correlated_events: Shows there is existing related events
     available.
    :type has_correlated_events: bool
    :param kind: Constant filled by server.
    :type kind: str
    :param partition_id: An internal ID used by Service Fabric to uniquely
     identify a partition. This is a randomly generated GUID when the service
     was created. The partition ID is unique and does not change for the
     lifetime of the service. If the same service was deleted and recreated the
     IDs of its partitions would be different.
    :type partition_id: str
    :param metadata: Metadata about an Analysis Event.
    :type metadata: ~azure.servicefabric.models.AnalysisEventMetadata
    """

    _validation = {
        'event_instance_id': {'required': True},
        'time_stamp': {'required': True},
        'kind': {'required': True},
        'partition_id': {'required': True},
        'metadata': {'required': True},
    }

    _attribute_map = {
        'event_instance_id': {'key': 'EventInstanceId', 'type': 'str'},
        'time_stamp': {'key': 'TimeStamp', 'type': 'iso-8601'},
        'has_correlated_events': {'key': 'HasCorrelatedEvents', 'type': 'bool'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'partition_id': {'key': 'PartitionId', 'type': 'str'},
        'metadata': {'key': 'Metadata', 'type': 'AnalysisEventMetadata'},
    }

    _subtype_map = {
        'kind': {'PartitionPrimaryMoveAnalysis': 'PartitionPrimaryMoveAnalysisEvent'}
    }

    def __init__(self, event_instance_id, time_stamp, partition_id, metadata, has_correlated_events=None):
        super(PartitionAnalysisEvent, self).__init__(event_instance_id=event_instance_id, time_stamp=time_stamp, has_correlated_events=has_correlated_events, partition_id=partition_id)
        self.metadata = metadata
        self.kind = 'PartitionAnalysisEvent'
