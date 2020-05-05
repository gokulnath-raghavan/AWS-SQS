import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    # create a boto3 client
    client = boto3.client('sqs')
    
  
	#Give your Queue name here , for example fifo queue would end with .fifo
    queues = client.list_queues(QueueNamePrefix="testfifo.fifo")
    testpolling_queue_url = queues['QueueUrls'][0]
    
	#To find the number of messages in the Queue
    response = client.get_queue_attributes(
    QueueUrl=testpolling_queue_url,
    AttributeNames=['ApproximateNumberOfMessages'])
    print('number of messages in the queue.....'+response['Attributes']['ApproximateNumberOfMessages'])
    print(response)
    
    # send messages to the queue via code, below code will produce 100 messages, please change the range dependending on the number of messages
    for i in range(0,100):
        # we set a simple message body for each message
        #enqueue_response = client.send_message(QueueUrl=testpolling_queue_url,MessageGroupId=str(i+1),MessageDeduplicationId=str(i+1), MessageBody='This is test message #'+str(i))
        enqueue_response = client.send_message(QueueUrl=testpolling_queue_url, MessageBody='This is test message #'+str(i))
        # the response contains MD5 of the body, a message Id, MD5 of message attributes, and a sequence number
        print('Message ID : ',enqueue_response['MessageId'])
	
	# receive the message from queue, here we can mention the maximum number of messages	
    messages = client.receive_message(QueueUrl=testpolling_queue_url,MaxNumberOfMessages=10)
	print(messages)
    if 'Messages' in messages:
        for message in messages['Messages']:
            print(message)
    # next, we dequeue these messages - 10 messages at a time (SQS max limit) till the queue is exhausted.
    # in production/real setup, I suggest using long polling as you get billed for each request, regardless of an empty response
    while True:
        messages = client.receive_message(QueueUrl=testpolling_queue_url,MaxNumberOfMessages=10) # adjust MaxNumberOfMessages if needed
        if 'Messages' in messages: # when the queue is exhausted, the response dict contains no 'Messages' key
            for message in messages['Messages']: # 'Messages' is a list
                # process the messages
                print(message)
                print(message['Body'])
                # next, we delete the message from the queue so no one else will process it again
                client.delete_message(QueueUrl=testpolling_queue_url,ReceiptHandle=message['ReceiptHandle'])
        else:
            print('Queue is now empty')
            break
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
