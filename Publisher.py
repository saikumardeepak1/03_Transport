import json
from google.cloud import pubsub_v1

project_id = "de-class-activity-420602"
topic_id = "MyTopic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

with open('bcsample.json', 'r') as file:
    records = json.load(file)

for record in records:
    message_json = json.dumps(record)
    message_bytes = message_json.encode('utf-8')
    future = publisher.publish(topic_path, message_bytes)
    print(future.result())

print(f"Published messages to {topic_path}.")
