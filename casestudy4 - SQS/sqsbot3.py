
import boto3

# Initialize SQS client
sqs = boto3.client('sqs', region_name='us-east-1')

# Create a queue (or use existing)
response = sqs.create_queue(QueueName='MyQueue')
queue_url = response['QueueUrl']
print(f"Queue URL: {queue_url}")

# Send a message
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody='Hello from Coderrange!',
    MessageAttributes={
        'Sender': {
            'StringValue': 'Venkatesh',
            'DataType': 'String'
        }
    }
)

# Receive a message
messages = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    WaitTimeSeconds=5
)

# Process and delete
for msg in messages.get('Messages', []):
    print("📥 Received:", msg['Body'])
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=msg['ReceiptHandle']
    )
