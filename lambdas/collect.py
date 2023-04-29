import json
from src.historical import main



def lambda_handler(event, context):
    main()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
