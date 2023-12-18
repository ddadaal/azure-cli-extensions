# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pylint: disable=too-many-statements

from uuid import uuid4
from dataclasses import dataclass
from knack.log import get_logger

from azure.cli.core.commands import AzCliCommand
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.models import RoleAssignmentCreateParameters, PrincipalType
from azure.mgmt.kubernetesconfiguration import SourceControlConfigurationClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.kubernetesconfiguration.models import Extension, Identity
from azure.cli.core.commands.client_factory import get_mgmt_service_client


logger = get_logger(__name__)

# pylint: disable=line-too-long

# https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#kubernetes-extension-contributor
KUBERNETES_EXTENSION_CONTRIBUTOR_ROLE_ID = "/providers/Microsoft.Authorization/roleDefinitions/85cb6faf-e071-4c9b-8136-154b5a04f717"
STORAGE_CLASS_CONTRIBUTOR_ROLE_ID = "/providers/Microsoft.Authorization/roleDefinitions/0cd9749a-3aaf-4ae5-8803-bd217705bf3b"
STORAGE_CLASS_EXTENSION_NAME = "arc-k8s-storage-class"
STORAGE_CLASS_EXTENSION_TYPE = "Microsoft.ManagedStorageClass"
KUBERNETES_RUNTIME_RP = "Microsoft.KubernetesRuntime"


class InvalidResourceUriException(Exception):
    def __init__(self):
        super().__init__("Resource uri must reference a Microsoft.Kubernetes/connectedClusters resource.")


def _compare_caseless(a: str, b: str) -> bool:
    return a.casefold() == b.casefold()


@dataclass
class ConnectedClusterResourceId:
    subscription_id: str
    resource_group: str
    cluster_name: str

    @staticmethod
    def parse(resource_uri: str) -> "ConnectedClusterResourceId":
        parts = resource_uri.split("/")

        if len(parts) != 9:
            raise InvalidResourceUriException()

        if not (_compare_caseless(parts[1], "subscriptions") and _compare_caseless(parts[3], "resourceGroups") and _compare_caseless(parts[5], "providers") and _compare_caseless(parts[6], "Microsoft.Kubernetes") and _compare_caseless(parts[7], "connectedClusters")):
            raise InvalidResourceUriException()

        return ConnectedClusterResourceId(
            subscription_id=parts[2],
            resource_group=parts[4],
            cluster_name=parts[8]
        )

    @property
    def resource_uri(self) -> str:
        return f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Kubernetes/connectedClusters/{self.cluster_name}"


def enable_storage_class(cmd: AzCliCommand, resource_uri: str):
    """
    Enable storage class service in a connected cluster


    :param resource_uri: The resource uri of the connected cluster
    """

    resource_id = ConnectedClusterResourceId.parse(resource_uri)

    print(f"Register Kubernetes Runtime RP in subscription {resource_id.subscription_id}...")
    resource_management_client: ResourceManagementClient = get_mgmt_service_client(cmd.cli_ctx, ResourceManagementClient, subscription_id=resource_id.subscription_id)

    resource_management_client.providers.register(
        resource_provider_namespace=KUBERNETES_RUNTIME_RP
    )

    print(f"Installing Storage class Arc Extension in cluster {resource_id.cluster_name}...")
    source_control_configuration_client: SourceControlConfigurationClient = get_mgmt_service_client(cmd.cli_ctx, SourceControlConfigurationClient)

    lro = source_control_configuration_client.extensions.begin_create(
        resource_group_name=resource_id.resource_group,
        cluster_rp="Microsoft.Kubernetes",
        cluster_resource_name="connectedClusters",
        cluster_name=resource_id.cluster_name,
        extension_name=STORAGE_CLASS_EXTENSION_NAME,
        extension=Extension(
            identity=Identity(
                type="SystemAssigned"
            ),
            extension_type=STORAGE_CLASS_EXTENSION_TYPE,
            release_train="dev"
        )
    )

    # Prevent blocking KeyboardInterrupt
    while not lro.done():
        lro.wait(1)

    extension = lro.result()

    authorization_management_client: AuthorizationManagementClient = get_mgmt_service_client(cmd.cli_ctx, AuthorizationManagementClient)

    print("Assign the extension with Storage Class Contributor role under the cluster scope")
    sc_contributor_role_assignment = authorization_management_client.role_assignments.create(
        scope=resource_id.resource_uri,
        role_assignment_name=str(uuid4()),
        # pylint: disable=missing-kwoa
        parameters=RoleAssignmentCreateParameters(
            role_definition_id=STORAGE_CLASS_CONTRIBUTOR_ROLE_ID,
            principal_id=extension.identity.principal_id,
            principal_type=PrincipalType.SERVICE_PRINCIPAL
        ),
    )

    print("Assign the extension with Kubernetes Extension Contributor role under the cluster scope")
    k8s_extension_contributor_role_assignment = authorization_management_client.role_assignments.create(
        scope=resource_id.resource_uri,
        role_assignment_name=str(uuid4()),
        # pylint: disable=missing-kwoa
        parameters=RoleAssignmentCreateParameters(
            role_definition_id=KUBERNETES_EXTENSION_CONTRIBUTOR_ROLE_ID,
            principal_id=extension.identity.principal_id,
            principal_type=PrincipalType.SERVICE_PRINCIPAL
        ),
    )

    return {
        "extension": extension,
        "storage_class_contributor_role_assignment": sc_contributor_role_assignment,
        "kubernetes_extension_contributor_role_assignment": k8s_extension_contributor_role_assignment,
    }
