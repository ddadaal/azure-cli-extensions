# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, Callable, Dict, Optional, TypeVar, Union

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from .. import models as _models
from ..._serialization import Serializer
from .._vendor import _convert_request

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


def build_get_request(
    resource_group_name: str,
    cluster_rp: Union[str, _models.Enum0],
    cluster_type: Union[str, _models.Enum5],
    cluster_name: str,
    extension_type_name: str,
    subscription_id: str,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2021-05-01-preview"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{clusterRp}/{clusterType}/{clusterName}/providers/Microsoft.KubernetesConfiguration/extensionTypes/{extensionTypeName}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str", min_length=1),
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1
        ),
        "clusterRp": _SERIALIZER.url("cluster_rp", cluster_rp, "str"),
        "clusterType": _SERIALIZER.url("cluster_type", cluster_type, "str"),
        "clusterName": _SERIALIZER.url("cluster_name", cluster_name, "str"),
        "extensionTypeName": _SERIALIZER.url("extension_type_name", extension_type_name, "str"),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


class ClusterExtensionTypeOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.kubernetesconfiguration.v2021_05_01_preview.SourceControlConfigurationClient`'s
        :attr:`cluster_extension_type` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs):
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")
        self._api_version = input_args.pop(0) if input_args else kwargs.pop("api_version")

    @distributed_trace
    def get(
        self,
        resource_group_name: str,
        cluster_rp: Union[str, _models.Enum0],
        cluster_type: Union[str, _models.Enum5],
        cluster_name: str,
        extension_type_name: str,
        **kwargs: Any
    ) -> _models.ExtensionType:
        """Get Extension Type details.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param cluster_rp: The Kubernetes cluster RP - either Microsoft.ContainerService (for AKS
         clusters) or Microsoft.Kubernetes (for OnPrem K8S clusters). Known values are:
         "Microsoft.ContainerService" and "Microsoft.Kubernetes". Required.
        :type cluster_rp: str or ~azure.mgmt.kubernetesconfiguration.v2021_05_01_preview.models.Enum0
        :param cluster_type: The Kubernetes cluster resource name - either managedClusters (for AKS
         clusters) or connectedClusters (for OnPrem K8S clusters). Known values are: "managedClusters"
         and "connectedClusters". Required.
        :type cluster_type: str or ~azure.mgmt.kubernetesconfiguration.v2021_05_01_preview.models.Enum5
        :param cluster_name: The name of the kubernetes cluster. Required.
        :type cluster_name: str
        :param extension_type_name: Extension type name. Required.
        :type extension_type_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ExtensionType or the result of cls(response)
        :rtype: ~azure.mgmt.kubernetesconfiguration.v2021_05_01_preview.models.ExtensionType
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop(
            "api_version", _params.pop("api-version", self._api_version or "2021-05-01-preview")
        )
        cls: ClsType[_models.ExtensionType] = kwargs.pop("cls", None)

        request = build_get_request(
            resource_group_name=resource_group_name,
            cluster_rp=cluster_rp,
            cluster_type=cluster_type,
            cluster_name=cluster_name,
            extension_type_name=extension_type_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.get.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ExtensionType", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{clusterRp}/{clusterType}/{clusterName}/providers/Microsoft.KubernetesConfiguration/extensionTypes/{extensionTypeName}"
    }
