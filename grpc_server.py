import grpc
from concurrent import futures
import inventory_pb2
import inventory_pb2_grpc
from google.protobuf.empty_pb2 import Empty
import numpy as np


class InventoryService(inventory_pb2_grpc.InventoryServiceServicer):
    def __init__(self, inventory_data):
        self.inventory_data = inventory_data  # Your inventory data here...

    def SearchByID(self, request, context):
        # Implement search logic here
        ID = request.ID

        for record in self.inventory_data:
            if record["Inventory Id"] == ID:
                # Create an InventoryRecord with the matching data
                inventory_record = inventory_pb2.InventoryRecord(
                    ID=record["Inventory Id"],
                    Name=record["Name"],
                    Description=record["Description"],
                    UnitPrice=record["Unit Price"],
                    QuantityInStock=record["Quantity in Stock"],
                    InventoryValue=record["Inventory Value"],
                    ReorderLevel=record["Reorder Level"],
                    ReorderTimeInDays=record["Reorder Time in Days"],
                    QuantityInReorder=record["Quantity in Reorder"],
                    Discontinued=record["Discontinued?"]
                )

                # Set the inventory_record in the response and return it
                response = inventory_pb2.InventoryResponse(inventory_record=inventory_record)
                return response

        # If no matching record is found, return an empty response
        return Empty()

    def Search(self, request, context):
        # Implement search logic here
        key_name = request.KeyName
        key_value = request.KeyValue

        for record in self.inventory_data:
            if record[key_name] == key_value:
                # Create an InventoryRecord with the matched data
                inventory_record = inventory_pb2.InventoryRecord(
                    ID=record["Inventory Id"],
                    Name=record["Name"],
                    Description=record["Description"],
                    UnitPrice=record["Unit Price"],
                    QuantityInStock=record["Quantity in Stock"],
                    InventoryValue=record["Inventory Value"],
                    ReorderLevel=record["Reorder Level"],
                    ReorderTimeInDays=record["Reorder Time in Days"],
                    QuantityInReorder=record["Quantity in Reorder"],
                    Discontinued=record["Discontinued?"]
                )

                # Set the inventory_record in the response and return it
                response = inventory_pb2.InventoryResponse(inventory_record=inventory_record)
                return response

        # If no matching record is found, return an empty response
        return Empty()

    def SearchRange(self, request, context):
        # Implement the getDistribution method
        key_name = request.KeyName
        key_value_start = request.KeyValueStart
        key_value_end = request.KeyValueEnd

        matching_records = []

        for record in self.inventory_data:
            try:
                # Attempt to convert the value to a float
                value = record[key_name]
                if key_name in record and key_value_start <= value <= key_value_end:
                    matching_records.append(record)
            except ValueError:
                # Skip non-numeric values
                pass

        for record in matching_records:
            yield inventory_pb2.InventoryResponse(inventory_record=inventory_pb2.InventoryRecord(
                ID=record["Inventory Id"],
                Name=record["Name"],
                Description=record["Description"],
                UnitPrice=record["Unit Price"],
                QuantityInStock=record["Quantity in Stock"],
                InventoryValue=record["Inventory Value"],
                ReorderLevel=record["Reorder Level"],
                ReorderTimeInDays=record["Reorder Time in Days"],
                QuantityInReorder=record["Quantity in Reorder"],
                Discontinued=record["Discontinued?"]
            ))

        # If no matching record is found, return an empty response
        return Empty()

    def GetDistribution(self, request, context):
        key_name = request.KeyName
        percentile = request.Percentile

        values = []
        for record in self.inventory_data:
            if key_name in record:
                value = record[key_name]
                try:
                    # Attempt to convert the value to a float
                    value = float(value)
                    values.append(value)
                except ValueError:
                    # Skip non-numeric values
                    pass

        if values:
            # Calculate the specified percentile
            result = np.percentile(values, percentile)
            return inventory_pb2.GetDistributionResponse(Value=result)
        else:
            return Empty()

    def Update(self, request, context):
        key_name = request.KeyName
        key_value = request.KeyValue
        val_name = request.ValName
        val_val_new = request.ValValNew

        # Search for the record to update
        for record in self.inventory_data:
            if key_name in record and record[key_name] == key_value:
                # Update the value
                if val_name in record:
                    record[val_name] = val_val_new
                    return inventory_pb2.UpdateResponse(Success=True)

        # If the record was not found or the update was unsuccessful
        return inventory_pb2.UpdateResponse(Success=False)


