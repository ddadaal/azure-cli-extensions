# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "k8s-runtime storage-class list",
    is_preview=True,
)
class List(AAZCommand):
    """List StorageClass resources by parent

    :example: List all storage classes in a cluster
        az k8s-runtime storage-class list --resource-uri subscriptions/00000000-1111-2222-3333-444444444444/resourceGroups/example/providers/Microsoft.Kubernetes/connectedClusters/cluster1
    """

    _aaz_info = {
        "version": "2023-10-01-preview",
        "resources": [
            ["mgmt-plane", "/{resourceuri}/providers/microsoft.kubernetesruntime/storageclasses", "2023-10-01-preview"],
        ]
    }

    AZ_SUPPORT_PAGINATION = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_paging(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_uri = AAZStrArg(
            options=["--resource-uri"],
            help="The fully qualified Azure Resource manager identifier of the resource.",
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.StorageClassList(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance.value, client_flatten=True)
        next_link = self.deserialize_output(self.ctx.vars.instance.next_link)
        return result, next_link

    class StorageClassList(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/{resourceUri}/providers/Microsoft.KubernetesRuntime/storageClasses",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceUri", self.ctx.args.resource_uri,
                    skip_quote=True,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-10-01-preview",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.next_link = AAZStrType(
                serialized_name="nextLink",
            )
            _schema_on_200.value = AAZListType(
                flags={"required": True},
            )

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.access_modes = AAZListType(
                serialized_name="accessModes",
            )
            properties.allow_volume_expansion = AAZStrType(
                serialized_name="allowVolumeExpansion",
            )
            properties.data_resilience = AAZStrType(
                serialized_name="dataResilience",
            )
            properties.failover_speed = AAZStrType(
                serialized_name="failoverSpeed",
            )
            properties.limitations = AAZListType()
            properties.mount_options = AAZListType(
                serialized_name="mountOptions",
            )
            properties.performance = AAZStrType()
            properties.priority = AAZIntType()
            properties.provisioner = AAZStrType()
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.type_properties = AAZObjectType(
                serialized_name="typeProperties",
                flags={"required": True},
            )
            properties.volume_binding_mode = AAZStrType(
                serialized_name="volumeBindingMode",
            )

            access_modes = cls._schema_on_200.value.Element.properties.access_modes
            access_modes.Element = AAZStrType()

            limitations = cls._schema_on_200.value.Element.properties.limitations
            limitations.Element = AAZStrType()

            mount_options = cls._schema_on_200.value.Element.properties.mount_options
            mount_options.Element = AAZStrType()

            type_properties = cls._schema_on_200.value.Element.properties.type_properties
            type_properties.type = AAZStrType(
                flags={"required": True},
            )

            disc_blob = cls._schema_on_200.value.Element.properties.type_properties.discriminate_by("type", "Blob")
            disc_blob.azure_storage_account_key = AAZStrType(
                serialized_name="azureStorageAccountKey",
                flags={"secret": True},
            )
            disc_blob.azure_storage_account_name = AAZStrType(
                serialized_name="azureStorageAccountName",
                flags={"required": True},
            )

            disc_nfs = cls._schema_on_200.value.Element.properties.type_properties.discriminate_by("type", "NFS")
            disc_nfs.mount_permissions = AAZStrType(
                serialized_name="mountPermissions",
            )
            disc_nfs.on_delete = AAZStrType(
                serialized_name="onDelete",
            )
            disc_nfs.server = AAZStrType(
                flags={"required": True},
            )
            disc_nfs.share = AAZStrType(
                flags={"required": True},
            )
            disc_nfs.sub_dir = AAZStrType(
                serialized_name="subDir",
            )

            disc_rwx = cls._schema_on_200.value.Element.properties.type_properties.discriminate_by("type", "RWX")
            disc_rwx.backing_storage_class_name = AAZStrType(
                serialized_name="backingStorageClassName",
                flags={"required": True},
            )

            disc_smb = cls._schema_on_200.value.Element.properties.type_properties.discriminate_by("type", "SMB")
            disc_smb.domain = AAZStrType()
            disc_smb.password = AAZStrType(
                flags={"secret": True},
            )
            disc_smb.source = AAZStrType(
                flags={"required": True},
            )
            disc_smb.sub_dir = AAZStrType(
                serialized_name="subDir",
            )
            disc_smb.username = AAZStrType()

            system_data = cls._schema_on_200.value.Element.system_data
            system_data.created_at = AAZStrType(
                serialized_name="createdAt",
            )
            system_data.created_by = AAZStrType(
                serialized_name="createdBy",
            )
            system_data.created_by_type = AAZStrType(
                serialized_name="createdByType",
            )
            system_data.last_modified_at = AAZStrType(
                serialized_name="lastModifiedAt",
            )
            system_data.last_modified_by = AAZStrType(
                serialized_name="lastModifiedBy",
            )
            system_data.last_modified_by_type = AAZStrType(
                serialized_name="lastModifiedByType",
            )

            return cls._schema_on_200


class _ListHelper:
    """Helper class for List"""


__all__ = ["List"]
