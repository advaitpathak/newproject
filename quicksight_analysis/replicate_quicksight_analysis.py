import boto3
from copy import deepcopy


def get_analysis_definition():
    # Get analysis name from source
    source_analysis = source_client.describe_analysis(
        AwsAccountId=SOURCE_ACCOUNT_ID,
        AnalysisId=SOURCE_ANALYSIS_ID
    )
    analysis_name = source_analysis["Analysis"]["Name"]
    # Get analysis definition from source
    source_definition = source_client.describe_analysis_definition(
        AwsAccountId=SOURCE_ACCOUNT_ID,
        AnalysisId=SOURCE_ANALYSIS_ID
    )
    definition = source_definition["Definition"]
    return analysis_name, definition


def physical_logical_map(dataset):
    for table_id, table_def in dataset['PhysicalTableMap'].items():
        physical_table = table_def.get('RelationalTable') or table_def.get('CustomSql')
        if physical_table:
            data_source_arn = physical_table['DataSourceArn']
            source_data_source_id = data_source_arn.split('/')[-1]
            print(f"\tFound datasource in dataset: {source_data_source_id}")
            target_data_source_id = source_data_source_id + "-copy"

            try:
                # Check if data source already exists in the target account
                target_client.describe_data_source(
                    AwsAccountId=TARGET_ACCOUNT_ID,
                    DataSourceId=target_data_source_id
                )
                print(f"\tTarget data source already exists: {target_data_source_id}")
            except target_client.exceptions.ResourceNotFoundException:
                print(f"\tReplicating data source: {source_data_source_id} -> {target_data_source_id}")

                source_data_source = source_client.describe_data_source(
                    AwsAccountId=SOURCE_ACCOUNT_ID,
                    DataSourceId=source_data_source_id
                )['DataSource']

                # Clean up source data source details
                source_data_source.pop('Arn', None)
                source_data_source.pop('CreatedTime', None)
                source_data_source.pop('LastUpdatedTime', None)
                source_data_source.pop('Status', None)
                source_data_source.pop('RequestId', None)

                # Prepare to create data source in target
                target_client.create_data_source(
                    AwsAccountId=TARGET_ACCOUNT_ID,
                    DataSourceId=target_data_source_id,
                    Name=source_data_source['Name'] + " (Copy)",
                    Type=source_data_source['Type'],
                    DataSourceParameters=source_data_source['DataSourceParameters'],
                    # Permissions=[],  # Optional: define as per need
                    SslProperties=source_data_source.get('SslProperties'),
                    # VpcConnectionProperties=source_data_source.get('VpcConnectionProperties'),
                    # Tags=source_data_source.get('Tags', [])
                )
                print(f"\tData source created: {target_data_source_id}")

            # Update DataSourceArn in PhysicalTableMap to point to new target ARN
            new_arn = f"arn:aws:quicksight:{AWS_REGION}:{TARGET_ACCOUNT_ID}:datasource/{target_data_source_id}"
            physical_table['DataSourceArn'] = new_arn


def replicate_datasets(analysis_definition):
    source_target_dataset_mapping = {}
    print("Replicating datasets from source to target account...")
    for dataset_identifier in analysis_definition["DataSetIdentifierDeclarations"]:
        dataset_name = dataset_identifier["Identifier"]
        dataset_arn = dataset_identifier["DataSetArn"]
        print(f"Found a dataset: {dataset_name} -> {dataset_arn}")

        # Extract dataset ID from ARN
        dataset_id = dataset_arn.split("/")[-1]

        # Describe dataset from source
        response = source_client.describe_data_set(
            AwsAccountId=SOURCE_ACCOUNT_ID,
            DataSetId=dataset_id
        )
        dataset = response['DataSet']

        # Update fields for target account
        target_dataset_id = dataset['DataSetId'] + "-copy"
        target_dataset_name = dataset['Name'] + " (Copy)"
        target_dataset_arn = f"arn:aws:quicksight:{AWS_REGION}:{TARGET_ACCOUNT_ID}:dataset/{target_dataset_id}"

        dataset['DataSetId'] = target_dataset_id
        dataset['Name'] = target_dataset_name
        dataset['Permissions'] = []  # Optional: set if needed
        dataset['ImportMode'] = dataset.get('ImportMode', 'SPICE')  # or 'DIRECT_QUERY'
        dataset['DataSourceArn'] = target_dataset_arn

        # Check for internal datasets if any present (RelationalTable or CustomSql).
        #  If present create those dataset first, so they can be referenced in PhysicalTableMap and LogicalTableMap.
        physical_logical_map(dataset)

        # Remove read-only or unnecessary keys
        dataset.pop('Arn', None)
        dataset.pop('CreatedTime', None)
        dataset.pop('LastUpdatedTime', None)
        dataset.pop('Status', None)
        dataset.pop('RowLevelPermissionDataSet', None)
        dataset.pop('ColumnLevelPermissionRules', None)

        try:
            # Check if data source already exists in the target account
            target_client.describe_data_set(
                AwsAccountId=TARGET_ACCOUNT_ID,
                DataSetId=dataset['DataSetId']
            )
            print(f"Target dataset already exists: {dataset['DataSetId']}")
        except target_client.exceptions.ResourceNotFoundException:
            # Create dataset in target account
            response = target_client.create_data_set(
                AwsAccountId=TARGET_ACCOUNT_ID,
                DataSetId=dataset['DataSetId'],
                Name=dataset['Name'],
                PhysicalTableMap=dataset['PhysicalTableMap'],
                LogicalTableMap=dataset.get('LogicalTableMap', {}),
                ImportMode=dataset['ImportMode']
            )
            print(f"Dataset replicated successfully: {response['Arn']}")
        source_target_dataset_mapping[dataset_arn] = target_dataset_arn

    return source_target_dataset_mapping