inventory_list = [
    {'Inventory Id': 'IN001', 'Name': 'Item 1', 'Description': 'Desc 1', 'Unit Price': '$51.00', 'Quantity in Stock': 25, 'Inventory Value': '$1,275.00', 'Reorder Level': 29, 'Reorder Time in Days': 13, 'Quantity in Reorder': 50, 'Discontinued?': False},
    {'Inventory Id': 'IN002', 'Name': 'Item 2', 'Description': 'Desc 2', 'Unit Price': '$93.00', 'Quantity in Stock': 132, 'Inventory Value': '$12,276.00', 'Reorder Level': 231, 'Reorder Time in Days': 4, 'Quantity in Reorder': 50, 'Discontinued?': False},
    {'Inventory Id': 'IN003', 'Name': 'Item 3', 'Description': 'Desc 3', 'Unit Price': '$510.00', 'Quantity in Stock': 25, 'Inventory Value': '$175.00', 'Reorder Level': 290, 'Reorder Time in Days': 23, 'Quantity in Reorder': 30, 'Discontinued?': True},
    {'Inventory Id': 'IN004', 'Name': 'Item 4', 'Description': 'Desc 4', 'Unit Price': '$19.00', 'Quantity in Stock': 186, 'Inventory Value': '$3,534.00', 'Reorder Level': 158, 'Reorder Time in Days': 6, 'Quantity in Reorder': 50, 'Discontinued?': False},
    {"Inventory Id": "IN005", "Name": "Item 5", "Description": "Desc 5", "Unit Price": "$75.00", "Quantity in Stock": 62, "Inventory Value": "$4,650.00", "Reorder Level": 39, "Reorder Time in Days": 12, "Quantity in Reorder": 50, "Discontinued?": False},
    {"Inventory Id": "IN006", "Name": "Item 6", "Description": "Desc 6", "Unit Price": "$11.00", "Quantity in Stock": 5, "Inventory Value": "$55.00", "Reorder Level": 9, "Reorder Time in Days": 13, "Quantity in Reorder": 150, "Discontinued?": False},
    {"Inventory Id": "IN007", "Name": "Item 7", "Description": "Desc 7", "Unit Price": "$56.00", "Quantity in Stock": 58, "Inventory Value": "$3,248.00", "Reorder Level": 109, "Reorder Time in Days": 7, "Quantity in Reorder": 100, "Discontinued?": True},
    {"Inventory Id": "IN008", "Name": "Item 8", "Description": "Desc 8", "Unit Price": "$38.00", "Quantity in Stock": 101, "Inventory Value": "$3,838.00", "Reorder Level": 162, "Reorder Time in Days": 3, "Quantity in Reorder": 100, "Discontinued?": False},
    {"Inventory Id": "IN009", "Name": "Item 9", "Description": "Desc 9", "Unit Price": "$59.00", "Quantity in Stock": 122, "Inventory Value": "$7,198.00", "Reorder Level": 82, "Reorder Time in Days": 3, "Quantity in Reorder": 150, "Discontinued?": False},
    {"Inventory Id": "IN0010", "Name": "Item 10", "Description": "Desc 10", "Unit Price": "$50.00", "Quantity in Stock": 175, "Inventory Value": "$8,750.00", "Reorder Level": 283, "Reorder Time in Days": 8, "Quantity in Reorder": 150, "Discontinued?": False},
    {"Inventory Id": "IN0011", "Name": "Item 11", "Description": "Desc 11", "Unit Price": "$59.00", "Quantity in Stock": 176, "Inventory Value": "$10,384.00", "Reorder Level": 229, "Reorder Time in Days": 1, "Quantity in Reorder": 100, "Discontinued?": False},
    {"Inventory Id": "IN0012", "Name": "Item 12", "Description": "Desc 12", "Unit Price": "$18.00", "Quantity in Stock": 22, "Inventory Value": "$396.00", "Reorder Level": 36, "Reorder Time in Days": 12, "Quantity in Reorder": 50, "Discontinued?": False},
    {"Inventory Id": "IN0013", "Name": "Item 13", "Description": "Desc 13", "Unit Price": "$26.00", "Quantity in Stock": 72, "Inventory Value": "$1,872.00", "Reorder Level": 102, "Reorder Time in Days": 9, "Quantity in Reorder": 100, "Discontinued?": False},
    {"Inventory Id": "IN0014", "Name": "Item 14", "Description": "Desc 14", "Unit Price": "$42.00", "Quantity in Stock": 62, "Inventory Value": "$2,604.00", "Reorder Level": 83, "Reorder Time in Days": 2, "Quantity in Reorder": 100, "Discontinued?": False},
    {"Inventory Id": "IN0015", "Name": "Item 15", "Description": "Desc 15", "Unit Price": "$32.00", "Quantity in Stock": 46, "Inventory Value": "$1,472.00", "Reorder Level": 23, "Reorder Time in Days": 15, "Quantity in Reorder": 50, "Discontinued?": False},
    {"Inventory Id": "IN0016", "Name": "Item 16", "Description": "Desc 16", "Unit Price": "$90.00", "Quantity in Stock": 96, "Inventory Value": "$8,640.00", "Reorder Level": 180, "Reorder Time in Days": 3, "Quantity in Reorder": 50, "Discontinued?": False},
    {"Inventory Id": "IN0017", "Name": "Item 17", "Description": "Desc 17", "Unit Price": "$97.00", "Quantity in Stock": 57, "Inventory Value": "$5,529.00", "Reorder Level": 98, "Reorder Time in Days": 12, "Quantity in Reorder": 50, "Discontinued?": True},
    {"Inventory Id": "IN0018", "Name": "Item 18", "Description": "Desc 18", "Unit Price": "$12.00", "Quantity in Stock": 6, "Inventory Value": "$72.00", "Reorder Level": 7, "Reorder Time in Days": 13, "Quantity in Reorder": 50, "Discontinued?": False},
    {"Inventory Id": "IN0019", "Name": "Item 19", "Description": "Desc 19", "Unit Price": "$82.00", "Quantity in Stock": 143, "Inventory Value": "$11,726.00", "Reorder Level": 164, "Reorder Time in Days": 12, "Quantity in Reorder": 150, "Discontinued?": False},
    {"Inventory Id": "IN0020", "Name": "Item 20", "Description": "Desc 20", "Unit Price": "$16.00", "Quantity in Stock": 124, "Inventory Value": "$1,984.00", "Reorder Level": 113, "Reorder Time in Days": 14, "Quantity in Reorder": 50, "Discontinued?": False},
    {"Inventory Id": "IN0021", "Name": "Item 21", "Description": "Desc 21", "Unit Price": "$19.00", "Quantity in Stock": 112, "Inventory Value": "$2,128.00", "Reorder Level": 75, "Reorder Time in Days": 11, "Quantity in Reorder": 50, "Discontinued?": False},
    {"Inventory Id": "IN0022", "Name": "Item 22", "Description": "Desc 22", "Unit Price": "$24.00", "Quantity in Stock": 182, "Inventory Value": "$4,368.00", "Reorder Level": 132, "Reorder Time in Days": 15, "Quantity in Reorder": 150, "Discontinued?": False},
    {"Inventory Id": "IN0023", "Name": "Item 23", "Description": "Desc 23", "Unit Price": "$29.00", "Quantity in Stock": 106, "Inventory Value": "$3,074.00", "Reorder Level": 142, "Reorder Time in Days": 1, "Quantity in Reorder": 150, "Discontinued?": True},
    {"Inventory Id": "IN0024", "Name": "Item 24", "Description": "Desc 24", "Unit Price": "$75.00", "Quantity in Stock": 173, "Inventory Value": "$12,975.00", "Reorder Level": 127, "Reorder Time in Days": 9, "Quantity in Reorder": 100, "Discontinued?": False},
    {"Inventory Id": "IN0025", "Name": "Item 25", "Description": "Desc 25", "Unit Price": "$14.00", "Quantity in Stock": 28, "Inventory Value": "$392.00", "Reorder Level": 21, "Reorder Time in Days": 8, "Quantity in Reorder": 50, "Discontinued?": False},
]


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryService(inventory_list), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
