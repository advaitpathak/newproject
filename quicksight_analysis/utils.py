import boto3

SOURCE_ACCOUNT_ID = "040890314520"
ANALYSIS_ID = "90cb99e9-d0a8-4963-8525-4b4629377fea"

client = boto3.client("quicksight", region_name="us-east-1")


def get_all_dataset_id():
    response = client.list_data_sets(AwsAccountId=SOURCE_ACCOUNT_ID)
    for dataset in response["DataSetSummaries"]:
        # if "copy" in dataset:
        print(dataset["Name"], "->", dataset["DataSetId"])


def get_all_analysis_id():
    response = client.list_analyses(AwsAccountId=SOURCE_ACCOUNT_ID)
    print(f"##################### Matching Analysis IDs to {ANALYSIS_ID} #####################")
    for analysis in response["AnalysisSummaryList"]:
        if ANALYSIS_ID in analysis["AnalysisId"]:
            # print(analysis["Name"], "→", analysis["AnalysisId"])
            print(analysis["Name"], "→", analysis["Arn"])


def get_dataset_arn():
    print(f"##################### Dataset IDs for analysis id {ANALYSIS_ID} #####################")
    response = client.describe_analysis_definition(
        AwsAccountId=SOURCE_ACCOUNT_ID,
        AnalysisId=ANALYSIS_ID
    )

    for ds in response["Definition"]["DataSetIdentifierDeclarations"]:
        print(f"{ds['Identifier']}: {ds['DataSetArn']}")


if __name__ == "__main__":
    # get_dataset_arn()
    # get_all_analysis_id()
    get_all_dataset_id()
