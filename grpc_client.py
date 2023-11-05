import grpc
import inventory_pb2
import inventory_pb2_grpc


def main():
    # Establish a gRPC channel to the server
    channel = grpc.insecure_channel('localhost:50051')
    stub = inventory_pb2_grpc.InventoryServiceStub(channel)

    # Call the searchByID method
    # id_request = inventory_pb2.InventoryRequest(ID="IN002")
    # response = stub.SearchByID(id_request)
    # print("SearchByID Response:", response)

    # Call the search method
    # search_request = inventory_pb2.SearchRequest(KeyName="Name", KeyValue="Item 3")
    # response = stub.Search(search_request)
    # print("Search Response:", response)

    # Call the searchRange method
    range_request = inventory_pb2.SearchRangeRequest(KeyName="Quantity in Stock", KeyValueStart=25, KeyValueEnd=100)
    for response in stub.SearchRange(range_request):
        print("SearchRange Response:", response)

    # Call the getDistribution method
    # distribution_request = inventory_pb2.GetDistributionRequest(KeyName="Quantity in Stock", Percentile=50)
    # response = stub.GetDistribution(distribution_request)
    # print("GetDistribution Response:", response)

    # Call the update method
    # update_request = inventory_pb2.UpdateRequest(
    #     KeyName="Inventory Id",
    #     KeyValue="IN001",
    #     ValName="Name",
    #     ValValNew="Updated Name"
    # )
    # response = stub.Update(update_request)
    # print("Update Response:", response)


if __name__ == '__main__':
    main()
