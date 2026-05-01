from infrastructure.notification_formatter import lambda_handler

event = {
    'version': '0',
    'id': '2e661836-e9f9-8f0a-6fc1-d7010dad2852',
    'detail-type': 'Data Quality Evaluation Results Available',
    'source': 'aws.glue-dataquality',
    'account': '040890314520',
    'time': '2023-07-25T12:26:21Z',
    'region': 'us-east-1',
    'resources': [
        'arn:aws:glue:us-east-1:040890314520:table/presentation_dev/propertysales',
        'arn:aws:glue:us-east-1:040890314520:dqRun/dqrun-37adb01fcf0731b7edd149dcf572d48cf2b49635',
        'arn:aws:glue:us-east-1:040890314520:dataQualityRuleset/recommended-ruleset-hliu-lambda-propertysales-1234-CLONE'
    ],
    'detail': {
        'resultId': 'dqresult-d2897e19846cc7a485c60b3eb321cc6ee23f60f8',
        'context': {
            'runId': 'dqrun-37adb01fcf0731b7edd149dcf572d48cf2b49635',
            'databaseName': 'presentation_dev',
            'tableName': 'propertysales',
            'catalogId': '040890314520',
            'contextType': 'GLUE_DATA_CATALOG'
        },
        'rulesetNames': ['recommended-ruleset-hliu-lambda-propertysales-1234-CLONE'],
        'state': 'FAILED',
        'score': 0.75,
        'numRulesSucceeded': 3,
        'numRulesFailed': 1,
        'numRulesSkipped': 0
    }
}
lambda_handler(event, '')
