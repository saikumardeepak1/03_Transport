from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

project_id = "de-class-activity-420602"
subscription_id = "MySub"
timeout = None

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received message: {message.data.decode('utf-8')}")
    message.ack()

print(f"Listening for messages on {subscription_path}...")

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

with subscriber:
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        print("Subscription canceled by user.")
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
        print("Timed out waiting for messages.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        streaming_pull_future.cancel()
        streaming_pull_future.result()

print("Finished listening for messages.")