def update_analysis_definition(source_analysis_definition, source_target_dataset_mapping):
    # Replace dataset ARNs in the definition
    print("Found below datasets in source analysis definition:")
    print(source_analysis_definition.get("DataSetIdentifierDeclarations", "No datasets found."))
    target_analysis_definition = deepcopy(source_analysis_definition)
    for ds in target_analysis_definition["DataSetIdentifierDeclarations"]:
        ds["DataSetArn"] = source_target_dataset_mapping[ds["DataSetArn"]]
    return target_analysis_definition


def create_target_analysis(analysis_name, target_analysis_definition):
    try:
        # Check if data source already exists in the target account
        target_client.describe_analysis(
            AwsAccountId=TARGET_ACCOUNT_ID,
            AnalysisId=TARGET_ANALYSIS_ID
        )
        print(f"Target analysis already exists: {TARGET_ANALYSIS_ID}")
    except target_client.exceptions.ResourceNotFoundException:
        # Create analysis in target account
        response = target_client.create_analysis(
            AwsAccountId=TARGET_ACCOUNT_ID,
            AnalysisId=TARGET_ANALYSIS_ID,
            Name=analysis_name,
            Definition=target_analysis_definition,
            Permissions=[
                {
                    "Principal": f"arn:aws:quicksight:{AWS_REGION}:{TARGET_ACCOUNT_ID}:group/default/ALL_USERS",
                    "Actions": [
                        "quicksight:DescribeAnalysis",
                        "quicksight:QueryAnalysis",
                        "quicksight:ListAnalyses"
                    ]
                }
            ]
        )
        print(f"Analysis created in target account: {response['Arn']}")


if __name__ == "__main__":
    # SOURCE_ACCOUNT_ID = "040890314520"
    # SOURCE_ANALYSIS_ID = "90cb99e9-d0a8-4963-8525-4b4629377fea"
    # TARGET_ACCOUNT_ID = "040890314520"

    AWS_REGION = "us-east-1"

    SOURCE_ACCOUNT_ID = input(f"Enter the source AWS account ID: ")
    SOURCE_ANALYSIS_ID = input(f"Enter the source analysis ID that you want to replicate: ")
    TARGET_ACCOUNT_ID = input(f"Enter the target AWS account ID: ")
    TARGET_ANALYSIS_ID = f"{SOURCE_ANALYSIS_ID}-copy"
    print(f"The target analysis ID will be: {TARGET_ANALYSIS_ID}")

    # Setup clients
    source_session = boto3.Session(profile_name="source")  # AWS CLI profile for source account
    target_session = boto3.Session(profile_name="target")  # AWS CLI profile for target account

    source_client = source_session.client("quicksight", region_name=AWS_REGION)
    target_client = target_session.client("quicksight", region_name=AWS_REGION)

    source_analysis_name, source_analysis_definition = get_analysis_definition()

    source_target_dataset_mapping = replicate_datasets(source_analysis_definition)

    target_analysis_definition = update_analysis_definition(source_analysis_definition, source_target_dataset_mapping)

    create_target_analysis(source_analysis_name, target_analysis_definition)
