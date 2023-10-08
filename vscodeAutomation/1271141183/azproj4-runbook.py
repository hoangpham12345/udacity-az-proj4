#!/usr/bin/env python3
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

SUBSCRIPTION_ID="17fa567b-e6eb-4e3c-a2e1-c445717eb2aa"

azure_credential = DefaultAzureCredential()

import os
import requests
# printing environment variables
endpoint = os.getenv('IDENTITY_ENDPOINT')+"?resource=https://management.azure.com/"
identityHeader = os.getenv('IDENTITY_HEADER')
payload={}
headers = {
'X-IDENTITY-HEADER' : identityHeader,
'Metadata' : True
}
response = requests.get(endpoint, headers)
print(response.text)

# Initialize client with the credential and subscription.
compute_client = ComputeManagementClient(
    azure_credential,
    SUBSCRIPTION_ID
)

myvmss = compute_client.virtual_machine_scale_sets.get("cloud-demo", "udacity-vmss")
print("Initial myvmss.sku.capacity = ",myvmss.sku.capacity)
myvmss.sku.capacity = 4
print("New myvmss.sku.capacity = ",myvmss.sku.capacity)
# Increase the VMSS SKU Capacity
async_vmss = compute_client.virtual_machine_scale_sets.begin_create_or_update("cloud-demo", "udacity-vmss", myvmss)
async_vmss.wait()