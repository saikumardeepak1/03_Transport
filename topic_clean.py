from google.cloud import pubsub_v1


project_id = "de-class-activity-420602"
topic_id = "MyTopic"


publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, "MySub")

def callback(message):
    print(f"Received and discarded message: {message.data.decode('utf-8')}")
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path} and discarding them...")


with subscriber:
    try:
        # Run indefinitely
        streaming_pull_future.result()
    except KeyboardInterrupt:
        # Allows the subscriber to be closed gracefully if operation is stopped manually
        streaming_pull_future.cancel()
        streaming_pull_future.result()
        print("Subscription canceled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        streaming_pull_future.cancel()
        streaming_pull_future.result()

print("Finished discarding messages.")
