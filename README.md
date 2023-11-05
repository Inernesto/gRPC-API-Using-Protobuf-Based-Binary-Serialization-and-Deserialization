# gRPC-API-Using-Protobuf-Based-Binary-Serialization-and-Deserialization

The InventoryService gRPC project provides a powerful and efficient way to manage inventory data using gRPC. This service allows you to interact with your inventory records through various methods, such as searching for records, retrieving distribution statistics, and performing updates.

## Table of Contents

- [General Overview](#general-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [SearchByID](#searchbyid)
  - [Search](#search)
  - [SearchRange](#searchrange)
  - [GetDistribution](#getdistribution)
  - [Update](#update)
- [Contributing](#contributing)
- [License](#license)

## General Overview

The InventoryService gRPC project is built to handle inventory records efficiently. It includes several gRPC methods for querying, analyzing, and updating your inventory data. You can use this service to search for specific records, retrieve distribution statistics for a specific key, and make updates to your inventory records.

## Getting Started

### Prerequisites

Before using the InventoryService, ensure you have the following prerequisites:

- Python 3.7 or higher installed
- gRPC and Protobuf Python packages
- Access to the service or server hosting the InventoryService

### Installation

To get started, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Inernesto/gRPC-API-Using-Protobuf-Based-Binary-Serialization-and-Deserialization.git
   ```

2. Install the required Python packages:

  ```bash
  pip install grpcio grpcio-tools
  ```

3. Generate the Python code from the .proto file:

  ```bash
  python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. inventory.proto
  ```

4. Run the gRPC server:

```bash
python grpc_server.py
```

# Usage

You can use the InventoryService by making gRPC calls to its various methods. Below are examples of how to make calls to each method using the appropriate argument types.
But first you have to run the gRPC client

```bash
python grpc_client.py
```

## SearchByID

Search for a single inventory record by its unique ID.

Request:

```bash
inventory_pb2.InventoryRequest(ID="IN001")
```

Response:

```bash
inventory_pb2.InventoryResponse
```

## Search

Search for inventory records by a specific key and its value.

Request:

```bash
inventory_pb2.SearchRequest(KeyName="Name", KeyValue="Item 2")
```

Response:

```bash
inventory_pb2.InventoryResponse
```

## SearchRange

Search for inventory records within a range of values for a specific key.

Request:

```bash
inventory_pb2.SearchRangeRequest(KeyName="Unit Price", KeyValueStart=50.0, KeyValueEnd=100.0)
```

Response:

```bash
stream inventory_pb2.InventoryResponse
```

## GetDistribution

Retrieve the distribution statistics for a specific key.

Request:

```bash
inventory_pb2.GetDistributionRequest(KeyName="Quantity in Stock", Percentile=75)
```

Response:

```bash
inventory_pb2.GetDistributionResponse
```

## Update

Update an inventory record's attribute value.

Request:

```bash
inventory_pb2.UpdateRequest(KeyName="Name", KeyValue="Item 1", ValName="Quantity in Stock", ValValNew="50")
```

Response:

```bash
inventory_pb2.UpdateResponse
```

# Contributing

If you would like to contribute to the InventoryService gRPC project, please follow these guidelines:

1. Fork the project and create a new branch for your contributions.

2. Make your changes or enhancements to the code.

3. Write clear and concise commit messages.

4. Submit a pull request for review.

Your contributions are greatly appreciated!

# License

This project is authorized for educational and informative purposes; for any other use, please contact the author.

Good luck with your InventoryService gRPC project! If you have any questions or encounter issues, please don't hesitate to reach out for assistance.
