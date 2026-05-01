import boto3

ACCOUNT_ID = "040890314520"


def delete_analysis(analysis_ids):
    for analysis in analysis_ids:
        try:
            response = qs_client.delete_analysis(
                AwsAccountId=ACCOUNT_ID,
                AnalysisId=analysis,
                ForceDeleteWithoutRecovery=True  # Optional: deletes even if the analysis is referenced
            )
            print(f"Analysis deleted: {response['Status']} - {response['Arn']}")
        except qs_client.exceptions.ResourceNotFoundException:
            print("Analysis not found.")
        except Exception as e:
            print(f"Failed to delete analysis: {e}")


def delete_dataset(dataset_ids):
    for dataset in dataset_ids:
        try:
            response = qs_client.delete_data_set(
                AwsAccountId=ACCOUNT_ID,
                DataSetId=dataset,
                ForceDeleteWithoutRecovery=True  # Optional: deletes even if the dataset is referenced
            )
            print(f"Dataset deleted: {response['Status']} - {response['Arn']}")
        except qs_client.exceptions.ResourceNotFoundException:
            print("Dataset not found.")
        except Exception as e:
            print(f"Failed to delete dataset: {e}")


if __name__ == "__main__":
    qs_client = boto3.client("quicksight", region_name="us-east-1")

    analysis_ids = ["90cb99e9-d0a8-4963-8525-4b4629377fea-copy"]
    delete_analysis(analysis_ids)

    dataset_ids = ["d1f61941-f7e8-4ced-9221-a0a6d644d9c5-copy", "2fb7fa66-5a3c-4168-b5f9-c06be6183066-copy"]
    delete_dataset(dataset_ids)
